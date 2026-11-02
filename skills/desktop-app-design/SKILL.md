---
name: desktop-app-design
description: Design and build desktop apps for macOS, Windows and Linux that feel native, intentional and polished, not like generic AI slop. Distilled from Apple's HIG, Microsoft Fluent 2, the GNOME and KDE guidelines, WCAG 2.2, Nielsen Norman Group research, emotional-design and trust research, and respected motion and craft practitioners. Use it whenever the user designs, builds, reviews or polishes desktop UI — windows and title bars, sidebars, toolbars, menus and shortcuts, command palettes, settings, dashboards, tables, onboarding, empty/loading/error states, dark mode, animations and microinteractions, or a design system — in SwiftUI, AppKit, WinUI, WPF, GTK/libadwaita, Qt, Electron, Tauri, Flutter or other desktop stacks. Also use it when someone says their app looks like every other AI app, feels like a website, looks amateur or feels off, wants it to feel premium or polished, or asks for a UX, usability or accessibility review of a desktop app.
---

# Desktop app design

Rules and tools for desktop apps that people trust, find easy, and remember. Current as of **November 2026**: macOS 26 Tahoe and macOS 27, Windows 11 with Windows App SDK 2.x, GNOME 50–51, KDE Plasma 6.8, Electron 45, Tauri 2.12, WCAG 2.2.

The core idea: **familiar structure, distinctive details, every state designed.**
- People judge an app in under a second, and they judge it against the other apps on their computer. Be conventional where people *operate* the app: window chrome, menus, shortcuts, controls, dialogs, keyboard. Be distinctive where they *perceive* it: type, color, icons, copy, and one signature moment.
- "AI slop" isn't a font or a color. It's defaults nobody chose, decoration that carries no information, and states nobody designed.
- Polish comes mostly from removing defects (misalignment, jank, missing states, broken keyboard paths), not from adding effects.

## 1. Start here: identify the target

| You see | Platform / stack | Read |
|---|---|---|
| `*.xcodeproj` / `Package.swift` with a macOS target, `NSApplication`, `.commands`, `MenuBarExtra` | macOS: SwiftUI or AppKit | `macos.md` |
| `.csproj` with `Microsoft.WindowsAppSDK`, `*.xaml` (WPF if `<UseWPF>`) | Windows: WinUI 3 / WPF | `windows.md` |
| `meson.build`, `*.blp` / `*.ui`, `gtk4` / `libadwaita` crates, `gi.require_version("Adw", …)` | GNOME: GTK 4 + libadwaita | `linux.md` |
| `*.qml`, `CMakeLists.txt` with Qt 6, `org.kde.kirigami` | Qt / KDE | `linux.md`, plus `cross-platform.md` for Qt on Mac/Windows |
| `package.json` with `electron` | Electron | `cross-platform.md` + the file for each OS you ship |
| `src-tauri/`, `tauri.conf.json`, `wails.json` | Tauri / Wails (system webview) | `cross-platform.md` (webview differences) + OS files |
| `pubspec.yaml` with `macos/`, `windows/`, `linux/` folders | Flutter desktop | `cross-platform.md` |
| `compose.desktop`, `*.axaml`, React Native macOS/Windows | Compose / Avalonia / RN | `cross-platform.md` |
| Only a description | Ask which OSes if it changes the answer; otherwise design for the user's own OS and note the differences | |

Then check:
- **Which OSes ship.** Behavior follows each OS, even when the visual identity is shared.
- **Minimum OS and SDK versions.** For example, Liquid Glass needs the macOS 26 SDK, there are Windows App SDK 2.x APIs, and features vary by libadwaita version.
- **Existing tokens and components.** If the project has a theme, read it and extend it. A second, parallel design system is worse than an imperfect one used consistently.

## 2. Reference map and tools

All references are in `references/`. Each has a contents line at the top, so read only the sections you need.

