# Desktop design review checklist

Use this to audit an app, window, flow, screenshot or PR, or to check your own work before calling it done. It pulls the highest-impact checks from the other reference files, and each line points to where the detail lives. Skip what doesn't apply, and spend most of your attention on the app's top tasks.

**Severity guide:**
- **Blocker**: loses data, blocks a task, or excludes people (keyboard, screen-reader or low-vision users).
- **Major**: breaks a platform convention people rely on, or a usability problem most people will hit.
- **Minor**: friction or inconsistency.
- **Polish**: craft details.

Report in the format in SKILL.md §9, most important first. For a full audit, fix, polish or redesign of an existing app, follow the process in `audit-and-fix.md` and use this list for its passes.

## 0. Before you start
- [ ] Run `python3 scripts/ui_audit.py <app> --save /tmp/before.json` (and `tokens.py <app>` for the token picture), and open every hit to confirm it. Pattern matches can be wrong, and the audit can't see layout, copy or flow problems.
- [ ] Note the context in one line: who uses the app, how often (sovereign, transient or daemon), the top 3 tasks, which OSes it ships on. *(interaction §3, §5)*
- [ ] If you can run it, capture screenshots in light and dark, at the minimum window size, with large text, and keyboard-only. Record the main transitions; a still screenshot hides jank.

## 1. Intent and hierarchy
- [ ] Each window's job is obvious within a few seconds; the primary action is the strongest element; at most one prominent button per view. *(visual-craft §1)*
- [ ] Hierarchy comes from weight, color and dimming, not just size; secondary items step back. *(visual-craft §0)*
- [ ] The app has a recognizable personality: 3 adjectives show up consistently in type, color, motion and copy, and the anti-adjective doesn't. *(emotional-design §11a)*
- [ ] Exactly one signature moment, tied to the core value; nothing else competes. *(emotional-design §11c)*
- [ ] Structure is familiar for the category; distinctiveness lives in details, not in navigation, controls or window chrome. *(emotional-design §11b)*

## 2. Platform fit
- [ ] Window chrome is native, or a native-controls overlay:
  - traffic lights top-left on Mac
  - caption buttons with working Snap Layouts on Windows
  - GNOME's `button-layout` respected
  - drag from empty title-bar space, OS-correct double-click and right-click

  *(cross-platform A1; windows §6; macos §2; linux §8)*
- [ ] Commands live where the OS expects them:
  - Mac: full menu bar in standard order, every command present, disabled not hidden
  - Windows: menu bar or CommandBar with access keys
  - GNOME: header bar plus "Main Menu" with no Quit
  - KDE: menu bar or hamburger

  *(macos §3; windows §7; linux §2, §6)*
- [ ] Settings are named and placed per OS:
  - Mac: "Settings…" ⌘, in the App menu
  - Windows: "Settings" at the bottom of navigation
  - GNOME: "Preferences" Ctrl+,
  - KDE: "Configure <App>…"

  Changes apply instantly with no OK/Cancel. *(cross-platform A1; macos §5)*
- [ ] Standard shortcuts work and none are repurposed; redo, find next and full screen use each OS's keys; global hotkeys are rebindable and conflict-checked. *(cross-platform A2; macos §3)*
- [ ] Dialog button order and default button follow the OS; buttons are labeled with verbs; Cancel or the safe choice is the default for destructive actions. *(cross-platform A3)*
- [ ] Lifecycle: a Mac app stays running with no windows open; Windows and Linux apps quit on last window close unless they're tray apps; there's never a tray-only way back on GNOME. *(cross-platform A1, A4)*
- [ ] Wording and capitalization follow the OS (Title Case on Mac and KDE, sentence case on Windows, header caps on GNOME); "…" only when more input follows. *(cross-platform A1, A3)*
- [ ] The app follows the system appearance (light/dark/auto) with no forced in-app theme. Accent, contrast, transparency and motion settings are honored and update live. *(macos §7; windows §4; linux §8; accessibility §4)*
- [ ] Mac 26+: no custom backgrounds behind system bars, no glass on content, no glass on glass. Windows: Mica only on the base layer, Acrylic only on transient surfaces. *(macos §1; windows §5)*

