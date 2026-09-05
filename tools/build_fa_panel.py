# -*- coding: utf-8 -*-
"""
سازندهٔ پنل فارسی edgetunnel
Builds the Persian (fa) admin panel by injecting a runtime translation
overlay into the pristine upstream HTML. The overlay:
  * sets <html lang="fa" dir="rtl"> and the page title,
  * swaps in a Persian font stack,
  * translates rendered Chinese text (text nodes + placeholder/title/aria)
    using the dictionary in fa_panel/fa_dict.py,
  * re-applies translations as the SPA renders content dynamically.

Usage:
    python tools/build_fa_panel.py

Input : tools/upstream-panel.zip   (pristine EDT-Pages.github.io archive)
Output: panel/admin/index.html     (translated, self-contained)
        panel/login/index.html     (hand-patched once; not overwritten)
"""
import io
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZIP = ROOT / "tools" / "upstream-panel.zip"
OUT = ROOT / "panel" / "admin" / "index.html"
ZIP_ADMIN = "EDT-Pages.github.io-main/admin/index.html"

sys.path.insert(0, str(ROOT / "tools"))
from fa_panel.fa_dict import all_entries  # noqa: E402

OVERLAY_CSS = """<style id="fa-i18n-style">
/* ---- Persian (fa) overrides ---- */
html[lang="fa"] body,
html[lang="fa"] button,
html[lang="fa"] input,
html[lang="fa"] select,
html[lang="fa"] textarea,
html[lang="fa"] .leaflet-container { font-family: 'Vazirmatn','Inter','Segoe UI',Tahoma,Arial,sans-serif !important; }
/* keep values/code left-to-right even inside the RTL layout */
html[lang="fa"] input,
html[lang="fa"] textarea,
html[lang="fa"] code,
html[lang="fa"] pre,
html[lang="fa"] .leaflet-container,
html[lang="fa"] .leaflet-popup-content { direction: ltr; text-align: left; }
html[lang="fa"] .leaflet-control, html[lang="fa"] .leaflet-popup { direction: ltr; }
</style>"""


def overlay_script(entries):
    data = json.dumps(entries, ensure_ascii=False)
    return """<script id="fa-i18n">
/* edgetunnel panel — Persian (fa) translation overlay */
(function () {
    'use strict';
    if (document.getElementById('fa-i18n')) return;
    var D = %s;
    var ATTRS = ['placeholder', 'title', 'aria-label'];
    try {
        document.documentElement.lang = 'fa';
        document.documentElement.dir = 'rtl';
    } catch (e) {}
    function tr(s) {
        if (!s) return s;
        for (var i = 0; i < D.length; i++) {
            var k = D[i][0];
            if (s.indexOf(k) >= 0) {
                s = s.split(k).join(D[i][1]);
            }
        }
        return s;
    }
    function hasHan(s) { return /[\\u4e00-\\u9fff]/.test(s); }
    function run() {
        try {
            if (document.title && hasHan(document.title)) document.title = tr(document.title);
            var root = document.documentElement;
            var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
            var nodes = [], n;
            while ((n = walker.nextNode())) { if (n.nodeValue && hasHan(n.nodeValue)) nodes.push(n); }
            for (var i = 0; i < nodes.length; i++) {
                var nt = tr(nodes[i].nodeValue);
                if (nt !== nodes[i].nodeValue) nodes[i].nodeValue = nt;
            }
            var els = root.querySelectorAll('*');
            for (var j = 0; j < els.length; j++) {
                var el = els[j];
                for (var a = 0; a < ATTRS.length; a++) {
                    var an = ATTRS[a];
                    if (el.hasAttribute(an)) {
                        var av = el.getAttribute(an);
                        if (av && hasHan(av)) {
                            var nv = tr(av);
                            if (nv !== av) el.setAttribute(an, nv);
                        }
                    }
                }
            }
        } catch (e) { if (window.console) console.log('[fa-i18n]', e); }
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', run);
    } else {
        run();
    }
    var scheduled = false;
    function schedule() {
        if (scheduled) return;
        scheduled = true;
        setTimeout(function () { scheduled = false; run(); }, 120);
    }
    if (window.MutationObserver) {
        try {
            new MutationObserver(schedule).observe(document.documentElement, {
                childList: true, subtree: true, characterData: true, attributes: false
            });
        } catch (e) {}
    } else {
        setInterval(run, 2000);
    }
})();
</script>""" % data


def main():
    if not ZIP.exists():
        print("missing %s — download it from github.com/EDT-Pages/EDT-Pages.github.io" % ZIP)
        return 1
    with zipfile.ZipFile(ZIP) as zf:
        html = zf.read(ZIP_ADMIN).decode("utf-8-sig")
    # lang / title
    html = html.replace('<html lang="zh-CN">', '<html lang="fa" dir="rtl">', 1)
    html = re.sub(r"<title>[^<]*</title>", "<title>پنل مدیریت</title>", html, count=1)
    # inject css + overlay before the closing body tag
    inject = OVERLAY_CSS + "\n" + overlay_script(all_entries())
    if "</body>" in html:
        html = html.replace("</body>", inject + "\n</body>", 1)
    else:
        html += inject
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print("wrote %s (%d bytes)" % (OUT, len(html)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