| You're working on | Read |
|---|---|
| Deciding how the app should feel, personality, delight, trust, voice, the signature moment | `emotional-design.md` (§11 is the playbook) |
| Flows and behavior: heuristics, commands, keyboard, menus, selection, drag and drop, tables, forms, settings, dialogs, errors, empty states, onboarding, autosave; evaluating a design | `interaction.md` |
| Animation, transitions, hover/press feedback, loading, any microinteraction | `motion.md` |
| Typography, color, depth, radius, density, layout, "make it look better", avoiding the generic look | `visual-craft.md` |
| Keyboard access, screen readers, contrast, OS display settings, compliance | `accessibility.md` |
| Mac / Windows / Linux specifics | `macos.md`, `windows.md`, `linux.md` |
| One codebase on several OSes; Electron, Tauri, Flutter, Qt, Compose, Avalonia, Wails | `cross-platform.md` |
| Reviewing an app, screen, screenshot or PR, or checking your own work | `review-checklist.md` |

Tools (in `scripts/`, Python 3, no dependencies):

```bash
python3 scripts/ui_audit.py path/to/app      # generic-UI tells, web-in-a-window mistakes, a11y gaps, token sprawl
python3 scripts/contrast.py "#9b9b9b" "#ffffff" --fix          # WCAG contrast + nearest passing color
python3 scripts/spring.py --duration 0.3 --bounce 0.1          # one spring for SwiftUI, CSS linear(), Motion, libadwaita, Flutter, Compose
```

`ui_audit.py` scans web-stack UI code (CSS, TSX/JSX, Vue, Svelte), Electron main-process code, `tauri.conf.json`, SwiftUI and XAML. Treat its hits as leads: open each location and confirm before changing anything.

## 3. Workflow for a new app, window or flow

**0. Intent before pixels.** Write 5–10 lines and show them to the user for anything bigger than a small tweak:
- **Who and how often.** Is this a *sovereign* app used for hours (dense, keyboard-first, remembers everything), a *transient* utility opened for seconds (instant, focused, out of the way), or a *daemon* (menu bar or tray, almost invisible)? Cooper's postures change density, launch behavior and chrome. See `interaction.md` §3.
- **The 3–5 key tasks, ranked by frequency.** The most frequent task gets the fastest path: a keyboard shortcut, the fewest steps, no animation in the way.
- **The feeling: 3 adjectives + 1 anti-adjective**, e.g. "calm, precise, warm — not cute". Each adjective must change at least one decision in type, color, motion and copy. See `emotional-design.md` §11a.
- **One signature moment** tied to the core value, at a peak or an ending. See `emotional-design.md` §11c.

**1. Structure it the platform way.** Decide window types, navigation (sidebar → list → detail, tabs, or a single canvas), where commands live, and where settings go. Use the table in §4.

**2. Plan the tokens before writing code.** Write down:
- 4–6 named colors, built on the system's semantic colors where native
- type roles and a scale
- a 4-based spacing scale and a radius scale
- a shadow ladder (floating layers only)
- one icon set
- motion tokens

Then ask: *"Would a similar prompt give anyone this same plan?"* If yes, change something on purpose. See `visual-craft.md` §0 and §7.

**3. Native chrome, content with identity.** Use the system font, controls and materials in menus, toolbars and sidebars. The brand lives in content, headings, empty states, the app icon and the signature moment.

**4. Design every state**, not just the happy path:
- first-run empty, no results
- loading (nothing under 1 s, skeleton, then progress)
- error with recovery, offline or syncing, partial data
- permission denied, disabled
- selected while the window is inactive, drag-over
- very long content, the minimum window size and a very wide window
- light, dark and high contrast; large text

**5. Add microinteractions on purpose** (`motion.md`):
- Every input gets visible feedback within 100 ms.
- Animate state changes people need to follow.
- Nothing frequent or keyboard-driven waits on an animation.
- Reduced motion swaps movement for fades.

**6. Build accessibility in as you go** (`accessibility.md`): a keyboard path for everything, visible focus, accessible names and roles, contrast that passes, and live-updating OS settings.

