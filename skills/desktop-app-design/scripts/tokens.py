#!/usr/bin/env python3
"""Design-token extractor for existing apps. Standard library only.

Finds every hard-coded color, spacing, radius, font size, font weight and
animation duration in an app's styles, groups near-duplicates (e.g. eleven
slightly different grays), and proposes a small token set. It can write the
token file and preview or apply the replacements in stylesheets.

Usage:
  tokens.py [PATH]                        report what's used and the proposed tokens
  tokens.py src --type-scale mac          snap font sizes to macOS text-style sizes (web | mac | windows)
  tokens.py src --motion windows          snap durations to 83/167/250/333 ms (web | windows)
  tokens.py src --write src/tokens.css    write the proposed tokens as CSS custom properties
  tokens.py src --write src/tokens.css --diff     also preview literal -> var() replacements
  tokens.py src --write src/tokens.css --apply    rewrite stylesheets (review the diff first)
  tokens.py src --json                    machine-readable report

Replacements touch .css/.scss/.less files only, skip custom-property
definitions, and never change box-shadow colors or negative values.
Inline styles in components are reported, not rewritten.
Snapping changes values slightly (e.g. 10px -> 8px or 12px): that's the point,
but look at the result. Name tokens for their role before shipping.
"""
import argparse
import difflib
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contrast import parse as parse_color, ratio as contrast_ratio  # noqa: E402

SKIP_DIRS = {
    "node_modules", ".git", "dist", "build", "out", ".next", ".nuxt", ".svelte-kit", "target", "vendor",
    "coverage", ".venv", "venv", "__pycache__", "Pods", "DerivedData", ".turbo", ".cache", "release",
    "bin", "obj", ".output", "storybook-static",
}
STYLE_EXT = {".css", ".scss", ".sass", ".less"}
COMPONENT_EXT = {".tsx", ".jsx", ".ts", ".js", ".vue", ".svelte", ".html", ".astro"}

SPACE_SCALE = [2, 4, 6, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96]
RADIUS_SCALE = [2, 4, 6, 8, 10, 12, 16, 20, 24]
TYPE_SCALES = {
    "web": [11, 12, 13, 14, 15, 16, 18, 20, 22, 24, 28, 32, 36, 40, 48, 60],
    "mac": [10, 11, 12, 13, 15, 17, 22, 26],          # macOS text styles (pt): caption…large title
    "windows": [12, 14, 18, 20, 28, 40, 68],           # Windows 11 type ramp (epx)
}
MOTION_SCALES = {"web": [100, 150, 200, 250, 300, 400], "windows": [83, 167, 250, 333]}
WEIGHTS = {400: "regular", 500: "medium", 600: "semibold", 700: "bold"}
NAMED = {"white": "#ffffff", "black": "#000000"}

COLOR_PROPS = {"color", "background", "background-color", "border", "border-color", "border-top", "border-right",
               "border-bottom", "border-left", "border-top-color", "border-right-color", "border-bottom-color",
               "border-left-color", "outline", "outline-color", "fill", "stroke", "caret-color",
               "text-decoration-color", "accent-color", "box-shadow", "column-rule-color"}
SPACING_PROPS = re.compile(r"^(padding|margin)(-(top|right|bottom|left|inline|block)(-(start|end))?)?$|^(row-|column-)?gap$")
RADIUS_PROPS = re.compile(r"^border(-(top|bottom|start|end)-(left|right|start|end))?-radius$")
DURATION_PROPS = {"transition", "transition-duration", "animation", "animation-duration"}
COLOR_RE = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b|rgba?\([^)]*\)|\b(?:white|black)\b")
DECL_RE = re.compile(r"(?<![\w-])([a-z-]+)\s*:\s*([^;{}]+)")
JS_DECL_RE = re.compile(r"\b([a-zA-Z]+)\s*:\s*(?:['\"]([^'\"\n]+)['\"]|(\d+(?:\.\d+)?))(?=\s*[,}\n])")
PX_JS_PROPS = re.compile(r"^(padding|margin|gap|row-gap|column-gap|font-size|border-radius)")


