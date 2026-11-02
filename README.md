# Desktop App Design — an agent skill

An [agent skill](https://docs.claude.com/en/docs/claude-code/skills) that helps AI coding agents (Claude Code and others that support `SKILL.md`) design and build **desktop apps for macOS, Windows and Linux that feel native, intentional and polished**, not like every other AI-generated app.

It turns platform guidelines, usability research, emotional-design research and respected craft into rules and tools. An agent applies them while writing SwiftUI, AppKit, WinUI, GTK/libadwaita, Qt, Electron, Tauri or Flutter code, or while auditing, fixing, polishing or redesigning an app that already exists.

Current as of **November 2026**:
- macOS 26 Tahoe and macOS 27
- Windows 11 with Windows App SDK 2.x
- GNOME 50–51 and KDE Plasma 6.8
- Electron 45 and Tauri 2.12
- WCAG 2.2

## What it teaches

- **Intent before pixels.** Before designing, the agent writes down who the app is for, how often they use it, and their top tasks. It also picks the feeling (3 adjectives plus 1 to avoid) and one signature moment, and every later decision traces back to these.
- **Familiar structure, distinctive details.** Behave exactly like the platform in what people *operate*: window controls, menus, shortcuts, dialogs, keyboard. Be distinctive in what they *perceive*: type, color, icons, copy, one memorable moment.
- **Usability heuristics and user-centered design.** This covers Nielsen, Shneiderman, Norman and ISO 9241, Fitts's law and timing models. It includes an evaluation routine the agent runs on its own work: a heuristic pass, a walkthrough of the main task, and keyboard-only use.
- **Microinteractions and motion with real numbers.** It covers when *not* to animate, desktop durations and easing, and springs that can be interrupted. Reduced motion is handled properly, and there's a catalog of hover, press, drag, undo and loading details.
- **Avoiding the generic AI look.** A table of 25 "slop tells" with what to do instead, plus a pixel-level polish checklist.
- **Trust and accessibility.** Honest saved and sync states, undo instead of "Are you sure?", no dark patterns, full keyboard access, screen readers, contrast, and respect for OS settings.
- **Auditing and fixing existing apps.** The agent first says which of four modes it's in, and stays inside it:
  - **Audit:** a report only, no code changes.
  - **Fix:** defects only, same look.
  - **Polish:** a consistent system and details.
  - **Redesign:** one key screen first, then the rest after you approve.

  Every finding needs a rule, proof and one concrete fix. Findings are grouped by root cause and fixed in batches without changing how the app works. The result is measured before and after.

## What the agent gets

| File | What's in it |
|---|---|
| `SKILL.md` | The workflow, a platform cheat sheet (macOS / Windows / GNOME / KDE), the 21 rules that matter most, key numbers, the anti-slop table, coding guidance, and a review format |
| `references/emotional-design.md` | Making the app feel a certain way on purpose: personality, delight, trust, voice, the signature moment, and the line between persuasion and manipulation |
| `references/interaction.md` | Heuristics, laws, desktop patterns (command palettes, menus, selection, drag and drop, tables, settings, errors, empty states, autosave) and an evaluation process |
| `references/motion.md` | Motion and microinteractions: purpose, timing and easing per platform, springs, perceived speed, reduced motion, code for each stack |
| `references/visual-craft.md` | Typography, color systems, depth, density, the slop-tell table, case studies (Linear, Things, Raycast, Figma, Sketch, Bear), a polish checklist |
| `references/accessibility.md` | Keyboard, screen-reader APIs per toolkit, OS display settings, contrast, targets, testing, legal baseline (WCAG2ICT, EN 301 549, EAA) |
| `references/macos.md` | Apple HIG for the Mac: menu bar, windows, toolbars, sidebars, settings, Liquid Glass, SwiftUI/AppKit snippets |
| `references/windows.md` | Windows 11 / Fluent 2 / WinUI 3: Mica, title bars and Snap Layouts, type ramp, navigation, dialogs, motion tokens |
| `references/linux.md` | GNOME/libadwaita, KDE/Kirigami, elementary, freedesktop portals, Flathub quality rules |
| `references/cross-platform.md` | Per-OS differences (shortcuts, dialog button order, wording, lifecycle) and Electron, Tauri, Flutter, Qt, Compose, Avalonia, Wails |
| `references/audit-and-fix.md` | The process for existing apps: modes, inventory, audit passes, evidence rules, root causes, a scorecard, fix recipes per platform, and report formats |
| `references/review-checklist.md` | A checklist for auditing an app or checking your own work |
| `scripts/ui_audit.py` | Finds generic-UI tells, "website in a window" mistakes, accessibility gaps and design-token sprawl in your code; saves a baseline and compares before and after a fix |
| `scripts/tokens.py` | Gathers the colors, spacing, font sizes, corners and animation speeds an app already uses, merges near-duplicates into a token set, and can rewrite the stylesheets to use it |
| `scripts/spring.py` | One spring, converted for SwiftUI, CSS `linear()`, Motion, libadwaita, Flutter and Compose |
| `scripts/contrast.py` | WCAG contrast checker that handles translucent colors and suggests the nearest passing color |

The agent always reads `SKILL.md` and opens a reference file only when the task needs it.

## Install

With the [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add pablonification/desktop-app-design-skill@desktop-app-design -g -y
```

Or manually for Claude Code:

```bash
git clone https://github.com/pablonification/desktop-app-design-skill.git
cp -R desktop-app-design-skill/skills/desktop-app-design ~/.claude/skills/
```

## Use

Once installed, you don't need to call it. The agent picks it up for desktop UI work, for example:

- "Build the main window for my Mac notes app in SwiftUI"
- "My Electron app looks like every other AI app and the window feels off on Windows. Fix it"
- "Add a command palette to my Tauri app and make it feel like Raycast"
- "Design the first-run experience for my WinUI journaling app. It should feel calm and personal"
- "Review this app for usability and accessibility"
- "Audit my Mac app, but don't change any code yet"
- "My styles grew messy. Clean them up into a consistent system without changing the look"

The tools also work on their own (Python 3, no dependencies):

```bash
python3 skills/desktop-app-design/scripts/ui_audit.py path/to/your/app
# MAJOR (8)
#   [electron-frameless] Electron window with frame:false and no native controls overlay
#       main.js:7  new BrowserWindow({ frame: false … })
#       fix: Use titleBarStyle 'hidden'/'hiddenInset' + titleBarOverlay so traffic lights /
#            caption buttons, Snap Layouts and drag regions keep working.
#   …
# DESIGN TOKENS (distinct values used directly; fewer = more consistent)
#   off-grid spacing    7  14px 10px 22px 18px 42px 30px 6px  <- not on a 4px grid

python3 skills/desktop-app-design/scripts/ui_audit.py path/to/your/app --save /tmp/before.json
# …fix things, then:
python3 skills/desktop-app-design/scripts/ui_audit.py path/to/your/app --compare /tmp/before.json
# UI audit comparison: 9 findings before -> 0 after
#   color literals     37 ->   0
#   off-grid spacing   14 ->   0

python3 skills/desktop-app-design/scripts/tokens.py path/to/your/app
# COLORS: 37 distinct literals -> 20 tokens (near-duplicates merged)
#   --color-text-1   #222222   <- #222222 ×1, #252525 ×1, #1f1f1f ×1   15.24:1 on #fafafa
#   --color-text-3   #9a9a9a   <- #9a9a9a ×1, #959595 ×1, #a0a0a0 ×1   2.69:1 on #fafafa  <- below 4.5:1
# SPACING: 18 distinct -> 10 tokens (snapped to a 4 px grid)
# then: --write src/tokens.css --diff   (preview), --apply   (rewrite the stylesheets)

python3 skills/desktop-app-design/scripts/spring.py --duration 0.35 --bounce 0.15
# Spring: duration 0.350 s, bounce 0.15  (damping ratio 0.85)
# Settles in ~450 ms (within 0.20% of the distance); overshoot: 0.6%
# SwiftUI     .spring(duration: 0.350, bounce: 0.15)
# Motion      { type: "spring", stiffness: 322.3, damping: 30.52, mass: 1.00 }
# CSS         --spring-350ms-b15: linear(0, 0.031, 0.107, …, 1)

python3 skills/desktop-app-design/scripts/contrast.py "#9b9b9b" "#ffffff" --fix
# #9b9b9b on #ffffff  ->  2.77:1
#   closest passing color for 4.5:1 -> #767676 (4.54:1)
```

## Tests

`skills/desktop-app-design/evals/` holds six test cases, each with pass/fail checks in the layout read by `claude plugin eval`:
- reviewing a flawed Electron app
- building a Mac notes app in SwiftUI
- a polished command palette in Tauri
- a WinUI journaling app designed from a stated feeling
- auditing a flawed Mac app without touching the code
- cleaning up messy styles into a token system while keeping the look

Two of the cases were run with and without the skill, and graded blind:

| Case | With skill | Without skill |
|---|---|---|
| Review and fix a flawed Electron app | 11/11 | 5/11 |
| Add a polished command palette to a Tauri app | 9/11 | 7/11 |

Without the skill, the agent:
- kept the browser "Are you sure?" popup;
- removed the menu on Windows, losing the zoom shortcuts;
- didn't rank its findings by importance;
- left the command palette without recent commands or a helpful no-results state.

The two audit-and-fix cases were run with the skill only, and the results were checked directly:

| Case | With skill |
|---|---|
| Audit a flawed Mac app, no code changes | 11/11 (file left untouched; every planted problem found, plus a dead Share button and no saving) |
| Clean up messy styles, keep the look | 9/9 (37 colors → 15 named by role; audit findings 9 → 0; no new dependencies; every visible change listed) |

This is one run per case, so treat it as a sign of direction, not a benchmark.

## Sources

Every rule in the reference files links to its source. Claims that couldn't be fully verified are marked ⚠️ and listed at the end of each file.

- **Platform guidelines:**
  - Apple Human Interface Guidelines, plus WWDC sessions such as *Designing Fluid Interfaces* (2018), *The details of UI typography* (2020), *Animate with springs* (2023) and the 2025–2026 design sessions.
  - Microsoft's Windows app design guidance, Fluent 2, and the WinUI source.
  - The GNOME HIG and libadwaita, the KDE HIG and Kirigami, elementary OS, freedesktop.org specs and Flathub.
- **Standards:** W3C WCAG 2.2, WCAG2ICT and the ARIA Authoring Practices; ETSI EN 301 549; the European Accessibility Act.
- **Usability and HCI:**
  - Nielsen Norman Group, Shneiderman's Eight Golden Rules, Tognazzini's First Principles, ISO 9241-110 and -210.
  - Norman's *The Design of Everyday Things*, Cooper's *About Face*, Raskin's *The Humane Interface*.
  - Fitts, Hick–Hyman, Accot & Zhai, and Card, Moran & Newell's Keystroke-Level Model.
- **Emotional design and trust:**
  - Norman's *Emotional Design*, Walter's *Designing for Emotion*, the Kano model, Hassenzahl.
  - Studies of beauty and usability (Kurosu & Kashimura 1995; Tractinsky 2000; Tuch 2012), first impressions (Lindgaard 2006), and how polished a design looks (Moshagen & Thielsch 2010).
  - Studies of credibility and trust (Fogg 2003; Sillence 2004), how endings shape memory (Kahneman 1993), and manipulative design (Gray 2018; Mathur 2019).
- **Motion and craft:**
  - Dan Saffer's *Microinteractions*, Emil Kowalski, Rauno Freiberg, Vercel's Web Interface Guidelines.
  - *Refactoring UI*, Butterick's *Practical Typography*, Radix Colors, Linear's design writing, and Anthropic's `frontend-design` skill.
- **Hand-picked practitioner sources** (cross-checked, with conflicts marked):
  - Kole Jain, [Everything you need to Design macOS Apps EXACTLY like Apple](https://www.youtube.com/watch?v=Vy0KKvZJRH8)
  - Kole Jain, [EVERYTHING you need to know to build a Dashboard UI in 8 minutes](https://www.youtube.com/watch?v=B7k5rOgmOGY)
  - uxpeak, [UX Design Thinking Behind The Most Loved Apps](https://www.youtube.com/watch?v=U7jTCgIWS4w)
  - Benji Taylor, [Stageshow](https://benji.org/stageshow)
  - Sahil Jada's [font picks](https://x.com/BySahilJada/status/2116834000765681757)
  - Vercel, [Introducing Geist Serif](https://vercel.com/blog/introducing-geist-serif)
  - Julien Thibeaut, [ui-skills](https://github.com/ibelick/ui-skills)

Where a practitioner tip conflicts with a platform guideline or an accessibility standard, the skill follows the standard. Examples: an in-app light/dark switch, a global shortcut that steals ⇧⌘S, or a confirmation dialog for every delete.

Platform guidelines change several times a year, so check the official pages for anything version-specific.
