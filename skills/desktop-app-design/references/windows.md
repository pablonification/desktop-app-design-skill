# Windows app design (Windows 11, Fluent 2, WinUI 3)

Read this for any Windows app: WinUI 3 / Windows App SDK, WPF, WinForms, Win32, or a cross-platform shell running on Windows. epx = effective pixels (Windows' scale-independent unit). Every rule cites its source inline; ⚠️ marks claims that couldn't be fully verified (collected at the end). Researched November 2026 — platform details change, so re-check anything version-specific.

Contents: 0. TL;DR rules · 1. Principles & current platform versions · 2. Layout, spacing, corner radius, breakpoints · 3. Typography · 4. Color, themes, contrast themes · 5. Materials & depth · 6. Title bar · 7. Navigation & commands · 8. Feedback & dialogs · 9. Motion · 10. Iconography & target sizes · 11. Focus & input · 12. Snippets · 13. Inclusive design · 14. Common mistakes on Windows · Unverified / open questions

## 0. TL;DR rules (apply before anything else)

1. **Use the platform, don't paint it**: WinUI 3 / Windows App SDK 2.x controls (or WPF Fluent theme, or Electron with `backgroundMaterial`+`titleBarOverlay`). In-box controls give you theming, HC, text scaling, focus, UIA, motion for free.
2. **Window shell**: Mica (or Mica Alt with tabs) as the single base layer → content layer `LayerFillColorDefaultBrush` → cards `CardBackgroundFillColorDefaultBrush`. Extend Mica under a **32 epx** title bar (48 with search/avatar/tabs); keep system caption buttons so **Snap Layouts** work; min window width ≤ 500 (aim 330–360).
3. **Geometry**: 4-epx grid; 8 between buttons, 12 between label/control and content areas, 16 surface padding, 24 page margin (12 when < 640). Radius 4 for controls, 8 for windows/flyouts/dialogs, 0 when maximized/snapped.
4. **Type**: Segoe UI Variable; ramp 12/16 · 14/20 · 18/24 · 20/28 · 28/36 · 40/52 · 68/92; Regular + SemiBold only; sentence case; min 12 Regular / 14 SemiBold.
5. **Color**: only `{ThemeResource}` brushes; follow system theme; accent sparingly; Light + Dark + HighContrast dictionaries; test the 4 contrast themes.
6. **Navigation**: NavigationView (Left 5–10 items / Top ≤ 5 / Auto adaptive at 641 & 1008), TabView for documents, MenuBar+CommandBar for editors; Settings at the bottom of nav.
7. **Commands**: CommandBar with overflow; CommandBarFlyout as context menu via `ContextFlyout`; KeyboardAccelerators with the standard Windows shortcuts; AccessKeys for Alt keytips.
8. **Feedback**: ContentDialog only for must-read/confirm (do-it buttons left, Cancel right, `XamlRoot` set); InfoBar for persistent status; TeachingTip to teach; toasts rarely and cleaned up.
9. **Motion**: built-in transitions; custom = 83 / 167 / 250 / 333 ms, enter `cubic-bezier(0,0,0,1)`, exit `cubic-bezier(1,0,1,1)`, exits faster; obey `UISettings.AnimationsEnabled`.
10. **Input**: everything keyboard-reachable with visible 2-tone focus rect; arrows inside groups, Tab between, F6 between panes; 40 epx touch targets; tooltips on icon-only buttons; text scales to 225 % without clipping.

## 1. Principles & current platform versions

Source of truth: `MicrosoftDocs/windows-dev-docs` (cloned at commit of 2026-10-14) = https://learn.microsoft.com/windows/apps/design/

**Windows 11 design principles** (https://learn.microsoft.com/windows/apps/design/design-principles): *Effortless* (fast, focus, precision) · *Calm* ("softer and decluttered; fades into the background") · *Personal* (adapts to user prefs — theme, accent, text size) · *Familiar* (no learning curve) · *Complete + Coherent* (consistent across platforms). Signature experiences = Color, Elevation & layering, Iconography, Materials, Geometry, Typography, Motion. Each design page defers to Fluent 2 (https://fluent2.microsoft.design/) for the cross-platform language; Windows pages give the Windows-specific numbers — use Windows numbers when they differ.

**Platform status (Nov 2026):**
- **Windows App SDK 2.x is current stable — latest is 2.6.4 (2026-10-27)**; 1.8.12 (2026-09-24) was the *final* 1.8 servicing release (https://github.com/microsoft/WindowsAppSDK/releases). 2.0.1 (2026-04-29) was the first major bump since 1.0 (Nov 2021) and moved to SemVer: NuGet `Microsoft.WindowsAppSDK` version == SDK version, roughly monthly minors (2.2 Jun, 2.3 Jul, 2.4 Aug, 2.5 Sep, 2.6 Oct), next side-by-side major = 3.0 (https://learn.microsoft.com/windows/apps/windows-app-sdk/release-notes/windows-app-sdk-2-0). ⚠️ The learn.microsoft.com downloads page (docs commit 2026-10-14) still lists 2.1.3 — trust GitHub releases / NuGet for the version number.
- 2.3–2.6 UI-relevant: 2.3.1 `XamlOptionalChanges` (opt into XAML breaking changes) + opt-in style perf (`DefaultStyleOptimizations`, `OptimizeApplyStyles`: lighter `FontIcon` tree, faster `ThemeResource` lookup); 2.4.0 touchpad/mouse **haptics** via `Windows.Devices.Haptics` and touchpad single-finger panning; 2.5.1 NavigationView/CommandBar fixes (e.g. spurious overflow button at 175 %); the rest is mostly Windows AI (Phi Silica structured JSON, LoRA, VideoScaler) (GitHub release notes).
- **Experimental channel (not for production, but signals direction)**: 2.3-expA `Window.Width/Height/MinWidth/MinHeight/MaxWidth/MaxHeight` (DPI-aware logical px, settable from XAML); 2.4-exp WinUI 3 **inking** (`InkCanvas`, `InkToolbar`, `InkPresenter`); 2.5-exp **`TableView`** (grouping, sort/filter, resizable columns) and **`Chart`** (line/area/bar) controls, `FrameworkElement.SetThemeResourceBinding` (ThemeResource from code) (https://github.com/microsoft/WindowsAppSDK/releases). Until stable, build tables with `ItemsView`/`ListView` + column headers, or a community DataGrid ⚠️ (Toolkit 8.x status unverified).
- UI-relevant 2.x additions: `SystemBackdropElement` (place Mica/Acrylic anywhere in the tree, with `CornerRadius` — restores WinUI 2-style in-app acrylic; was `SystemBackdropHost` in experimental); `TitleBar` drag-region fix (gaps draggable by default; `TitleBar.IsDragRegion` attached prop, `TitleBar.AutoRefreshDragRegions`, `TitleBar.RecomputeDragRegions()`); `SplitMenuFlyoutItem` (stable since 1.8.6); XAML conditionals `IXamlCondition`; deprecated `Window.Current`, `DependencyObject.Dispatcher`, `FocusManager.GetFocusedElement` (no-arg) (same source).
- WinUI 3 is open-source-buildable from `microsoft/microsoft-ui-xaml` (VS 2026 build support added in 2.0 exp4) (same source).
- WinUI 3 Gallery app (Store 9P3JFPWWDZRC, github.com/microsoft/WinUI-Gallery) is the live reference for every control — open `winui3gallery://item/<Control>`.

## 2. Layout, spacing, corner radius, breakpoints

**Units.** Design in *effective pixels* (epx) — DPI-independent. Scale plateaus: 100/125/150/175/200/225/250/300/350/400 %. **All sizes, margins, positions = multiples of 4 epx** (4×125 % = 5 px, whole pixels → crisp edges); text exempt (https://learn.microsoft.com/windows/apps/design/layout/screen-sizes-and-breakpoints-for-responsive-design).

**Spacing ramp (Windows, epx)** (https://learn.microsoft.com/windows/apps/design/basics/content-basics):
| Between | epx |
|---|---|
| buttons (in a row) | 8 |
| button and its flyout | 8 |
| control and its header | 8 |
| control and its label | 12 |
| content areas / Title–Subtitle–Body blocks | 12 |
| surface edge and text inside it | 16 |

**Page margins / gutters:** 12 epx gutters when window < 640; 24 epx otherwise (https://learn.microsoft.com/windows/apps/develop/ui/alignment-margin-padding). NavigationView content: 12 px margins in `Minimal` mode, 24 px otherwise (https://learn.microsoft.com/windows/apps/develop/ui/controls/navigationview). In-box silhouettes: utility/editor apps (Notepad, Terminal) use 12 epx; media/settings-style apps (Photos, Settings) use up to 56 epx (https://learn.microsoft.com/windows/apps/design/basics/app-silhouette).

**Breakpoints (window width, not screen):** Small ≤ 640 · Medium 641–1007 · Large ≥ 1008 epx (breakpoints doc). NavigationView `Auto` uses exactly these: `LeftMinimal` ≤ 640, `LeftCompact` 641–1007, `Left` ≥ 1008 (`CompactModeThresholdWidth`=641, `ExpandedModeThresholdWidth`=1008). Use `VisualStateManager` + `AdaptiveTrigger MinWindowWidth="…"` (narrow layout is the default XAML; states add wider layouts). Desktop windows get resized and snapped to halves/thirds/quarters — a 1920 screen snapped in thirds = 640 epx, so every app must work at Small.
- Mockups: set DPI 72 and use the effective resolution (breakpoints doc).
- Line length: 50–60 characters; never < 20 or > 60 (https://learn.microsoft.com/windows/apps/design/signature-experiences/typography).

**Corner radius** (https://learn.microsoft.com/windows/apps/design/signature-experiences/geometry):
| Radius | Applies to |
|---|---|
| **8 px** (`OverlayCornerRadius`) | top-level containers: app windows, flyouts, MenuFlyout, ContentDialog, TeachingTip |
| **4 px** (`ControlCornerRadius`) | in-page controls: Button, CheckBox, ComboBox, TextBox, ListView item backplates; bars (ProgressBar, ScrollBar, Slider); **ToolTip** (exception, small) |
| **0** | straight edges meeting other straight edges; parts of a SplitButton that touch; the side of a flyout attached to its invoker; **windows when snapped or maximized** |
- Nested rule (practitioner/Fluent 2): inner radius = outer radius − padding so curves look concentric; cards on Windows typically 8 px (WinUI Gallery / SettingsCard use `OverlayCornerRadius`) ⚠️ (convention, not stated in the geometry doc).
- Win32: `DwmSetWindowAttribute(hwnd, DWMWA_WINDOW_CORNER_PREFERENCE, &DWMWCP_ROUND, …)` (`DWMWCP_ROUNDSMALL` for small popups) (https://learn.microsoft.com/windows/apps/desktop/modernize/ui/apply-rounded-corners).

**Density.** Standard WinUI controls are ~32 epx tall (Button: `ButtonPadding` 11,5,11,6 + 20 px line + 1 px borders; `ControlContentThemeFontSize` 14) (`microsoft-ui-xaml/controls/dev/CommonStyles/Button_themeresources.xaml`). Opt-in **Compact** density = merge `Compact.xaml` (sets `TextControlThemeMinHeight` 24, `ComboBoxMinHeight` 24, `TreeViewItemMinHeight` 24, `ListViewItemMinHeight` 32, `NavigationViewItemOnLeftMinHeight` 32) (`controls/dev/dll/DensityStyles/Compact.xaml`); URI `ms-appx:///Microsoft.UI.Xaml/DensityStyles/Compact.xaml` ⚠️ (the old "Control size and density" docs page now redirects to content-basics). Use compact only for data-dense, mouse-first pro tools.

**Content composition** (content-basics): confined title → `BodyStrong` with no extra spacing; very confined (command labels) → `Caption`; multi-line list items = Body + Caption + **32 epx icons**, `BodyStrong` section headers; grid items with icons/avatars → centred Caption; in Expanders right-align controls with **16 epx** to the chevron and indent nested controls **48 epx**.

## 3. Typography

**Font:** Segoe UI Variable (system font since Win 11; XAML picks it via `XamlAutoFontFamily`). Axes: `wght` 100–700 and automatic `opsz` (optical size, 8–36 pt) — small text gets open counters, large text gets tighter "Display" shapes. In HTML/Electron you must name it in CSS (e.g. `font-family: "Segoe UI Variable", "Segoe UI", system-ui, sans-serif`; the font also exposes named instances "Segoe UI Variable Text/Small/Display" ⚠️) — optical sizing is then automatic (https://learn.microsoft.com/windows/apps/design/signature-experiences/typography). Off-Windows metric-compatible fallback: **Selawik** (open source). Non-Latin: Yu Gothic UI (ja), Malgun Gothic (ko), Microsoft YaHei UI (zh-Hans), Microsoft JhengHei UI (zh-Hant), Nirmala UI (Indic), Leelawadee UI (Thai/Lao/Khmer), Segoe UI (Arabic/Hebrew/Armenian/Georgian). Use `LanguageFont` APIs to pick per-language fonts. Monospace: Cascadia Code/Mono ⚠️ (not listed on the page; Consolas is).

**Type ramp** (exact; epx size / line height) — style keys verified in `microsoft-ui-xaml/controls/dev/CommonStyles/TextBlock_themeresources.xaml` and https://learn.microsoft.com/windows/apps/develop/platform/xaml/xaml-theme-resources#the-xaml-type-ramp:
| Style key | Size/LH | Weight | Use |
|---|---|---|---|
| `CaptionTextBlockStyle` | 12/16 | Regular | captions, title bar title, metadata |
| `BodyTextBlockStyle` | 14/20 | Regular | default body; control text (`ControlContentThemeFontSize`=14) |
| `BodyStrongTextBlockStyle` | 14/20 | SemiBold | emphasis, list primary line, card header |
| `BodyLargeTextBlockStyle` | 18/24 | Regular | lead paragraph (new ramp step) |
| `BodyLargeStrongTextBlockStyle` | 18/24 | SemiBold | — |
| `SubtitleTextBlockStyle` | 20/28 | SemiBold ("Display") | section headers |
| `TitleTextBlockStyle` | 28/36 | SemiBold | page titles |
| `TitleLargeTextBlockStyle` | 40/52 | SemiBold | hero titles |
| `DisplayTextBlockStyle` | 68/92 | SemiBold | splash/hero only |
Base style: `TextTrimming=CharacterEllipsis`, `TextWrapping=Wrap`, `LineStackingStrategy=MaxHeight`. Size resources are overridable: `CaptionTextBlockFontSize`, `BodyTextBlockFontSize`, … `DisplayTextBlockFontSize`.

Rules (typography doc):
- Weights: Regular for text, **SemiBold for titles**. No Bold, **no Italic** in the ramp (italic hurts dyslexic readers) — use SemiBold for emphasis.
- **Minimums: 12 px Regular, 14 px SemiBold** — smaller is illegible in some languages.
- **Sentence case everywhere**, including titles and buttons ("Save as", not "Save As"). Left-aligned; centre only under icons.
- One font family per app. Truncation: ellipsis in most cases.
- ⚠️ Conflict: the typography page says "use ellipses in most cases", while the text-scaling page says "Clipping is preferred to ellipses as ellipses take up space" and clip the *end*. Practical rule: ellipsis for labels in undefined containers or with "see more"; clip + tooltip in tight fixed cells.

**Text scaling** (Settings › Accessibility › Text size, 100 %→**225 %**; independent of display scaling) (https://learn.microsoft.com/windows/apps/develop/input/text-scaling):
- WinUI text controls scale automatically. Your job: no fixed heights on anything containing text; use `Auto`/`*` grid sizes; enable `TextWrapping="Wrap"` (and `AcceptsReturn` for TextBox); if you clip, add a `ToolTip` with the full text; let the title bar grow.
- Don't scale font-glyph icons: `IsTextScaleFactorEnabled="False"` on icon TextBlocks/FontIcons.
- Custom renderers (DirectWrite, GDI, SwapChainPanel, Win32 beyond menus/icons/toolbars, game engines, Flutter/Qt custom text) do **not** scale natively → read `UISettings.TextScaleFactor` and handle `UISettings.TextScaleFactorChanged`.
- Test at 225 % with the window snapped to 640 epx — that's the worst realistic case.

## 4. Color, themes, contrast themes

Principles (https://learn.microsoft.com/windows/apps/design/signature-experiences/color): color is a *calm foundation*; accent used **sparingly** for important elements and interactive state; pick one color to mean "interactive"; never use red/green as the sole differentiator (~8 % of men are red-green colorblind).

**Themes.** Default = follow the user (omit `Application.RequestedTheme`). Per-element override with `FrameworkElement.RequestedTheme`. Contrast themes override everything. Test Light, Dark, and all 4 contrast themes (https://learn.microsoft.com/windows/apps/develop/ui/theming).

**Never hard-code colors** — use theme brushes via `{ThemeResource …}` (re-evaluated on theme change; `{StaticResource}` is not). Inside your own `ThemeDictionaries` use `StaticResource`, except for theme-agnostic keys (`SystemAccentColor*`, `SystemColor*Color`). Define **Light, Dark and HighContrast** dictionaries explicitly — a lone "Default" + "HighContrast" causes theme bleed when mixing per-element themes (https://learn.microsoft.com/windows/apps/develop/platform/xaml/xaml-theme-resources).

**Key semantic tokens** (values from `microsoft-ui-xaml/controls/dev/CommonStyles/Common_themeresources_any.xaml`, main branch Nov 2026; append `Brush` for the brush key):
| Token | Light | Dark | Use |
|---|---|---|---|
| `TextFillColorPrimary` | #E4000000 | #FFFFFF | body text |
| `TextFillColorSecondary` | #9E000000 | #C5FFFFFF | secondary text, captions |
| `TextFillColorTertiary` | #72000000 | #87FFFFFF | hints, placeholder |
| `TextFillColorDisabled` | #5C000000 | #5DFFFFFF | disabled |
| `AccentTextFillColorPrimaryBrush` | = SystemAccentColorDark2 | = SystemAccentColorLight3 | accent-colored text/links |
| `AccentFillColorDefaultBrush` | = SystemAccentColorDark1 | = SystemAccentColorLight2 | accent button/fill |
| `TextOnAccentFillColorPrimary` | #FFFFFF | #000000 | text on accent fill |
| `ControlFillColorDefault` | #B3FFFFFF | #0FFFFFFF | control background |
| `CardBackgroundFillColorDefault` | #B3FFFFFF | #0DFFFFFF | cards (with `CardStrokeColorDefault`) |
| `LayerFillColorDefault` | #80FFFFFF | #4C3A3A3A | content layer on Mica |
| `LayerOnMicaBaseAltFillColorDefault` | #B3FFFFFF | #733A3A3A | commanding layer on Mica Alt |
| `SolidBackgroundFillColorBase` | #F3F3F3 | #202020 | Mica fallback / opaque window bg |
| `SolidBackgroundFillColorBaseAlt` | #DADADA | #0A0A0A | Mica Alt fallback |
| `SmokeFillColorDefault` | #4D000000 | #4D000000 | modal scrim |
| `DividerStrokeColorDefault` | #0F000000 | #15FFFFFF | separators |
| `SystemFillColorSuccess/Caution/Critical` | #0F7B0F / #9D5D00 / #C42B1C | #6CCB5F / #FCE100 / #FF99A4 | status (InfoBar, InfoBadge, validation) |
| `FocusStrokeColorOuter/Inner` | #E4000000 / #B3FFFFFF | #FFFFFF / #B3000000 | two-tone focus rect |
Note the pattern: neutrals are *alpha* overlays (black-on-light, white-on-dark), so they compose over Mica/Acrylic. Light-theme accent fills use **darker** shades, dark-theme uses **lighter** shades — never use raw `SystemAccentColor` for text.

**Accent palette**: `SystemAccentColor` + `SystemAccentColorLight1/2/3` + `SystemAccentColorDark1/2/3` (generated by the shell; `UISettings.GetColorValue(UIColorType.AccentLight2)` in code). Brand override: `<Color x:Key="SystemAccentColor">#107C10</Color>` in App.xaml — but check contrast and prefer respecting the user's accent (theming doc). ⚠️ Overriding only `SystemAccentColor` does not regenerate Light/Dark shades — override all seven.

**Contrast themes** (https://learn.microsoft.com/windows/apps/design/accessibility/high-contrast-themes): Aquatic, Desert, Dusk, Night sky (≥7:1 typical); toggle with **Left Alt + Left Shift + PrtScn**. Detect: `Microsoft.UI.System.ThemeSettings.HighContrast` (WinUI) / `SystemParameters.HighContrast` (WPF) / `forced-colors: active` (Electron/web).
- In the `HighContrast` dictionary map every custom brush to a `SystemColor*` pair: `SystemColorWindowColor`+`SystemColorWindowTextColor` (surfaces/text), `SystemColorHotlightColor` (**links only**), `SystemColorGrayTextColor` (**disabled only** — not secondary text), `SystemColorHighlightColor`+`SystemColorHighlightTextColor` (selected/hover/pressed), `SystemColorButtonFaceColor`+`SystemColorButtonTextColor` (interactive controls). Never mix pairs.
- Set `HighContrastAdjustment="None"` once your brushes are correct (default auto-adjust forces white text on black backplates).
- Add HC-only **2 px borders** on flyouts/dialogs and wherever two surfaces share a background (nav pane vs content).
- In ListView item templates don't set `TextBlock.Foreground` explicitly — breaks selection inversion in HC.
- Images/icons: provide `contrast-black`/`contrast-white` asset qualifiers (MRT) for bitmaps; prefer font/vector icons that inherit `Foreground`.

## 5. Materials & depth (Mica, Mica Alt, Acrylic, Smoke, elevation)

Sources: https://learn.microsoft.com/windows/apps/design/signature-experiences/materials · .../design/style/mica · .../design/style/acrylic · .../signature-experiences/layering

| Material | Opaque? | Use for | Never use for |
|---|---|---|---|
| **Mica** (`MicaBackdrop Kind="Base"`) | opaque, samples wallpaper once (cheap) | base layer of long-lived windows (main app window, settings) | individual elements; more than once per app |
| **Mica Alt** (`MicaBackdrop Kind="BaseAlt"`) | opaque, stronger wallpaper tint | base layer when you need contrast between title bar and commanding area — esp. **tabbed title bars** | same |
| **Acrylic – background** (`DesktopAcrylicBackdrop`) | translucent frosted glass, GPU-heavy | transient light-dismiss surfaces: flyouts, context menus, popups that draw outside the window | "large background surfaces of your app" |
| **Acrylic – in-app** (`AcrylicBrush`, now `SystemBackdropElement`) | blurs app content behind | supporting UI that overlaps content: NavigationView pane in Compact/Minimal overlay | side-by-side panes (visible seam); permanently docked vertical panes → use opaque |
| **Smoke** | translucent black, not mode-aware | dim content behind a modal (ContentDialog does it for you) | — |

Rules:
- Mica/Mica Alt fall back to solid `SolidBackgroundFillColorBase` / `SolidBackgroundFillColorBaseAlt` when: Transparency effects off, Battery Saver on, low-end HW, **window inactive**, or OS < build 22000. High contrast shows the user's chosen background. Design must look right on the fallback too (mica doc).
- To see Mica, every layer between window and element must be `Transparent`. "Don't apply backdrop material more than once." Show Mica in the title bar (extend content into title bar, transparent caption buttons) (mica doc).
- **Two-layer system**: *base* layer (Mica; holds menus, commands, navigation) + *content* layer (`LayerFillColorDefaultBrush` — a low-opacity fill, as one contiguous surface ("standard pattern") or as cards ("card pattern")). With Mica Alt: base → commanding layer `LayerOnMicaBaseAltFillColorDefaultBrush` → content layer `LayerFillColorDefaultBrush` (mica doc). NavigationView already draws the content layer in its content area; to do cards, override its background/border resources.
- Acrylic: don't put accent-colored text or hyperlinks on acrylic (contrast fails at 14px); don't stack acrylic surfaces; extend acrylic to at least one window edge (acrylic doc). Auto-disabled by Battery Saver and Transparency effects off.
- **Elevation values** (shadow + 1px stroke "contour"): Window 128 · Dialog 128 · Flyout 32 · Tooltip 16 · Card 8 · Control 2 (rest/hover) → 1 (pressed) · Layer 1 (layering doc). Shadows are purposeful, not decorative; in-box controls already have them. Implement custom with `ThemeShadow` (+ `Translation="0,0,32"`) or Composition `DropShadow` (https://learn.microsoft.com/windows/apps/develop/ui/shadows).
- Light *and* dark: darker = less important surface, lighter = more important (color doc).
- Fluent 2 web tokens use a different ramp: `shadow2` `0 0 2px ambient, 0 1px 2px key` · `shadow4` (0 2px 4px) · `shadow8` (0 4px 8px) · `shadow16` (0 8px 16px) · `shadow28` (0 0 8px, 0 14px 28px) · `shadow64` (0 0 8px, 0 32px 64px) (https://github.com/microsoft/fluentui/blob/master/packages/tokens/src/utils/shadows.ts). For Electron/web-on-Windows map: control→shadow2, card→shadow4/8, tooltip→shadow16, flyout→shadow28, dialog/window→shadow64 ⚠️ (mapping is my synthesis).

## 6. Title bar

Design spec (https://learn.microsoft.com/windows/apps/design/basics/titlebar-design):
- **Height 32 epx** standard; **48 epx** when it hosts interactive content (search box, PersonPicture, tabs). Background = Mica; blend it with the window rather than a contrasting band.
- **Icon** 16×16, 16 epx from the left edge (LTR), vertically centred (8 epx top/bottom at 32 height). Click → system menu; double-click → close.
- **Title** 16 epx after icon/back button; `CaptionTextBlockStyle` (12 epx); Segoe UI Variable; truncate with ellipsis — icon and caption buttons must always stay fully visible. Title must respond to text scaling (title bar may grow).
- **Back button** (glyph E830 `ChromeBack`) leftmost, 16 epx from edge and from the next element, full-bleed backplate, has rest/hover/pressed/active/inactive states.
- **Search** box centred in the window; **PersonPicture** just left of the caption buttons; **tabs** may occupy the title bar with caption buttons anchored right.
- TitleBar control template constants: `TitleBarCompactHeight` 32, `TitleBarExpandedHeight` 48 (auto-switches to 48 when `Content`/`LeftHeader`/`RightHeader` is set), `TitleBarIconMaxHeight` 16 (`microsoft-ui-xaml/controls/dev/TitleBar/TitleBar_themeresources.xaml`, `TitleBar.cpp`).
- **Behaviour**: all empty space + non-interactive elements (title text) are draggable; right-click → system window menu; double-click → maximize/restore.
- **Inactive state**: dim title text, icons, buttons when window deactivates (`Window.Activated` → `WindowActivationState.Deactivated`; Win32 `WM_ACTIVATE`) (https://learn.microsoft.com/windows/apps/develop/title-bar).
- High contrast: use `SystemColors` for title bar colors.
- Custom caption glyphs if you must draw your own: E921 ChromeMinimize, E922 ChromeMaximize, E923 ChromeRestore, E8BB ChromeClose; full-bleed backplates; maximize/restore glyphs have rounded corners.

Implementation (https://learn.microsoft.com/windows/apps/develop/title-bar, .../develop/ui/controls/title-bar):
1. **Simplest/recommended (WinUI 3, WASDK ≥1.7):** the `TitleBar` control — properties `Title`, `Subtitle`, `IconSource`, `IsBackButtonVisible/Enabled` + `BackRequested`, `IsPaneToggleButtonVisible` + `PaneToggleRequested` (pair with NavigationView: set NavView `IsBackButtonVisible="Collapsed"`, `IsPaneToggleButtonVisible="False"`), `LeftHeader`, `Content` (centre, e.g. AutoSuggestBox), `RightHeader` (e.g. PersonPicture). It reserves a *min drag region* beside the caption buttons and mirrors in RTL. Code: `ExtendsContentIntoTitleBar = true; SetTitleBar(MyTitleBar);`. Stable since WASDK 1.7, which also added `AppWindowTitleBar.PreferredTheme` (light/dark caption buttons), `AppWindow.SetTitleBarIcon`/`SetTaskBarIcon`, and `OverlappedPresenter.PreferredMinimumWidth/Height` (https://learn.microsoft.com/windows/apps/windows-app-sdk/release-notes/windows-app-sdk-1-7).
2. **WASDK 2.1.3+:** drag regions inside `TitleBar.Content` are computed by walking the tree: only *interactive* controls punch holes; gaps are draggable. Override with attached `TitleBar.IsDragRegion="True|False"`, set `AutoRefreshDragRegions="True"` for dynamic content, or call `RecomputeDragRegions()` (https://learn.microsoft.com/windows/apps/windows-app-sdk/release-notes/windows-app-sdk-2-0).
3. **Full manual (AppWindow, any framework incl. WPF/WinForms/Win32):** `AppWindow.TitleBar.ExtendsContentIntoTitleBar = true`; `PreferredHeightOption = TitleBarHeightOption.Tall` (48; must set *after* extending or it throws); interactive areas via `InputNonClientPointerSource.GetForWindowId(id).SetRegionRects(NonClientRegionKind.Passthrough, rects)` — rects in **physical pixels** (multiply by `XamlRoot.RasterizationScale`), recomputed in the title bar's `SizeChanged` (not `Window.Changed` — fires before resize). Reserve caption area with padding *columns* sized from `TitleBar.LeftInset/RightInset` (RTL-safe) and `TitleBar.Height`. Never put interactive UI under the caption buttons — they get no input.
4. **Caption button colors:** when extended, set `ButtonBackgroundColor`/`ButtonInactiveBackgroundColor = Colors.Transparent` so Mica shows through. Set `AppWindow.TitleBar.PreferredTheme` (1.7+; `Legacy`/`UseDefaultAppMode`/`Light`/`Dark`): `UseDefaultAppMode` follows the *Windows* app mode — if the user picked a theme inside your app, set `Light`/`Dark` to match it (https://learn.microsoft.com/windows/windows-app-sdk/api/winrt/microsoft.ui.windowing.titlebartheme); if you set `ButtonForegroundColor`/`ButtonHoverBackgroundColor` yourself, re-apply them on `ActualThemeChanged`. In non-extended (colors-only) customization alpha is ignored — no transparency.
5. Full-screen / compact overlay presenters: `sender.TitleBar.ResetToDefault()` or hide your custom bar (title-bar doc).

**Snap Layouts** (hover maximize or Win+Z) (https://learn.microsoft.com/windows/apps/desktop/modernize/ui/apply-snap-layout-menu):
- Appears automatically if the system draws the caption buttons. **It breaks when you draw your own caption buttons/fake title bar.** Fixes: let WASDK/AppWindow draw caption buttons; in raw Win32 return `HTMAXBUTTON` from `WM_NCHITTEST` over your maximize button; Electron ≥ 13 supports it (use `titleBarStyle:'hidden'` + `titleBarOverlay` so Windows draws real caption buttons).
- Snaps fail silently if min window size is too big: **min width ≤ 500 epx required, ≤ 330 epx recommended**.
- Also preserve: Win+Arrow snapping, Aero Shake, double-click-to-maximize, drag-from-maximized-to-restore, right-click system menu, Alt+Space menu. These all come free with `HTCAPTION`/real drag regions, and break with JS `mousemove` window-dragging.

## 7. Navigation & commands

**Pick a silhouette first** (https://learn.microsoft.com/windows/apps/design/basics/app-silhouette): *Left nav* (Settings) · *Top nav* (Photos) · *MenuBar + CommandBar* (Notepad) · *TabView in title bar* (Terminal). Don't invent a fifth.

**NavigationView** (https://learn.microsoft.com/windows/apps/develop/ui/controls/navigationview):
- `PaneDisplayMode="Top"`: ≤ 5 equally important top-level categories, want max content space, icons can't describe categories well. Overflow goes to "More".
- `Left`: 5–10 equally important categories, want nav prominent. `LeftCompact` = icon rail (overlay when opened); `LeftMinimal` = hamburger only.
- `Auto` (default): Left ≥ 1008 → LeftCompact 641–1007 → LeftMinimal ≤ 640. If Top doesn't fit, switch to `LeftMinimal` via `AdaptiveTrigger` rather than letting items overflow.
- Hierarchy: nested `NavigationViewItem.MenuItems`; **two levels is ideal**.
- Settings item: built in (`IsSettingsVisible`, pinned bottom). Extra nav items at bottom → `FooterMenuItems`; non-nav content at bottom → `PaneFooter`. Search → `NavigationView.AutoSuggestBox` (or title bar).
- With custom title bar: hide NavView's own back/pane-toggle buttons and use `TitleBar.IsBackButtonVisible`/`IsPaneToggleButtonVisible` (title-bar doc).
**TabView** (.../controls/tab-view): for document tabs/browser-like apps. Always keep one active tab. Built-in: Ctrl+Tab / Ctrl+Shift+Tab cycle, Ctrl+F4 raises `TabCloseRequested`. You should add: **Ctrl+T** new tab, **Ctrl+W** close, **Ctrl+Shift+T** reopen closed, **Ctrl+1…8** jump to tab N, **Ctrl+9** last tab; extra tab actions (duplicate, pin) in a tab context menu. `CanTearOutTabs` (WASDK ≥ 1.6) for drag-to-new-window. Close window when last tab closes. Put tabs in the title bar with Mica Alt.
**BreadcrumbBar** (.../controls/breadcrumbbar): use for deep hierarchies (file managers) where any ancestor is a jump target; **don't** use with only 2 levels — a back button suffices. Last item = current location; handle `ItemClicked`.
**Back navigation**: put back in the title bar (`ChromeBack` E830); also support Alt+Left, mouse XButton1, and Backspace ⚠️ only where no text input has focus.

**CommandBar** (.../controls/command-bar): `PrimaryCommands` ordered by importance (overflow automatically when narrow, `IsDynamicOverflowEnabled`), rarely used ones in `SecondaryCommands` ("See more" …). Icon 20×20 in bar, 16×16 in overflow. `DefaultLabelPosition="Right"` for desktop toolbars (Windows 11 in-box apps style) ⚠️ (convention). Labels: one word ideally. Settings entry = last item in overflow. **Order: Accept/Yes/OK to the LEFT of Reject/No/Cancel** (command-bar doc) — Windows order, opposite of macOS.
**Context menus** (.../controls/menus-and-context-menus): use `UIElement.ContextFlyout` (handles right-click, Shift+F10, Menu key, touch press-and-hold). Recommended control = `CommandBarFlyout`: Cut/Copy/Paste/Delete/Share as an icon row of `PrimaryCommands`, everything else as `SecondaryCommands` (expanded when invoked by right-click; collapsed when shown proactively, e.g. on selection) (.../controls/command-bar-flyout). Menu on a *button* = `Button.Flyout` with `MenuFlyout`. Menu item icons 16×16 — only when the icon is standard or truly illustrative; "cryptic icons … create visual clutter" (.../controls/menus). Use `MenuFlyoutSeparator`, `ToggleMenuFlyoutItem`, `RadioMenuFlyoutItem`, `MenuFlyoutSubItem`, and new `SplitMenuFlyoutItem` (default action + submenu; stable since 1.8.6). Scope context-menu accelerators with `KeyboardAccelerator.ScopeOwner`.
**MenuBar** (`MenuBar`/`MenuBarItem`): classic File/Edit/View for document & pro apps (Notepad, Paint). Lives on the base layer with a CommandBar below.

**Keyboard accelerators** (https://learn.microsoft.com/windows/apps/develop/input/keyboard-accelerators): `<KeyboardAccelerator Modifiers="Control" Key="S"/>` on buttons/menu items; shown automatically in menu items and tooltips (`KeyboardAcceleratorPlacementMode`). Standard set — never repurpose: Ctrl+N new, Ctrl+Shift+N new secondary, Ctrl+O ⚠️, Ctrl+S save, Ctrl+W close, Ctrl+P print, Ctrl+Z undo, **Ctrl+Y redo** (not Ctrl+Shift+Z), Ctrl+X/C/V (+Ctrl+Insert/Shift+Insert), Ctrl+Alt+V paste special, Ctrl+A select all, Ctrl+F find, F3 next result, Ctrl+H replace, F2 rename, Del delete (with undo), Shift+Del delete permanently, Ctrl+B/I/U, F5 or Ctrl+R refresh, Ctrl+ +/−/0 zoom, F6/Shift+F6 next/prev pane, Ctrl+E edit mode/search ⚠️, Ctrl+D favorite. Also system: Alt+F4 close window, F10/Alt to menu, Shift+F10 context menu, F1 help, F11 full screen.
**Access keys / KeyTips** (https://learn.microsoft.com/windows/apps/develop/input/access-keys): press **Alt** → keytip badges appear; `AccessKey="S"` on controls; single-char keys also work as Alt+S directly. Scope large sets with `IsAccessKeyScope="True"` (Word ribbon pattern); avoid collisions in one scope. Every MenuBar item/command should have one.

**Settings page** (https://learn.microsoft.com/windows/apps/design/app-settings/guidelines-for-app-settings — updated with Toolkit controls):
- Entry: NavigationView built-in Settings item (bottom), or last item in CommandBar overflow. Full window, single scrollable column, **max width ~1000–1100 px**, section headers in `BodyStrong`.
- Use `SettingsCard` (Header, Description, HeaderIcon, action control on the right; `IsClickEnabled` for navigating cards) and `SettingsExpander` (sub-options in `Items`) from **CommunityToolkit.WinUI.Controls.SettingsControls**.
- Toggle for binary; RadioButtons for ≤ 5 exclusive options; ComboBox otherwise. **Apply immediately — no Save/OK button.** Keep to ~4–5 settings groups; one-word headers ("Accounts", not "Account settings"); disable (don't hide) irrelevant settings and say why in `Description`.
- Theme picker: ComboBox with exactly "Light", "Dark", "Use system setting" + hyperlink "Windows color settings" → `ms-settings:colors`.
- "About" `SettingsExpander` at the bottom: app name, icon, version; links to repo/feedback, dependencies, legal.
- Workflow commands (brush size, etc.) never go in Settings.

## 8. Feedback & dialogs

**Choose the surface** (https://learn.microsoft.com/windows/apps/develop/ui/controls/infobar, .../dialogs-and-flyouts/dialogs, .../teaching-tip):
| Need | Use |
|---|---|
| Must read / confirm / app-blocking state | `ContentDialog` (modal, smoke behind) |
| Contextual info or light input anchored to an element | `Flyout` (light-dismiss) |
| App-wide persistent status (offline, update ready, sync failed) | `InfoBar` (inline, stays until closed/resolved) |
| Teach a new feature once | `TeachingTip` (transient; never critical info) |
| Field validation | **inline** next to the field — never a dialog |
| Background task done while app not focused | app notification (toast) |

**ContentDialog** (dialogs doc):
- Title optional (short, relates to buttons); content required; first line states the issue.
- Always a safe button via `CloseButtonText` ("Cancel"/"Close"); Esc, gamepad B and system back map to it. Up to two "do it" buttons via `PrimaryButtonText`/`SecondaryButtonText`.
- **Button order: "do it" buttons LEFT, safe/nondestructive RIGHT** (Windows; opposite of macOS). Button text = specific verbs answering the question ("Delete", "Allow"/"Block"), not Yes/No.
- `DefaultButton = ContentDialogButton.Primary` → gets Accent style + Enter key. No default is set by default — for destructive actions leave no default (or default to Close) ⚠️ (practice; doc only says "optionally").
- Only one ContentDialog per window at a time (second throws). WinUI 3: **must set `XamlRoot`**. Don't use deprecated `MessageDialog`.
**InfoBar**: `Severity` = Informational (default) / Success (long-running/background task finished) / Warning (may cause a problem later) / Error. Don't use for confirming a user action, time-sensitive alerts, or non-essential messages. Don't let it flash in/out rapidly; text required (color+icon not enough); to re-announce to screen readers close and reopen. `IsClosable`, `ActionButton`.
**TeachingTip**: 3–5 words read on average — keep it tiny; stagger tips across sessions; `Target` for tail; `IsLightDismissEnabled` when it can escape the root.
**Progress** (.../controls/progress-controls): determinate `ProgressBar` when duration known (install/download); indeterminate `ProgressBar` = working but **non-blocking**; indeterminate `ProgressRing` = **blocking** ("Signing in…"). Pair with a line of status text. ⚠️ Practitioner rule (not in doc): show nothing for < ~1 s, then indicator; use skeletons for content loading.
**App notifications/toasts** (https://learn.microsoft.com/windows/apps/develop/notifications/app-notifications/app-notifications-ux-guidance; API `Microsoft.Windows.AppNotifications.AppNotificationManager` + `AppNotificationBuilder`):
- Notify only for things worth an interruption; otherwise post **silently** to Notification Center (suppress popup). Respect Focus sessions (`FocusSessionManager`/Do Not Disturb).
- Clicking opens the app *in that context*; background actions (quick reply) must not launch the app.
- **Clean up**: remove notifications the user has already seen in-app (`AppNotificationManager.Default.RemoveByTagAsync/RemoveByGroupAsync`).
- Use buttons, inline reply, progress bar (downloads) to save a trip to the app. Never notify that the app itself is "running" or for marketing.
**Sound**: control sounds via `ElementSoundPlayer.State` (On/Off/Auto) — don't turn them on for a desktop productivity app; the docs don't state the default ⚠️ (https://learn.microsoft.com/windows/apps/develop/ui/sound).

## 9. Motion

Principles (https://learn.microsoft.com/windows/apps/design/signature-experiences/motion): **Connected** (same object morphs between states), **Consistent** (same entry point → same invoke/dismiss motion), **Responsive** (adapts to input type), **Delightful** (brief, purposeful), **Resourceful** ("Avoid custom animations where possible" — use built-in controls).

**Windows motion table** (same source) — use these for custom animations:
| Purpose | Easing | Duration (ms) | Animate |
|---|---|---|---|
| Direct entrance (fast in) | `cubic-bezier(0,0,0,1)` | 167 / 250 / 333 | position, scale, rotation |
| Existing element, point-to-point | `cubic-bezier(0.55,0.55,0,1)` | 167 / 250 / 333 | position, scale, rotation |
| Direct exit (fast out) | `cubic-bezier(0,0,0,1)` | 167 | position/scale/rotation — **always combined with fade-out** |
| Gentle exit (soft out) | `cubic-bezier(1,0,1,1)` | 167 | position, scale |
| Bare minimum (fade) | linear | 83 | opacity |
| Strong entrance (elastic, 3 keyframes) | (0.85,0,0,1) → (0.85,0,0.75,1) → (0.85,0,0,1) | 167 → 167 → 333 | position, scale |
- Short=167 for small/near moves, 250 normal, 333 for large/far moves.
- XAML duration resources: `ControlFasterAnimationDuration` = **83 ms**, `ControlFastAnimationDuration` = **167 ms**, `ControlNormalAnimationDuration` = **250 ms**; spline `ControlFastOutSlowInKeySpline` = `0,0,0,1` (https://learn.microsoft.com/windows/apps/design/motion/timing-and-easing; values confirmed in `Common_themeresources_any.xaml`).
- Two named curves: *Fast Out, Slow In* `cubic-bezier(0,0,0,1)` for anything **entering**; *Slow Out, Fast In* `cubic-bezier(1,0,1,1)` for anything **exiting** (timing-and-easing doc).
- Recipe (https://learn.microsoft.com/windows/apps/develop/motion/motion-in-practice): forward nav = old page fade out 150 ms (accelerate) → new page slide up 150 px over 300 ms (decelerate); back nav = slide down 150 ms → fade in 300 ms; expand 300 ms (standard), contract 150 ms (accelerate). Exits are faster than entrances.
- **Fluent 2 cross-platform tokens** (web/React; https://github.com/microsoft/fluentui/blob/master/packages/tokens/src/global/durations.ts, curves.ts): `durationUltraFast` 50, `durationFaster` 100, `durationFast` 150, `durationNormal` 200, `durationGentle` 250, `durationSlow` 300, `durationSlower` 400, `durationUltraSlow` 500 ms; `curveDecelerateMid` (0,0,0,1) = Windows' entrance curve; `curveAccelerateMid` (1,0,1,1) = Windows' exit curve; `curveDecelerateMax` (0.1,0.9,0.2,1); `curveDecelerateMin` (0.33,0,0.1,1); `curveAccelerateMax` (0.9,0.1,1,0.2); `curveAccelerateMin` (0.8,0,0.78,1); `curveEasyEaseMax` (0.8,0,0.2,1); `curveEasyEase` (0.33,0,0.67,1); `curveLinear`. fluent2.microsoft.design/motion itself lists **no** numbers — only: quick natural durations, bigger elements get longer, top-level nav = quick **fade** not slide, prefer staggering, ship a "no motion" option. For Electron/web apps on Windows use the Windows 83/167/250/333 table + these curves.

**Page transitions** (https://learn.microsoft.com/windows/apps/develop/motion/page-transitions) — pass as 3rd arg to `Frame.Navigate`:
- `EntranceNavigationTransitionInfo` (*page refresh*: slide up + fade) — top-level jumps (NavView items, tabs). Frame default.
- `DrillInNavigationTransitionInfo` — going deeper (list → detail).
- `SlideNavigationTransitionInfo { Effect = FromRight/FromLeft }` — sibling pages (NavView Top does this automatically).
- `SuppressNavigationTransitionInfo` — when you run a connected animation instead. `Frame.GoBack(transitionInfo)` for back.
**Connected animation** (https://learn.microsoft.com/windows/apps/develop/motion/connected-animation): source `ConnectedAnimationService.GetForCurrentView().PrepareToAnimate("key", srcElement)`; destination `GetAnimation("key")?.TryStart(destElement)`. Default `GravityConnectedAnimationConfiguration` for forward nav; `DirectConnectedAnimationConfiguration` (150 ms, decelerate) for back nav; `BasicConnectedAnimationConfiguration` for non-nav.
**Implicit animations**: `OpacityTransition`/`RotationTransition` (`ScalarTransition`), `ScaleTransition`/`TranslationTransition` (`Vector3Transition`), `BackgroundTransition` (`BrushTransition`) on Border/Panel/ContentPresenter (motion-in-practice). Also `ThemeTransition`s in `ChildrenTransitions` (`EntranceThemeTransition`, `RepositionThemeTransition`, `AddDeleteThemeTransition`) for lists. `AnimatedIcon` (Lottie) for micro-interactions.

**User settings to honor** (https://learn.microsoft.com/uwp/api/windows.ui.viewmanagement.uisettings):
- Settings › Accessibility › Visual effects › **Animation effects** → `UISettings.AnimationsEnabled` + `AnimationsEnabledChanged` (since 2004/19041). Built-in control/theme animations are expected to follow it ⚠️; **gate your own Storyboards/Composition animations** on it. Electron/web: `@media (prefers-reduced-motion: reduce)` (Chromium maps it to this setting ⚠️).
- **Transparency effects** → `UISettings.AdvancedEffectsEnabled` + `AdvancedEffectsEnabledChanged`. System backdrops fall back automatically; custom blur/transparency must check it.
- Also: `AutoHideScrollBars` (Settings › Accessibility › Visual effects › "Always show scrollbars"), `MessageDuration` (Settings › Accessibility › "Dismiss notifications after…" — scale your toast/InfoBar auto-dismiss timeouts by it), `TextScaleFactor`.

## 10. Iconography & target sizes

**System (in-app) icons** (https://learn.microsoft.com/windows/apps/design/iconography/, .../iconography/segoe-fluent-icons-font):
- Use **Segoe Fluent Icons** (replaced Segoe MDL2 Assets in Win 11). Monoline, 1 epx stroke; principles Minimal / Harmonious / Evolved. 1 em = icon square (16 px font = 16×16 icon).
- Crisp sizes only: **16, 20, 24, 32, 40, 48, 64**. Command bar 20, menu/overflow 16, title bar icon 16, multi-line list icons 32.
- XAML: `<SymbolIcon Symbol="Save"/>`, or `<FontIcon Glyph="&#xE74E;" FontFamily="{StaticResource SymbolThemeFontFamily}"/>` (resolves to Segoe Fluent Icons, fallback MDL2 on Win 10). PUA codepoints — not usable inline with text; not shipped on Win 10/macOS (may not redistribute to other platforms).
- Compose meaning: *base* icon fills the square, *modifier* goes in a bottom quadrant; state changes (selected/filled) by **layering** two glyphs.
- Ship-anywhere alternative (Electron/Flutter/Qt/web): **Fluent UI System Icons** (MIT, github.com/microsoft/fluentui-system-icons) — `Regular` and `Filled` variants at 16/20/24/28/32/48; use Regular by default and Filled for selected/active state (e.g. selected nav item) ⚠️ (the filled-for-selected convention is from Fluent 2 iconography; verify sizes per icon).
- Don't add icons to every menu item; don't use emoji as UI icons; never mix icon families.

**App icon** (https://learn.microsoft.com/windows/apps/design/iconography/app-icon-design, .../app-icon-construction):
- One literal metaphor, simple forms; **no text/letters** in the icon; designed on a **48×48 grid** with soft rounded corners; front-facing (perspective only when needed); subtle gradients (default **120°**, 1–2 steps), light from top-left; layered flat objects with soft inner shadows; ≥ half the icon ≥ **3:1** contrast on both light and dark backgrounds. No HC asset needed on Win 11.
- Sizes Windows actually uses: 16/20/24/32/40/48/64 (title bar, context menu, tray @100–400 %); 24/30/36/48/60/72/96 (taskbar, search, all apps); 32/40/48/64/80/96/256 (Start pins). **Minimum set: 16, 24, 32, 48, 256** (ICO for Win32). MSIX: `AppList.targetsize-{16…256}.png` + `_altform-unplated` + `_altform-lightunplated` variants — supply all theme variants or Windows puts your icon on a contrast plate. Transparent background preferred.

**Target sizes** (https://learn.microsoft.com/windows/apps/develop/input/guidelines-for-targeting): touch target ≈ **7.5 mm ≈ 40×40 epx**; WinUI controls are built to this. Bigger for frequent/consequential actions; keep destructive targets away from edges and other frequent targets. Mouse-only dense UIs can go to 32 epx controls (standard) / 24 epx (Compact) but keep **hit areas** ≥ 32 for pointer and ≥ 40 for touch-capable devices ⚠️ (synthesis; WCAG 2.2 AA min 24×24 CSS px). Never shrink caption buttons or title-bar back button below system size.

## 11. Focus & input

**Focus visual** (https://learn.microsoft.com/windows/apps/develop/input/guidelines-for-visualfeedback): one design for all inputs — two-tone rect: **primary (outer) 2 px** `SystemControlFocusVisualPrimaryBrush` (= `FocusStrokeColorOuter`: near-black in light, white in dark) around **secondary (inner) 1 px** `SystemControlFocusVisualSecondaryBrush` (= `FocusStrokeColorInner`); default margin 1 px outside bounds (`FocusVisualMargin`, Button uses −3). Properties: `FocusVisualPrimaryThickness`, `FocusVisualSecondaryThickness`, `FocusVisualPrimaryBrush/SecondaryBrush`, `UseSystemFocusVisuals`. Shown only for keyboard/gamepad focus (`FocusState.Keyboard`), not on click. **Never set `UseSystemFocusVisuals="False"` without a replacement.** Electron/web: style `:focus-visible` with `outline: 2px solid; outline-offset` + inner 1px contrasting ring; never `outline: none`.

**Keyboard model** (https://learn.microsoft.com/windows/apps/develop/input/keyboard-interactions, .../focus-navigation):
- Every interactive element is a tab stop (except inside a *group*); non-interactive (labels) are not. Tab order = visual order (top→bottom, left→right; mirrored RTL); avoid custom `TabIndex` jumps. Set sensible initial focus.
- **Tab between groups, arrows within groups** ("inner navigation"): lists, menus, radio groups, dialog button rows, toolbars. For custom groups: `XYFocusKeyboardNavigation="Enabled"` + `TabFocusNavigation="Once"` on the container. Single row → Left/Right, column → Up/Down, grid → all four.
- **F6 / Shift+F6** cycle major panes (nav, toolbar, content) — implement it in multi-pane apps. Space = activate; Enter = activate/commit (and default dialog button); Esc = cancel/close transient UI; Home/End in lists; Shift+F10 / Menu key = context menu.
- Text inputs swallow keys — don't bind single-letter accelerators that fire while typing.
- Gamepad/remote: XY focus is automatic; test with `XYFocusKeyboardNavigation` for 2-D layouts.

**Pointer, touch, pen differences** (https://learn.microsoft.com/windows/apps/develop/input/touch-interactions, .../mouse-interactions):
- Hover is mouse/pen-only: never hide essential actions behind hover; reveal on hover *and* show on focus/selection; touch equivalent of right-click = press-and-hold (use `ContextFlyout`, which handles all of these).
- Touch needs 40 epx targets and scroll bars become thin panning indicators (WinUI `ScrollView`/`ScrollViewer` auto-switch); mouse gets full scroll bars when hovered (respect "Always show scrollbars" → `UISettings.AutoHideScrollBars`).
- Check `PointerRoutedEventArgs.Pointer.PointerDeviceType` (Mouse/Touch/Pen) to adapt (e.g. larger padding after touch). Pen: support ink where natural (`InkCanvas`), barrel button = right-click.
- Use the themed WinUI scroll bars; never custom-paint thin always-visible mac-style scroll bars or hide them entirely.

**Tooltips** (https://learn.microsoft.com/windows/apps/develop/ui/controls/tooltips): **required on icon-only buttons**; otherwise sparingly. Supplemental, concise, never repeating visible text, never interactive content. Include the accelerator ("Copy (Ctrl+C)") — WinUI adds it automatically for `KeyboardAccelerators`. Tooltip surface: 4 px radius, elevation 16. Also set `AutomationProperties.Name` on icon-only buttons (tooltip ≠ accessible name in all frameworks).

## 12. Snippets (WinUI 3, WPF, Win32, Electron, Tauri, Flutter)

**WinUI 3 shell: Mica + TitleBar + NavigationView** (composed from https://learn.microsoft.com/windows/apps/develop/ui/controls/title-bar and .../system-backdrops):
```xml
<Window x:Class="App.MainWindow" ...>
  <Window.SystemBackdrop><MicaBackdrop Kind="Base"/></Window.SystemBackdrop> <!-- BaseAlt if tabs in title bar -->
  <Grid RowDefinitions="Auto,*">
    <TitleBar x:Name="AppTitleBar" Title="Contoso Notes" Subtitle="Preview"
              IsBackButtonVisible="True" IsBackButtonEnabled="{x:Bind ContentFrame.CanGoBack, Mode=OneWay}"
              BackRequested="OnBack" IsPaneToggleButtonVisible="True" PaneToggleRequested="OnPaneToggle">
      <TitleBar.IconSource><ImageIconSource ImageSource="ms-appx:///Assets/AppIcon.png"/></TitleBar.IconSource>
      <AutoSuggestBox PlaceholderText="Search" QueryIcon="Find" MinWidth="320" MaxWidth="480"/> <!-- [ContentProperty]=Content; any Content/LeftHeader/RightHeader switches TitleBar 32→48 automatically -->
    </TitleBar>
    <NavigationView x:Name="Nav" Grid.Row="1" IsBackButtonVisible="Collapsed" IsPaneToggleButtonVisible="False"
                    IsSettingsVisible="True" SelectionChanged="OnNav">
      <NavigationView.MenuItems>
        <NavigationViewItem Content="Home" Icon="Home" Tag="home"/>
        <NavigationViewItem Content="Documents" Tag="docs"><NavigationViewItem.Icon><FontIcon Glyph="&#xE8A5;"/></NavigationViewItem.Icon></NavigationViewItem>
      </NavigationView.MenuItems>
      <Frame x:Name="ContentFrame"/>  <!-- NavView paints LayerFillColorDefaultBrush content layer -->
    </NavigationView>
  </Grid>
</Window>
```
```csharp
public MainWindow() {
    InitializeComponent();
    ExtendsContentIntoTitleBar = true;           // hide system title bar, keep system caption buttons (Snap Layouts OK)
    SetTitleBar(AppTitleBar);
    AppWindow.TitleBar.PreferredHeightOption = TitleBarHeightOption.Tall; // make system caption buttons 48 too (TitleBar control does not set this)
    AppWindow.SetIcon("Assets/AppIcon.ico");
    if (AppWindow.Presenter is OverlappedPresenter p) { p.PreferredMinimumWidth = 360; p.PreferredMinimumHeight = 400; } // ≤500 for Snap
}
void OnPaneToggle(TitleBar s, object a) => Nav.IsPaneOpen = !Nav.IsPaneOpen;
void OnBack(TitleBar s, object a) { if (ContentFrame.CanGoBack) ContentFrame.GoBack(); }
void OnNav(NavigationView s, NavigationViewSelectionChangedEventArgs e) =>
    ContentFrame.Navigate(PageFor(e), null, new EntranceNavigationTransitionInfo()); // top-level = page refresh
```
**ContentDialog (destructive confirm)**:
```csharp
var dlg = new ContentDialog {
    XamlRoot = this.Content.XamlRoot,                 // required in WinUI 3
    Title = "Delete 3 files permanently?",
    Content = "You can't undo this action.",
    PrimaryButtonText = "Delete",                     // "do it" on the left
    CloseButtonText = "Cancel",                       // safe action on the right; Esc maps here
    DefaultButton = ContentDialogButton.Close         // don't make Enter delete
};
if (await dlg.ShowAsync() == ContentDialogResult.Primary) { /* delete */ }
```
**Theme resources (custom brush that survives Light/Dark/HighContrast)**:
```xml
<ResourceDictionary.ThemeDictionaries>
  <ResourceDictionary x:Key="Light"><StaticResource x:Key="PanelBg" ResourceKey="CardBackgroundFillColorDefaultBrush"/></ResourceDictionary>
  <ResourceDictionary x:Key="Dark"><StaticResource x:Key="PanelBg" ResourceKey="CardBackgroundFillColorDefaultBrush"/></ResourceDictionary>
  <ResourceDictionary x:Key="HighContrast"><SolidColorBrush x:Key="PanelBg" Color="{ThemeResource SystemColorWindowColor}"/></ResourceDictionary>
</ResourceDictionary.ThemeDictionaries>
<!-- usage: Background="{ThemeResource PanelBg}" BorderBrush="{ThemeResource CardStrokeColorDefaultBrush}" CornerRadius="{StaticResource OverlayCornerRadius}" -->
```
**Honor motion/transparency settings**:
```csharp
var ui = new Windows.UI.ViewManagement.UISettings();
bool motion = ui.AnimationsEnabled, glass = ui.AdvancedEffectsEnabled; double textScale = ui.TextScaleFactor;
ui.AnimationsEnabledChanged += (_, _) => DispatcherQueue.TryEnqueue(UpdateMotion); // events fire off-UI-thread
```
**Other stacks (one-liners):**
- **WPF (.NET 9/10):** `<Application ThemeMode="System">` (or `Light`/`Dark`) or merge `pack://application:,,,/PresentationFramework.Fluent;component/Themes/Fluent.xaml`. Still **experimental** (`#pragma warning disable WPF0001`); .NET 10 added Fluent styles for DatePicker, GridSplitter, GridView, GroupBox, Hyperlink, Label, NavigationWindow, RichTextBox, TextBox and says "Fluent UI style support is still in progress" (https://learn.microsoft.com/dotnet/desktop/wpf/whats-new/net100). Custom styles may block Fluent restyling. Mature alternative: WPF-UI (lepoco) ⚠️.
- **Win32/DWM (build ≥ 22621):** `DwmSetWindowAttribute(hwnd, DWMWA_SYSTEMBACKDROP_TYPE /*38*/, &type, sizeof(type))` with `DWMSBT_MAINWINDOW` (Mica) / `DWMSBT_TABBEDWINDOW` (Mica Alt) / `DWMSBT_TRANSIENTWINDOW` (Acrylic); extend frame into client (`DwmExtendFrameIntoClientArea` margins −1) and paint transparent; dark caption: `DWMWA_USE_IMMERSIVE_DARK_MODE` (20) ⚠️; corners: `DWMWA_WINDOW_CORNER_PREFERENCE` (33) = `DWMWCP_ROUND`; custom caption buttons must return `HTMAXBUTTON` from `WM_NCHITTEST` (https://learn.microsoft.com/windows/win32/api/dwmapi/ne-dwmapi-dwm_systembackdrop_type). Or use `MicaController` via WASDK.
- **Electron:** `new BrowserWindow({ backgroundMaterial: 'mica' /* auto|none|mica|acrylic|tabbed; Win 11 22H2+ */, titleBarStyle: 'hidden', titleBarOverlay: { color: '#00000000', symbolColor: '#…', height: 32 } })` — keeps real caption buttons + Snap Layouts; mark drag areas with `-webkit-app-region: drag` and interactive ones `no-drag`; read `nativeTheme.shouldUseDarkColors`, `systemPreferences.getAccentColor()`, CSS `forced-colors` / `prefers-reduced-motion` (https://www.electronjs.org/docs/latest/api/base-window). Re-set `titleBarOverlay.symbolColor` on theme change.
- **Tauri 2:** `windowEffects: { effects: ["mica"] }` (also `tabbed`, `acrylic`; Mica/Tabbed Win 11 only; acrylic laggy on resize) + transparent window. `decorations: false` **kills Snap Layouts** unless you handle `WM_NCHITTEST`→`HTMAXBUTTON` (community `tauri-plugin-frame`) — prefer native decorations or `titleBarStyle` overlay where available ⚠️ (https://v2.tauri.app/reference/javascript/api/namespacewindow/; https://dev.to/zbrooklyn/windows-11-snap-layouts-in-a-frameless-tauri-app-the-part-every-guide-gets-wrong-2fjh).
- **Flutter:** no first-party Fluent; community `fluent_ui` package for widgets + `flutter_acrylic`/`window_manager` for Mica and title bar ⚠️ (https://github.com/alexmercerind/flutter_acrylic).
- **Qt 6:** use the native `windows11` QStyle (Qt ≥ 6.7) rather than Fusion on Windows ⚠️.

## 13. Inclusive design (persona spectrum)

- Microsoft's definition: "disability = a mismatch between the needs of the individual and the service, product or environment offered" (https://learn.microsoft.com/windows/apps/design/accessibility/designing-inclusive-software). Methodology principles (https://inclusive.microsoft.design/): **Recognize exclusion · Learn from diversity · Solve for one, extend to many.** Windows-doc principles: Think universal · Make it personal · Keep it simple · Create delight.
- **Persona spectrum** (Kat Holmes / Microsoft Inclusive Design toolkit): design each constraint across *permanent → temporary → situational*: Touch = one arm → arm in a cast → holding a child; See = blind → cataract → distracted driver; Hear = deaf → ear infection → loud bar; Speak = non-verbal → laryngitis → heavy accent ⚠️ (examples quoted from secondary sources; toolkit PDF not fetched). Agent translation: one-handed/keyboard-only works, glanceable at 225 % text, no audio-only cues, no voice-only input.
- 57 % of US working-age computer users could benefit from AT (Forrester for Microsoft, 2003–04) (same doc). Define audience in *functional* terms (vision, hearing, cognition, dexterity, literacy, language).
- Choosing the framework is an accessibility decision — standard controls inherit UIA semantics, keyboard behavior and HC support; every custom control is a debt (implement `AutomationPeer`).
- Doc's contrast target: **≥ 5:1 normal text, 3:1 large (18 pt / 14 pt bold)** — ⚠️ stricter than WCAG 2.x AA (4.5:1); use 4.5:1 as the floor and 5:1+ as the Microsoft target.
- ~7 % of males have some color vision deficiency (this doc) vs "8 % of men are red-green colorblind" (color doc) — either way: never color-only state.

## 14. Common mistakes on Windows (checklist for review)

**macOS-isms (wrong on Windows)**
- Traffic-light buttons top-left, or caption buttons drawn by you → Windows caption buttons are **top-right** (top-left in RTL), drawn by the system (§6).
- Dialog buttons "Cancel | OK" with primary on the right → Windows: **primary/"do it" left, Cancel right** (§8).
- Global menu bar assumptions, ⌘ glyphs in menus/tooltips, "Preferences…" → use **Ctrl**, show "Ctrl+S", name it **"Settings"** (NavView built-in item / overflow last item) (§7).
- Ctrl+Shift+Z as the only redo → Windows redo is **Ctrl+Y** (support both). Missing Alt+F4, F2 rename, Del, F5, Ctrl+W, Esc-closes-dialog.
- Title Case Labels ("Save As…") → **sentence case** ("Save as") (§3). Bold for emphasis → SemiBold.
- Sheets sliding from the title bar, popovers with arrows everywhere → ContentDialog (centred, smoke) and Flyout/TeachingTip.
- Thin overlay scroll bars always hidden → use themed system scroll bars that respect "Always show scrollbars".
- Keeping the app alive after the last window closes (mac pattern) → on Windows closing the main window exits the app; tray-resident only for genuine background apps, and say so ⚠️ (convention).

**Fake chrome**
- Custom title bar with hand-drawn min/max/close → **breaks Snap Layouts**, Win+Z, hover tooltips, touch targets, RTL and accessibility. Use system caption buttons (`ExtendsContentIntoTitleBar`, Electron `titleBarOverlay`, Win32 `HTMAXBUTTON`).
- JS/mousemove window dragging instead of real drag regions → loses double-click maximize, Aero Snap drag, system menu.
- Interactive controls inside the drag region without passthrough → unclickable search box/avatar.
- Title bar not dimmed when window inactive; Mica not extended under title bar (visible seam).
- Min window width > 500 epx → snaps fail silently.

**Ignoring user settings**
- Fixed-height rows/buttons that clip at Text size 225 %; text-scaling ignored by custom renderers.
- Hard-coded hex colors / brand colors → invisible text in Dark or contrast themes; `SystemColorGrayTextColor` used for secondary text; colored text on acrylic; raw `SystemAccentColor` used as text color.
- Forcing Dark (or Light) with no "Use system setting" option.
- Custom animations that ignore Animation effects off; custom blur ignoring Transparency effects / battery saver.
- No focus visual (`outline:none`, `UseSystemFocusVisuals=False`), Tab order jumps, icon buttons without accessible names/tooltips, no keyboard path to drag-and-drop or hover-only actions.

**Visual slop tells**
- Every surface in acrylic, acrylic panes side by side, Mica applied twice, or a backdrop on a non-window element (§5).
- Random radii (12/16/20 px pills everywhere) instead of 4/8; mixed icon sets/emoji icons; icons on every menu item.
- Spacing not on the 4-epx grid; content stretched to 2560 px with no max width (use ~1000–1100 px for settings-type pages).
- Toast spam ("Sync complete" every minute, "App is running"), notifications not cleared after the user saw the content.
- InfoBar that flashes in/out; dialogs for inline validation errors; ProgressRing for non-blocking work.
- Heavy drop shadows/neumorphism; Windows uses subtle elevation (control = 2, card = 8, flyout = 32, dialog = 128) plus 1 px strokes.
- Tiny targets (< 32 epx pointer, < 40 epx touch) and close (X) buttons crammed against other actions.

## Unverified / open questions

- **Version drift**: learn.microsoft.com (docs commit 2026-10-14) lists WASDK 2.1.3 as latest; GitHub shows **2.6.4 (2026-10-27)**. Always check NuGet before pinning. Experimental `TableView`/`Chart`/`Window.Width` may change or disappear.
- **Compact density URI** `ms-appx:///Microsoft.UI.Xaml/DensityStyles/Compact.xaml` — file exists in WinUI source, but the docs page ("Control size and density") was removed/redirected in 2026; URI recalled from WinUI 2 era.
- **Card corner radius = 8** and "inner radius = outer − padding" are conventions (Gallery/SettingsCard), not in the geometry doc.
- **CommandBar `DefaultLabelPosition="Right"`** as the Win 11 desktop norm — observed convention, not stated.
- **Destructive-dialog default button** (leave none / Close): doc only says DefaultButton is optional.
- **Backspace as back** — legacy UWP behaviour; not re-verified for WinUI 3.
- **Ctrl+O, Ctrl+E** in the accelerator list: Ctrl+O isn't in Microsoft's table (universal convention); Ctrl+E is listed as "Begin editing mode" (many apps use it for search).
- **Chromium mapping** of Windows "Animation effects" → `prefers-reduced-motion`, and whether Electron/Chromium honors Windows *Text size* scaling — not verified.
- **Segoe UI Variable CSS family names** ("Segoe UI Variable Text/Small/Display") — not verified on a primary page.
- **Fluent System Icons sizes** (16/20/24/28/32/48) and "Filled = selected" convention — from memory of the repo/Fluent 2, not re-fetched.
- **Fluent 2 web shadow → Windows elevation mapping** in §5 is my synthesis.
- **Target sizes for mouse** (≥ 32 hit area) — synthesis; Microsoft only specifies the 7.5 mm / 40 epx touch target.
- **WPF-UI, Flutter `fluent_ui`/`flutter_acrylic`, Qt `windows11` style (Qt ≥ 6.7), Tauri snap-layout plugin** — third-party/community; versions not verified. DWM `DWMWA_USE_IMMERSIVE_DARK_MODE` = 20 from memory.
- **Persona-spectrum examples** taken from secondary sources; the Inclusive Design toolkit PDF wasn't fetched (inclusive.microsoft.design home page doesn't list it).
- **Accent override**: whether overriding `SystemAccentColor` alone regenerates `SystemAccentColorLight*/Dark*` — I believe it doesn't (shades come from the shell), so override all seven; not verified.
- **Conflicts to know**: (a) ellipsis vs clipping (typography vs text-scaling pages); (b) contrast 5:1 (Windows inclusive doc) vs 4.5:1 (WCAG AA); (c) colour-blindness stats 7 % vs 8 %; (d) Fluent 2 web says top-level nav = quick *fade*, Windows `EntranceNavigationTransitionInfo` = slide-up + fade — on Windows follow the Windows control behaviour; (e) Fluent 2 web radius tokens (2/4/6/8/12/16…) and spacing (2/4/6/8/10/12/16/20/24/32) are finer-grained than Windows' 4/8 radius + 4-epx grid — on Windows use the Windows values.
- **.NET 11 / WPF Fluent** — .NET 11 GA expected Nov 2026; whether `ThemeMode` leaves experimental there is unknown as of 2026-11-02.

