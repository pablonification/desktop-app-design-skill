#!/usr/bin/env python3
"""Spring animation converter. Standard library only.

Describe a spring the way Apple does (duration + bounce) or with physics
(stiffness, damping, mass), and get the same spring for every stack you ship:
SwiftUI, Motion (React), CSS linear(), libadwaita, Flutter and Compose.
It also prints how long the spring really takes to settle and how far it
overshoots, so you can check it against the motion budget.

Usage:
  spring.py --duration 0.35 --bounce 0.15     Apple-style (bounce 0 = no overshoot)
  spring.py --stiffness 300 --damping 30      physics (mass defaults to 1)
  spring.py --preset snappy                   SwiftUI presets: smooth, snappy, bouncy
  spring.py --duration 0.3 --css-only         just the CSS custom property
  spring.py --duration 0.3 --points 40 --epsilon 0.001

Formulas (SwiftUI's Spring, checked against the macOS 26 SDK):
  mass = 1, stiffness = (2*pi / duration)^2, damping = (1 - bounce) * 4*pi / duration
  damping ratio = 1 - bounce. "duration" is perceptual; the spring settles later.

Desktop guidance (see references/motion.md): bounce 0 by default; 0.1-0.2 only
for rare or gesture-driven moments; menus/popovers <= 150-200 ms, panels and
dialogs 200-300 ms. Don't animate frequent or keyboard-driven actions at all.
"""
import argparse
import math
import sys

PRESETS = {  # SwiftUI presets: duration 0.5 s
    "smooth": (0.5, 0.0),
    "snappy": (0.5, 0.15),
    "bouncy": (0.5, 0.3),
}


def from_apple(duration, bounce):
    k = (2 * math.pi / duration) ** 2
    c = (1 - bounce) * 4 * math.pi / duration
    return 1.0, k, c


def to_apple(mass, k, c):
    omega = math.sqrt(k / mass)
    zeta = c / (2 * math.sqrt(k * mass))
    duration = 2 * math.pi / omega
    return duration, 1 - zeta, zeta


def position(t, mass, k, c, v0=0.0):
    """Progress 0 -> 1 at time t (seconds) for a spring released at 0 with velocity v0."""
    w0 = math.sqrt(k / mass)
    zeta = c / (2 * math.sqrt(k * mass))
    y0 = -1.0  # displacement from the target
    if abs(zeta - 1) < 1e-9:
        b = v0 + w0 * y0
        y = (y0 + b * t) * math.exp(-w0 * t)
    elif zeta < 1:
        wd = w0 * math.sqrt(1 - zeta * zeta)
        b = (v0 + zeta * w0 * y0) / wd
        y = math.exp(-zeta * w0 * t) * (y0 * math.cos(wd * t) + b * math.sin(wd * t))
    else:
        s = math.sqrt(zeta * zeta - 1)
        r1, r2 = -w0 * (zeta - s), -w0 * (zeta + s)
        c2 = (v0 - r1 * y0) / (r2 - r1)
        c1 = y0 - c2
        y = c1 * math.exp(r1 * t) + c2 * math.exp(r2 * t)
    return 1 + y


def simulate(mass, k, c, epsilon, v0=0.0, limit=10.0, step=0.0005):
    """Return (settle_time, overshoot) where settle = last time |x - 1| > epsilon."""
    settle, peak, t = 0.0, 0.0, 0.0
    while t <= limit:
        x = position(t, mass, k, c, v0)
        if abs(x - 1) > epsilon:
            settle = t
        peak = max(peak, x)
        t += step
    return settle + step, max(0.0, peak - 1)


def css_linear(mass, k, c, settle, points, v0=0.0):
    vals = []
    for i in range(points + 1):
        t = settle * i / points
        vals.append(position(t, mass, k, c, v0))
    vals[0], vals[-1] = 0.0, 1.0
    out = []
    for v in vals:
        s = ("%.3f" % v).rstrip("0").rstrip(".")
        out.append(s if s not in ("-0", "") else "0")
    return "linear(" + ", ".join(out) + ")"