def kebab(name):
    return re.sub(r"([A-Z])", lambda m: "-" + m.group(1).lower(), name)


def to_px(num, unit):
    v = float(num)
    return v * 16 if unit == "rem" else v


def norm_color(lit):
    lit = lit.strip().lower()
    lit = NAMED.get(lit, lit)
    try:
        r, g, b, a = parse_color(lit)
    except ValueError:
        return None
    if a >= 0.999:
        return "#%02x%02x%02x" % (r, g, b)
    return "rgba(%d, %d, %d, %s)" % (r, g, b, ("%.2f" % a).rstrip("0").rstrip("."))


def oklab(hexish):
    r, g, b, a = parse_color(hexish)

    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = lin(r), lin(g), lin(b)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s, a)


def hue_name(a, b):
    h = (math.degrees(math.atan2(b, a)) + 360) % 360
    for limit, name in ((20, "pink"), (50, "red"), (80, "orange"), (110, "yellow"), (160, "green"),
                        (200, "teal"), (245, "cyan"), (290, "blue"), (330, "purple"), (360, "pink")):
        if h < limit:
            return name
    return "pink"


def snap(value, scale):
    return min(scale, key=lambda s: (abs(s - value), -s))


class Scan:
    def __init__(self):
        self.colors = Counter()                 # normalized color -> count
        self.color_roles = defaultdict(Counter)  # color -> role -> count
        self.spacing = Counter()
        self.radii = Counter()
        self.sizes = Counter()
        self.weights = Counter()
        self.durations = Counter()
        self.existing = {}                      # custom property -> value
        self.inline = Counter()                 # inline-style literals in components
        self.arbitrary = Counter()              # Tailwind arbitrary values
        self.style_files = []
        self.files = 0
        self.base_bg = None                     # background of html/body/#root/.app: kept as its own token

    def role_for(self, prop):
        if prop == "box-shadow":
            return "shadow"
        if prop.startswith(("background",)):
            return "surface"
        if prop.startswith(("border", "outline", "column-rule")):
            return "border"
        return "text"

    def add_decl(self, prop, value, inline=False):
        if prop.startswith("--"):
            return
        if "var(" in value and not COLOR_RE.search(value):
            return
        if prop in COLOR_PROPS:
            for lit in COLOR_RE.findall(value):
                c = norm_color(lit)
                if c:
                    self.colors[c] += 1
                    self.color_roles[c][self.role_for(prop)] += 1
                    if inline:
                        self.inline["color " + c] += 1
        if SPACING_PROPS.match(prop):
            for num, unit in re.findall(r"(?<![\w.-])(\d+(?:\.\d+)?)(px|rem)\b", value):
                v = to_px(num, unit)
                if v > 1:
                    self.spacing[v] += 1
        if RADIUS_PROPS.match(prop):
            for num, unit in re.findall(r"(?<![\w.-])(\d+(?:\.\d+)?)(px|rem)\b", value):
                self.radii[to_px(num, unit)] += 1
        if prop == "font-size":
            m = re.match(r"\s*(\d+(?:\.\d+)?)(px|rem)\b", value)
            if m:
                self.sizes[to_px(*m.groups())] += 1
        if prop == "font-weight":
            v = value.strip().lower()
            v = {"normal": "400", "bold": "700"}.get(v, v)
            if v.isdigit():
                self.weights[int(v)] += 1
        if prop in DURATION_PROPS:
            for num, unit in re.findall(r"(?<![\w.-])(\d*\.?\d+)(ms|s)\b", value):
                self.durations[float(num) * (1 if unit == "ms" else 1000)] += 1

    def scan_file(self, path):
        ext = os.path.splitext(path)[1].lower()
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError:
            return
        self.files += 1
        text_nc = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
        if ext in STYLE_EXT or ext in (".vue", ".svelte", ".html", ".astro"):
            if ext in STYLE_EXT:
                self.style_files.append(path)
            for m in re.finditer(r"(--[\w-]+)\s*:\s*([^;{}]+)", text_nc):
                self.existing[m.group(1)] = m.group(2).strip()
            for m in DECL_RE.finditer(text_nc):
                self.add_decl(m.group(1), m.group(2))
            for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", text_nc):
                sel = m.group(1).strip().split("\n")[-1].strip()
                bg = re.search(r"background(?:-color)?\s*:\s*(" + COLOR_RE.pattern + r")\s*(?:;|$|!)", m.group(2))
                if bg and self.base_bg is None and re.search(r"(^|[\s,])(html|body|:root|#root|#app|\.app)\s*$", sel):
                    self.base_bg = norm_color(bg.group(1))
        if ext in COMPONENT_EXT:
            for m in JS_DECL_RE.finditer(text_nc):
                prop = kebab(m.group(1))
                if m.group(2) is not None:
                    self.add_decl(prop, m.group(2), inline=True)
                elif PX_JS_PROPS.match(prop):
                    self.add_decl(prop, m.group(3) + "px", inline=True)
            for m in re.finditer(r"\b[a-z-]+-\[[^\]\s]+\]", text_nc):
                self.arbitrary[m.group(0)] += 1


