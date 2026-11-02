#!/usr/bin/env python3
"""Desktop UI audit: finds generic "AI slop" tells, desktop-feel mistakes,
accessibility gaps and design-token sprawl in an app's source. Standard library only.

Usage:
  ui_audit.py [PATH]                 scan a project folder (default: current folder)
  ui_audit.py src/ --max-per-rule 10 show more locations per rule (default 5)
  ui_audit.py . --json               machine-readable output
  ui_audit.py . --no-tokens          skip the design-token report

Scans web-stack UI (CSS/SCSS/Less, TSX/JSX/TS/JS, Vue, Svelte, HTML, Astro),
Electron main-process code, tauri.conf.json, SwiftUI (.swift) and WinUI/WPF (.xaml).
It pattern-matches, so treat every finding as a lead to verify, not a verdict.
Exit code: 1 if any Blocker or Major finding, else 0.
"""
import argparse
import colorsys
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contrast import parse as parse_color, ratio as contrast_ratio, blend  # noqa: E402

SKIP_DIRS = {
    "node_modules", ".git", "dist", "build", "out", ".next", ".nuxt", ".svelte-kit", "target",
    "vendor", "coverage", ".venv", "venv", "__pycache__", "Pods", "DerivedData", ".turbo",
    ".cache", "release", "bin", "obj", ".output", "storybook-static", ".expo", "gen",
}
WEB_EXT = {".css", ".scss", ".sass", ".less", ".tsx", ".jsx", ".ts", ".js", ".mjs", ".cjs",
           ".vue", ".svelte", ".html", ".astro"}
STYLE_EXT = {".css", ".scss", ".sass", ".less"}
MARKUP_EXT = {".tsx", ".jsx", ".vue", ".svelte", ".html", ".astro"}
SEVERITIES = ["Blocker", "Major", "Minor", "Polish"]

