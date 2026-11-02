#!/usr/bin/env python3
"""WCAG 2.x contrast checker for UI colors. Standard library only.

Usage:
  contrast.py FG BG                 check one pair, e.g. contrast.py "#8E8E93" "#FFFFFF"
  contrast.py FG BG --fix           also suggest the closest FG that passes (default target 4.5)
  contrast.py FG BG --fix --target 3
  contrast.py --pairs "#777:#fff" "#3C3C4399:#F2F2F7" ...   check many pairs at once

Colors: #RGB, #RRGGBB, #RRGGBBAA, rgb(r,g,b), rgba(r,g,b,a). A translucent FG
(e.g. #3C3C4399, a label gray at 60% opacity, or text on a translucent sidebar)
is blended over BG before measuring, which is what the user actually sees.
For text over blur/Mica/glass, test against the lightest and darkest backdrop it can show.

Thresholds (WCAG 2.2):
  4.5:1  normal text (AA)          1.4.3
  3:1    large text (AA): >= 24 regular or >= 19 bold, in CSS px / macOS pt / Windows epx
         (WCAG's "18pt / 14pt bold" are typographic points; Mac's 13pt body text is normal text)
  3:1    icons, input borders, focus rings, chart lines (AA)   1.4.11
  7:1    normal text (AAA)         1.4.6
"""
import argparse
import colorsys
import math
import re
import sys


def parse(color):
    c = color.strip().lower()
    m = re.fullmatch(r"rgba?\(([^)]*)\)", c)
    if m:
        parts = [p.strip() for p in m.group(1).split(",")]
        r, g, b = (int(float(p)) for p in parts[:3])
        a = float(parts[3]) if len(parts) > 3 else 1.0
        return (r, g, b, a)
    c = c.lstrip("#")
    if len(c) in (3, 4):
        c = "".join(ch * 2 for ch in c)
    if len(c) not in (6, 8) or not re.fullmatch(r"[0-9a-f]+", c):
        raise ValueError("can't read color: %r" % color)
    r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
    a = int(c[6:8], 16) / 255 if len(c) == 8 else 1.0
    return (r, g, b, a)


def blend(fg, bg):
    """Composite a possibly-translucent fg over an opaque bg."""
    a = fg[3]
    return tuple(round(fg[i] * a + bg[i] * (1 - a)) for i in range(3))


def luminance(rgb):
    def chan(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(v) for v in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg_rgb, bg_rgb):
    l1, l2 = sorted((luminance(fg_rgb), luminance(bg_rgb)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def shown(r):
    """Format a ratio truncated (not rounded) to 2 decimals: WCAG says never round up,
    so 2.996 must not display as a passing 3.00."""
    return "%.2f" % (math.floor(r * 100) / 100)


def hexify(rgb):
    return "#%02X%02X%02X" % tuple(rgb[:3])


def fix(fg_rgb, bg_rgb, target):
    """Move fg lightness (keeping hue and saturation) away from bg until it passes.
    Returns the passing color closest to the original, or None if impossible."""
    h, l, s = colorsys.rgb_to_hls(*(v / 255 for v in fg_rgb))
    bg_light = luminance(bg_rgb) > 0.18  # rough midpoint between black and white
    candidates = []
    for direction in ((-1,) if bg_light else (1,)) + ((1,) if bg_light else (-1,)):
        lo, hi = (0.0, l) if direction < 0 else (l, 1.0)
        end = lo if direction < 0 else hi
        if ratio(_hls(h, end, s), bg_rgb) < target:
            continue  # even the extreme doesn't pass in this direction
        # binary search for the passing lightness closest to the original
        near, far = l, end
        for _ in range(30):
            mid = (near + far) / 2
            if ratio(_hls(h, mid, s), bg_rgb) >= target:
                far = mid
            else:
                near = mid
        candidates.append((abs(far - l), _hls(h, far, s)))
    return min(candidates)[1] if candidates else None


def _hls(h, l, s):
    return tuple(round(v * 255) for v in colorsys.hls_to_rgb(h, l, s))


def report(fg_s, bg_s, do_fix=False, target=4.5):
    fg, bg = parse(fg_s), parse(bg_s)
    if bg[3] < 1:
        print("note: background %s is translucent; measuring as if opaque" % bg_s)
    bg_rgb = bg[:3]
    seen = blend(fg, bg_rgb)
    r = ratio(seen, bg_rgb)
    ok = lambda t: "pass" if r >= t else "FAIL"
    label = fg_s if fg[3] == 1 else "%s (seen as %s)" % (fg_s, hexify(seen))
    print("%s on %s  ->  %s:1" % (label, bg_s, shown(r)))
    print("  normal text AA 4.5: %s | large text / icons / borders 3.0: %s | AAA 7.0: %s"
          % (ok(4.5), ok(3.0), ok(7.0)))
    if do_fix and r < target:
        better = fix(seen, bg_rgb, target)
        if better:
            print("  closest passing color for %.1f:1 -> %s (%s:1)"
                  % (target, hexify(better), shown(ratio(better, bg_rgb))))
        else:
            print("  no lightness change of this hue reaches %.1f:1 on this background" % target)
    return r >= target


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("colors", nargs="*", help="FG BG")
    p.add_argument("--pairs", nargs="+", metavar="FG:BG", help="check several pairs")
    p.add_argument("--fix", action="store_true", help="suggest a passing FG")
    p.add_argument("--target", type=float, default=4.5, help="ratio to aim for (default 4.5)")
    a = p.parse_args()

    pairs = []
    if a.pairs:
        for item in a.pairs:
            if item.count(":") != 1:
                p.error("pairs look like FG:BG, got %r" % item)
            pairs.append(tuple(item.split(":")))
    if a.colors:
        if len(a.colors) != 2:
            p.error("give exactly two colors: FG BG")
        pairs.append(tuple(a.colors))
    if not pairs:
        p.print_help()
        return 2

    all_ok = True
    for fg_s, bg_s in pairs:
        try:
            all_ok &= report(fg_s, bg_s, a.fix, a.target)
        except ValueError as e:
            print("error: %s" % e)
            all_ok = False
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