def cluster_colors(scan, threshold):
    clusters = []  # [rep, members(Counter), lab]
    for color, count in scan.colors.most_common():
        lab = oklab(color)
        for cl in clusters:
            L, a, b, alpha = cl[2]
            if color == scan.base_bg or cl[0] == scan.base_bg:
                continue   # the app background stays itself, so cards and panels keep their contrast with it
            if abs(math.hypot(a, b) - math.hypot(*lab[1:3])) > 0.01:
                continue   # a tinted color (pale blue tag) is not a near-duplicate of a plain gray
            if abs(alpha - lab[3]) < 0.05 and math.dist((L, a, b), lab[:3]) <= threshold:
                cl[1][color] += count
                break
        else:
            clusters.append([color, Counter({color: count}), lab])
    tokens, used = [], set()
    named = Counter()
    for rep, members, (L, a, b, alpha) in clusters:
        roles = Counter()
        for c in members:
            roles.update(scan.color_roles[c])
        only_shadow = set(roles) == {"shadow"}
        roles.pop("shadow", None)
        role = roles.most_common(1)[0][0] if roles else "shadow"
        mixed = bool(roles) and roles[role] < 0.75 * sum(roles.values())   # used as text and surface, etc.
        if mixed:
            role = "neutral"
        chroma = math.hypot(a, b)
        if only_shadow:
            base = "shadow"
        elif chroma < 0.03 and mixed:
            base = "neutral-%d" % min(950, max(50, int(round((1 - L) * 10)) * 100))
        elif chroma < 0.03:
            base = role
        else:
            shade = min(950, max(50, int(round((1 - L) * 10)) * 100))
            base = "%s-%d" % (hue_name(a, b), shade)
        if rep == scan.base_bg:
            name, role = "--color-bg", "surface"
        else:
            named[base] += 1
            numbered = (chroma < 0.03 and not mixed) or only_shadow
            name = "--color-%s-%d" % (base, named[base]) if numbered else "--color-%s" % base
        stem, n = name, 2
        while name in used:
            name, n = "%s-%d" % (stem, n), n + 1
        used.add(name)
        tokens.append({"name": name, "value": rep, "role": "shadow" if only_shadow else role,
                       "uses": sum(members.values()), "members": dict(members),
                       "surface_uses": roles.get("surface", 0)})
    return tokens


def scale_tokens(counter, scale, prefix, fmt="{:g}px", keep_over=None):
    mapping, tokens = {}, Counter()
    for v, count in counter.items():
        if keep_over is not None and v > keep_over:
            continue
        s = snap(v, scale)
        mapping[v] = s
        tokens[s] += count
    names = {s: "--%s-%s" % (prefix, ("%g" % s).replace(".", "_")) for s in tokens}
    return mapping, tokens, names


