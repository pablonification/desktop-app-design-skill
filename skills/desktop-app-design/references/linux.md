# Linux desktop app design (GNOME, KDE, elementary, cross-desktop)

Read this for any Linux app: GTK 4 + libadwaita, Qt + Kirigami, or a cross-platform toolkit that has to fit in on GNOME and KDE. Also covers freedesktop integration (portals, .desktop files, app IDs) and Flathub quality rules. Every rule cites its source inline; ⚠️ marks claims that couldn't be fully verified (collected at the end). Researched November 2026 — platform details change, so re-check anything version-specific.

Contents: 0. TL;DR rules for agents · 1. GNOME HIG — principles, versions, 2025–2026 changes · 2. GNOME structure & libadwaita widgets · 3. GNOME visuals — type, style classes, accent, dark, spacing, icons, writing · 4. GNOME keyboard · 5. GNOME motion & accessibility · 6. KDE HIG, Kirigami, Breeze, Plasma 6 · 7. elementary OS · 8. Freedesktop / cross-desktop integration · 9. Flathub quality guidelines · 10. Electron / Qt / Flutter / Tauri on Linux — mistakes & fixes · 11. Code snippets · Unverified / open questions

## 0. TL;DR rules for agents
1. **Pick the target desktop's language** — GNOME (GTK 4 + libadwaita ≥1.8), KDE (Qt 6 + Kirigami/KF6), or cross-platform toolkit + freedesktop integration (§8). Don't mix idioms (e.g. GNOME header-bar app with KDE icon-on-every-button rules).
2. **One app ID everywhere** (`com.example.App`): `.desktop` name, icon, metainfo, D-Bus, Wayland `app_id`, `StartupWMClass`. Mismatch = wrong/generic icon.
3. **Follow the system**: colour scheme, accent, contrast, reduced motion, fonts, text scale — via libadwaita/Kirigami automatically, or the Settings portal `org.freedesktop.appearance` (§8). Never hard-code blue, fonts or px font sizes.
4. **Wayland first**: native Wayland (no XWayland blur), CSD on GNOME, respect `button-layout`, don't restore x/y, test 100/125/150/200% scaling. X11 sessions are gone in GNOME 50 / Plasma 6.8.
5. **Undo over confirm**: destructive actions get an Undo toast/passive notification; confirm only if irreversible. Dialogs never unprompted, always modal to a parent, verbs not OK/Yes.
6. **Button order is platform-specific**: GNOME/elementary = Cancel then affirmative (affirmative at the end); KDE/Qt `KdeLayout` = OK then Cancel. Use `AdwAlertDialog` / `QDialogButtonBox` roles, never hand-place.
7. **GNOME window recipe**: `AdwApplicationWindow` → `AdwToolbarView` → `AdwHeaderBar` (actions start, title centre, `open-menu-symbolic` "Main Menu" end) → `AdwNavigationSplitView`/`AdwViewStack` + `AdwBreakpoint`; content in `AdwClamp`/boxed lists; empty states `AdwStatusPage`; feedback `AdwToast`/`AdwBanner`.
8. **KDE window recipe**: `Kirigami.ApplicationWindow` + `pageStack` of `ScrollablePage`s with `actions`, `GlobalDrawer` (nav or hamburger), `FormLayout` settings, `PlaceholderMessage`, `InlineMessage`, `showPassiveNotification`; spacing only via `Kirigami.Units`.
9. **Writing**: GNOME header caps for titles/buttons/menus, sentence caps for labels/body; no trailing periods; "…" only when more input follows; real Unicode (… “ ” ’ × –). KDE similar (Title Case vs sentence case), imperative verbs, no "you", every error actionable.
10. **Keyboard**: Ctrl+Q/W, F1, F10 menu, Ctrl+? shortcuts (`AdwShortcutsDialog`), Ctrl+, prefs (GNOME) / Ctrl+Shift+, (KDE); never Super/Meta; everything reachable by Tab, Esc closes transient UI.
11. **Accessibility**: label every icon-only button (tooltip + accessible name), never colour-only meaning, test High Contrast, Large Text/font 14, keyboard-only, Orca, reduced motion.
12. **No tray dependence; no "Advanced" pages; no splash screens; settings apply instantly.**
13. **Ship store-quality metadata**: Flathub name ≤15 chars, summary 10–25 chars imperative, 3–6 window-only screenshots at ≤1000×700 with default settings, brand colours, SVG icon without baked shadow, release notes every release.

## 1. GNOME HIG — principles, versions, 2025–2026 changes

HIG: https://developer.gnome.org/hig/ — written for "GTK 4 and Libadwaita"; source repo `Teams/Websites/developer.gnome.org-hig`. libadwaita docs: https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/.