RULES = {
    # id: (severity, title, fix, reference)
    "focus-removed": ("Major", "Focus outline removed",
        "Keep a visible :focus-visible ring (2px+, 3:1 contrast, not box-shadow only) on every control.",
        "accessibility.md §2, §10"),
    "focus-removed-nowhere": ("Blocker", "Focus outline removed and no :focus-visible style anywhere",
        "Keyboard users can't see where they are. Add a designed :focus-visible ring for all controls.",
        "accessibility.md §2, §10"),
    "transition-all": ("Major", "`transition: all` / `transition-all`",
        "Name the properties (transform, opacity, color, background-color). `all` animates layout and feels janky.",
        "motion.md §0, §7.1"),
    "no-reduced-motion": ("Major", "Animations but no reduced-motion handling anywhere",
        "Honor prefers-reduced-motion (CSS media query, Tailwind motion-reduce:, Motion reducedMotion=\"user\"): replace movement with fades.",
        "motion.md §8, accessibility.md §4"),
    "motion-lib-default": ("Major", "Motion/Framer Motion used without reducedMotion=\"user\"",
        "Wrap the app in <MotionConfig reducedMotion=\"user\">; the library ignores the OS setting by default.",
        "motion.md §4.4, §8"),
    "browser-dialog": ("Major", "Browser alert()/confirm()/prompt() in a desktop app",
        "Use undo for routine deletes, an inline error next to the source, or a native dialog for irreversible actions.",
        "interaction.md §4.13, cross-platform.md Part C"),
    "hover-only": ("Major", "Controls revealed only on hover",
        "Also reveal on keyboard focus (group-focus-within / :focus-within) and keep a non-hover path (context menu, selection).",
        "accessibility.md §10"),
    "electron-frameless": ("Major", "Electron window with frame:false and no native controls overlay",
        "Use titleBarStyle 'hidden'/'hiddenInset' + titleBarOverlay so traffic lights / caption buttons, Snap Layouts and drag regions keep working.",
        "cross-platform.md B1, windows.md §6"),
    "electron-menu-removed": ("Major", "Application menu removed",
        "Keep a menu built from roles (undo, redo, cut, copy, paste, selectAll, zoom, window, quit); on macOS the menu bar is required.",
        "cross-platform.md B1, macos.md §3"),
    "electron-ctrl-accelerator": ("Major", "Hard-coded Ctrl accelerator",
        "Use 'CmdOrCtrl+…' (or per-OS tables) so Mac users get ⌘.",
        "cross-platform.md A2"),
    "xaml-hardcoded-color": ("Major", "Hard-coded color in XAML",
        "Use {ThemeResource …} brushes so Light, Dark and contrast themes work.",
        "windows.md §4"),
    "xaml-no-focus": ("Blocker", "System focus visuals turned off",
        "Remove UseSystemFocusVisuals=\"False\"; keyboard users need the focus rect.",
        "windows.md §11"),
    "low-contrast-pair": ("Major", "Text/background pair below 4.5:1",
        "Raise text contrast (run scripts/contrast.py FG BG --fix).",
        "accessibility.md §0, §6"),
    "low-contrast-on-base": ("Minor", "Text color below 4.5:1 on the app's base background",
        "If this text sits on the base background, darken/lighten it (scripts/contrast.py --fix).",
        "accessibility.md §6"),
    "tailwind-light-gray-text": ("Minor", "Light gray text (300/400 shade)",
        "gray-400 on white is about 2.5:1. Use 500–600 on light surfaces; keep 400 for dark mode only.",
        "accessibility.md §6"),
    "electron-white-flash": ("Minor", "BrowserWindow without backgroundColor / show:false",
        "Create hidden (show:false), set backgroundColor to the app's surface, show on 'ready-to-show'.",
        "cross-platform.md B1"),
    "electron-quit-on-close-mac": ("Minor", "Quits when the last window closes, also on macOS",
        "Guard with process.platform !== 'darwin'; Mac apps stay running and reopen on Dock click.",
        "cross-platform.md A1"),
    "tauri-no-decorations": ("Minor", "Tauri window with decorations:false",
        "A custom title bar must keep native controls, drag region, double-click and Snap; prefer titleBarStyle 'Overlay' on macOS.",
        "cross-platform.md B2"),
    "toast-error": ("Minor", "Errors shown in toasts",
        "Show errors next to their source with a next step; toasts auto-dismiss and are easy to miss.",
        "interaction.md §4.14, visual-craft.md §10"),
    "layout-transition": ("Minor", "Transitions on layout properties",
        "Animate transform/opacity; use FLIP/layout animation for size and position changes.",
        "motion.md §7.0"),
    "long-duration": ("Minor", "Animation of 500 ms or longer",
        "Routine desktop UI: 80–150 ms feedback, 150–200 menus, 200–300 panels/dialogs, nothing routine over 400 ms.",
        "motion.md §3.1"),
    "pointer-cursor-buttons": ("Minor", "Pointing-hand cursor on buttons",
        "Desktop convention: arrow cursor on buttons and menu items, hand only on links.",
        "cross-platform.md A4"),
    "emoji-ui": ("Minor", "Emoji or dingbat characters used as icons",
        "Emoji render differently on each OS and read as generic. Use the app's icon set (SF Symbols, Fluent, Adwaita, or one chosen family).",
        "visual-craft.md §7"),
    "placeholder-data": ("Minor", "Placeholder or fake content",
        "Use realistic, varied content: long names, missing images, 0/1/999+ counts, accented and RTL text.",
        "visual-craft.md §7, §9"),
    "webkit-prefix": ("Minor", "Unprefixed property that WebKit webviews need prefixed",
        "Tauri/Wails use WKWebView/WebKitGTK: add -webkit-user-select / -webkit-backdrop-filter.",
        "cross-platform.md B2"),
    "no-user-select": ("Minor", "App chrome text is selectable like a web page",
        "Set user-select: none (and -webkit-user-select) on chrome; keep content, inputs and messages selectable.",
        "cross-platform.md Part C"),
    "swift-fixed-font": ("Minor", "Fixed font size in SwiftUI",
        "Use text styles (.body is 13 pt on Mac; .headline, .caption…) so sizes stay consistent and scale.",
        "macos.md §7"),
    "swift-hardcoded-color": ("Minor", "Hard-coded color in SwiftUI/AppKit",
        "Use semantic colors (.primary, .secondary, Color(nsColor: .labelColor)) or asset-catalog colors with light/dark variants.",
        "macos.md §7"),
    "swift-tap-gesture": ("Minor", "onTapGesture used for an action",
        "Use Button (keyboard, VoiceOver and focus work); keep onTapGesture for non-actions.",
        "accessibility.md §3"),
    "swift-no-reduce-motion": ("Minor", "SwiftUI animations but no Reduce Motion check",
        "Read @Environment(\\.accessibilityReduceMotion) and swap movement for fades.",
        "motion.md §8"),
    "xaml-fixed-font": ("Minor", "Fixed FontSize in XAML",
        "Use the type ramp styles (BodyTextBlockStyle, SubtitleTextBlockStyle…) so text scaling and consistency work.",
        "windows.md §3"),
    "purple-gradient": ("Polish", "Purple/indigo gradient",
        "The default 'AI' look. Pick an accent from the product's world and use it sparingly; solid surfaces.",
        "visual-craft.md §7"),
    "gradient-text": ("Polish", "Gradient text",
        "Solid text colors; use color only where it carries meaning.",
        "visual-craft.md §7"),
    "sparkle-ai": ("Polish", "Sparkle icon for AI features",
        "Name the action ('Summarize', 'Draft reply') with a specific icon in the normal accent.",
        "visual-craft.md §7"),
    "scale-from-zero": ("Polish", "Element scales in from 0",
        "Start from scale 0.95–0.97 plus opacity, from the trigger's origin.",
        "motion.md §0"),
    "entrance-everywhere": ("Polish", "Entrance animation on many elements",
        "Animate in response to input or real state changes, not every element on mount.",
        "motion.md §1, visual-craft.md §7"),
    "glass-everywhere": ("Polish", "Blur/glass used in many places",
        "Use the platform material only where the OS does (sidebar, toolbar, popovers); never on content.",
        "visual-craft.md §7, macos.md §1, windows.md §5"),
    "huge-z-index": ("Polish", "Very large z-index",
        "Use a small layer scale (base, dropdown, sticky, overlay, modal, toast).",
        "visual-craft.md §9"),
    "marketing-greeting": ("Polish", "Marketing-style greeting in the app",
        "Apps open to the user's work or last state, not a hero banner.",
        "visual-craft.md §7"),
    "swift-hidden-titlebar": ("Polish", "Hidden title bar style",
        "Fine for special windows; keep the traffic lights and a draggable area. Main windows use the standard title/toolbar.",
        "macos.md §2"),
}

EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\U00002700-\U000027BF\U00002600-\U000026FF\U0001F000-\U0001F2FF]")
HEX_RE = r"#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b"
COLOR_LIT_RE = re.compile(HEX_RE + r"|rgba?\([^)]*\)|hsla?\([^)]*\)|oklch\([^)]*\)|oklab\([^)]*\)")
PURPLE_NAMES = {"purple", "violet", "indigo", "fuchsia", "magenta", "blueviolet", "mediumpurple", "darkviolet", "rebeccapurple"}
TW_SIZES = r"(?:xs|sm|base|lg|xl|[2-9]xl)"


class Audit:
    def __init__(self, root, max_per_rule):
        self.root = root
        self.max = max_per_rule
        self.findings = defaultdict(list)  # rule -> [(path, line, snippet)]
        self.files = Counter()
        self.flags = Counter()  # project-level presence flags
        self.tokens = defaultdict(Counter)
        self.base_bg = None
        self.color_decls = []  # (path, line, color)
        self.stack = set()
        self.current_text = ""

    def add(self, rule, path, line, snippet):
        self.findings[rule].append((os.path.relpath(path, self.root), line, snippet.strip()[:120]))

    # ---------- walking ----------
    def run(self):
        self.detect_stack()
        for dirpath, dirnames, filenames in os.walk(self.root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
            for fn in filenames:
                path = os.path.join(dirpath, fn)
                ext = os.path.splitext(fn)[1].lower()
                if ".min." in fn or fn.endswith(".d.ts"):
                    continue
                try:
                    if os.path.getsize(path) > 1_000_000:
                        continue
                except OSError:
                    continue
                if ext in WEB_EXT:
                    self.scan_web(path, ext)
                elif ext == ".swift":
                    self.scan_swift(path)
                elif ext == ".xaml":
                    self.scan_xaml(path)
                elif fn in ("tauri.conf.json", "tauri.conf.json5", "Tauri.toml"):
                    self.scan_tauri(path)
        self.project_checks()

    def detect_stack(self):
        pj = os.path.join(self.root, "package.json")
        if os.path.isfile(pj):
            try:
                with open(pj, encoding="utf-8", errors="replace") as f:
                    data = json.load(f)
            except (ValueError, OSError):
                data = {}
            deps = {}
            for key in ("dependencies", "devDependencies"):
                deps.update(data.get(key) or {})
            for name, tag in (("electron", "electron"), ("@tauri-apps/api", "tauri"), ("react", "react"),
                              ("vue", "vue"), ("svelte", "svelte"), ("tailwindcss", "tailwind"),
                              ("framer-motion", "motion"), ("motion", "motion"), ("@wailsio/runtime", "wails")):
                if name in deps:
                    self.stack.add(tag)
        for marker, tag in (("src-tauri", "tauri"), ("wails.json", "wails")):
            if os.path.exists(os.path.join(self.root, marker)):
                self.stack.add(tag)

    def read(self, path):
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                return f.read()
        except OSError:
            return ""

    # ---------- web ----------
    def scan_web(self, path, ext):
        text = self.read(path)
        if not text:
            return
        self.files["web"] += 1
        low = text.lower()
        for needle, flag in (("focus-visible", "focus_visible"), ("prefers-reduced-motion", "reduced_motion"),
                             ("motion-reduce:", "reduced_motion"), ("motion-safe:", "reduced_motion"),
                             ("usereducedmotion", "reduced_motion"), ("reducedmotion", "reduced_motion_cfg"),
                             ("user-select", "user_select"), ("@keyframes", "anim"), ("animation:", "anim"),
                             ("animate-", "anim"), ("transition-transform", "anim"), ("transition-all", "anim")):
            if needle in low:
                self.flags[flag] += 1
        self.current_text = text
        if re.search(r"transition(-property)?\s*:[^;{}]*\b(all|transform|translate|scale|rotate|top|left|right|bottom|width|height|margin)\b", text):
            self.flags["anim"] += 1
        uses_motion_lib = re.search(r"from\s+['\"](framer-motion|motion/react|motion)['\"]", text)
        if uses_motion_lib:
            self.flags["motion_lib"] += 1
            self.flags["anim"] += 1
        if "new BrowserWindow" in text:
            self.scan_electron_main(path, text)
        is_markup = ext in MARKUP_EXT
        is_style = ext in STYLE_EXT
        in_block_comment = False
        for n, line in enumerate(text.splitlines(), 1):
            s = line.strip()
            if in_block_comment:
                if "*/" in s:
                    in_block_comment = False
                continue
            if s.startswith("/*") and "*/" not in s:
                in_block_comment = True
                continue
            if s.startswith(("//", "<!--", "/*")):
                continue
            self.web_line(path, n, line, s, is_markup, is_style, ext)
        if is_style or ext in (".vue", ".svelte", ".html", ".astro"):
            self.css_blocks(path, text)

    def web_line(self, path, n, line, s, is_markup, is_style, ext):
        if re.search(r"transition(-property)?\s*:\s*all\b|\btransition-all\b|transition:\s*['\"]all", s):
            self.add("transition-all", path, n, s)
        if re.search(r"outline\s*:\s*(none|0)\b|(?<![\w-])outline-none\b|outline:\s*['\"]none", s) \
                and ":not(:focus-visible)" not in s and "focus:not(" not in s:
            self.add("focus-removed", path, n, s)
        if re.search(r"(?<![\w.$])(?:window\.)?(alert|confirm|prompt)\(\s*['\"`]", s):
            self.add("browser-dialog", path, n, s)
        if re.search(r"toast\.error\(|variant:\s*['\"]destructive['\"]", s):
            self.add("toast-error", path, n, s)
        if re.search(r"group-hover:(opacity-100|flex|block|visible|inline-flex|grid)\b", s) and "focus" not in s:
            self.add("hover-only", path, n, s)
        if re.search(r"transition(-property)?\s*:[^;{}]*\b(width|height|top|left|right|bottom|margin[\w-]*|padding[\w-]*)\b", s):
            self.add("layout-transition", path, n, s)
        long_anim = any(float(m.group(1)) * (1 if m.group(2) == "ms" else 1000) >= 500
                        for m in re.finditer(r"(?:transition|animation)(?:-duration)?\s*:[^;{}]*?(\d*\.?\d+)(ms|s)\b", s))
        if long_anim or re.search(r"\bduration-(500|700|1000|\[\d{3,}ms\])\b", s) \
                or re.search(r"duration:\s*(0\.[5-9]|[1-9](\.\d+)?)\b(?!\s*ms)", s):
            self.add("long-duration", path, n, s)
        if re.search(r"\bscale\(\s*0\s*\)|(?<![\w-])scale-0\b|scale:\s*0\s*[,}]", s):
            self.add("scale-from-zero", path, n, s)
        if re.search(r"(?:-webkit-)?background-clip\s*:\s*text|\bbg-clip-text\b|backgroundClip:\s*['\"]text", s):
            self.add("gradient-text", path, n, s)
        if self.is_purple_gradient(s):
            self.add("purple-gradient", path, n, s)
        if re.search(r"\bSparkles?\b|✨|sparkle", s) and not s.startswith("import type"):
            self.add("sparkle-ai", path, n, s)
        if re.search(r"z-index\s*:\s*(\d{5,}|9999)\b|\bz-\[(\d{5,}|9999)\]|zIndex:\s*(\d{5,}|9999)\b", s):
            self.add("huge-z-index", path, n, s)
        if re.search(r"lorem ipsum|\bJohn Doe\b|\bJane Doe\b|\bAcme (Inc|Corp)\b|\$1,234\b", s, re.I):
            self.add("placeholder-data", path, n, s)
        if re.search(r"backdrop-filter|backdrop-blur|backdropFilter", s):
            self.flags["glass"] += 1
            if "-webkit-backdrop-filter" not in self.current_text and "backdrop-filter" in s and {"tauri", "wails"} & self.stack:
                self.add("webkit-prefix", path, n, s)
        if re.search(r"(?<!-webkit-)user-select\s*:\s*none", s) and {"tauri", "wails"} & self.stack \
                and "-webkit-user-select" not in self.current_text:
            self.add("webkit-prefix", path, n, s)
        if re.search(r"\btext-(gray|zinc|neutral|slate|stone)-(300|400)\b", s) and not re.search(r"dark:text-(gray|zinc|neutral|slate|stone)-(300|400)", s):
            self.add("tailwind-light-gray-text", path, n, s)
        if re.search(r"initial=\{\{[^}]*opacity:\s*0", s) or re.search(r"\banimate-(fade|slide)-?(in|up)\b", s):
            self.add("entrance-everywhere", path, n, s)
        if is_markup or ext in (".ts", ".js"):
            if EMOJI_RE.search(s) and not re.search(r"✨", s):
                self.add("emoji-ui", path, n, s)
            if re.search(r"Welcome (back|to)\b", s):
                self.add("marketing-greeting", path, n, s)
            if re.search(r"<button[^>]*cursor-pointer|cursor-pointer[^>]*<button|<Button[^>]*cursor-pointer", s):
                self.add("pointer-cursor-buttons", path, n, s)
            if re.search(r"(accelerator\s*:\s*|globalShortcut\.register\(\s*)['\"]Ctrl\+", s):
                self.add("electron-ctrl-accelerator", path, n, s)
            if re.search(r"Menu\.setApplicationMenu\(\s*null\s*\)|\.removeMenu\(\)|\.setMenu\(\s*null\s*\)", s):
                self.add("electron-menu-removed", path, n, s)
        self.collect_tokens(s, is_style)

    def is_purple_gradient(self, s):
        if re.search(r"\b(from|via|to)-(purple|violet|indigo|fuchsia)-\d{2,3}\b", s):
            return True
        m = re.search(r"(?:linear|radial|conic)-gradient\((.*)", s)
        if not m:
            return False
        body = m.group(1).lower()
        if any(re.search(r"\b%s\b" % name, body) for name in PURPLE_NAMES):
            return True
        for lit in re.findall(HEX_RE, body):
            try:
                r, g, b, _ = parse_color(lit)
            except ValueError:
                continue
            h, l, sat = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            if 235 <= h * 360 <= 300 and sat > 0.35 and 0.2 < l < 0.85:
                return True
        return False

    def css_blocks(self, path, text):
        clean = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
        for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", clean):
            selector, body = m.group(1).strip(), m.group(2)
            line = clean.count("\n", 0, m.start(2)) + 1
            fg = re.search(r"(?<![\w-])color\s*:\s*(" + HEX_RE + r"|rgba?\([^)]*\))", body)
            bg = re.search(r"background(?:-color)?\s*:\s*(" + HEX_RE + r"|rgba?\([^)]*\))\s*(?:;|$|!)", body)
            sel_last = selector.split("\n")[-1].strip()
            if re.search(r"(^|[\s,])(html|body|:root|#root|#app|\.app)\s*$", sel_last) and bg and self.base_bg is None:
                if "@media" not in selector:
                    self.base_bg = bg.group(1)
            if fg and bg:
                self.check_pair(path, line, fg.group(1), bg.group(1), selector)
            elif fg:
                self.color_decls.append((path, line, fg.group(1), sel_last))
            if ":hover" in sel_last and re.search(r"opacity\s*:\s*1\b|visibility\s*:\s*visible|display\s*:\s*(block|flex|grid|inline)", body) \
                    and "focus-within" not in clean and "focus-visible" not in clean:
                self.add("hover-only", path, line, sel_last + " { … }")
            if re.search(r"cursor\s*:\s*pointer", body) and re.search(r"button|\.btn|\[role=.?button|menu|tab\b|toolbar", sel_last, re.I):
                self.add("pointer-cursor-buttons", path, line, sel_last + " { cursor: pointer }")

    def check_pair(self, path, line, fg_s, bg_s, selector):
        try:
            fg, bg = parse_color(fg_s), parse_color(bg_s)
        except ValueError:
            return
        if bg[3] < 1:
            return
        r = contrast_ratio(blend(fg, bg[:3]), bg[:3])
        if r < 4.5:
            self.add("low-contrast-pair", path, line, "%s: %s on %s = %.2f:1" % (selector.split("\n")[-1].strip()[:50], fg_s, bg_s, int(r * 100) / 100))

    def collect_tokens(self, s, is_style):
        t = self.tokens
        for m in re.finditer(r"font-size\s*:\s*([^;}{]+)", s):
            v = m.group(1).strip()
            if not v.startswith("var("):
                t["font sizes"][v] += 1
        for m in re.finditer(r"(?<![\w-])text-(" + TW_SIZES + r"|\[[^\]]+\])(?![\w-])", s):
            t["font sizes"]["text-" + m.group(1)] += 1
        for m in re.finditer(r"border-radius\s*:\s*([^;}{]+)", s):
            v = m.group(1).strip()
            if not v.startswith("var("):
                t["radii"][v] += 1
        for m in re.finditer(r"(?<![\w-])rounded(?:-[trbl]{1,2})?(-(?:none|sm|md|lg|xl|[23]xl|full|\[[^\]]+\]))?(?![\w-])", s):
            t["radii"]["rounded" + (m.group(1) or "")] += 1
        for m in re.finditer(r"box-shadow\s*:\s*([^;}{]+)", s):
            v = m.group(1).strip()
            if not v.startswith("var(") and v != "none":
                t["shadows"][v[:60]] += 1
        for m in re.finditer(r"(?<![\w-])shadow(-(?:sm|md|lg|xl|2xl|inner|\[[^\]]+\]))?(?![\w-])", s):
            t["shadows"]["shadow" + (m.group(1) or "")] += 1
        for m in re.finditer(r"(?:transition|animation)(?:-duration)?\s*:[^;{}]*?(\d*\.?\d+(?:ms|s))\b", s):
            t["durations"][m.group(1)] += 1
        for m in re.finditer(r"\bduration-(\d+)\b", s):
            t["durations"][m.group(1) + "ms"] += 1
        for m in re.finditer(r"font-weight\s*:\s*(\d{3}|bold|normal)", s):
            t["font weights"][m.group(1)] += 1
        for m in re.finditer(r"(?<![\w-])font-(thin|extralight|light|normal|medium|semibold|bold|extrabold|black)\b", s):
            t["font weights"][m.group(1)] += 1
        for m in re.finditer(r"font-family\s*:\s*([^;}{]+)", s):
            fam = m.group(1).split(",")[0].strip().strip("'\"")
            if not fam.startswith("var("):
                t["font families"][fam] += 1
        for m in re.finditer(r"(?:padding|margin|gap|row-gap|column-gap)(?:-[a-z]+)?\s*:\s*([^;}{]+)", s):
            for px in re.findall(r"(?<![\d.])(\d+(?:\.\d+)?)px", m.group(1)):
                v = float(px)
                if v > 2 and v % 4:
                    t["off-grid spacing"][px + "px"] += 1
        decl = re.match(r"\s*--[\w-]+\s*:", s)
        if not decl:
            for lit in COLOR_LIT_RE.findall(s):
                t["color literals"][lit.lower()] += 1
        for m in re.finditer(r"(?<![\w-])(?:bg|text|border|from|to|via|fill|stroke)-\[(#[0-9a-fA-F]{3,8}|rgb[^\]]*)\]", s):
            t["color literals"][m.group(1).lower()] += 1

    def scan_electron_main(self, path, text):
        for m in re.finditer(r"new BrowserWindow\(\s*\{(.*?)\}\s*\)", text, flags=re.S):
            opts = m.group(1)
            line = text.count("\n", 0, m.start()) + 1
            if re.search(r"frame\s*:\s*false", opts) and "titleBarOverlay" not in opts and "titleBarStyle" not in opts:
                self.add("electron-frameless", path, line, "new BrowserWindow({ frame: false … })")
            missing = [k for k in ("backgroundColor", "show") if not re.search(r"\b%s\s*:" % k, opts)]
            if missing and "ready-to-show" not in text:
                self.add("electron-white-flash", path, line, "missing: " + ", ".join(missing))
        if "window-all-closed" in text and "app.quit" in text and "darwin" not in text:
            line = text[: text.index("window-all-closed")].count("\n") + 1
            self.add("electron-quit-on-close-mac", path, line, "app.on('window-all-closed', … app.quit())")

    # ---------- native ----------
    def scan_swift(self, path):
        text = self.read(path)
        if not text or "SwiftUI" not in text and "AppKit" not in text and "Cocoa" not in text:
            return
        self.files["swift"] += 1
        if "accessibilityReduceMotion" in text or "reduceMotion" in text:
            self.flags["swift_reduce"] += 1
        for n, line in enumerate(text.splitlines(), 1):
            s = line.strip()
            if s.startswith("//"):
                continue
            if re.search(r"\.font\(\.system\(size:", s):
                self.add("swift-fixed-font", path, n, s)
            if re.search(r"Color\(\s*red:|Color\(\s*hex|NSColor\(\s*(calibrated|srgb|device)?[Rr]ed:|Color\(\s*#", s):
                self.add("swift-hardcoded-color", path, n, s)
            if ".onTapGesture" in s:
                self.add("swift-tap-gesture", path, n, s)
            if re.search(r"withAnimation|\.animation\(|\.transition\(", s):
                self.flags["swift_anim"] += 1
            if ".hiddenTitleBar" in s:
                self.add("swift-hidden-titlebar", path, n, s)
            if EMOJI_RE.search(s) and '"' in s:
                self.add("emoji-ui", path, n, s)

    def scan_xaml(self, path):
        text = self.read(path)
        if not text:
            return
        self.files["xaml"] += 1
        for n, line in enumerate(text.splitlines(), 1):
            s = line.strip()
            if re.search(r"\b(Background|Foreground|Fill|BorderBrush|Stroke)=\"#[0-9A-Fa-f]{6,8}\"", s):
                self.add("xaml-hardcoded-color", path, n, s)
            if re.search(r"\bFontSize=\"\d+(\.\d+)?\"", s):
                self.add("xaml-fixed-font", path, n, s)
            if 'UseSystemFocusVisuals="False"' in s:
                self.add("xaml-no-focus", path, n, s)

    def scan_tauri(self, path):
        text = self.read(path)
        for n, line in enumerate(text.splitlines(), 1):
            if re.search(r"\"?decorations\"?\s*[:=]\s*false", line):
                self.add("tauri-no-decorations", path, n, line)

    # ---------- project-level ----------
    def project_checks(self):
        if "focus-removed" in self.findings and not self.flags["focus_visible"]:
            self.findings["focus-removed-nowhere"] = self.findings.pop("focus-removed")
        if self.flags["anim"] and not self.flags["reduced_motion"] and not self.flags["reduced_motion_cfg"]:
            self.findings["no-reduced-motion"].append(("(project)", 0, "animations found, no prefers-reduced-motion / motion-reduce: / useReducedMotion"))
        if self.flags["motion_lib"] and not self.flags["reduced_motion_cfg"]:
            self.findings["motion-lib-default"].append(("(project)", 0, "framer-motion / motion imported; no reducedMotion setting found"))
        if self.flags["swift_anim"] and not self.flags["swift_reduce"]:
            self.findings["swift-no-reduce-motion"].append(("(project)", 0, "withAnimation/.animation used; accessibilityReduceMotion never read"))
        if {"electron", "tauri", "wails"} & self.stack and self.files["web"] and not self.flags["user_select"]:
            self.findings["no-user-select"].append(("(project)", 0, "no user-select rule anywhere"))
        if len(self.findings.get("entrance-everywhere", [])) < 4:
            self.findings.pop("entrance-everywhere", None)
        if self.flags["glass"] >= 6:
            self.findings["glass-everywhere"].append(("(project)", 0, "%d blur/backdrop uses" % self.flags["glass"]))
        if self.base_bg:
            seen = set()
            for path, line, color, sel in self.color_decls:
                try:
                    fg, bg = parse_color(color), parse_color(self.base_bg)
                except ValueError:
                    continue
                r = contrast_ratio(blend(fg, bg[:3]), bg[:3])
                if r < 4.5 and (color, sel) not in seen:
                    seen.add((color, sel))
                    self.add("low-contrast-on-base", path, line, "%s { color: %s } on base %s = %.2f:1" % (sel[:40], color, self.base_bg, int(r * 100) / 100))

    # ---------- output ----------
    def token_report(self):
        limits = {"font sizes": 8, "radii": 6, "shadows": 5, "durations": 6, "font weights": 4,
                  "color literals": 24, "off-grid spacing": 0, "font families": 3}
        rows = []
        for key in ("font sizes", "font weights", "font families", "radii", "shadows", "durations",
                    "color literals", "off-grid spacing"):
            c = self.tokens.get(key)
            if not c:
                continue
            over = len(c) > limits[key]
            rows.append((key, len(c), over, [v for v, _ in c.most_common(12)]))
        return rows

    def print_text(self, show_tokens):
        stack = ", ".join(sorted(self.stack)) or "not detected"
        counts = ", ".join("%s %d" % (k, v) for k, v in sorted(self.files.items())) or "none"
        print("UI audit of %s  (files: %s; stack: %s)\n" % (self.root, counts, stack))
        total = 0
        for sev in SEVERITIES:
            rules = [r for r in self.findings if self.findings[r] and RULES[r][0] == sev]
            if not rules:
                continue
            n = sum(len(self.findings[r]) for r in rules)
            total += n
            print("%s (%d)" % (sev.upper(), n))
            for r in sorted(rules, key=lambda r: -len(self.findings[r])):
                _, title, fix, ref = RULES[r]
                hits = self.findings[r]
                print("  [%s] %s  x%d" % (r, title, len(hits)))
                for path, line, snip in hits[: self.max]:
                    loc = path if line == 0 else "%s:%d" % (path, line)
                    print("      %s  %s" % (loc, snip))
                if len(hits) > self.max:
                    print("      … %d more" % (len(hits) - self.max))
                print("      fix: %s  (references/%s)" % (fix, ref))
            print()
        if not total:
            print("No pattern-level issues found. That doesn't mean the UI is good: still run the review checklist.\n")
        if show_tokens:
            rows = self.token_report()
            if rows:
                print("DESIGN TOKENS (distinct values used directly; fewer = more consistent)")
                for key, n, over, top in rows:
                    flag = "  <- too many: define a scale and use tokens" if over else ""
                    if key == "off-grid spacing" and n:
                        flag = "  <- not on a 4px grid"
                    print("  %-17s %3d  %s%s" % (key, n, " ".join(top), flag))
                print()
        print("These are leads from pattern matching, not verdicts. Open each location and confirm before changing it.")

    def as_json(self):
        out = {"root": self.root, "stack": sorted(self.stack), "files": dict(self.files), "findings": [], "tokens": {}}
        for r, hits in self.findings.items():
            if not hits:
                continue
            sev, title, fix, ref = RULES[r]
            out["findings"].append({"rule": r, "severity": sev, "title": title, "fix": fix, "reference": ref,
                                    "locations": [{"file": p, "line": l, "snippet": s} for p, l, s in hits]})
        for key, n, over, top in self.token_report():
            out["tokens"][key] = {"distinct": n, "too_many": over, "most_used": top}
        return out


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("path", nargs="?", default=".", help="project folder or file to scan")
    p.add_argument("--max-per-rule", type=int, default=5, help="locations shown per rule (default 5)")
    p.add_argument("--json", action="store_true", help="JSON output")
    p.add_argument("--no-tokens", action="store_true", help="skip the design-token report")
    a = p.parse_args()
    root = os.path.abspath(a.path)
    if not os.path.exists(root):
        p.error("no such path: %s" % a.path)
    audit = Audit(root if os.path.isdir(root) else os.path.dirname(root), a.max_per_rule)
    if os.path.isfile(root):
        ext = os.path.splitext(root)[1].lower()
        if ext in WEB_EXT:
            audit.scan_web(root, ext)
        elif ext == ".swift":
            audit.scan_swift(root)
        elif ext == ".xaml":
            audit.scan_xaml(root)
        audit.project_checks()
    else:
        audit.run()
    if a.json:
        print(json.dumps(audit.as_json(), indent=2))
    else:
        audit.print_text(not a.no_tokens)
    bad = any(hits and RULES[r][0] in ("Blocker", "Major") for r, hits in audit.findings.items())
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