def propose(scan, a):
    colors = cluster_colors(scan, a.threshold)
    sp_map, sp_tok, sp_names = scale_tokens(scan.spacing, SPACE_SCALE, "space", keep_over=96)
    rad_full = {v for v in scan.radii if v >= 100}
    rad_map, rad_tok, rad_names = scale_tokens(Counter({v: c for v, c in scan.radii.items() if v < 100}), RADIUS_SCALE, "radius")
    for v in rad_full:
        rad_map[v] = "full"
    if rad_full:
        rad_names["full"] = "--radius-full"
        rad_tok["full"] = sum(scan.radii[v] for v in rad_full)
    ty_map, ty_tok, ty_names = scale_tokens(scan.sizes, TYPE_SCALES[a.type_scale], "text")
    du_map, du_tok, du_names = scale_tokens(Counter({v: c for v, c in scan.durations.items() if v > 0}), MOTION_SCALES[a.motion], "dur")
    return {"colors": colors, "spacing": (sp_map, sp_tok, sp_names), "radii": (rad_map, rad_tok, rad_names),
            "sizes": (ty_map, ty_tok, ty_names), "durations": (du_map, du_tok, du_names)}


def fmt_num(v):
    return "%g" % v


def report(scan, prop, a):
    print("Design tokens in %s  (%d files scanned, %d stylesheets)\n" % (a.path, scan.files, len(scan.style_files)))
    if scan.existing:
        print("EXISTING CUSTOM PROPERTIES: %d already defined (extend these before adding new ones)" % len(scan.existing))
        print("  " + "  ".join(list(scan.existing)[:12]) + ("  …" if len(scan.existing) > 12 else ""))
        print()
    colors = prop["colors"]
    surfaces = [t for t in colors if t["surface_uses"] and parse_color(t["value"])[3] == 1]
    main_bg = scan.base_bg or (max(surfaces, key=lambda t: t["surface_uses"])["value"] if surfaces else None)
    print("COLORS: %d distinct literals -> %d tokens (near-duplicates within OKLab distance %g merged)"
          % (len(scan.colors), len(colors), a.threshold))
    for t in colors:
        others = ", ".join("%s ×%d" % (c, n) for c, n in sorted(t["members"].items(), key=lambda x: -x[1]))
        note = ""
        if t["role"] == "text" and main_bg and parse_color(t["value"])[3] == 1:
            r = contrast_ratio(parse_color(t["value"])[:3], parse_color(main_bg)[:3])
            note = "   %s:1 on %s%s" % (int(r * 100) / 100, main_bg, "  <- below 4.5:1" if r < 4.5 else "")
        print("  %-26s %-22s <- %s%s" % (t["name"], t["value"], others, note))
    print()
    for key, label, unit_note in (("spacing", "SPACING", "snapped to a 4 px grid"), ("radii", "RADII", "snapped to a radius scale"),
                                  ("sizes", "FONT SIZES", "snapped to the %s type scale" % a.type_scale),
                                  ("durations", "DURATIONS", "snapped to the %s motion scale" % a.motion)):
        mapping, tok, names = prop[key]
        src = {"spacing": scan.spacing, "radii": scan.radii, "sizes": scan.sizes, "durations": scan.durations}[key]
        if not src:
            continue
        unit = "ms" if key == "durations" else "px"
        kept = len(src) - len(mapping)
        print("%s: %d distinct -> %d tokens (%s)%s" % (label, len(src), len(tok), unit_note,
              "; %d value(s) over 96 px left as-is (layout sizes)" % kept if kept else ""))
        changes = []
        for v in sorted(mapping, key=lambda x: (isinstance(x, str), x)):
            s = mapping[v]
            arrow = "" if s == v else "  (was %s%s)" % (fmt_num(v), unit)
            if s == "full":
                changes.append("%s%s -> %s" % (fmt_num(v), unit, names["full"]))
            elif s != v:
                changes.append("%s -> %s%s" % (fmt_num(v), fmt_num(s), unit))
        print("  tokens: " + "  ".join("%s=%s%s" % (names[s], fmt_num(s) if s != "full" else "9999", unit if s != "full" else "px")
                                        for s in sorted(tok, key=lambda x: (isinstance(x, str), x))))
        if changes:
            print("  snaps:  " + "  ".join(changes))
        if key == "durations":
            slow = [v for v in src if v >= 500]
            if slow:
                print("  note: %s ms is too slow for routine desktop UI (motion.md §3)" % ", ".join(fmt_num(v) for v in sorted(slow)))
        print()
    if scan.weights:
        odd = [w for w in scan.weights if w not in WEIGHTS]
        print("FONT WEIGHTS: %s%s" % (", ".join("%d ×%d" % (w, c) for w, c in sorted(scan.weights.items())),
                                     "   <- use 400/500/600/700 only (no thin or extra-heavy weights in UI)" if odd else ""))
        print()
    if scan.inline:
        print("INLINE STYLES IN COMPONENTS: %d color literals (move them to tokens by hand)" % sum(scan.inline.values()))
        print()
    if scan.arbitrary:
        print("TAILWIND ARBITRARY VALUES: %d distinct, e.g. %s (map them to theme values)"
              % (len(scan.arbitrary), " ".join(list(scan.arbitrary)[:6])))
        print()
    print("Next: name tokens for their role, add dark-mode values, then --write FILE [--diff | --apply].")