**Principles** (https://developer.gnome.org/hig/principles.html) — Design for People; Make it Simple ("do one thing and do it well", progressive disclosure, frequent actions close at hand); Reduce User Effort ("if something can be done automatically, do it automatically", fewer steps, less to remember, short text); Be Considerate ("Allow destructive actions to be undone instead of asking for confirmation", don't interrupt).

**Version map** (rows 49–51 verified on release.gnome.org; libadwaita versions from NEWS)
| GNOME | Date | libadwaita | GTK | Notable for app makers |
|---|---|---|---|---|
| 47 | 2024-09 ⚠️ | 1.6 | 4.16 ⚠️ | System accent colours (9 fixed, CSS `--accent-*`), `AdwSpinner`, `AdwBottomSheet`, `AdwButtonRow`, `AdwMultiLayoutView`; deprecates `AdwMessageDialog`/`AdwAboutWindow`/`AdwPreferencesWindow` (dialogs arrived in 1.5/GNOME 46) — libadwaita NEWS |
| 48 | 2025-03 ⚠️ | 1.7 | 4.18 ⚠️ | **Adwaita Sans / Adwaita Mono** default fonts (Inter / Iosevka-based); `AdwToggleGroup`, `AdwInlineViewSwitcher`, `AdwWrapBox`; `.dimmed` replaces `.dim-label` (NEWS 1.7) |
| 49 | 2025-09 | 1.8 | 4.20 | `AdwShortcutsDialog` + `AdwShortcutLabel` (replace deprecated `GtkShortcutsWindow`), `.document` style class, GTK CSS media queries for color-scheme/contrast; **X11 session disabled by default** — https://release.gnome.org/49/developers/ |
| 50 | 2026-03 | 1.9 | 4.22 | **`AdwSidebar` + `AdwViewSwitcherSidebar`** (replaces `GtkStackSidebar`), most widgets honour **reduced motion**, `style-dark.css`/`style-hc*.css` deprecated → use `style.css` + media queries; native in-process SVG renderer (GtkSvg); X11 backend removed from Mutter/Shell (Xwayland stays) — https://release.gnome.org/50/developers/ |
| 51 "A Coruña" | 2026-09-16 | 1.10 | 4.23/4.24 ⚠️ | `AdwCssClassBinding`, `:prefix`/`:suffix` on sidebars, `AdwEnumListModel` deprecated → `GtkEnumList`; `GtkSvgWidget`; GtkSpinner/GtkStack/GtkRevealer honour reduced motion; pixel snapping at fractional scale; SVG cursors — https://release.gnome.org/51/developers/ , https://release.gnome.org/51/ |

Rules for agents:
- Target **libadwaita ≥ 1.8** (GNOME 49 runtime) as a floor in 2026; 1.9+ if you want `AdwSidebar`. Check runtime: Flathub `org.gnome.Platform//49|50|51`.
- Don't use deprecated: `GtkShortcutsWindow`, `GtkStackSidebar`, `AdwLeaflet`/`AdwFlap`/`AdwSqueezer`/`AdwViewSwitcherTitle` (deprecated 1.4), `AdwMessageDialog`/`AdwPreferencesWindow`/`AdwAboutWindow` (use the `*Dialog` versions, 1.5+), `.dim-label` (→ `.dimmed`), `.large-title` (→ `.title-1`), flat header bar class (→ `AdwToolbarView`), `.opaque` (deprecated 1.6) — https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/style-classes.html#deprecated-style-classes
- The HIG typography page still lists `large-title`; libadwaita docs say it's deprecated since 1.2 — trust libadwaita.

## 2. GNOME structure & libadwaita widgets

Docs base below = `https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/` (abbrev. **LA/**). HIG base = `https://developer.gnome.org/hig/` (**HIG/**).

**Window skeleton** (always): `AdwApplicationWindow` → `AdwToolbarView` (top: `AdwHeaderBar`, bottom: optional bars) → content. `AdwToolbarView` manages flat/raised bar styles and scroll undershoot shadows; don't hand-roll them (LA/style-classes.html#undershoot-indicators). `AdwDialog` requires the parent to be `AdwWindow`/`AdwApplicationWindow` (LA/adaptive-layouts.html#dialogs).

**Header bar** (HIG/patterns/containers/header-bars.html, LA/class.HeaderBar.html)
- Three alignment points: **start** = main actions (New/Add/Open/Back), **center** = title (or `AdwViewSwitcher`/`AdwWindowTitle` with subtitle), **end** = menus. Few controls; always leave empty space to drag; every header-bar control needs a tooltip.
- Header bar content should change with the current view/mode.
- Buttons in header bars are auto-flat if icon-only, icon+label (`AdwButtonContent`), split buttons, menu buttons. Avoid text-only, `.suggested-action`, `.destructive-action`, `.linked` in a *primary window* header bar; group with `GtkSeparator.spacer` instead of `.linked`. (Action dialogs may keep text buttons.)
- Window controls follow the system layout automatically; in `AdwDialog` only a close button is shown (same side as system close). In split views, title buttons hide except at window edges. Back button appears automatically with `AdwNavigationView`/`AdwNavigationSplitView`.
- **Primary menu** (HIG/patterns/controls/menus.html): `GtkMenuButton` with `icon-name=open-menu-symbolic`, `primary=True` (gets F10), tooltip/accessible label **"Main Menu"**; at header-bar end, or above the sidebar if there is one; only on top-level page with hierarchical nav. Last section items: *Preferences*, *Keyboard Shortcuts*, *Help*, *About <AppName>* (About is mandatory). **No Close/Quit items.** Secondary menus = per-view actions, `view-more-symbolic` ⚠️ (icon name not stated in HIG).

**Adaptive layouts** (HIG/guidelines/adaptive.html, LA/adaptive-layouts.html)
- Must work at **1024×600**; phone-capable apps down to **360×294** px. Design narrowest first. Constrain wide content with `AdwClamp` (lists/text never stretch edge-to-edge).
- `AdwBreakpoint` on the window: `<condition>max-width: 550sp</condition>` + `<setter object=… property=…>`. When using breakpoints the window has no min size → **set `width-request`/`height-request`** yourself (e.g. 360×294).
- Doc thresholds: view switcher → bottom bar at `max-width: 550sp`; sidebar collapse at `400sp`; triple-pane at `860sp`/`500sp`. Use `sp` units so thresholds scale with text size.
- `AdwNavigationSplitView` (sidebar + content, both `AdwNavigationPage`); collapses into `AdwNavigationView` (sidebar = root page). Use for HIG "sidebar" navigation.
- `AdwOverlaySplitView` — sidebar overlays content when collapsed (utility panes, F9 toggle).
- `AdwNavigationView` — push/pop pages (`AdwNavigationPage` with `title` + `tag`); back button + Alt+← + swipe come free.
- `AdwViewStack` + `AdwViewSwitcher` (header, `policy=wide`) ↔ `AdwViewSwitcherBar` (bottom, `reveal` via breakpoint). HIG: **3–5 views**, noun labels in header caps, similar lengths; more views → sidebar (HIG/patterns/nav/view-switchers.html).
- **New 1.9 (GNOME 50):** `AdwSidebar` (sections, items, tooltips, context menus, drop target) and `AdwViewSwitcherSidebar` (sidebar for `AdwViewStack`, replaces `GtkStackSidebar`). Switch `mode` to `page` (boxed-list page) in the same breakpoint that collapses the split view. 1.10 adds `:prefix`/`:suffix` (LA/class.Sidebar.html, https://release.gnome.org/50/developers/).
- Others: `AdwMultiLayoutView` (different layouts per breakpoint), `AdwBottomSheet`, `AdwWrapBox` (word-wrapping row of chips, `child-spacing`/`line-spacing` 6), `AdwToggleGroup` / `AdwInlineViewSwitcher` (segmented control, 1.7), `AdwTabView`/`AdwTabBar`/`AdwTabOverview`.

**Boxed lists** (HIG/patterns/containers/boxed-lists.html, LA/boxed-lists.html): `GtkListBox` + `.boxed-list` (or `.boxed-list-separate`), `selection-mode=none`. Rows: `AdwActionRow`, `AdwSwitchRow`, `AdwComboRow`, `AdwEntryRow`, `AdwPasswordEntryRow`, `AdwSpinRow`, `AdwExpanderRow`, `AdwButtonRow`, property rows (`AdwActionRow.property`). Max **1 control per row (never >2)**; clicking the row triggers the control; row links to another view → trailing `go-next-symbolic`. Row icons symbolic. For big/dynamic data use `GtkListView`/`GtkColumnView`. Reorderable lists: drag handle at start + menu with *Move Up/Move Down/Remove* (accessibility).

**Preferences** — `AdwPreferencesDialog` → `AdwPreferencesPage` (icon+title → becomes view switcher when >1 page) → `AdwPreferencesGroup` (title, description, `header-suffix`) → rows. Built-in search (`search-enabled`). Page layout = 24px top/bottom, 12px sides, 24px between groups (stylesheet `_preferences.scss`). Apply changes instantly, no OK/Apply buttons ⚠️ (universal GNOME practice; not stated in current HIG text). `AdwPreferencesWindow` deprecated 1.6. View-switched preference pages must not affect each other (HIG/patterns/nav/view-switchers.html).

**Dialogs** (HIG/patterns/feedback/dialogs.html, LA/class.AlertDialog.html)
- Prefer **undo toast over confirmation**; confirm only when undo is impossible. Avoid error dialogs; use toasts for non-critical errors. Never pop dialogs unprompted; always modal to a parent.
- **Button order: Cancel first (left in LTR), affirmative last (right).** Return → affirmative *unless* destructive/irreversible (then no default or default=cancel). Esc → cancel. Single-button alert: Esc and Return same button.
- `AdwAlertDialog`: heading (header caps or informal sentence), body, 1–3 responses, each with id + mnemonic label (`_Replace`); `set_response_appearance(id, ADW_RESPONSE_SUGGESTED|DESTRUCTIVE)`; `default-response`, `close-response`; `choose()` async API. Buttons stack vertically at medium widths unless `prefer-wide-layout`. Labels = specific verbs (*Replace*, *Discard*, *Save*), never OK/Yes/No.
- Action dialogs: `AdwDialog` with its own header bar, heading describing the action, Cancel + verb button; affirmative insensitive until valid. `AdwDialog` floats on wide windows, becomes a **bottom sheet** on narrow ones.

**Feedback**
- **Toast** (HIG/patterns/feedback/toasts.html, LA/class.Toast.html): wrap content in `AdwToastOverlay`; `adw_toast_overlay_add_toast()`. Short title in *informal sentence* style ("File deleted"), optional single button (typically **Undo**). Default `timeout` **5 s** (0 = sticky); won't hide while hovered/focused. `priority` normal = queue, high = replace. Events only — not ongoing states.
- **Banner** `AdwBanner` (HIG/patterns/feedback/banners.html): top strip for *persistent states* ("Working offline", "Metered network ‒ automatic updates paused", "Unlock to change settings"); title + optional button; set `revealed`.
- **Placeholder/empty state** `AdwStatusPage` (HIG/patterns/feedback/placeholders.html): icon/illustration + heading + optional description + optional `.pill .suggested-action` button. Initial-run empty state may be colourful and address the user; otherwise symbolic icon, neutral tone ("Empty Folder", "No Results Found"). Use `.compact` for small spaces.
- **Notifications** (HIG/patterns/feedback/notifications.html): only for events relevant when the app isn't focused; title header-caps, body sentence-caps; ≤3 action buttons, none duplicating default action; withdraw stale ones; summarise floods; window must also show everything. Use `GNotification`/`g_application_send_notification` (portal-friendly).
- Spinners: `AdwSpinner` (1.6+); progress: `GtkProgressBar` (`.osd` when overlaid).

**About** `AdwAboutDialog` (1.5+; `AdwAboutWindow` deprecated): build from metainfo with `adw_about_dialog_new_from_appdata("/com/example/App/metainfo.xml", "1.2.0")` (sets icon from `<id>`, name, developer, version, website, release notes) — 1.9 also adds `appdata-resource-path` property. Add credits, legal sections, `issue-url`, `support-url`; 1.10 adds `other-apps-title`.

## 3. GNOME visuals — type, style classes, accent, dark, spacing, icons, writing

**Fonts** (HIG/guidelines/typography.html, LA/css-variables.html#fonts): UI default is **Adwaita Sans** (custom Inter variant, GNOME 48+); monospace **Adwaita Mono** (Iosevka-based ⚠️ lineage from GNOME 48 notes, not re-fetched). `--document-font-*` default Adwaita Sans 12pt, `--monospace-font-*` Adwaita Mono 11pt. **Never hard-code font family/size**; use style classes or relative sizes. No italics for emphasis, no ALL CAPS, don't put text over textures/images.
**Type classes** (LA/style-classes.html#typography): `.title-1`…`.title-4` (display headings, only with lots of whitespace — e.g. status pages, welcome), `.heading` (window titles, group labels), `.body` (wrapping UI text, extra line height), `.document` (1.8+; main reading content like chat messages/articles), `.caption`, `.caption-heading` (sub-text), `.monospace` (code/logs), `.numeric` (tabular figures for timers, progress, aligned numbers). Minimise distinct sizes/weights per view.
**Colour/state classes**: `.accent`, `.success`, `.warning`, `.error` (also on `GtkEntry` for validation), `.dimmed` (1.7+, replaces `.dim-label`; opacity 55% regular / 90% HC via `--dim-opacity`).
**Buttons**: `.suggested-action` (accent; affirmative in action dialog; **max one suggested *or* destructive button per view**, HIG/patterns/controls/buttons.html), `.destructive-action`, `.flat`, `.raised` (inside toolbars), `.circular` (icon or 1–2 chars), `.pill` (standalone important button, e.g. in status page). Outside header bars a button has icon **or** label, not both; keep ≤2 button widths per window; make invalid buttons insensitive instead of erroring; no double-click/right-click actions on buttons.
**Containers**: `.boxed-list`, `.boxed-list-separate`, `.card` (+`.activatable` for hover; buttons get it free), `.navigation-sidebar` (on list/grid views), `.toolbar` (6px spacing, flattens buttons), `GtkSeparator.spacer`, `.osd` (overlays on media), `.inline` (search/tab bar not attached to header), `.property` rows, `.devel` window class for nightly builds (striped header), `.icon-dropshadow` (app icons >32px) / `.lowres-icon` (≤32px).
**Accent colours** (GNOME 47 / libadwaita 1.6+; LA/styles-and-appearance.html#accent-color): apps follow the system accent automatically. One of 9: blue `#3584e4`, teal `#2190a4`, green `#3a944a`, yellow `#c88800`, orange `#ed5b00`, red `#e62d42`, pink `#d56199`, purple `#9141ac`, slate `#6f8396` (bg values; fg always white). Rules: never hard-code blue — use `var(--accent-bg-color)`/`--accent-fg-color`/`--accent-color` (standalone, for text on neutral bg) or `StyleManager:accent-color-rgba`; avoid accent on large surfaces or many items per view (LA/css-variables.html#accent-colors). Brand override: `:root { --accent-bg-color: var(--accent-green); }`; if bright (e.g. `var(--yellow-3)`) also set `--accent-fg-color: rgb(0 0 0 / 80%)`.
**Dark style** (LA/styles-and-appearance.html, HIG/guidelines/ui-styling.html): default `ADW_COLOR_SCHEME_PREFER_LIGHT` = follow system. Media/photo/video apps may default to `PREFER_DARK`. Per-app switch only for long-use apps (editors) and must offer **System / Light / Dark** → `PREFER_LIGHT` / `FORCE_LIGHT` / `FORCE_DARK`; hide "System" if `system-supports-color-schemes` is false. Custom CSS: one `style.css` with `@media (prefers-color-scheme: dark)` and `@media (prefers-contrast: more)` — `style-dark.css`/`style-hc*.css` **deprecated in 1.9** (LA/class.Application.html). Use CSS variables (`--window-bg-color`, `--view-bg-color`, `--card-bg-color`, `--headerbar-bg-color`, `--border-color` = `color-mix(in srgb, currentColor 15%, transparent)`) instead of hex. Reduced motion: `@media (prefers-reduced-motion: reduce)` (1.9+).
**Radii** (Adwaita SCSS `_common.scss`, main branch): button **9px**, menu 9px, card/boxed list **12px**, popover 15px, dialog 15px, window **15px** (`--window-radius`; 0 when maximized/tiled), alert dialog 18px, checkbox 6px. Nested radius = outer radius − padding (dialog 15 = button 9 + 6).
**Spacing**: no formal grid in HIG; libadwaita uses multiples of **6px**: 6 (toolbar/header spacing, wrap-box, group-title gap), 12 (side margins, row padding, list-header gap), 18 (list section header top padding), 24 (page top/bottom margins, gap between groups). Canonical clamp page: `margin-top/bottom 24`, `margin-start/end 12`, `spacing 24` (LA/adaptive-layouts.html#clamp). Header bar min-height 47px (`_header-bar.scss`).
**UI icons** (HIG/guidelines/ui-icons.html): symbolic, monochrome, drawn at **16×16** (usable at 32/64/128 only), 2px strokes, no perspective, recoloured by theme; name ends `-symbolic`. Reuse icons from GTK/Icon Development Kit via the *Icon Library* app; make new ones with *Symbolic Preview*. Icon **or** label, not both (except sidebars/view switchers). Only use universally recognised icons (search, menu, back/forward, share); otherwise use text. Since libadwaita 1.9 internal icons are bundled; ship custom symbolics in GResource `…/icons/scalable/actions/`.
**App icon** (HIG/guidelines/app-icons.html): unique (never reuse stock), one simple metaphor tied to the name, no mascots/logos. Drawn on **128×128** canvas (viewed at 64, down to 32) using the template's guides and baseline; 2px grid; simple geometric, not flat — top + darker "front" profile ≤ 4px; flat colours on flat surfaces, gradients only on curves; no outer shadows (system adds). Use the GNOME palette (HIG/reference/palette.html). Also ship a **symbolic** variant (`<id>-symbolic.svg`) and a **nightly** variant for dev builds. Tools: *App Icon Preview*.
**App name** (HIG/guidelines/app-naming.html): 1–2 simple nouns, **<15 chars**, header caps ("Icon Preview"), domain-related; no "G" prefix, no trademarks, no puns, no made-up words.
**Writing** (HIG/guidelines/writing-style.html)
- **Header Capitalization** for headings, header-bar titles, tabs, buttons, switch labels, menu items, tooltips: capitalise words ≥4 letters, all verbs and nouns, first & last word, hyphenated parts → "Find and Replace", "Document Cannot Be Found".
- **Sentence capitalization** for checkbox/radio/slider/entry/field labels, combobox labels, body text in dialogs and notifications.
- Headings drop articles/auxiliaries: "Three Documents Updated". Informal heading = full sentence, sentence caps, still bold ("File has changed on disk") — use for toasts and banners.
- **Ellipsis "…" (U+2026)** only when more input is needed before the action runs: *Save As…*, *Find…*, *Delete…*; NOT on *Preferences*/*Properties*.
- **No trailing periods** on labels/headings/descriptions, even full sentences (only for multi-sentence text).
- Neutral tone; avoid "you"/"my" (prefer "Your Records"); no "e.g./i.e."; no sentences split across controls; use domain terms, not system terms.
- Typography: “curly quotes”, ’ apostrophe, × for dimensions, – en dash for ranges, U+202F narrow no-break space before units ("32 GB").

## 4. GNOME keyboard

Standard shortcuts (HIG/reference/keyboard.html) — implement every one your app has a matching action for:
| Action | Keys | Action | Keys |
|---|---|---|---|
| Close tab/window | Ctrl+W | Quit app | Ctrl+Q |
| Help | F1 | Toggle side/utility pane | F9 |
| Open primary/secondary menu | F10 | Keyboard shortcuts dialog | **Ctrl+?** |
| Preferences | **Ctrl+,** | New / Open / Save | Ctrl+N / Ctrl+O / Ctrl+S |
| Save As | Shift+Ctrl+S | Print / Preview | Ctrl+P / Shift+Ctrl+P |
| Send/share | Ctrl+M | Properties | Alt+Return |
| Undo / Redo | Ctrl+Z / **Shift+Ctrl+Z** | Paste special | Shift+Ctrl+V |
| Duplicate | Ctrl+U ⚠️ (HIG lists Ctrl+U for both Duplicate and Underline) | Select all / none | Ctrl+A / Shift+Ctrl+A |
| Find / next / prev | Ctrl+F / Ctrl+G / Shift+Ctrl+G | Replace | Ctrl+H |
| Zoom in / out / reset | Ctrl++ / Ctrl+- / Ctrl+0 | Reload | Ctrl+R |
| Back / Forward / Up / Home | Alt+← / Alt+→ / Alt+↑ / Alt+Home | Location | Ctrl+L |
| Bookmark / edit bookmarks | Ctrl+D / Ctrl+Alt+D | First/last page | Ctrl+Home / Ctrl+End |

- Never use **Super** (system-reserved) or bare **Alt+letter** (access keys). Avoid Alt+Tab, Alt+F4–F8, Alt+Space, Ctrl+Alt+Tab, Ctrl+Alt+Del (HIG/guidelines/keyboard.html).
- Custom shortcuts: Ctrl+letter, mnemonic (Ctrl+E = edit); Shift+Ctrl+letter = reverse/extend; one-hand reach for common actions; don't bind everything.
- Access keys (mnemonics): underline in labels (`_Save`) for all labelled controls; prefer first letter, avoid thin letters (i, l) and descenders (g, y); consonants before vowels.
- Navigation keys must work in custom widgets: Tab/Shift+Tab, Ctrl+Tab (when Tab is consumed), Return activate, Space toggle, F10 menu, Menu/Shift+F10 context menu, Esc closes transient containers (menus, popovers, dialogs). Modal windows close on Esc; all windows on Ctrl+W. Focus order = widget tree order; labels precede their control. Give dialogs sensible initial focus.
- **Shortcuts dialog**: `AdwShortcutsDialog` (1.8+, adaptive, searchable) replaces `GtkShortcutsWindow`. Put it in GResource as `shortcuts-dialog.ui` with id `shortcuts_dialog` → `AdwApplication` auto-creates `app.shortcuts` + **Ctrl+?** (Meta+? on macOS) (LA/class.Application.html). Sections follow menu-bar conventions but "General" instead of "File". Show shortcuts elsewhere with `AdwShortcutLabel`.
- Register accels with `gtk_application_set_accels_for_action(app, "win.find", (const char*[]){"<Control>f", NULL})`; Ctrl+, → `app.preferences`; Ctrl+Q → `app.quit`; Ctrl+W → `window.close` (built-in GtkWindow action).

## 5. GNOME motion & accessibility

**Motion** (LA/class.Animation.html, LA/class.SpringAnimation.html)
- `AdwTimedAnimation` (duration ms + `AdwEasing`, e.g. `ADW_EASE_OUT_CUBIC`; repeat/reverse/alternate) and `AdwSpringAnimation` (physics; `adw_spring_params_new(damping_ratio, mass, stiffness)`; no fixed duration, `estimated-duration`; `initial-velocity` for gesture hand-off; `clamp=TRUE` stops overshoot). Target via `adw_property_animation_target_new(widget, "opacity")` or `AdwCallbackAnimationTarget`.
- Animations auto-skip when the widget is unmapped or `GtkSettings:gtk-enable-animations` is FALSE. Since 1.9 stock widgets (`AdwNavigationView`, `AdwDialog`, `AdwBottomSheet`, `AdwTabOverview`) swap slides for **crossfades** under reduced motion; GTK 4.23+ makes `GtkStack`/`GtkRevealer`/`GtkSpinner` comply too (https://release.gnome.org/51/developers/). For your own motion: `@media (prefers-reduced-motion: reduce)` in CSS, or read `GtkSettings:gtk-interface-reduced-motion` ⚠️ (GTK version that added it not confirmed) and use a fade or no animation.
- Use motion to explain spatial change only (page push/pop, reveal); resizing must be smooth, widgets must not jump/disappear without animation (HIG/guidelines/adaptive.html). No flashing/blinking (seizure risk; HIG/guidelines/ui-styling.html).

**Accessibility** (HIG/guidelines/accessibility.html, https://docs.gtk.org/gtk4/section-accessibility.html)
- Test matrix before shipping: **High Contrast** (Settings or GTK Inspector), **Large Text**, keyboard-only, **Orca** screen reader ("can you turn the display off and still use the app?"), on-screen keyboard.
- High contrast can't be disabled by apps; support it by using `.dimmed`, `--border-color`, `--dim-opacity` and other helper variables instead of hard-coded opacities/colours; `@media (prefers-contrast: more)` for extras.
- Never convey info by colour alone (add shape/text/position).
- Every control needs a short accessible name. Icon-only buttons: set `tooltip-text` *and* accessible label: `gtk_accessible_update_property(GTK_ACCESSIBLE(btn), GTK_ACCESSIBLE_PROPERTY_LABEL, _("Add Item"), -1)`; in UI files `<accessibility><property name="label" translatable="yes">Add Item</property></accessibility>`. Entries: `GTK_ACCESSIBLE_RELATION_LABELLED_BY` / `DESCRIBED_BY`. Non-standard keys → `GTK_ACCESSIBLE_PROPERTY_HELP_TEXT`.
- Custom widgets: `gtk_widget_class_set_accessible_role(klass, GTK_ACCESSIBLE_ROLE_BUTTON)` (role is fixed per instance), keep `STATE_DISABLED/HIDDEN/CHECKED` in sync, decorative → `GTK_ACCESSIBLE_ROLE_PRESENTATION`, value controls implement `GtkAccessibleRange` (4.10+), tabs use `TAB_LIST`/`TAB` + `RELATION_CONTROLS`. Containers: `GROUP` (semantic) vs `GENERIC` (layout only).
- GTK talks AT-SPI on Linux; inspect with GTK Inspector (Ctrl+Shift+D / `GTK_DEBUG=interactive`) → Accessibility tab.
- GNOME 51 added a setting to disable the focus-ring timeout — never hide focus rings yourself (https://release.gnome.org/51/).

## 6. KDE HIG, Kirigami, Breeze, Plasma 6

KDE HIG (rewritten, short): https://develop.kde.org/hig/ (repo active 2026-11-01). Abbrev **KHIG/**.

**Philosophy** (KHIG/kde_app_design): **"Simple by default, powerful when needed."** Make the 80% workflow obvious for casual users; customization serves diverse workflows (aesthetics secondary); apps may grow powerful features. New apps: **QtQuick + Kirigami** (QtWidgets for complex legacy-style desktop apps).
- Simple by default (KHIG/simple_by_default): show something actionable at first launch (`Kirigami.PlaceholderMessage` with icon, text, `helpfulAction`); wizards only for mandatory setup or optional tutorials; preselect the likely choice, skip choices with one option; rename inline; keep primary functions **visible** (not hover-only, shortcut-only or gesture-only); progress indicator for anything >1 s (`BusyIndicator` indeterminate, `Kirigami.LoadingPlaceholder` determinate); default window big enough to avoid elision; **don't keep running in the tray when closed**; move files to trash, offer undo for removals (`showPassiveNotification` or `Kirigami.InlineMessage`); remember window size (and position on X11).
- Powerful when needed (KHIG/powerful_when_needed): settings must switch between valid workflows, not toggle features on/off; never an **"Advanced"** page — use progressive disclosure (sub-page/expander); settings via `Kirigami.FormLayout`; **apply settings immediately, no relaunch**; shortcuts for every action or user-assignable (use `KStandardShortcut`); only **two-finger** gestures; **never Meta** for app shortcuts.

**Layout & spacing** (KHIG/layout_and_nav) — always `Kirigami.Units`, never literal px. Default values (`kirigami/src/platform/units.cpp`): `gridUnit` 18, `smallSpacing` 4, `mediumSpacing` 6, `largeSpacing` 8, `cornerRadius` 5; durations `veryShortDuration` 50 / `shortDuration` 100 / `longDuration` 200 / `veryLongDuration` 400 ms; `toolTipDelay` 700; `humanMoment` 2000. Icon sizes `small` 16, `smallMedium` 22, `medium` 32, `large` 48, `huge` 64, `enormous` 128. (Platform theme can rescale gridUnit from font metrics.)
| Use | Value |
|---|---|
| title ↔ subtitle | 0 |
| title group ↔ content; related items | `smallSpacing` |
| between groups | `largeSpacing` |
| toolbar items | `mediumSpacing` |
| window edge ↔ frameless views | 0; ↔ other UI `largeSpacing` |
| fixed sizes, default/min window size | multiples of `gridUnit` |
| icons: menu items & raised buttons / flat toolbar buttons & 1-line list items / 2-line list items | `small` / `smallMedium` / `medium` |
- Responsive mapping: toolbar top (desktop) → bottom (mobile); sidebar leading → on-demand/first page; menubar → hamburger; tab bar → bottom; status bar → omitted. Phones need a real mobile UI. `Kirigami.Settings.tabletMode`, `Kirigami.Settings.isMobile`; test with `QT_QUICK_CONTROLS_MOBILE=1`.
- Shortcuts with modifier+alphanumeric, never a bare F-key only (laptops). Pixel-by-pixel touchpad scrolling.
- Navigation: linear → `pageStack` (`Kirigami.PageRow`) with breadcrumbs/back; ≤5 destinations → `Kirigami.NavigationTabBar`; more → `Kirigami.GlobalDrawer` (`modal: false` = persistent sidebar on desktop). Contextual actions → `Page.actions` (shown in toolbar via `ActionToolBar`, overflow menu automatic) and `Kirigami.ContextDrawer` on mobile.
- Menus: small apps none; medium apps **hamburger** (`application-menu` icon, static, ≤ ~15 items, disable don't hide, no Quit/Minimize); large apps a real menubar between titlebar and toolbar (`KHamburgerMenu` for QtWidgets gives both).
- RTL: test `LANGUAGE=ar_AR app`; use `-rtl` icons; don't mirror images.

**Input & dialogs** (KHIG/getting_input): `ToolButton` in toolbars, `RoundButton` floating over content (icon only), `Button` elsewhere. **Switch = instant apply, CheckBox otherwise**; avoid checkable buttons. ≤3 short options → radio; ≤10 → ComboBox; >10 → list. Slider for speed, SpinBox for precision. Validate text input with `Kirigami.InlineMessage` + disable confirm. Dialogs only for an immediate required decision or blocking progress; `Kirigami.PromptDialog` (yes/no or text prompt), `Kirigami.MenuDialog` (choose action); **never >1 dialog at a time, never dialogs spawning dialogs**; file pickers = `QtQuick.Dialogs.FileDialog` (portal-backed), never custom. Overlays need a contrasting outline (dark schemes). Underlined links only for URLs; pointing-hand cursor only on links.
- **Button order: use `QDialogButtonBox`/`standardButtons` roles, never hand-place.** Qt's `KdeLayout`: Help, Reset, ⟷, Yes, No, Action, **OK/Accept**, Alternate, Apply, Destructive, **Cancel/Reject** (affirmative left of Cancel); `GnomeLayout`: …, Destructive, Alternate, **Cancel**, **OK** (Cancel left) — chosen from the running platform theme (https://github.com/qt/qtbase/blob/dev/src/gui/kernel/qplatformdialoghelper.cpp).

**Content** (KHIG/displaying_content): lists for text, grids for visual; standard delegates; add-actions on `Kirigami.InlineViewHeader`; remove buttons visible inline (not hover); bold for active item; push a Page for full-size content, `Kirigami.OverlaySheet` only for read-only scrollable aux content, `Kirigami.Dialog` for input. Tabs: mutable (`TabBar`, reorderable, closable, full width) vs immutable (`NavigationTabBar`); hide tab bar with one tab; >4–5 tabs → sidebar. Tables only for ≥3 comparable columns; avoid tree views. Important help inline under the control; long help → `Kirigami.ContextualHelpButton`; nothing important only in hover tooltips.

**Status** (KHIG/status_changes): show success by changing the UI, not a "Done" message. **Every error must be actionable** (none > fix-it action > what happened + how to proceed; never only a description, jargon, or silent failure); blame third parties explicitly. Colours via `Kirigami.Theme`: `highlightColor` (blue, selection/benign), `neutralTextColor`/`neutralBackgroundColor` (orange, warnings/non-default), `negativeTextColor`/`negativeBackgroundColor` (red, errors/danger); never colour alone. No system notifications while your window is focused → passive notification or `InlineMessage` (page header position). Use `KNotification` urgency Low/Normal/Critical; never advertise features via notifications. Progress/unread counts: Task Manager badge `QGuiApplication::setBadgeNumber()` / `com.canonical.Unity.LauncherEntry`. **Tray icon = last resort: opt-in, only visible when there's abnormal status and no window.**

**Writing** (KHIG/text_and_labels): **Title Case** for buttons/menus/headings/window titles; **sentence case** for sentences, subtitles, tooltips, placeholders, checkbox/radio/combo labels, `FormData.label`. Imperative verbs ("Show Info", not "Info"; "Apply", not "Yes"); positive phrasing; avoid "you" ("Permanently delete all items from the Trash?"); nothing longer than "Configure Keyboard Shortcuts" in a control; ≤85 chars per line (~450px); no acronyms (URL → Link, RAM → Memory); "…" only when more input is required; window title = content ("Inbox — konqi@kde.org"), no vendor/version/paths; dialog titles echo the triggering verb ("Save File"); "Delete" means removing from disk; serial comma; leave 50% room for translation; `i18nc()`/`i18ncp()`. Use `Kirigami.Heading`/`Controls.Label`, never raw `QtQuick.Text` (ignores system font). Icon-only buttons still set `text` + `display: AbstractButton.IconOnly` + `ToolTip`. App name: single catchy word, not a generic word ("Files"), no forced "K".
**Icons** (KHIG/icons): follow freedesktop icon naming; look perfect in **Breeze**. Unlike GNOME, **put an icon on every button and menu item** (no duplicates in one view). Icon-only only when space-critical and the glyph is universal. Destructive: red `edit-delete` (destroy) / `edit-delete-remove` (removable); `trash-empty` (black) for Move to Trash. Monochrome icons 16px (menus, raised buttons) and 22px (ToolButtons), pixel-aligned, emblem bottom-right ≥5px; colourful icons 32/48/64 with depth; **app icons colourful, 48px baseline**.
**Accessibility** (KHIG/accessibility): keyboard-only pass; font size 14 test; switch colour scheme; Orca reads "Label, Type"; animations off → instant transitions/static spinners; inclusive, neutral words (Kill→Close, Abort→Exit, Execute→Run).
**KDE standard shortcuts** (KStandardShortcut, `kconfig/src/gui/kstandardshortcut.cpp`): Configure App **Ctrl+Shift+,** (differs from GNOME's Ctrl+,), Configure Shortcuts Ctrl+Alt+,, Show Menubar Ctrl+M, Full Screen Ctrl+Shift+F, Open Main Menu F10, Find Next F3, Rename F2, Move to Trash Del, Delete Shift+Del. Use `KStandardActions` for standard text/icons/shortcuts.

**Plasma state (2026)**: Plasma **6.8** released **2026-10-14** — X11 *session* retired (apps still run via XWayland; KDE apps keep X11 support), **Union** theming engine in beta (CSS-driven, styles QtQuick *and* QtWidgets; opt-in "Breeze (Union)", not default) — https://kde.org/announcements/plasma/6/6.8.0/ . Breeze remains the default; style via `Kirigami.Theme` roles so you survive the switch. Plasma has user accent colours and light/dark colour schemes, exported to apps via the portal (§8).

## 7. elementary OS (distinctive points only)

Source: https://docs.elementary.io/hig (repo `elementary/hig`). Current: elementary OS **8.1** (Jan 2026; Wayland "Secure Session" default), 8.1.1 Feb 2026 ⚠️ (secondary sources); toolkit GTK 4 + **Granite 7**. Unwritten sections defer to the GNOME HIG.
- **Always saved**: no Save buttons for settings/info dialogs; changes apply instantly; closing + reopening must restore everything (documents, scroll, undo history). **No minimize button** in the OS; never minimize-instead-of-close; finish background tasks after close, then quit (…/user-workflow/always-saved, …/closing).
- **No splash screens** ("if your app requires a splash screen, you're doing it wrong"); restore last state on launch; first-run config goes *inside* the main window as a Welcome screen (Granite 7 `Granite.Placeholder` ⚠️ class name not re-checked) (…/normal-launch, …/accessible-configuration).
- **Avoid configuration**: ask the OS (name, location) instead of the user; put options in context next to the affected objects; never ask users for uninformed engineering decisions.
- **Preference dialogs are transient but NOT modal**, so changes are visible live (…/widgets/container-widgets). Dialogs/alerts have no window title. Window title separator: " — " (em dash with spaces); no vendor/version.
- **Dialog buttons**: affirmative at the very **end**, **Cancel immediately before it**, alternative actions before Cancel, incidental (Help) at the **start**; only one suggested *or* destructive button; explicit verbs, never "OK". Use `Granite.MessageDialog`: primary text = sentence case, no period; secondary text = details + side effects (…/widgets/providing-feedback).
- **Tool buttons** icon-only, borderless, with sentence-case tooltips **including the shortcut** (`Granite.markup_accel_tooltip()`); text buttons title case; toast titles affirm the action ("Foo was deleted" + Undo).
- **Differences from GNOME**: AP-style title case; "Preferences…" *does* take an ellipsis (opens a window) — GNOME says no ellipsis. App icons: hand-design **6 sizes 16/24/32/48/64/128**, 1px outline 30% darker than the fill (…/reference/iconography).

## 8. Freedesktop / cross-desktop integration (any toolkit)

**IDs**: pick a reverse-DNS app ID (`com.example.Notes`) and use it *everywhere*: `.desktop` basename, icon name, metainfo id, D-Bus name, GApplication/`QGuiApplication::setDesktopFileName`, Wayland `xdg_toplevel.app_id`. On Wayland the shell matches window → `.desktop` **by app_id = desktop-file basename**; mismatch = generic icon, unpinnable dock entry.

**Desktop entry** (spec 1.5, https://specifications.freedesktop.org/desktop-entry/latest/recognized-keys.html) — `/usr/share/applications/com.example.Notes.desktop`:
```ini
[Desktop Entry]
Type=Application
Name=Notes
GenericName=Note Taker          # e.g. "Web Browser"
Comment=Write and organize notes
Icon=com.example.Notes           # theme name, not a path
Exec=notes %U
Categories=Office;Utility;       # menu-spec main + additional categories
Keywords=memo;jot;markdown;      # search terms, not repeating Name
StartupNotify=true
StartupWMClass=com.example.Notes # = X11 WM_CLASS; keep identical to app_id
DBusActivatable=true             # if GApplication/D-Bus activation; keep Exec too
SingleMainWindow=true            # only if you can't open a 2nd window
Actions=new-note;
[Desktop Action new-note]
Name=New Note
Exec=notes --new
```
Also: `MimeType=` for file associations, `PrefersNonDefaultGPU=true` for GPU-heavy apps, `NoDisplay=true` for helpers. Validate with `desktop-file-validate`.

**Icons** (icon theme spec, https://specifications.freedesktop.org/icon-theme/latest/): install `hicolor/scalable/apps/<id>.svg` (+ PNG ≥256 if no SVG) and `hicolor/symbolic/apps/<id>-symbolic.svg`; `hicolor` is the mandatory fallback theme; UI icons by freedesktop **icon-naming-spec** names (`document-open`, `edit-delete`) so themes (Adwaita, Breeze) can restyle them.

**AppStream metainfo** (`/usr/share/metainfo/<id>.metainfo.xml`; https://www.freedesktop.org/software/appstream/docs/ ⚠️ not re-fetched): `<id>`, `<name>`, `<summary>`, `<description>`, `<launchable type="desktop-id">`, `<developer id=…><name>`, `<url type="homepage|bugtracker|donation|vcs-browser">`, `<screenshots>` with `<caption>`, `<releases>` with `<description>`, `<content_rating type="oars-1.1">`, `<branding><color type="primary" scheme_preference="light|dark">`, `<requires>/<recommends>` `<display_length compare="ge">360</display_length>` + `<control>keyboard|pointing|touch</control>`. Feeds GNOME Software, Discover, Flathub *and* `AdwAboutDialog.new_from_appdata`. Validate: `appstreamcli validate --pedantic`.

**Settings portal** (`org.freedesktop.portal.Settings` v2; https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.Settings.html): namespace `org.freedesktop.appearance` keys — `color-scheme` (u: 0 no pref, **1 dark**, 2 light), `accent-color` ((ddd) sRGB 0–1; out-of-range = unset), `contrast` (u: 0 normal, 1 high), `reduced-motion` (u: 0, 1 reduce). Call `ReadOne` (v2) or `ReadAll(["org.freedesktop.appearance"])`, subscribe to `SettingChanged` to switch live. Works in and out of sandbox, on GNOME/KDE/others.
```sh
gdbus call --session -d org.freedesktop.portal.Desktop -o /org/freedesktop/portal/desktop \
  -m org.freedesktop.portal.Settings.ReadOne org.freedesktop.appearance color-scheme
```
- GNOME's backend also exposes gsettings namespaces incl. `org.gnome.desktop.interface` (fonts, `clock-format`) and **`org.gnome.desktop.wm.preferences`** (`button-layout`) to sandboxed apps (`xdg-desktop-portal-gnome/src/settings.c`).
- **File chooser**: always use the portal (`org.freedesktop.portal.FileChooser`): GTK 4 `GtkFileDialog`, Qt `QFileDialog`/QML `FileDialog` (with `xdg-desktop-portal` platform theme or in Flatpak), Electron `dialog.showOpenDialog` (portal used by Chromium when available ⚠️). Never ship a custom file browser; sandboxed apps only get access to what the user picks.
- Other portals worth using: OpenURI (open links/files), Notification, Background (autostart/run in background with user consent), Inhibit (prevent sleep), ScreenCast/Screenshot, Secret (keyring), GlobalShortcuts (KDE + GNOME 48+ ⚠️).

**Notifications**: GTK `GNotification` / KDE `KNotification` / portal `org.freedesktop.portal.Notification` (sandbox-safe) rather than raw `org.freedesktop.Notifications`. Default action must focus the relevant window; withdraw stale notifications (`g_application_withdraw_notification`).

**Tray / StatusNotifierItem**: GNOME ships **no tray** (needs the AppIndicator extension; Ubuntu enables it by default ⚠️). KDE supports SNI but HIG says opt-in, only show on abnormal status. Rule: **never make the tray the only way to reach a window or quit**; closing the last window should quit unless the user opted into background mode — then request the Background portal and show a notification/"running in background" status. Use badges (`com.canonical.Unity.LauncherEntry`, `QGuiApplication::setBadgeNumber`) and notifications instead.

**Window decorations on Wayland**: GNOME/Mutter does **not** implement `xdg-decoration` server-side decorations → every app must draw **client-side decorations** there; KDE/KWin offers SSD. GTK 4/libadwaita always CSD (header bar). Qt on GNOME uses the upstream **Adwaita decoration plugin** by default (reads portal for dark/light + button layout; force elsewhere with `QT_WAYLAND_DECORATION=adwaita`) — https://code.qt.io/cgit/qt/qtwayland.git/log/src/plugins/decorations/adwaita/main.cpp ⚠️ first Qt version not confirmed.
- **Respect the button layout**: GTK setting `gtk-decoration-layout` (string like `appmenu:close` — GNOME default per gsettings-desktop-schemas — or `close,minimize,maximize:` for left-side). Source on GNOME: gsettings `org.gnome.desktop.wm.preferences button-layout` (portal-readable). Left of `:` = start side, right = end side. If you draw your own title bar, parse this and place buttons accordingly; show only buttons listed (GNOME hides minimize/maximize by default). Double-click title = maximize, right-click = window menu (GTK/Qt do this; custom title bars call `xdg_toplevel.show_window_menu`), keep a drag area.
- **Fractional scaling**: protocol `wp_fractional_scale_v1` + `wp_viewporter`. GTK 4 handles it (GTK 4.23+ also snaps to device pixels — https://release.gnome.org/51/developers/); Qt 6 native Wayland handles it; Electron ≥38 runs native Wayland by default → crisp. Running under **XWayland at 125/150% = blurry text** (or tiny UI if the user enabled Xwayland native scaling). Test at 100%, 125%, 150%, 200%; use vector icons and logical px, never device px.
- Wayland realities: no global window positioning (don't restore x/y; restore **size** only), no global key grabs (use GlobalShortcuts portal), no screen scraping (Screenshot/ScreenCast portals). GNOME 50 and Plasma 6.8 removed/retired X11 sessions — test on Wayland first.

## 9. Flathub quality guidelines (current, https://docs.flathub.org/docs/for-app-authors/metainfo-guidelines/quality-guidelines)

Not required to publish, but needed for featuring (banner, App of the Day, trending; distros reuse the list).
- **Runtime not EOL**; verified developer.
- **Brand colours**: `<branding>` with a light and a dark `primary` colour; colourful (no white/black/near-grey), contrast with the icon (used as banner bg behind it), dark = darker/muted variant, not identical.
- **Icon**: SVG or PNG ≥ **256×256**, square; reasonable footprint (use Flathub icon grid; don't touch edges, don't be tiny); good contrast on light *and* dark (no single-colour glyphs, no dark edges); recognisable at small sizes but not a flat single-colour symbol; **no baked-in shadows/glows**; contemporary style (GNOME/KDE icon guidelines); custom-style game icons → embed in square/circle grid shape.
- **Name**: ideally ≤ **15** chars, must be < **20**; just the name ("Fractal", not "Fractal (Matrix Client)"); no all-caps/lowercase/CamelCase/punctuation unless an established brand.
- **Summary**: ideally **10–25** chars, max **35**; non-technical (no toolkit/language/"free and open source"); avoid "app/tool/client"; sentence case, no trailing period; don't repeat the name; no leading article — prefer an imperative verb ("View images and videos", "Write markdown in style").
- **Description**: substantially longer than summary (≈3–6 lines of ~70 chars; ≤10 for big apps); don't rephrase the summary; lists ≤ 10 items.
- **Screenshots**: ≥1 in English (3–6 typical, 6–10 for large apps, >10 too many); best one first; `xml:lang` tags; **just the app window with its shadow + rounded corners** (no wallpaper/desktop, no cropping, no marketing text); taken **on Linux**; **default settings** (window controls, font, accent, light style — dark only as an extra); not maximised; window **≤1000×700** logical (2000×1400 HiDPI); one-sentence caption, no period, not starting with a number; real, attractive content (no empty states); keep current.
- **Release notes** for every release, 2–3 user-facing sentences, never "bug fixes and performance improvements".
- **OARS age rating** reflecting content reachable without searching.

## 10. Electron / Qt / Flutter / Tauri on Linux — mistakes & fixes

| Mistake | Symptom | Fix |
|---|---|---|
| Running under XWayland | blurry text at 125/150%, wrong cursor size | Electron **≥38 defaults `--ozone-platform=auto`** (native Wayland in Wayland sessions; `ELECTRON_OZONE_PLATFORM_HINT` removed) — https://electronjs.org/docs/latest/breaking-changes ; older Electron: `--ozone-platform-hint=auto --enable-features=WaylandWindowDecorations`. Qt 6 / GTK native Wayland by default. Only force `x11` for debugging. |
| app_id ≠ `.desktop` name | generic "W"/Electron icon in dock, can't pin, duplicate dock entries | Electron: `"desktopName": "com.example.Notes.desktop"` in package.json (sets `xdg_toplevel.app_id`; falls back to binary name, e.g. "electron" on NixOS — see electron PR #51479). Qt: `QGuiApplication::setDesktopFileName("com.example.Notes")`. GTK: `application_id`. Flutter: `APPLICATION_ID` in `linux/CMakeLists.txt` (template `{{linuxIdentifier}}`, often left `com.example.*`). Tauri: `enableGTKAppId: true` (default false) — https://v2.tauri.app/reference/config/ . Always also set `StartupWMClass=` to the same string (X11/XWayland). |
| Ignoring system dark style/accent | white app on dark desktop, blue buttons on a pink-accent desktop | Read portal `org.freedesktop.appearance` `color-scheme`/`accent-color`/`contrast`/`reduced-motion` and listen to `SettingChanged` (§8). Electron: `nativeTheme` has historically derived dark mode from the GTK theme, and live portal changes may not propagate ⚠️ (electron#28838, #25925) → subscribe to the portal in the main process (D-Bus) and set `nativeTheme.themeSource`. Tauri: window `theme` config "only implemented on Windows and macOS" → portal yourself. Qt ≥6.5: `QStyleHints::colorScheme()` + `colorSchemeChanged` ⚠️ (portal-backed on Linux). Web UIs: honour `prefers-color-scheme`, `prefers-contrast`, `prefers-reduced-motion`. |
| Hard-coded fonts/sizes | Segoe/SF/Inter look alien; ignores Large Text | Use `font-family: system-ui` (fontconfig default → Adwaita Sans on GNOME 48+, Noto Sans on Plasma ⚠️), size in rem/relative; Qt `QFontDatabase::systemFont()` / QML `Kirigami.Theme.defaultFont`, Controls `Label` not `Text`; GNOME text-scaling is exposed as `org.gnome.desktop.interface text-scaling-factor` via the portal. Ship a font only for brand display text. |
| Custom title bar ignoring layout | close button on the wrong side, missing maximize, no window menu, no drag/double-click | Prefer native/CSD frame on Linux. If custom (Electron `frame:false`/`titleBarStyle:'hidden'`, Tauri `decorations:false` + `data-tauri-drag-region`, Flutter `bitsdojo`/custom): read `button-layout` (`org.gnome.desktop.wm.preferences` via portal on GNOME; `gtk-decoration-layout`), honour start/end sides + which buttons exist; double-click = maximize, right-click = window menu, keep drag space; draw rounded corners + shadow for floating windows (Tauri: `shadow` "Linux: Unsupported"). Qt on GNOME: default Adwaita decoration plugin already does this. |
| Tray-only app | invisible on GNOME (no tray without extension); "app won't quit" on KDE | Window is the primary surface; quit on last window close (Electron `app.on('window-all-closed', () => app.quit())`); background mode is opt-in + Background portal; tray only as an optional extra with a visible fallback (notification / reopen via launcher). KDE HIG: tray opt-in & only for abnormal status. |
| No `.desktop`/metainfo/icon | not in app grid/search, wrong name in Alt+Tab, no About data | Ship all three with the same app ID (§8); hicolor SVG + symbolic; `desktop-file-validate`, `appstreamcli validate`. |
| Custom file dialogs / direct `$HOME` access | broken in Flatpak/Snap; alien UI | Use FileChooser portal (GTK `GtkFileDialog`, Qt `QFileDialog` with portal platform theme, QML `FileDialog`, Electron `dialog.*`, Tauri `@tauri-apps/plugin-dialog` ⚠️ portal backend). |
| Restoring window x/y | ignored on Wayland, odd placement on X11 multi-monitor | Restore size + maximized state only. |
| Toolkit-default look | Material/Cupertino in a GNOME/KDE desktop | Flutter Linux runs on GTK 3 (template: 1280×720, header bar commented out — opt-in); use desktop density, system font, accent from portal; consider community Adwaita/Yaru widget packages ⚠️. Tauri = WebKitGTK (GTK 3); on NVIDIA+Wayland blank windows are commonly worked around with `WEBKIT_DISABLE_DMABUF_RENDERER=1` ⚠️. |
| Notifications that open nothing | notification click does nothing / spawns a 2nd instance | Default action focuses the existing window (single-instance via D-Bus/GApplication); in sandbox use the Notification portal. |
| Ctrl+, vs Ctrl+Shift+, | inconsistent prefs shortcut | GNOME HIG: Ctrl+, ; KDE KStandardShortcut: Ctrl+Shift+, . Pick per target DE or bind both. Ctrl+Q quit, Ctrl+W close, F10 main menu, F1 help on both. |

## 11. Code snippets

**libadwaita (Python/PyGObject, libadwaita ≥1.5 for `AdwAlertDialog`)** — header bar + primary menu, adaptive split view, empty state, undo toast:
```python
import sys, gi
gi.require_version("Gtk", "4.0"); gi.require_version("Adw", "1")
from gi.repository import Adw, Gio, Gtk

class Win(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Notes", default_width=900, default_height=600)
        self.set_size_request(360, 294)                      # required with breakpoints
        menu = Gio.Menu()
        menu.append("_Preferences", "app.preferences")
        menu.append("_Keyboard Shortcuts", "app.shortcuts")
        menu.append("_About Notes", "app.about")
        side_hb = Adw.HeaderBar()
        side_hb.pack_end(Gtk.MenuButton(icon_name="open-menu-symbolic", menu_model=menu,
                                        primary=True, tooltip_text="Main Menu"))  # F10
        side = Adw.ToolbarView(); side.add_top_bar(side_hb)
        side.set_content(Gtk.ScrolledWindow(child=Gtk.ListBox(css_classes=["navigation-sidebar"])))
        main_hb = Adw.HeaderBar()
        delete = Gtk.Button(icon_name="user-trash-symbolic", tooltip_text="Delete Note")
        delete.connect("clicked", self.on_delete); main_hb.pack_end(delete)
        self.toasts = Adw.ToastOverlay(child=Adw.StatusPage(
            icon_name="document-edit-symbolic", title="No Note Selected",
            description="Select a note or create a new one"))
        main = Adw.ToolbarView(); main.add_top_bar(main_hb); main.set_content(self.toasts)
        split = Adw.NavigationSplitView(
            sidebar=Adw.NavigationPage(title="Notes", tag="sidebar", child=side),
            content=Adw.NavigationPage(title="Note", tag="content", child=main))
        self.set_content(split)
        bp = Adw.Breakpoint.new(Adw.BreakpointCondition.parse("max-width: 400sp"))
        bp.add_setter(split, "collapsed", True)             # sidebar becomes root page
        self.add_breakpoint(bp)

    def on_delete(self, _btn):                               # undo > confirmation dialog
        self.toasts.add_toast(Adw.Toast(title="Note deleted", button_label="_Undo",
                                        action_name="win.undo-delete"))

app = Adw.Application(application_id="com.example.Notes")   # = .desktop basename
app.connect("activate", lambda a: Win(a).present())
app.set_accels_for_action("app.preferences", ["<Control>comma"])
app.set_accels_for_action("app.quit", ["<Control>q"])
sys.exit(app.run(sys.argv))
```
Confirmation when undo is impossible (Cancel left, destructive right, not default):
```python
d = Adw.AlertDialog(heading="Delete Notebook?", body="All 12 notes will be permanently deleted")
d.add_response("cancel", "_Cancel"); d.add_response("delete", "_Delete")
d.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
d.set_default_response("cancel"); d.set_close_response("cancel")
d.choose(parent_window, None, on_response)   # finish with d.choose_finish(result)
```
Custom CSS (`style.css` in GResource; one file for all modes):
```css
.note-chip { background: var(--accent-bg-color); color: var(--accent-fg-color); border-radius: 9px; }
@media (prefers-color-scheme: dark) { .note-paper { background: var(--card-bg-color); } }
@media (prefers-contrast: more) { .note-chip { outline: 1px solid var(--border-color); } }
@media (prefers-reduced-motion: reduce) { .note-chip { transition: none; } }
```

**Kirigami (QML, KF6)** — page with toolbar actions, hamburger global drawer, placeholder, undoable delete:
```qml
import QtQuick
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami

Kirigami.ApplicationWindow {
    id: root
    title: i18nc("@title:window", "Notes")
    minimumWidth: Kirigami.Units.gridUnit * 20
    width: Kirigami.Units.gridUnit * 45
    globalDrawer: Kirigami.GlobalDrawer {
        isMenu: true                                   // hamburger on desktop
        actions: [
            Kirigami.Action { text: i18nc("@action", "Configure Notes…"); icon.name: "configure"; shortcut: "Ctrl+Shift+," },
            Kirigami.Action { text: i18nc("@action", "About Notes"); icon.name: "help-about" }
        ]
    }
    pageStack.initialPage: Kirigami.ScrollablePage {
        title: i18nc("@title", "All Notes")
        actions: [
            Kirigami.Action { icon.name: "list-add"; text: i18nc("@action:button", "New Note"); shortcut: StandardKey.New; onTriggered: notes.append({ title: i18n("Untitled") }) },
            Kirigami.Action { icon.name: "edit-delete"; text: i18nc("@action:button", "Delete Note")
                enabled: list.currentIndex >= 0
                onTriggered: { const n = notes.get(list.currentIndex).title; const i = list.currentIndex; notes.remove(i)
                    root.showPassiveNotification(i18n("Note deleted"), "long", i18n("Undo"), () => notes.insert(i, { title: n })) } }
        ]
        ListView {
            id: list
            model: ListModel { id: notes }
            delegate: Controls.ItemDelegate { required property string title; required property int index
                width: ListView.view.width; text: title; onClicked: list.currentIndex = index }
            Kirigami.PlaceholderMessage {
                anchors.centerIn: parent
                width: parent.width - Kirigami.Units.gridUnit * 4
                visible: list.count === 0
                icon.name: "note"
                text: i18n("No notes yet")
                helpfulAction: Kirigami.Action { icon.name: "list-add"; text: i18n("New Note"); onTriggered: notes.append({ title: i18n("Untitled") }) }
            }
        }
    }
}
```
Settings page: `Kirigami.FormLayout { Controls.Switch { Kirigami.FormData.label: i18n("Spell checking:"); text: i18n("Check while typing") } }` — instant apply, no OK button.

## Unverified / open questions
- ⚠️ GNOME 47/48 release months and GTK version for GNOME 51 (page says "GTK 4.23"; stable numbering likely 4.24) — table rows 47/48 from memory + libadwaita NEWS, not release pages.
- ⚠️ Adwaita Mono being Iosevka-based (GNOME 48 notes not re-fetched; Adwaita Sans = Inter variant is confirmed by HIG).
- ⚠️ Secondary-menu icon `view-more-symbolic` and "settings apply instantly" for GNOME — common practice, not in current HIG text (KDE and elementary HIGs state instant apply explicitly).
- ⚠️ `GtkSettings:gtk-interface-reduced-motion` — exists (used by libadwaita source) but GTK version that introduced it not confirmed.
- ⚠️ Electron: whether current releases read the Settings portal for `nativeTheme` live changes (issues #28838/#25925); whether Chromium always uses the FileChooser portal; `titleBarOverlay` behaviour on Linux.
- ⚠️ Qt: first Qt version shipping the upstream Adwaita Wayland decoration plugin; `QStyleHints::colorScheme` portal backing on non-KDE desktops; `setColorScheme` (6.8?).
- ⚠️ Flutter Linux dark-mode source (GTK theme vs portal) and recommended Adwaita/Yaru packages; Tauri dialog plugin portal backend; `WEBKIT_DISABLE_DMABUF_RENDERER` still needed in 2026.
- ⚠️ GNOME tray: Ubuntu enabling AppIndicator extension by default (true historically, not re-checked for 26.04/26.10).
- ⚠️ GlobalShortcuts portal availability on GNOME (believed 48+).
- ⚠️ Plasma default UI font (Noto Sans) and whether `xdg-desktop-portal-kde` exports the KDE accent via `accent-color` (expected, not re-checked).
- ⚠️ elementary OS 8.1/8.1.1 dates from secondary sources; elementary HIG repo itself last pushed 2026-09-30.
- ⚠️ AppStream element list summarised from memory of the spec (not re-fetched); Flathub guidelines and desktop-entry keys were fetched live.
- Open: KDE HIG no longer documents dialog button order explicitly — Qt's `KdeLayout` (source) is the de-facto rule. Union (Plasma 6.8 beta) may change Breeze visuals in 2027; style via `Kirigami.Theme`/`Units` to stay compatible.
