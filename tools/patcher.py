#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BEGIN = "<!-- KBP-DARK-MODE:BEGIN -->"
END = "<!-- KBP-DARK-MODE:END -->"

ADMIN_TARGETS = [
    "admin/template/page.html",
    "admin/template/page_popup.html",
    "admin/template/login.html",
]

LEGACY_CLIENT_TARGET = "client/template.txt"

ASSETS = {
    "admin/css/kbp-dark-mode.css": "assets/admin/kbp-dark-mode.css",
    "admin/jscript/kbp-theme.js": "assets/common/kbp-theme.js",
    "client/skin/kbp-dark-mode.css": "assets/client/kbp-dark-mode.css",
    "client/jscript/kbp-theme.js": "assets/common/kbp-theme.js",
}


def project_version() -> str:
    version_file = PROJECT_ROOT / "VERSION"
    version = version_file.read_text(encoding="utf-8").strip()
    if not version:
        raise RuntimeError("Arquivo VERSION vazio")
    return version


VERSION = project_version()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as f:
        return f.read()


def write_text(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        f.write(text)


def newline_for(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def client_targets(root: Path) -> list[str]:
    skin = root / "client" / "skin"
    if not skin.is_dir():
        return []

    return [
        path.relative_to(root).as_posix()
        for path in sorted(skin.glob("view_*/*/page.html"))
        if path.is_file()
    ]


def target_block(rel: str, newline: str = "\n") -> str:
    if rel.startswith("admin/"):
        lines = [
            "    <!-- KBP-DARK-MODE:BEGIN -->",
            '    <link rel="stylesheet" href="css/kbp-dark-mode.css?v={pvhash}">',
            '    <script src="jscript/kbp-theme.js?v={pvhash}"></script>',
            "    <!-- KBP-DARK-MODE:END -->",
            "",
        ]
    else:
        lines = [
            "    <!-- KBP-DARK-MODE:BEGIN -->",
            '    <link rel="stylesheet" href="{base_href}client/skin/kbp-dark-mode.css?v={pvhash}">',
            '    <script src="{base_href}client/jscript/kbp-theme.js?v={pvhash}"></script>',
            "    <!-- KBP-DARK-MODE:END -->",
            "",
        ]
    return newline.join(lines)


def selected(area: str, rel: str) -> bool:
    if area == "both":
        return True
    return rel.startswith(area + "/")


def validate_root(root: Path, area: str) -> None:
    if not root.is_dir():
        raise RuntimeError(f"Diretório do KBPublisher não encontrado: {root}")

    missing = []
    if area in ("both", "admin"):
        for rel in ADMIN_TARGETS:
            if not (root / rel).is_file():
                missing.append(rel)

    if area in ("both", "client"):
        if not (root / "client" / "skin").is_dir():
            missing.append("client/skin/")
        elif not client_targets(root):
            missing.append("client/skin/view_*/*/page.html")

    if missing:
        raise RuntimeError("Estrutura do KBPublisher não reconhecida. Ausentes: " + ", ".join(missing))


def validate_markers(text: str, rel: str = "template") -> int:
    begins = text.count(BEGIN)
    ends = text.count(END)
    if begins != ends:
        raise RuntimeError(f"Marcadores incompletos em {rel}: BEGIN={begins}, END={ends}")
    if begins > 1:
        raise RuntimeError(f"Marcadores duplicados em {rel}: {begins} blocos encontrados")
    return begins


def backup_file(root: Path, rel: str, backup_root: Path) -> None:
    src = root / rel
    if not src.exists():
        return
    dst = backup_root / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def replace_block(text: str, block: str, rel: str = "template") -> str:
    count = validate_markers(text, rel)
    if count == 1:
        before, rest = text.split(BEGIN, 1)
        _, after = rest.split(END, 1)
        if after.startswith("\r\n"):
            after = after[2:]
        elif after.startswith("\n"):
            after = after[1:]
        return before + block + after

    if "</head>" not in text:
        raise RuntimeError(f"Não foi encontrado </head> em {rel}")
    return text.replace("</head>", block + "</head>", 1)


def remove_block(text: str, rel: str = "template") -> str:
    count = validate_markers(text, rel)
    if count == 0:
        return text
    before, rest = text.split(BEGIN, 1)
    _, after = rest.split(END, 1)
    if before.endswith("    "):
        before = before[:-4]
    if after.startswith("\r\n"):
        after = after[2:]
    elif after.startswith("\n"):
        after = after[1:]
    return before + after


def all_targets(root: Path, area: str) -> list[str]:
    targets: list[str] = []
    if area in ("both", "admin"):
        targets.extend(ADMIN_TARGETS)
    if area in ("both", "client"):
        targets.extend(client_targets(root))
    return targets


def state_path(root: Path) -> Path:
    return root / ".kbp-dark-mode" / "state.json"


def load_state(root: Path) -> dict:
    path = state_path(root)
    if not path.is_file():
        return {}
    try:
        data = json.loads(read_text(path))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def write_state(root: Path, state: dict) -> None:
    path = state_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    write_text(path, json.dumps(state, indent=2, ensure_ascii=False) + "\n")


def selected_areas(area: str) -> set[str]:
    return {"admin", "client"} if area == "both" else {area}


def migrate_v01_legacy_client_patch(root: Path, backup_root: Path, dry_run: bool) -> bool:
    path = root / LEGACY_CLIENT_TARGET
    if not path.is_file():
        return False
    old = read_text(path)
    new = remove_block(old, LEGACY_CLIENT_TARGET)
    if new == old:
        return False
    if not dry_run:
        backup_file(root, LEGACY_CLIENT_TARGET, backup_root)
        write_text(path, new)
    return True


def do_install(root: Path, project: Path, area: str, dry_run: bool = False) -> int:
    validate_root(root, area)
    meta = root / ".kbp-dark-mode"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup_root = meta / "backups" / stamp
    touched: list[str] = []
    changed_templates: list[str] = []
    changed_assets: list[str] = []

    if area in ("both", "client"):
        if migrate_v01_legacy_client_patch(root, backup_root, dry_run):
            print(("WOULD " if dry_run else "DONE  ") + f"migrar ponto antigo da v0.1: {LEGACY_CLIENT_TARGET}")

    for rel in all_targets(root, area):
        path = root / rel
        old = read_text(path)
        block = target_block(rel, newline_for(old))
        new = replace_block(old, block, rel)
        if new != old:
            changed_templates.append(rel)
            if not dry_run:
                backup_file(root, rel, backup_root)
                write_text(path, new)
        touched.append(rel)

    asset_hashes: dict[str, str] = {}
    for rel, src_rel in ASSETS.items():
        if not selected(area, rel):
            continue
        src = project / src_rel
        dst = root / rel
        src_hash = sha256(src)
        current_hash = sha256(dst) if dst.exists() else None
        if current_hash != src_hash:
            changed_assets.append(rel)
            if not dry_run:
                if dst.exists():
                    backup_file(root, rel, backup_root)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
        asset_hashes[rel] = src_hash

    if dry_run:
        for rel in changed_templates:
            print("WOULD patch:", rel)
        for rel in changed_assets:
            print("WOULD copy :", rel)
        if not changed_templates and not changed_assets:
            print("Nenhuma alteração necessária.")
        return 0

    previous = load_state(root)
    areas = set(previous.get("installed_areas", []))
    if not areas and previous.get("area"):
        areas |= selected_areas(previous["area"])
    areas |= selected_areas(area)

    templates = set(previous.get("templates", []))
    templates.update(touched)

    assets = dict(previous.get("assets", {}))
    assets.update(asset_hashes)

    state = {
        "version": VERSION,
        "installed_areas": sorted(areas),
        "installed_at_utc": previous.get("installed_at_utc") or datetime.now(timezone.utc).isoformat(),
        "updated_at_utc": datetime.now(timezone.utc).isoformat(),
        "templates": sorted(templates),
        "assets": assets,
        "last_backup": str(backup_root.relative_to(root)) if backup_root.exists() else None,
    }
    write_state(root, state)

    print(f"KBP Dark Mode {VERSION} instalado ({area}).")
    print("Preferência padrão: Automático (segue o sistema operacional/navegador).")
    if backup_root.exists():
        print(f"Backup: {backup_root}")
    elif not changed_templates and not changed_assets:
        print("Nenhuma alteração necessária; instalação já estava atualizada.")
    return 0


def templates_to_uninstall(root: Path, area: str) -> list[str]:
    ret: list[str] = []
    for rel in all_targets(root, area):
        if rel not in ret:
            ret.append(rel)

    if area in ("both", "client") and (root / LEGACY_CLIENT_TARGET).is_file():
        ret.append(LEGACY_CLIENT_TARGET)

    state = load_state(root)
    for rel in state.get("templates", []):
        if selected(area, rel) and rel not in ret:
            ret.append(rel)
    return ret


def do_uninstall(root: Path, project: Path, area: str, dry_run: bool = False) -> int:
    if not root.is_dir():
        raise RuntimeError(f"Diretório do KBPublisher não encontrado: {root}")

    warnings: list[str] = []
    removed_templates: list[str] = []
    removed_assets: list[str] = []

    for rel in templates_to_uninstall(root, area):
        path = root / rel
        if not path.is_file():
            continue
        old = read_text(path)
        new = remove_block(old, rel)
        if new != old:
            removed_templates.append(rel)
            if not dry_run:
                write_text(path, new)

    for rel, src_rel in ASSETS.items():
        if not selected(area, rel):
            continue
        dst = root / rel
        src = project / src_rel
        if not dst.exists():
            continue
        if src.exists() and sha256(dst) == sha256(src):
            removed_assets.append(rel)
            if not dry_run:
                dst.unlink()
        else:
            warnings.append(f"Mantido arquivo modificado: {rel}")

    if dry_run:
        for rel in removed_templates:
            print("WOULD unpatch:", rel)
        for rel in removed_assets:
            print("WOULD remove :", rel)
        for warning in warnings:
            print("AVISO:", warning)
        if not removed_templates and not removed_assets:
            print("Nenhuma alteração necessária.")
        return 0

    state = load_state(root)
    remaining_areas = set(state.get("installed_areas", []))
    if area == "both":
        remaining_areas.clear()
    else:
        remaining_areas.discard(area)

    if remaining_areas:
        state["installed_areas"] = sorted(remaining_areas)
        state["templates"] = [rel for rel in state.get("templates", []) if not selected(area, rel)]
        state["assets"] = {rel: digest for rel, digest in state.get("assets", {}).items() if not selected(area, rel)}
        state["version"] = VERSION
        state["updated_at_utc"] = datetime.now(timezone.utc).isoformat()
        write_state(root, state)
    else:
        path = state_path(root)
        if path.exists():
            path.unlink()

    print(f"KBP Dark Mode removido ({area}).")
    for warning in warnings:
        print("AVISO:", warning)
    return 0


def do_check(root: Path, project: Path, area: str) -> int:
    validate_root(root, area)
    ok = True

    for rel in all_targets(root, area):
        text = read_text(root / rel)
        try:
            count = validate_markers(text, rel)
            present = count == 1
        except RuntimeError as exc:
            print("BAD  ", rel, "-", exc)
            ok = False
            continue
        print(("OK   " if present else "MISS ") + rel)
        ok = ok and present

    if area in ("both", "client") and (root / LEGACY_CLIENT_TARGET).is_file():
        legacy = read_text(root / LEGACY_CLIENT_TARGET)
        if BEGIN in legacy or END in legacy:
            print("WARN client/template.txt ainda contém bloco legado da v0.1")
            ok = False

    for rel, src_rel in ASSETS.items():
        if not selected(area, rel):
            continue
        dst = root / rel
        src = project / src_rel
        if not dst.is_file():
            print("MISS " + rel)
            ok = False
            continue
        if sha256(dst) != sha256(src):
            print("MOD  " + rel)
            ok = False
        else:
            print("OK   " + rel)

    state = load_state(root)
    if not state:
        print("WARN .kbp-dark-mode/state.json ausente ou inválido")
        ok = False
    elif state.get("version") != VERSION:
        print(f"WARN estado registra versão {state.get('version')!r}; pacote atual é {VERSION}")
        ok = False
    else:
        print(f"OK   state.json (versão {VERSION})")

    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Instalador do overlay Dark Mode para KBPublisher Community 8.x")
    parser.add_argument("action", choices=["install", "uninstall", "check"])
    parser.add_argument("root", type=Path, help="Diretório raiz do KBPublisher")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--admin-only", action="store_true")
    group.add_argument("--client-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Mostra alterações sem gravar arquivos (install/uninstall)")
    args = parser.parse_args()

    if args.action == "check" and args.dry_run:
        parser.error("--dry-run não se aplica à ação check")

    root = args.root.resolve()
    area = "admin" if args.admin_only else "client" if args.client_only else "both"

    try:
        if args.action == "install":
            return do_install(root, PROJECT_ROOT, area, args.dry_run)
        if args.action == "uninstall":
            return do_uninstall(root, PROJECT_ROOT, area, args.dry_run)
        return do_check(root, PROJECT_ROOT, area)
    except Exception as exc:
        print("ERRO:", exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