def token_css(prop, a):
    out = ["/* Proposed design tokens, generated by tokens.py from the values this app already uses.",
           "   Review: rename for role (e.g. --color-text-2 -> --color-text-secondary), add dark values,",
           "   and check text/background pairs with contrast.py. */", ":root {"]
    groups = defaultdict(list)
    for t in prop["colors"]:
        groups[t["role"]].append(t)
    for role in ("text", "surface", "border", "neutral", "shadow"):
        if groups[role]:
            out.append("  /* color: %s */" % role)
            for t in groups[role]:
                merged = ", ".join(c for c in t["members"] if c != t["value"])
                out.append("  %s: %s;%s" % (t["name"], t["value"], "  /* merged: %s */" % merged if merged else ""))
    for key, title, unit in (("spacing", "spacing (4 px grid)", "px"), ("radii", "radius", "px"),
                             ("sizes", "font size (%s scale)" % a.type_scale, "px"), ("durations", "duration", "ms")):
        mapping, tok, names = prop[key]
        if not tok:
            continue
        out.append("  /* %s */" % title)
        for s in sorted(tok, key=lambda x: (isinstance(x, str), x)):
            out.append("  %s: %s;" % (names[s], "9999px" if s == "full" else fmt_num(s) + unit))
    if prop["durations"][1]:
        out.append("  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);   /* entrances (motion.md §3.3) */")
    out.append("}")
    out.append("@media (prefers-color-scheme: dark) {\n  :root {\n    /* TODO: a dark value for every color token above:"
               " dark grays, lighter surfaces for elevation, desaturated accents (visual-craft.md §3.6) */\n  }\n}")
    return "\n".join(out) + "\n"