## 3. Keyboard and commands
- [ ] The top task can be completed with the keyboard alone. Focus is always visible, Tab order is logical, and composite widgets have one Tab stop with arrow keys inside. *(accessibility §2)*
- [ ] Esc closes or cancels every transient surface; Return triggers the default button; F6 moves between panes (Windows/Linux); Shift+F10 or the Menu key opens context menus. *(accessibility §2.3)*
- [ ] Shortcuts are discoverable: shown in menus and tooltips, plus a shortcuts sheet (⌘/ or Ctrl+?). *(interaction §4.2)*
- [ ] Apps with many commands (over ~30) have a command palette with fuzzy search, recent items, synonyms and visible shortcuts. *(interaction §4.1)*
- [ ] Context menus open at the pointer, include only actions for the clicked object, have ≤ 10–12 items, ordered by frequency, with at most one submenu level; every item is also in the main menu. *(interaction §4.3)*
- [ ] Selection follows the platform model: click, Shift-range, ⌘/Ctrl-toggle, select all, Esc or background click to deselect. Selection, focus and hover look different from each other. *(interaction §4.4)*
- [ ] Drag and drop shows signifiers and a live preview, supports Esc-cancel and undo, and has a non-drag alternative. Files can be dragged in and out. *(interaction §4.5; accessibility §5)*

## 4. Layout and visual craft
- [ ] Every gap comes from a 4-based scale; spacing is tighter inside groups than between them; nothing is off by 1–2 px. *(visual-craft §9)*
- [ ] Type: the platform UI font for chrome; ≤ 4 sizes and 2–3 weights per view; tracking adjusted by size; tabular figures for changing or aligned numbers; prose ≤ 75 characters per line. *(visual-craft §2)*
- [ ] Color comes from tokens:
  - a perceptual scale with tinted neutrals
  - one accent with one meaning, never reused for decoration
  - no raw hex values in components
  - dark mode designed separately, not inverted

  *(visual-craft §3)*
- [ ] Separation uses space, then a background shift, then a hairline, then a shadow. Shadows only on floating layers, layered and tinted. Radii come from a scale and nest concentrically. *(visual-craft §4)*
- [ ] Desktop density: 28–32 px rows, 13–14 px UI text, quiet chrome; a compact/comfortable option where it helps. *(visual-craft §5)*
- [ ] One icon family, one stroke weight, icons optically aligned with text; icon-only buttons have a tooltip and an accessible name. *(visual-craft §4.5)*
- [ ] None of the generic-AI tells in `visual-craft.md` §7 (gradients, emoji icons, sparkle-AI buttons, card soup, glass everywhere, fake data, an in-app hero banner).
- [ ] Realistic content: long names, 0/1/999+ items, missing images, long words and URLs, accented and right-to-left text. The window works at its minimum size and when very wide. *(visual-craft §9)*

## 5. States and feedback
- [ ] Visible feedback within 0.1 s of every input; duplicate submits blocked. *(interaction §2.5)*
- [ ] Waiting is matched to duration:
  - nothing under 1 s
  - spinners delayed 150–300 ms, then visible at least 300–500 ms
  - skeletons that match the final layout
  - percent-done, a description and Cancel for 10 s or more
  - long jobs never block the window

  *(interaction §4.19; motion §5)*
- [ ] Empty states are distinct (first run, no results, failed to load, permission denied); each says why and offers the next action. "No items" never flashes while loading. *(interaction §4.16)*
- [ ] Errors appear next to their source, in plain words: what happened, what's safe, what to do. Never only a toast or color. *(interaction §4.14)*
- [ ] Routine destructive actions offer undo; only irreversible ones confirm, naming the consequence. *(interaction §4.13)*
- [ ] Save, sync, offline and background-job status is visible but quiet, and honest: "Saved" only once true. *(interaction §4.15, §4.20)*
- [ ] No layout shift: reserved sizes for images, stable button widths when the label changes, `scrollbar-gutter: stable` in web shells. *(visual-craft §9)*

## 6. Motion and microinteractions
- [ ] Every animation has a job: feedback, orientation, showing cause and effect, or a state change people need to follow. Nothing animates just because. *(motion §1)*
- [ ] Frequent and keyboard-driven actions don't animate: typing, arrow navigation, palette open, tab switching, selection. *(motion §0)*
- [ ] Durations fit desktop: micro 80–150 ms, menus ≤ 150–200 ms, panels and dialogs 200–300 ms, nothing routine over 400 ms; exits faster than entrances. *(motion §3)*
- [ ] Entrances decelerate; popovers and menus scale from 0.96–0.97 at their trigger; items leave the way they came; nothing scales from 0. *(motion §0, §3.3)*
- [ ] Motion is interruptible: CSS transitions or springs, not restart-from-zero keyframes. Bounce is 0 unless the motion follows a gesture or a rare moment. *(motion §4)*
- [ ] Only transform and opacity animate; no `transition: all`; smooth at 120 Hz. *(motion §7.0)*
- [ ] Reduced motion replaces slides, zooms and parallax with fades and keeps state feedback. The library default is overridden (`reducedMotion="user"`). *(motion §8)*
- [ ] Microinteractions follow the catalog: hover, press, toggle, copy confirmation, drag lift and drop, reorder, optimistic update + undo, toast enter and exit, number changes, sidebar collapse. *(motion §9)*

