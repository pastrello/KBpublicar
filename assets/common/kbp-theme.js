(function () {
    'use strict';

    var STORAGE_KEY = 'kbp_theme_mode';
    var MODES = ['auto', 'dark', 'light'];
    var media = null;

    function getMedia() {
        if (!media && window.matchMedia) {
            media = window.matchMedia('(prefers-color-scheme: dark)');
        }
        return media;
    }

    function readMode() {
        try {
            var mode = localStorage.getItem(STORAGE_KEY);
            return MODES.indexOf(mode) !== -1 ? mode : 'auto';
        } catch (e) {
            return 'auto';
        }
    }

    function resolvedMode(mode) {
        if (mode === 'auto') {
            var m = getMedia();
            return m && m.matches ? 'dark' : 'light';
        }
        return mode;
    }

    function strings() {
        var lang = (document.documentElement.lang || navigator.language || 'en').toLowerCase();
        if (lang.indexOf('pt') === 0) {
            return { theme: 'Tema', light: 'Claro', auto: 'Automático', dark: 'Escuro' };
        }
        return { theme: 'Theme', light: 'Light', auto: 'Auto', dark: 'Dark' };
    }

    function apply(mode, persist) {
        if (MODES.indexOf(mode) === -1) mode = 'auto';
        if (persist) {
            try { localStorage.setItem(STORAGE_KEY, mode); } catch (e) {}
        }

        var resolved = resolvedMode(mode);
        var root = document.documentElement;
        root.setAttribute('data-kbp-theme-mode', mode);
        root.setAttribute('data-kbp-theme', resolved);
        root.style.colorScheme = resolved;
        updateControl(mode);
    }

    function updateControl(mode) {
        var control = document.getElementById('kbp-theme-switcher');
        if (!control) return;
        var buttons = control.querySelectorAll('button[data-kbp-mode]');
        for (var i = 0; i < buttons.length; i++) {
            var active = buttons[i].getAttribute('data-kbp-mode') === mode;
            buttons[i].classList.toggle('is-active', active);
            buttons[i].setAttribute('aria-pressed', active ? 'true' : 'false');
        }
    }

    function makeButton(mode, label, symbol) {
        var button = document.createElement('button');
        button.type = 'button';
        button.setAttribute('data-kbp-mode', mode);
        button.setAttribute('aria-label', label);
        button.setAttribute('title', label);
        button.setAttribute('aria-pressed', 'false');

        var icon = document.createElement('span');
        icon.className = 'kbp-theme-icon';
        icon.setAttribute('aria-hidden', 'true');
        icon.textContent = symbol;

        var text = document.createElement('span');
        text.className = 'kbp-theme-text';
        text.textContent = label;

        button.appendChild(icon);
        button.appendChild(text);
        button.addEventListener('click', function () { apply(mode, true); });
        return button;
    }

    function createControl() {
        if (window.top !== window.self || document.getElementById('kbp-theme-switcher')) return;

        var s = strings();
        var control = document.createElement('div');
        control.id = 'kbp-theme-switcher';
        control.className = 'kbp-theme-switcher';
        control.setAttribute('role', 'group');
        control.setAttribute('aria-label', s.theme);

        var label = document.createElement('span');
        label.className = 'kbp-theme-switcher-label';
        label.textContent = s.theme + ':';
        control.appendChild(label);
        control.appendChild(makeButton('light', s.light, '\u2600'));
        control.appendChild(makeButton('auto', s.auto, '\u25D0'));
        control.appendChild(makeButton('dark', s.dark, '\u263E'));
        document.body.appendChild(control);
        updateControl(readMode());
    }

    function onSystemThemeChange() {
        if (readMode() === 'auto') apply('auto', false);
    }

    apply(readMode(), false);

    var m = getMedia();
    if (m) {
        if (m.addEventListener) m.addEventListener('change', onSystemThemeChange);
        else if (m.addListener) m.addListener(onSystemThemeChange);
    }

    window.addEventListener('storage', function (event) {
        if (event.key === STORAGE_KEY) apply(readMode(), false);
    });

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createControl);
    } else {
        createControl();
    }

    window.KBPTheme = {
        set: function (mode) { apply(mode, true); },
        get: readMode,
        resolved: function () { return resolvedMode(readMode()); }
    };
}());
