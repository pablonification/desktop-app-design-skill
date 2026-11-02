# Auditing, revising and fixing an existing app

Read this when the app already exists and the user wants it reviewed, fixed, polished, cleaned up, made consistent, or redesigned. It's the process; the *rules* the findings rest on live in the other reference files, and `review-checklist.md` is the list of things to check.

Contents: 1. Pick the mode · 2. Ground rules for changing someone else's app · 3. Understand before judging · 4. Audit in separate passes · 5. Root causes, priorities and the scorecard · 6. Plan the change · 7. Fix recipes · 8. Verify and report · 9. Revising the look without losing existing users · Sources

## 1. Pick the mode (and say which one you're in)

| Mode | The user says | You deliver | You don't |
|---|---|---|---|
| **Audit** | "review", "audit", "what's wrong", "rate my app", "critique" | A findings report, a scorecard and a plan. **No file changes.** | Edit code, even "small obvious fixes" |
| **Fix** | "fix it", "clean it up", "make it accessible", "it feels off, fix that" | Defects fixed in severity order; same features, same identity | Change the look or structure beyond what the defects require |
| **Polish** (revise) | "make it look better / premium / less generic", "polish", "make it consistent" | Fix + a consistent system (tokens, type scale, states), microinteractions, generic tells removed | Move navigation, rename features, change workflows without asking |
| **Redesign** | "redesign", "new look", "rethink the UX" | Intent brief → one key screen proposed → approval → staged rollout | Ship everything in one unreviewed step; silently break muscle memory |

- When the request is ambiguous, pick the smallest mode that answers it and offer the next one ("Here's the audit. Want me to fix batch 1?"). Ask one short question only when the choice changes a lot of work (e.g. "keep the current look, or are you open to a new visual direction?").
- "Review it and fix the important stuff" = Audit report first (short), then Fix (and Polish only for what's clearly generic or broken).
- State the mode in the first line of your reply so the user knows what to expect.

## 2. Ground rules for changing someone else's app

1. **Preserve behavior.** Features, data, file formats, shortcuts, copy meaning, public APIs and settings keep working. Any behavior change you make on purpose is listed explicitly in the report ("Delete is now undoable instead of asking first").
2. **Fix root causes, not symptoms.** One token file beats forty edited literals; one command table beats fixing shortcuts in five places (§5).
3. **Reuse what exists.** Extend the app's tokens, components and libraries. Don't add a parallel design system or new dependencies unless the user agrees.
4. **Smallest change that fully fixes it.** No drive-by refactors or reformatting; keep diffs reviewable, one concern per change (and per commit, if you commit).
5. **Verify every fix** (§8): re-run the tools, rebuild or type-check, look at it, try the keyboard path.
6. **Be honest about evidence.** If you couldn't run the app, say so, and mark findings that need a visual check.
7. **Respect existing users.** Changes by refinement; keep the positions of frequent commands; explain anything that moved (§9; `interaction.md` §4.23).

## 3. Understand before judging (inventory)

Do this before writing a single finding. Ten minutes here prevents wrong findings later.

1. **Read the project:** README, package/project files, the theme or token files, the component library, the main windows/routes. Note the stack(s), target OSes and minimum OS versions (SKILL.md §1).
2. **Reconstruct the design system as it actually is**, not as intended:
   ```bash
   python3 scripts/ui_audit.py <app> --save /tmp/before.json   # findings + token counts, saved for comparison
   python3 scripts/tokens.py <app>                                   # every color/spacing/radius/type/duration literal, clustered
   ```
   Save the baseline outside the user's project (it isn't theirs to commit, and Audit mode changes no files).
   If there's a `DESIGN.md`, theme file or token set, treat it as the app's own contract: inconsistencies *with it* are findings too.