def rewrite(text, prop):
    color_map = {}
    for t in prop["colors"]:
        if t["role"] == "shadow":
            continue
        for c in t["members"]:
            color_map[c] = t["name"]
    sp_map, _, sp_names = prop["spacing"]
    rad_map, _, rad_names = prop["radii"]
    ty_map, _, ty_names = prop["sizes"]
    du_map, _, du_names = prop["durations"]

    def px_sub(value, mapping, names):
        def f(m):
            v = to_px(m.group(1), m.group(2))
            s = mapping.get(v)
            return "var(%s)" % names[s] if s is not None else m.group(0)
        return re.sub(r"(?<![\w.-])(\d+(?:\.\d+)?)(px|rem)\b", f, value)

    def decl(m):
        prop_name, value = m.group(1), m.group(2)
        if prop_name.startswith("--"):
            return m.group(0)
        new = value
        if prop_name in COLOR_PROPS and prop_name != "box-shadow":
            new = COLOR_RE.sub(lambda c: "var(%s)" % color_map[norm_color(c.group(0))]
                               if norm_color(c.group(0)) in color_map else c.group(0), new)
        if SPACING_PROPS.match(prop_name):
            new = px_sub(new, sp_map, sp_names)
        elif RADIUS_PROPS.match(prop_name):
            new = px_sub(new, rad_map, rad_names)
        elif prop_name == "font-size":
            new = px_sub(new, ty_map, ty_names)
        elif prop_name in DURATION_PROPS:
            def d(mm):
                v = float(mm.group(1)) * (1 if mm.group(2) == "ms" else 1000)
                s = du_map.get(v)
                return "var(%s)" % du_names[s] if s is not None else mm.group(0)
            new = re.sub(r"(?<![\w.-])(\d*\.?\d+)(ms|s)\b", d, new)
        return m.group(0).replace(value, new, 1)

    parts = re.split(r"(/\*.*?\*/)", text, flags=re.S)   # keep comments untouched
    return "".join(part if part.startswith("/*") else DECL_RE.sub(decl, part) for part in parts)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("path", nargs="?", default=".")
    p.add_argument("--type-scale", choices=sorted(TYPE_SCALES), default="web")
    p.add_argument("--motion", choices=sorted(MOTION_SCALES), default="web")
    p.add_argument("--threshold", type=float, default=0.02, help="OKLab distance for merging colors (default 0.02)")
    p.add_argument("--write", metavar="FILE", help="write the proposed tokens as CSS")
    p.add_argument("--diff", action="store_true", help="preview replacements in stylesheets")
    p.add_argument("--apply", action="store_true", help="rewrite stylesheets (needs --write)")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    root = os.path.abspath(a.path)
    if not os.path.exists(root):
        p.error("no such path: %s" % a.path)
    if a.apply and not a.write:
        p.error("--apply needs --write FILE so every var() it inserts is defined")

    scan = Scan()
    if os.path.isfile(root):
        scan.scan_file(root)
    else:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
            for fn in filenames:
                ext = os.path.splitext(fn)[1].lower()
                if (ext in STYLE_EXT or ext in COMPONENT_EXT) and ".min." not in fn and not fn.endswith(".d.ts"):
                    path = os.path.join(dirpath, fn)
                    if a.write and os.path.abspath(a.write) == path:
                        continue
                    scan.scan_file(path)
    prop = propose(scan, a)

    if a.json:
        out = {"files": scan.files, "existing_custom_properties": scan.existing, "colors": prop["colors"]}
        for key in ("spacing", "radii", "sizes", "durations"):
            mapping, tok, names = prop[key]
            out[key] = {"map": {fmt_num(k): (v if v == "full" else v) for k, v in mapping.items()},
                        "tokens": {names[s]: s for s in tok}}
        out["font_weights"] = {str(k): v for k, v in scan.weights.items()}
        print(json.dumps(out, indent=2))
    else:
        report(scan, prop, a)

    if a.write:
        css = token_css(prop, a)
        with open(a.write, "w", encoding="utf-8") as f:
            f.write(css)
        print("\nWrote %s (%d tokens). Import it before your other styles." % (a.write, css.count(": ") - 1))
    if a.diff or a.apply:
        changed = 0
        for path in scan.style_files:
            with open(path, encoding="utf-8") as f:
                old = f.read()
            new = rewrite(old, prop)
            if new == old:
                continue
            changed += 1
            rel = os.path.relpath(path, root if os.path.isdir(root) else os.path.dirname(root))
            if a.diff or not a.apply:
                sys.stdout.writelines(difflib.unified_diff(old.splitlines(True), new.splitlines(True), "a/" + rel, "b/" + rel))
            if a.apply:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)
        print("\n%s %d stylesheet(s)." % ("Rewrote" if a.apply else "Would rewrite", changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