**7. Evaluate before you say "done".**
1. Run `ui_audit.py` and `contrast.py`.
2. Do a heuristic pass (Nielsen's 10) and a cognitive walkthrough of the top task, asking the 4 questions in `interaction.md` §5–7.
3. Complete the top task with the keyboard only.
4. If you can run the app, check screenshots in light and dark, at the minimum window size and with large text. Also *film the transitions* (a screen recording or frame-by-frame steps): a settled screenshot hides jank.
5. Run the emotional QA pass in `emotional-design.md` §11e.
6. Walk `review-checklist.md`.

## 4. Platform conventions at a glance

| | macOS | Windows 11 | GNOME | KDE Plasma |
|---|---|---|---|---|
| Window controls | Traffic lights top-left, system-drawn | Caption buttons top-right; Snap Layouts on maximize hover | Close only, right (read `button-layout`) | Minimize, maximize, close on the right (user-configurable) |
| Where commands live | Global menu bar: App · File · Edit · Format · View · … · Window · Help. Every command is there | Menu bar or CommandBar in the window; Alt access keys | Header bar + "Main Menu" (`open-menu-symbolic`); no Quit in it | Menu bar or hamburger |
| Settings | "Settings…" ⌘, in the App menu; own window; applies instantly | "Settings" pinned at the bottom of NavigationView; applies instantly | "Preferences" in Main Menu, Ctrl+, | "Configure <App>…", Ctrl+Shift+, |
| Redo · Find next · Full screen | ⇧⌘Z · ⌘G · ⌃⌘F | Ctrl+Y · F3 · F11 | Shift+Ctrl+Z · Ctrl+G · F11 | Ctrl+Shift+Z · F3 · Ctrl+Shift+F |
| Dialog buttons | Cancel left, default right | Action left, Cancel right | Cancel left, affirmative right | OK left, Cancel right |
| Last window closed | App keeps running | App quits (unless a tray app) | Quits | Quits |
| Quit | "Quit <App>" ⌘Q | "Exit"; Alt+F4 closes the window | "Quit" Ctrl+Q | "Quit" Ctrl+Q |
| UI font, body size | SF Pro, 13 pt | Segoe UI Variable, 14 epx | Adwaita Sans, 11 pt | Noto Sans, 10 pt |
| Controls | Regular 24 pt tall (16/20/24/28/36) | ~32 epx tall; 40 epx touch targets | Buttons radius 9 px | Spacing via `Kirigami.Units` |
| Radius | Concentric with the window | 4 controls · 8 windows, flyouts, dialogs | 9 buttons · 12 cards · 15 windows | Breeze defaults |
| Materials | Liquid Glass on floating controls only, never on content | Mica as the base layer; Acrylic for transient surfaces | Solid; follow the stylesheet | Solid; follow Breeze |
| Capitalization | Title Case menus and buttons | Sentence case everywhere | Header caps for titles and buttons; sentence case for labels | Title Case titles and buttons; sentence case for labels |
| Accent | User's accent (yours only under "Multicolor") | System accent via theme resources | System accent (9 colors) | System color scheme |

All OSes: the arrow cursor goes on buttons and the pointing hand only on links. Use native file dialogs, context menus and notifications. Detail and sources are in `cross-platform.md` Part A and each OS file.

## 5. The rules that matter most

**Behave like a real app**
1. **Respect the operating layer.**
   - Keep real window chrome, or the native controls overlay.
   - Put commands where the OS puts them.
   - Never repurpose a standard shortcut.
   - Use native file, print and share dialogs.
   - Honor the OS appearance, accent, contrast, transparency, motion and text-size settings, and update live when they change.
2. **Every command has one home and one name.** It appears in the menu bar or command surface with its shortcut shown, and is disabled rather than hidden. Use the same verb, icon and shortcut everywhere: menu, toolbar, context menu, command palette, tooltip.
3. **Keyboard-complete.**
   - Tab between controls, arrow keys inside composite widgets, F6 between panes.
   - Esc closes transient UI; Return triggers the default button.
   - Past about 30 commands, add a command palette (⌘K / Ctrl+K) with fuzzy search, recent items and visible shortcuts. It's an accelerator, never the only path.
4. **Respond within 100 ms** to every input. Over 1 s, show that work is happening. Over 10 s, show percent-done, what's happening, and Cancel. Never block the window.
5. **Never lose work.** Autosave. Restore windows, selection and scroll position on relaunch. Keep typed input through every error.
6. **Undo instead of "Are you sure?"** Confirm only irreversible actions: name the consequence, label buttons with verbs, and make the safe choice the default.
7. **Errors sit next to their source.** Say what happened, what's safe and what to do next. Never rely only on a toast or a red border, and never joke in high-stakes errors.
8. **Prefer modeless UI.** Use inspectors, inline editing and side panels over dialogs. Modals are only for decisions that must block. Never stack them or steal focus.
9. **Defaults are the design.** Few people (under 5% in one study) ever change settings, so ship the best default layout, density and toolbar. Settings apply instantly.

**Look intentional**

10. **Familiar structure, distinctive details** (the table in `emotional-design.md` §11b).
11. **Build hierarchy with weight, color and dimming, not just size.** Quiet the secondary instead of shouting the primary. One primary action per view.
12. **Separate with space first**, then a background shift, then a hairline, then a shadow. Shadows only for things that float.
13. **Use tokens, not literals.** Draw from a small set of colors (perceptual scales, tinted neutrals, one accent with one meaning), type sizes (at most about 4 per view, 2–3 weights), spacing, radii and durations.
14. **Desktop density**: 13–14 px UI text, 28–32 px rows, compact chrome, and prose capped at about 65–75 characters per line.
15. **Every interactive element has every state**: hover, pressed, focus-visible, selected (also with the window inactive), disabled, drag-over. Interaction *raises* contrast.
16. **Real content.** Test long names; 0, 1 and 999+ items; missing images; accented and right-to-left text; huge numbers; the minimum window size.

**Feel alive, not busy**

17. **Motion has a job**: feedback, orientation, or showing cause and effect.
    - Keep it short: menus 150–200 ms, panels and dialogs 200–300 ms.
    - Make it interruptible and origin-aware.
    - Animate only transform and opacity.
    - Never animate frequent or keyboard-driven actions.
18. **One signature moment, everything else quiet.** The more often something happens, the less ornament it gets. Deep delight (it was faster or easier than expected) beats surface delight (confetti).

**Earn trust**

19. **Honest states.**
    - Show "Saved" only once it is true; keep sync and offline status visible.
    - No fake urgency, nagging or dark patterns. "No" is as easy as "Yes", and cancel is as easy as subscribe.
    - Stressful moments (errors, payments, data at risk) get the plainest UI in the app.
20. **Accessible by default.**
    - Contrast of at least 4.5:1 for text and 3:1 for control boundaries, icons and focus rings, in light, dark, increased contrast, and over materials.
    - Accessible names and roles on every control.
    - Targets of at least 24 px.
21. **No web-app-in-a-window smells.**
    - Arrow cursor on buttons; no selectable chrome text.
    - No white flash on launch, no browser `alert()`/`confirm()`, no spinners for local data.
    - Native context menus; window size and position remembered.

## 6. Key numbers

| Topic | Number |
|---|---|
| Response time | 0.1 s feels instant · 1 s keeps flow · 10 s is the attention limit |
| Waiting | Delay spinners 150–300 ms, then keep them visible ≥ 300–500 ms; skeleton for content loads; percent-done + Cancel ≥ 10 s; speed progress up near the end, never stall late |
| Durations | Micro feedback 80–150 ms · tooltip 120–150 · menu/popover open ≤ 150–200, close ≤ 150 · panel 200–250 · dialog 200–300 in, 150–200 out · nothing routine > 400 |
| Windows motion | 83 / 167 / 250 / 333 ms; enter `cubic-bezier(0,0,0,1)`, exit `cubic-bezier(1,0,1,1)` |
| Easing | Entrances decelerate (`cubic-bezier(0,0,0,1)` or `(0.23,1,0.32,1)`); on-screen moves `(0.2,0,0,1)`; user dismissals are fast fades; linear only for opacity, progress, spinners |
| Springs | Apple model: stiffness = (2π/d)², damping = (1 − bounce)·4π/d. Bounce 0 by default, ≤ 0.15–0.3 after gestures, never > 0.4 (`spring.py`) |
| Popovers | Scale from 0.96–0.97, from the trigger's origin; never from 0 |
| Tooltips | First one after ~500 ms; then near-instant while moving between controls |
| Contrast | Text 4.5:1 · large text (≥ 24 regular / ≥ 19 bold, px/pt/epx) and UI parts 3:1 · never round up (4.499 fails) |
| Targets | WCAG minimum 24×24 (or enough spacing) · macOS hit area 28×28 pt default, 20×20 minimum · Windows touch 40 epx, dense mouse ≥ 32 |
| Text size | macOS 13 pt body (min 10; no Dynamic Type, so offer zoom) · Windows 14 epx, scales to 225% · GNOME 11 pt · KDE 10 pt |
| Windows shell | Title bar 32 epx (48 with search or tabs) · minimum window width ≤ 500 epx so Snap works (aim for 330–360) · page margin 24 (12 under 640 wide) |
| Spacing | 4-based scale: 4, 8, 12, 16, 24, 32, 48; tighter inside groups than between them |
| Fitts's law | Screen edges and corners are infinitely large targets; context menus open at the pointer |
| Menus | Context menus ≤ 10–12 items, ordered by frequency; submenus at most 1 level, with a safe triangle |
| Evaluation | 3–5 independent heuristic passes (one evaluator finds about 35% of problems); 5-user think-aloud tests; SUS average is 68 |
| Seizures | No more than 3 flashes per second; moving content over 5 s needs a pause control |

## 7. Avoiding the generic AI look

| Tell | Do instead |
|---|---|
| Purple/indigo gradients, gradient text, glowing borders | An accent taken from the product's world, used sparingly; solid text |
| Defaults left untouched (shadcn/Tailwind zinc, 0.5rem radius, stock shadows; Inter at one size and weight) | Your own tokens: neutrals, radius scale, a real type scale with tracking per size, your icon set, density |
| Identical rounded cards with the same shadow everywhere | Panes, lists and background shifts; shadows only on floating layers; radius by hierarchy |
| Glass/blur on everything | The platform material only where the OS uses it (sidebar, toolbar, popovers) |
| A centered "Welcome back 👋" hero inside an app | Open to the user's work or last state; first run = a useful empty state in the real layout |
| Emoji as icons; mixed icon sets | One icon family, one stroke weight, sized to the text; SF Symbols / Fluent / Adwaita where native |
| ✨ and purple for every AI feature | Name the action ("Summarize thread") with a specific icon in the normal accent |
| Pills and badges on everything; ALL-CAPS eyebrow labels over every heading | Plain text status with a small colored dot; labels only where they help scanning |
| `transition: all` and a fade-up on every element at load | Motion only in response to input or real state changes |
| Toasts for everything, a modal for every confirmation | Inline status, Undo, quiet status-bar text |
| Fake data ("John Doe", "$1,234", identical rows) | Realistic, varied content that exposes wrapping and truncation |
| Dark mode = inverted colors or pure black + neon | Dark grays, lighter surfaces for elevation, desaturated accents, contrast re-checked |

**The second wave.** When told to avoid the purple look, models drift to a new set of defaults: cream + serif + terracotta, black + acid green, newspaper-style hairlines, and tracked-out caps. Swapping one default for another is still slop. Derive choices from the product's subject, users and personality.

The full 25-row table is in `visual-craft.md` §7, and the pixel-level checklist in §9.

## 8. Writing UI code

- **Platform components first:** SwiftUI/AppKit controls, WinUI controls, libadwaita widgets, Kirigami. In web shells, use accessible primitives (React Aria, Radix, native `<button>`/`<dialog>`) and style them. Never use `<div onClick>` buttons or custom-drawn lists without keyboard support and accessibility roles.
- **Tokens in one place:** CSS custom properties, an asset catalog, a ResourceDictionary with ThemeResources, or style classes. No raw hex values or one-off pixel sizes in components.
- **One command table** (id, label, per-OS shortcut, enabled state) rendered into the menu bar, context menus, command palette and tooltips. Shortcuts come from a per-OS table, not one literal string (`CmdOrCtrl`, Qt `StandardKey`, Electron menu roles).
- **Web shells (Electron, Tauri, Wails):**
  - Chrome: `cursor: default` on controls; `user-select: none` on chrome (plus `-webkit-` for WebKit); `-webkit-app-region: drag` only on empty title-bar areas.
  - Launch: create the window hidden and show it on `ready-to-show` with a `backgroundColor`.
  - Theming: `color-scheme: light dark`; `system-ui` font for chrome.
  - Numbers and scrolling: `font-variant-numeric: tabular-nums` for changing numbers; `scrollbar-gutter: stable`.
  - Native integration: native menus with roles; titleBarOverlay or the native frame.
- **Motion code:**
  - Web: CSS transitions on transform/opacity (they're interruptible); `@media (prefers-reduced-motion: reduce)`; `<MotionConfig reducedMotion="user">` for Motion; springs from `spring.py`.
  - SwiftUI: `@Environment(\.accessibilityReduceMotion)`.
  - WinUI: `UISettings.AnimationsEnabled`.
  - GTK/libadwaita handle it for you.
- **Comment non-obvious design decisions** (why 167 ms, why this button order) so later edits don't undo them.

## 9. Reviewing an existing app

1. Run `scripts/ui_audit.py` on the code and confirm each hit by opening the file.
2. Walk `review-checklist.md`. Look at the running app or screenshots if you can.
3. Report findings **most important first**, grouped by severity:
   - **Blocker**: loses data, blocks a task, or excludes people (keyboard, screen-reader or low-vision users).
   - **Major**: breaks a platform convention people rely on, or a usability problem most people will hit.
   - **Minor**: friction or inconsistency.
   - **Polish**: craft details.

   For each finding, give:
   - **Where:** window › panel › control, and file:line.
   - **Problem:** what's wrong, in plain words.
   - **Why it matters:** the guideline, heuristic or research behind it (e.g. Nielsen #5, WCAG 1.4.3, macOS HIG Settings).
   - **Fix:** one concrete change.
4. End with what's already good (so it's kept) and the top 3 things to fix first.

Write the review for the person who asked, not for designers. Use plain words, and explain any term the first time ("caption buttons, the minimize/maximize/close buttons"). Keep it skimmable: one line per finding where possible.

When asked to *fix* rather than review, fix in severity order, keep behavior the same unless asked, then re-run the audit and say what changed.

## 10. Explaining design to the user

Use plain language and say what kind of evidence backs each recommendation. In order of strength:
- **A platform guideline or standard**, e.g. "Mac users look for Settings under the app menu with ⌘,".
- **Research**, e.g. "people answer routine 'Are you sure?' prompts on autopilot, so undo protects them better".
- **Practitioner taste**, e.g. "this is a taste call: the softer shadow feels calmer".

When the user's wish conflicts with a standard, explain the cost and offer the closest compliant option. For example, light gray text fails contrast, but a darker gray at a lighter weight keeps the quiet look.

## 11. Freshness

Platform guidelines change often:
- Apple: every June (WWDC).
- Windows App SDK: every few months.
- GNOME: every March and September.
- Electron: every 8 weeks.

The references were researched in November 2026. Each cites its sources inline and marks unverified claims with ⚠️. For anything version-specific (API names, new controls, OS-version behavior), check the official page before relying on it.