3. **Map the surfaces and the top tasks:** list the windows, main views and the 3 most frequent tasks. Trace how one key view actually renders (entry point → components → styles/tokens actually applied), rather than grepping the whole repo for problems. Unused CSS and dead components are not findings.
4. **Write the intent if it's missing** (SKILL.md §3 step 0): who, how often (sovereign / transient / daemon), top tasks. Also name the 3 adjectives the current UI *actually* expresses, versus the ones it should.
5. **Gather rendered evidence** whenever possible. A screenshot settles arguments that code reading can't (hierarchy, density, alignment, contrast over images).

| Stack | How to see it |
|---|---|
| Electron | Playwright `_electron.launch({ args: ['.'] })` → `page.screenshot()`; or `win.webContents.capturePage()` |
| Tauri / Wails / web UI | Run the front end's dev server and screenshot with Playwright. Use Playwright's **WebKit** for Tauri on macOS/Linux (WKWebView/WebKitGTK), Chromium for Windows (WebView2) |
| macOS native | `screencapture -o -l <windowID>` (window only) or `screencapture -x out.png`; SwiftUI `#Preview` or `ImageRenderer` for single views |
| Windows native | Ask the user for screenshots, or Win+Shift+S; Accessibility Insights for Windows shows the UI tree |
| GNOME / GTK | Launch with `GTK_DEBUG=interactive` to open the GTK Inspector (widget tree, CSS, a11y); `gnome-screenshot -w` |
| Can't run it | Say so. Audit from code; label visual findings "needs a visual check" |

Capture each key surface in light and dark, at the minimum window size, with large text or 200% zoom, and keyboard-only. For motion, record or step through frames: a settled screenshot hides jank and layout shift.

## 4. Audit in separate passes

A single evaluator finds only about a third of usability problems; separate passes with different lenses act like several evaluators (`interaction.md` §1.2, §5). Do each pass on its own and write findings as you go:

| Pass | Lens | Use |
|---|---|---|
| 1. Platform fit | Window chrome, menus and command placement, shortcuts, settings, dialogs, lifecycle, wording | `review-checklist.md` §2–3; the OS files |
| 2. Usability | Cognitive walkthrough of each top task (the 4 questions), then a sweep of Nielsen's 10 heuristics | `interaction.md` §1, §5–7 |
| 3. Accessibility | Keyboard-only run of the top task, names/roles, contrast, OS settings, targets | `review-checklist.md` §7; `accessibility.md` |
| 4. States and trust | Empty/loading/error/offline states, data safety, honest status, undo | `review-checklist.md` §5, §8 |
| 5. Visual craft | Hierarchy, spacing, type, color, depth, icons, density, generic-AI tells | `review-checklist.md` §4; `visual-craft.md` §7, §9 |
| 6. Motion | Purpose, durations, easing, interruptibility, reduced motion, frequent actions | `review-checklist.md` §6; `motion.md` |
| 7. Intent and feel | First 60 seconds, personality, signature moment, peaks and endings | `emotional-design.md` §11e |

**Evidence gate for every finding** (adapted from ibelick/ui-skills `improve-ui`, MIT). A finding needs all three:
- **Rule:** the guideline, standard, heuristic or research it breaks, or a direct contradiction of the app's own system ("the app's tokens say 8 px radius; this dialog uses 20").
- **Proof:** it actually reaches the user: file:line on the real render path, a screenshot, or a measured value (contrast ratio, duration, size). "This exists somewhere in the code" isn't proof.
- **Fix:** one concrete change, not "consider improving".