## 7. Accessibility
- [ ] Contrast: text ≥ 4.5:1 (large ≥ 3:1); control boundaries, icons, focus rings and chart marks ≥ 3:1. Check in light, dark, increased contrast, and over materials. Run `scripts/contrast.py`. *(accessibility §0, §6)*
- [ ] Nothing relies on color alone (status, errors, selection, charts). *(accessibility §6)*
- [ ] Every control has a short accessible name matching its visible text, the right role and state; icon-only buttons are named; decoration is hidden. *(accessibility §3)*
- [ ] Async results (saved, done, errors, toasts) are announced to screen readers; toasts don't vanish before they can be read. *(accessibility §3.2)*
- [ ] Targets ≥ 24 px (platform sizes preferred); no hover-only controls; actions fire on release; every drag has an alternative. *(accessibility §5)*
- [ ] Tooltips can be dismissed with Esc, can be hovered over, and stay put; essential information never lives only in a tooltip. *(accessibility §5)*
- [ ] Text scaling: Windows 225% and app zoom to 200% don't clip text; no fixed-height text containers. Mac apps offer their own zoom. *(accessibility §0, §5)*
- [ ] Windows contrast themes / `forced-colors`: system colors used; focus rings still visible (not `box-shadow` only). *(accessibility §4; windows §4)*
- [ ] Every window has a meaningful title, including custom title bars. *(accessibility §10)*

## 8. Data safety and trust
- [ ] Autosave or an explicit save that never loses work; crash recovery; windows, selection and scroll restored on relaunch. *(interaction §4.20; macos §2)*
- [ ] The first window: no white flash, no layout jump, correct size and position, on-screen even after a monitor change. *(emotional-design §11d; interaction §4.21)*
- [ ] Zero typos, consistent terms (the same verb from button to toast), no placeholder text. *(emotional-design §11d)*
- [ ] Data transparency: where data lives, what leaves the device and why, export in an open format. *(emotional-design §11d)*
- [ ] Permissions are asked at the moment of use with a specific reason. The app still works after a refusal, and Mac apps deep-link to System Settings for Accessibility, Screen Recording and Full Disk Access. *(macos §5)*
- [ ] Updates never interrupt work; anything that moved is explained. *(interaction §4.23)*

## 9. Web shells (Electron, Tauri, Wails)
- [ ] No browser smells:
  - arrow cursor on buttons
  - chrome text not selectable
  - no browser `alert`/`confirm`
  - no default browser context menu
  - no rubber-band scrolling on the whole window
  - no spinner for local data

  *(cross-platform Part C)*
- [ ] Launch: window created hidden, shown on `ready-to-show`, `backgroundColor` set; window state persisted. *(cross-platform B1)*
- [ ] An application menu built from roles exists (undo, copy, paste, zoom, window); accelerators use `CmdOrCtrl`. *(cross-platform B1)*
- [ ] Tauri/Wails: CSS checked against the oldest WebKit you support (`-webkit-user-select`, `-webkit-backdrop-filter`, feature-detected View Transitions). *(cross-platform B2)*
- [ ] Linux: native Wayland, one app ID everywhere (`.desktop`, icon, `StartupWMClass`), the dark-mode portal read. *(linux §8, §10)*

## 10. Ethics
- [ ] "No" is as easy as "Yes"; cancel is as easy as subscribe; trial end dates shown with a reminder before charging. No confirmshaming, fake urgency, nagging, pre-checked upsells or disguised ads. *(emotional-design §10)*

## 11. Tools to run when you can
- `python3 scripts/ui_audit.py <app>` (`--compare /tmp/before.json` after fixing), `python3 scripts/tokens.py <app>`, `python3 scripts/contrast.py --pairs FG:BG …`, `python3 scripts/spring.py …` to check spring timings.
- macOS: Accessibility Inspector audit, VoiceOver (⌘F5), Full Keyboard Access on, Increase Contrast and Reduce Transparency on.
- Windows: Accessibility Insights for Windows, Narrator or NVDA, all 4 contrast themes, Text size 225%, Animation effects off.
- Linux: Accerciser + Orca, High Contrast, Large Text, reduced motion, 100/125/150/200% scaling.
- Electron/Tauri: axe-core (e.g. via Playwright), the Chromium accessibility tree, macOS "Show scroll bars: Always".
- Automated checks miss reading order, label quality, keyboard flow and feel. Always do the manual pass too. *(accessibility §9)*
