#!/usr/bin/env python3
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
PATCHER = PROJECT / "tools" / "patcher.py"

ADMIN_TEMPLATE = """<!DOCTYPE HTML>\n<html><head><link rel=\"stylesheet\" href=\"css/style.css\"></head><body></body></html>\n"""
CLIENT_PAGE = """<!DOCTYPE HTML>\n<html><head>{custom_template_head}</head><body>{content}</body></html>\n"""
LEGACY_CLIENT_TEMPLATE = """<!DOCTYPE HTML>\n<html><head>{custom_template_head}</head><body>{content}</body></html>\n"""


class PatcherTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="kbp-dark-test-"))
        for p in [
            "admin/template", "admin/css", "admin/jscript",
            "client/skin/view_default/default", "client/jscript"
        ]:
            (self.tmp / p).mkdir(parents=True, exist_ok=True)
        for name in ["page.html", "page_popup.html", "login.html"]:
            (self.tmp / "admin/template" / name).write_text(ADMIN_TEMPLATE, encoding="utf-8")
        (self.tmp / "client/skin/view_default/default/page.html").write_text(CLIENT_PAGE, encoding="utf-8")
        (self.tmp / "client/template.txt").write_text(LEGACY_CLIENT_TEMPLATE, encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def runp(self, *args):
        return subprocess.run(["python3", str(PATCHER), *args], text=True, capture_output=True)

    def test_install_is_idempotent(self):
        self.assertEqual(self.runp("install", str(self.tmp)).returncode, 0)
        self.assertEqual(self.runp("install", str(self.tmp)).returncode, 0)
        admin = (self.tmp / "admin/template/page.html").read_text(encoding="utf-8")
        client = (self.tmp / "client/skin/view_default/default/page.html").read_text(encoding="utf-8")
        self.assertEqual(admin.count("KBP-DARK-MODE:BEGIN"), 1)
        self.assertEqual(client.count("KBP-DARK-MODE:BEGIN"), 1)
        self.assertTrue((self.tmp / "admin/css/kbp-dark-mode.css").exists())
        self.assertTrue((self.tmp / "client/jscript/kbp-theme.js").exists())

    def test_uninstall_removes_only_overlay(self):
        self.assertEqual(self.runp("install", str(self.tmp)).returncode, 0)
        page = self.tmp / "admin/template/page.html"
        page.write_text(page.read_text(encoding="utf-8").replace("<body>", "<!-- LOCAL -->\n<body>"), encoding="utf-8")
        self.assertEqual(self.runp("uninstall", str(self.tmp)).returncode, 0)
        txt = page.read_text(encoding="utf-8")
        self.assertNotIn("KBP-DARK-MODE:BEGIN", txt)
        self.assertIn("<!-- LOCAL -->", txt)

    def test_admin_only(self):
        self.assertEqual(self.runp("install", str(self.tmp), "--admin-only").returncode, 0)
        self.assertTrue((self.tmp / "admin/css/kbp-dark-mode.css").exists())
        self.assertFalse((self.tmp / "client/skin/kbp-dark-mode.css").exists())
        client = (self.tmp / "client/skin/view_default/default/page.html").read_text(encoding="utf-8")
        self.assertNotIn("KBP-DARK-MODE", client)

    def test_partial_uninstall_preserves_other_area_state(self):
        self.assertEqual(self.runp("install", str(self.tmp)).returncode, 0)
        self.assertEqual(self.runp("uninstall", str(self.tmp), "--admin-only").returncode, 0)
        state = json.loads((self.tmp / ".kbp-dark-mode/state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["installed_areas"], ["client"])
        self.assertFalse((self.tmp / "admin/css/kbp-dark-mode.css").exists())
        self.assertTrue((self.tmp / "client/skin/kbp-dark-mode.css").exists())
        self.assertIn("KBP-DARK-MODE:BEGIN", (self.tmp / "client/skin/view_default/default/page.html").read_text(encoding="utf-8"))

    def test_client_uses_real_skin_page(self):
        self.assertEqual(self.runp("install", str(self.tmp), "--client-only").returncode, 0)
        client = (self.tmp / "client/skin/view_default/default/page.html").read_text(encoding="utf-8")
        legacy = (self.tmp / "client/template.txt").read_text(encoding="utf-8")
        self.assertIn("KBP-DARK-MODE:BEGIN", client)
        self.assertNotIn("KBP-DARK-MODE:BEGIN", legacy)

    def test_upgrade_removes_v01_legacy_block(self):
        legacy = self.tmp / "client/template.txt"
        legacy.write_text(
            "<html><head>\n<!-- KBP-DARK-MODE:BEGIN -->\nold\n<!-- KBP-DARK-MODE:END -->\n</head><body></body></html>",
            encoding="utf-8",
        )
        self.assertEqual(self.runp("install", str(self.tmp), "--client-only").returncode, 0)
        self.assertNotIn("KBP-DARK-MODE:BEGIN", legacy.read_text(encoding="utf-8"))

    def test_upgrade_replaces_old_assets(self):
        old_css = self.tmp / "client/skin/kbp-dark-mode.css"
        old_css.write_text("/* old 0.2.0 */\n", encoding="utf-8")
        self.assertEqual(self.runp("install", str(self.tmp), "--client-only").returncode, 0)
        installed = old_css.read_text(encoding="utf-8")
        project = (PROJECT / "assets/client/kbp-dark-mode.css").read_text(encoding="utf-8")
        self.assertEqual(installed, project)
        self.assertIn('#search_menu', installed)
        self.assertIn('#search_field', installed)
        self.assertIn('.ezmodal-container', installed)

    def test_common_js_is_installed_in_both_areas(self):
        self.assertEqual(self.runp("install", str(self.tmp)).returncode, 0)
        source = (PROJECT / "assets/common/kbp-theme.js").read_bytes()
        self.assertEqual((self.tmp / "admin/jscript/kbp-theme.js").read_bytes(), source)
        self.assertEqual((self.tmp / "client/jscript/kbp-theme.js").read_bytes(), source)

    def test_version_is_030_and_single_source(self):
        self.assertEqual((PROJECT / "VERSION").read_text(encoding="utf-8").strip(), "0.3.0")
        patcher_text = PATCHER.read_text(encoding="utf-8")
        self.assertNotIn('VERSION = "0.3.0"', patcher_text)
        self.assertIn('VERSION = project_version()', patcher_text)

    def test_multiple_client_skins_are_detected(self):
        p = self.tmp / "client/skin/view_default/custom/page.html"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(CLIENT_PAGE, encoding="utf-8")
        self.assertEqual(self.runp("install", str(self.tmp), "--client-only").returncode, 0)
        self.assertIn("KBP-DARK-MODE:BEGIN", p.read_text(encoding="utf-8"))

    def test_check_detects_modified_asset(self):
        self.assertEqual(self.runp("install", str(self.tmp)).returncode, 0)
        css = self.tmp / "client/skin/kbp-dark-mode.css"
        css.write_text(css.read_text(encoding="utf-8") + "\n/* local */\n", encoding="utf-8")
        result = self.runp("check", str(self.tmp))
        self.assertEqual(result.returncode, 1)
        self.assertIn("MOD  client/skin/kbp-dark-mode.css", result.stdout)

    def test_malformed_markers_fail_safely(self):
        page = self.tmp / "admin/template/page.html"
        page.write_text(ADMIN_TEMPLATE.replace("</head>", "<!-- KBP-DARK-MODE:BEGIN -->\n</head>"), encoding="utf-8")
        result = self.runp("install", str(self.tmp), "--admin-only")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Marcadores incompletos", result.stderr)

    def test_dry_run_makes_no_changes(self):
        before = (self.tmp / "admin/template/page.html").read_bytes()
        result = self.runp("install", str(self.tmp), "--dry-run")
        self.assertEqual(result.returncode, 0)
        self.assertEqual((self.tmp / "admin/template/page.html").read_bytes(), before)
        self.assertFalse((self.tmp / ".kbp-dark-mode/state.json").exists())
        self.assertFalse((self.tmp / "admin/css/kbp-dark-mode.css").exists())
        self.assertIn("WOULD patch:", result.stdout)

    def test_crlf_is_preserved(self):
        page = self.tmp / "admin/template/page.html"
        page.write_bytes(ADMIN_TEMPLATE.replace("\n", "\r\n").encode("utf-8"))
        self.assertEqual(self.runp("install", str(self.tmp), "--admin-only").returncode, 0)
        data = page.read_bytes()
        self.assertIn(b"\r\n", data)
        self.assertNotIn(b"\n", data.replace(b"\r\n", b""))


if __name__ == "__main__":
    unittest.main()