Then **try to falsify it**: is it intentional and fine (a platform convention, an accessible alternative elsewhere, a deliberate brand choice that doesn't hurt usability)? Drop or downgrade it if so. Run `ui_audit.py` hits through the same gate; it pattern-matches and can be wrong.

**Severity** (consistent with SKILL.md §9), judged by frequency × impact × persistence (Nielsen):
- **Blocker:** loses data; blocks a top task; excludes keyboard, screen-reader or low-vision users; or a legal accessibility failure on a core path.
- **Major:** most people hit it in a top task, or it breaks a platform convention people rely on (menus, shortcuts, window controls, dialog order).
- **Minor:** friction or inconsistency off the main path.
- **Polish:** craft details: alignment, rhythm, a generic tell that doesn't hurt use.

## 5. Root causes, priorities and the scorecard

**Group findings by root cause.** Most audits collapse into a handful of causes, and fixing the cause fixes many findings at once:

| Root cause | Typical symptoms |
|---|---|
| No token system | Dozens of near-identical grays, off-grid spacing, 10+ font sizes, random radii and shadows, broken dark mode |
| No command model | Missing menu items, inconsistent shortcuts, actions only on hover or only in one place, no palette |
| Custom-drawn controls | No keyboard access, no focus ring, invisible to screen readers, wrong in high contrast |
| Web defaults in a desktop shell | Pointer cursor, selectable chrome, white flash, browser dialogs, no menu, no window state |
| No state design | Spinners everywhere, "No items" flashing while loading, errors in toasts, no empty states |
| No motion system | `transition: all`, random durations, entrance animations on everything, no reduced motion |
| No intent | Generic look, no hierarchy, everything equally loud, no signature moment |

**Prioritize** with impact × effort: quick wins (high impact, low effort) first, then root-cause fixes, then the long tail. Pick a **"fix first" top 3** and say why.

**Scorecard** (communicates progress; it's a judgment, not a measurement). Rate each area 0–4 before and after:

| Area | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Platform fit · Usability · Accessibility · States & trust · Visual craft · Motion · Intent & feel | Broken or absent | Many major issues | Works, with notable friction | Solid, minor issues | Exemplary; could be a reference |

Always pair the score with the evidence: "Accessibility 1 → 3: focus visible everywhere, contrast fixed (12 pairs), palette fully keyboard-driven; still missing screen-reader announcements for sync".

## 6. Plan the change

**Fix and Polish: work in batches, in this order**, re-running the tools after each:
1. **Safety and access:** data loss, blocked tasks, keyboard path, focus visibility, contrast on core paths.
2. **Platform behavior:** window chrome, menus and shortcuts (one command table), dialogs and button order, lifecycle, settings location.
3. **The system:** tokens (`tokens.py`), type scale, spacing, radius, icon set; replace literals.
4. **States and feedback:** empty/loading/error/offline, undo, inline errors, honest status.
5. **Motion:** remove what has no job; tokenized durations and easing; reduced motion; the microinteraction catalog (`motion.md` §9).
6. **Identity and polish:** generic tells out, hierarchy, one signature moment, pixel pass (`visual-craft.md` §9).

**Redesign:** write the intent brief first (SKILL.md §3 step 0), list what *stays* (structure, command positions, shortcuts, terms) and what changes, then do **one key screen first** and show it (screenshot or description with before/after) before rolling out. Roll out through the token layer so the change is consistent everywhere at once.

**Plan template** (for an audit deliverable, or when another agent or person will do the work; adapted from ibelick/ui-skills `improve-ui`, MIT). Each item is self-contained:
- **Goal:** one sentence, user-visible.
- **Evidence:** the finding(s) it resolves, with file:line or screenshot.
- **Decision:** the chosen fix and why (the rule it satisfies).
- **Changes:** files and what changes in each; what to reuse.
- **Preserve:** behaviors that must not change.
- **Verify:** exact checks (tool commands, keyboard path, screenshot to compare).
- **Stop and ask if:** conditions that mean the plan is wrong (e.g. "the color is set by a third-party theme you can't edit").

## 7. Fix recipes

The common findings and their standard fixes. Detail and sources are in the linked sections; adapt to the app's existing code style.

**System and consistency**
- **Color/spacing/type sprawl** → `python3 scripts/tokens.py <app> --write src/tokens.css` proposes a token file from the literals actually used (clustered colors, spacing snapped to the 4 px grid, radii and type sizes snapped to a scale). Review names and values, add dark-mode values, then `--diff` / `--apply` to replace literals in stylesheets; handle inline styles by hand. Native: asset-catalog colors (SwiftUI), `{ThemeResource}` brushes (WinUI), named colors/style classes (libadwaita). (`visual-craft.md` §3)
- **Too many font sizes/weights** → map every size to the platform's text styles (Mac: `.body` 13 pt …; Windows: type ramp styles; GNOME: style classes) or one scale; 2–3 weights. (`visual-craft.md` §2; OS files)
- **Card soup / heavy shadows** → remove shadows from anything that doesn't float; separate with space, then background shift, then hairline. (`visual-craft.md` §4)

**Platform behavior** (Electron shown; others in `cross-platform.md` Part B)
- **Frameless window / hand-drawn caption buttons:**
  ```js
  const isMac = process.platform === 'darwin';
  const win = new BrowserWindow({
    show: false, backgroundColor: '#f7f6f3',          // your real surface color: no white flash
    titleBarStyle: 'hidden',                           // mac: traffic lights stay, content goes full-height
    ...(isMac ? { trafficLightPosition: { x: 16, y: 14 } }
              : { titleBarOverlay: { color: '#00000000', symbolColor: '#5b5b5b', height: 40 } }), // real caption buttons + Snap Layouts
  });
  win.once('ready-to-show', () => win.show());
  ```
  Delete the custom min/max/close buttons; mark only empty title-bar areas `-webkit-app-region: drag` and every control inside it `no-drag`. (`cross-platform.md` B1; `windows.md` §6)
- **Menu removed / missing** → a role-based menu (`{ role: 'appMenu' }` on Mac, `fileMenu`, `editMenu`, `viewMenu`, `windowMenu`) plus app commands with `CmdOrCtrl` accelerators, built from one command table that also feeds the palette and tooltips. (`cross-platform.md` B1, A2)
- **Quits on Mac when the window closes** → `app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit() })` and re-create a window on `activate`.
- **Window size/position forgotten** → Electron 44+ `windowStatePersistence` (experimental) or save bounds yourself; SwiftUI restores automatically (`@SceneStorage` for selection); WinUI: save `AppWindow` position and size. Never restore off-screen.
- **Web feel in a desktop shell** → a desktop base layer:
  ```css
  :root { color-scheme: light dark; font: 13px/1.4 system-ui, -apple-system, "Segoe UI Variable Text", "Segoe UI", sans-serif; }
  body { cursor: default; -webkit-user-select: none; user-select: none; overscroll-behavior: none; }
  input, textarea, [contenteditable], .selectable, .content { -webkit-user-select: text; user-select: text; cursor: auto; }
  a[href] { cursor: pointer; }
  ```
  Plus a native context menu (or none) instead of the browser's. (`cross-platform.md` Part C)
- **Browser `confirm()` / `alert()`** → undo for anything reversible (below); a native dialog (`dialog.showMessageBox`, button order per OS) only for irreversible actions.

**Platform behavior, native**
- **SwiftUI / AppKit** (snippets in `macos.md` §9):
  - Hidden title bar with drawn controls → keep the real traffic lights; use the standard title bar plus `.toolbar` for the main window.
  - Fixed window → `.defaultSize(width:height:)`, `.frame(minWidth:minHeight:)`, `.windowResizability(.contentMinSize)`.
  - Settings in a sheet → a `Settings { }` scene with `@AppStorage`, changes applied at once.
  - Missing or hijacked shortcuts → `.commands { CommandGroup(…); CommandMenu("Item") { … } }`; standard keys keep their meaning.
  - Rows with `onTapGesture` → `List(selection:)` plus `.onDeleteCommand` and `.contextMenu`.
  - "Are you sure?" → act, and register undo with `@Environment(\.undoManager)`.
  - Fixed grays and sizes → `.secondary` and text styles.
  - In-app dark toggle → follow the system (or offer System/Light/Dark, defaulting to System).
- **WinUI** (snippets in `windows.md` §12):
  - Hard-coded colors → `{ThemeResource}` brushes with Light, Dark and HighContrast dictionaries.
  - `FontSize` literals → type ramp styles.
  - Custom caption buttons → `ExtendsContentIntoTitleBar` + `SetTitleBar` (system caption buttons, Snap Layouts work).
  - `UseSystemFocusVisuals="False"` → remove it.
  - Confirmations → `ContentDialog` with a verb button and no default for destructive actions.
- **GTK / libadwaita, Qt / Kirigami:** use the toolkit widgets, style classes and named colors (`linux.md` §2–3, §6, §11).

**Accessibility**
- **Focus ring removed** → delete `outline: none` overrides and add `:focus-visible { outline: 2px solid var(--focus, Highlight); outline-offset: 2px; }` (an outline, not only `box-shadow`, so it survives forced colors). Native: remove `UseSystemFocusVisuals="False"` and custom focus suppression. (`accessibility.md` §2)
- **Low contrast** → `python3 scripts/contrast.py FG BG --fix`; de-emphasize with weight or size rather than paler text; re-check in dark mode and over materials. (`accessibility.md` §6)
- **Hover-only actions** → also show on `:focus-within` and on the selected row; put the same actions in the context menu and the menu bar; give icon-only buttons a name and a tooltip with the shortcut.
- **Custom-drawn list/menu/tabs** → swap for the toolkit control, or implement the ARIA APG pattern (one Tab stop, arrows inside, roles and states). (`accessibility.md` §2.2)

**States and feedback**
- **Confirm-before-delete** → do it, then offer Undo (`interaction.md` §4.13):
  ```tsx
  function useUndoableRemove<T extends { id: string; name?: string }>(items: T[], setItems: (f: (x: T[]) => T[]) => void, commit: (id: string) => Promise<void>) {
    return (item: T, announce: (msg: string, undo: () => void) => void) => {
      const index = items.findIndex((x) => x.id === item.id);
      setItems((xs) => xs.filter((x) => x.id !== item.id));            // optimistic: gone immediately
      const timer = setTimeout(() => commit(item.id).catch(() => {      // commit after the undo window
        setItems((xs) => [...xs.slice(0, index), item, ...xs.slice(index)]);   // failed: put it back, say so inline
      }), 8000);
      announce(`Deleted “${item.name ?? 'item'}”`, () => { clearTimeout(timer); setItems((xs) => [...xs.slice(0, index), item, ...xs.slice(index)]); });
    };
  }
  ```
  The undo bar lives in a polite live region, stays while hovered or focused, and ⌘Z / Ctrl+Z triggers the same undo.
- **Errors in toasts** → show the error next to its source (the row, the field, the panel) with what's safe and a next step; announce it (`aria-live="polite"`, or `assertive` for blocking errors). (`interaction.md` §4.14)
- **Spinners everywhere** → no indicator under ~1 s; otherwise delay it 150–300 ms and keep it at least 300–500 ms once shown; skeletons that match the final layout; local data never shows a spinner. (`motion.md` §5)
- **Missing empty states** → separate first-run, no-results and failed-to-load states, each with a reason and one next action. (`interaction.md` §4.16)

**Motion**
- **`transition: all`, long or random durations** → name the properties; use tokens (`--dur-fast: 150ms; --dur-base: 200ms; --dur-slow: 300ms; --ease-out: cubic-bezier(0.23,1,0.32,1)`); remove entrance animations from things that just render. (`motion.md` §3, §7)
- **No reduced motion** → `@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: 1ms !important; animation-iteration-count: 1 !important; transition-duration: 1ms !important; scroll-behavior: auto !important; } }` as a safety net, then replace meaningful movement with fades deliberately; Motion: `<MotionConfig reducedMotion="user">`. (`motion.md` §8)

**Identity**
- **Generic tells** (gradient hero, gradient text, emoji icons, ✨ AI buttons, "Welcome back" banner) → open to the user's work or a real status summary; one icon set; name AI actions by what they do; an accent from the product's world, used sparingly. (`visual-craft.md` §7)
- **No personality** → write the 3 adjectives + 1 anti-adjective, then change type, color, motion and copy on purpose, and design one signature moment. (`emotional-design.md` §11)

## 8. Verify and report

**Verify** after each batch and at the end:
```bash
python3 scripts/ui_audit.py <app> --compare /tmp/before.json   # what got fixed, what's new, token counts before → after
python3 scripts/tokens.py <app>                                   # fewer distinct values?
python3 scripts/contrast.py --pairs "FG:BG" …                     # every text/background pair you touched
```
Then: build or type-check and run existing tests; complete the top task keyboard-only; compare before/after screenshots side by side (light, dark, minimum size); watch the transitions you changed; confirm no feature, shortcut or setting changed unless listed.

**Audit report** (Audit mode):
1. **Summary:** 2–3 sentences and the scorecard.
2. **Fix first:** the top 3 with why.
3. **Findings by severity:** Where (window › panel › control, file:line) · Problem · Why it matters (rule) · Fix · Effort (S/M/L).
4. **Root causes:** the 2–5 causes behind most findings.
5. **What's already good** (so nobody "fixes" it).
6. **Plan:** the batches from §6, and an offer: "Want me to start with batch 1?"

**Fix / Polish report:**
1. **Mode and scope** in one line.
2. **What changed**, grouped by area, one line each with the reason.
3. **Before → after:** scorecard and audit counts (`--compare` output, summarized).
4. **Behavior changes:** an explicit list (ideally empty or tiny).
5. **Not verified / needs a human look:** e.g. "Snap Layouts on a real Windows machine", "VoiceOver reading of the sidebar".
6. **What's left:** remaining Minor/Polish items.

Write for the person who asked: plain words, define any term the first time, one line per item where possible.

## 9. Revising the look without losing existing users

- **Refine, don't reinvent.** The crafted desktop apps evolve by refinement: same skeleton, quieter chrome, better type and color, one stronger signature element (`visual-craft.md` §8). Familiar structure keeps first impressions and muscle memory; distinctiveness goes into details (`emotional-design.md` §11b).
- **Keep muscle memory:** shortcuts, menu locations, toolbar order and the position of frequent commands stay put. If something must move, keep the old shortcut working and tell people where it went (`interaction.md` §4.23).
- **Change through the system:** new tokens, type and icons applied everywhere at once look intentional; screen-by-screen restyling looks broken in between.
- **For big changes**, give people a heads-up and a way to learn the new layout (a short "what moved" note at the moment they need it, not a launch tour; `interaction.md` §4.17).
- **Measure the result,** not the vibe: audit counts and scorecard before/after, the top task's step count or keystroke-level time (`interaction.md` §2.4), contrast pairs passing, distinct token values.

## Sources

- Nielsen Norman Group: heuristic evaluation, severity ratings, number of evaluators (via `interaction.md` §1–2, §5–7).
- ibelick/ui-skills `improve-ui` (MIT, © 2026 Julien Thibeaut), https://github.com/ibelick/ui-skills: the evidence gate (rule, proof, fix), falsification, and the self-contained plan template, paraphrased and adapted to desktop apps (our version adds accessibility and usability passes and gathers rendered evidence rather than skipping visual judgments).
- Platform and framework rules behind each recipe: `cross-platform.md`, `macos.md`, `windows.md`, `linux.md`, `accessibility.md`, `motion.md`, `visual-craft.md`, `interaction.md` (each cites its primary sources).
- Playwright Electron and WebKit automation: https://playwright.dev/docs/api/class-electron, https://playwright.dev/docs/browsers. macOS `screencapture`: `man screencapture`. GTK Inspector: https://docs.gtk.org/gtk4/running.html (⚠️ not re-verified for GTK 4.22).