def fmt(x, digits=1):
    return ("%." + str(digits) + "f") % x


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--duration", type=float, help="perceptual duration in seconds (Apple model)")
    p.add_argument("--bounce", type=float, default=0.0, help="0 = no overshoot (default), up to ~0.4")
    p.add_argument("--stiffness", type=float, help="physics stiffness k")
    p.add_argument("--damping", type=float, help="physics damping c")
    p.add_argument("--mass", type=float, default=1.0, help="physics mass (default 1)")
    p.add_argument("--preset", choices=sorted(PRESETS), help="SwiftUI preset")
    p.add_argument("--velocity", type=float, default=0.0,
                   help="initial velocity in distances per second (gesture hand-off), default 0")
    p.add_argument("--epsilon", type=float, default=0.002,
                   help="settled when within this fraction of the distance (default 0.002)")
    p.add_argument("--points", type=int, default=30, help="samples in the CSS linear() curve (default 30)")
    p.add_argument("--css-only", action="store_true", help="print only the CSS custom property")
    a = p.parse_args()

    if a.preset:
        a.duration, a.bounce = PRESETS[a.preset]
    if a.duration is not None:
        if a.duration <= 0:
            p.error("--duration must be positive")
        if not 0 <= a.bounce < 1:
            p.error("--bounce must be in [0, 1). Use 0 for no overshoot; negative (overdamped) springs aren't needed for UI")
        mass, k, c = from_apple(a.duration, a.bounce)
        duration, bounce, zeta = a.duration, a.bounce, 1 - a.bounce
    elif a.stiffness is not None and a.damping is not None:
        if a.stiffness <= 0 or a.damping < 0 or a.mass <= 0:
            p.error("stiffness and mass must be positive, damping non-negative")
        mass, k, c = a.mass, a.stiffness, a.damping
        duration, bounce, zeta = to_apple(mass, k, c)
    else:
        p.print_help()
        return 2
    if zeta <= 0:
        p.error("an undamped spring never settles; add damping")

    settle, overshoot = simulate(mass, k, c, a.epsilon, a.velocity)
    curve = css_linear(mass, k, c, settle, max(4, a.points), a.velocity)
    ms = int(round(settle * 1000))
    name = "--spring-%dms-b%s" % (int(round(duration * 1000)), fmt(max(bounce, 0) * 100, 0))

    if a.css_only:
        print("%s: %s; /* settle %d ms */" % (name, curve, ms))
        return 0

    over = "none" if overshoot < 0.0005 else "%s%%" % fmt(overshoot * 100)
    if zeta > 1:
        shape = "overdamped (damping ratio %s): slow to arrive, no overshoot" % fmt(zeta, 2)
    elif abs(zeta - 1) < 1e-9:
        shape = "critically damped: fastest arrival with no overshoot"
    else:
        shape = "damping ratio %s" % fmt(zeta, 2)
    print("Spring: duration %s s, bounce %s  (%s)" % (fmt(duration, 3), fmt(max(bounce, 0), 2), shape))
    print("Physics: mass %s, stiffness %s, damping %s" % (fmt(mass, 2), fmt(k), fmt(c, 2)))
    print("Settles in ~%d ms (within %s%% of the distance); overshoot: %s" % (ms, fmt(a.epsilon * 100, 2), over))
    if a.velocity:
        print("Initial velocity: %s distances/s" % fmt(a.velocity, 2))
    if ms > 500:
        print("Note: settles after 500 ms. Fine for a gesture release or a rare moment; too slow for routine desktop UI.")
    if bounce > 0.4:
        print("Note: bounce above ~0.4 'may feel too exaggerated' (Apple, WWDC23).")
    print()
    sb = "" if bounce == 0 else ", bounce: %s" % fmt(bounce, 2)
    if zeta <= 1:
        print("SwiftUI     .spring(duration: %s%s)" % (fmt(duration, 3), sb))
    else:
        print("SwiftUI     .spring(Spring(mass: %s, stiffness: %s, damping: %s))" % (fmt(mass, 2), fmt(k), fmt(c, 2)))
    print("Motion      { type: \"spring\", stiffness: %s, damping: %s, mass: %s }" % (fmt(k), fmt(c, 2), fmt(mass, 2)))
    print("libadwaita  adw_spring_params_new (%s, %s, %s)   /* damping_ratio, mass, stiffness */"
          % (fmt(zeta, 3), fmt(mass, 2), fmt(k)))
    print("Flutter     SpringDescription(mass: %s, stiffness: %s, damping: %s)" % (fmt(mass, 2), fmt(k), fmt(c, 2)))
    if abs(mass - 1) < 1e-9:
        print("Compose     spring(dampingRatio = %sf, stiffness = %sf)" % (fmt(zeta, 3), fmt(k)))
    print("WinUI       no direct conversion: SpringNaturalMotionAnimation's Period isn't this duration; "
          "start from Microsoft's values (references/motion.md 4.4)")
    print()
    print("CSS (fixed curve: it can't carry velocity if interrupted; use a JS spring for draggable or re-triggered UI)")
    print("  :root { %s: %s; }" % (name, curve))
    print("  .panel { transition: transform %dms var(%s); }" % (ms, name))
    print("  @media (prefers-reduced-motion: reduce) { .panel { transition: opacity 150ms linear; } }")
    return 0


if __name__ == "__main__":
    sys.exit(main())
