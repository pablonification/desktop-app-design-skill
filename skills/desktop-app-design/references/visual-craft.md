# Visual craft and avoiding generic "AI slop" UI

Read this for typography, color systems, depth, radius, density and layout, for the slop-tell table, for case studies of crafted desktop apps, and for the pixel-level polish checklist. Every rule cites its source inline; ⚠️ marks claims that couldn't be fully verified (collected at the end). Researched November 2026 — platform details change, so re-check anything version-specific.

Contents: 0. TL;DR for agents · 1. Refactoring UI principles that matter most · 2. Typography for UI · 3. Color systems · 4. Depth, shape, detail · 5. Density & layout for desktop · 6. Anti-slop: what credible sources say · 7. Slop tell → why it reads generic → do instead · 8. Case studies: crafted desktop apps · 9. Pixel-level polish checklist · 10. Practitioner notes from hand-picked sources · Unverified / open questions · Sources

## 0. TL;DR for agents
1. **Decide tokens before code** (Anthropic skill, Refactoring UI "Limit your choices"): 4–6 named colours, type roles + scale, spacing scale, radius scale, shadow ladder, icon set. Then ask: "would a similar prompt produce this same plan?" If yes, change something on purpose.
2. **Chrome = platform; content = identity.** System UI font, native sizes and behaviours for menus/toolbars/sidebars/controls; brand font, colour and illustration live in the content layer, headings, empty states and one signature element (Apple HIG Branding 2026; Things, Raycast, Linear).
3. **Hierarchy by weight + colour + dimming**, not by making things bigger. De-emphasise the secondary (Linear's dimmer sidebar) instead of shouting the primary.
4. **Perceptual colour**: OKLCH/LCH scales, 12 steps with jobs (Radix), tinted neutrals with tiny chroma, one accent used sparingly, semantic tokens only in components. Dark mode = dark greys, elevation by lightness, desaturated accents — never inverted.
5. **Separate with space → background → hairline → shadow**, in that order. Shadows only on floating layers, two+ layers, tinted, one light source.
6. **Radius scale with concentric nesting** (inner = outer − padding); radius grows with container size.
7. **Desktop density**: 28–32 px rows/controls, 13–14 px UI text, quiet chrome; prose panes capped at ~65–75ch; optional Compact/Comfortable switch.
8. **Numbers and text details**: tabular figures, locale formatting, `…`, curly quotes, `text-wrap: balance/pretty`, middle-truncation + tooltip.
9. **Every state designed**: hover, pressed, focus-visible, selected (focused + unfocused window), disabled, loading, empty, error, overflow, dark mode, high contrast.
10. **Slop = defaults without decisions + decoration without information + missing states** — not any specific font or colour (§6–7). The 2026 Anthropic skill names the new clusters (cream/serif/terracotta, black/acid-green, broadsheet, SaaS-card kit, template chrome).

## 1. Refactoring UI principles that matter most

Source: Adam Wathan & Steve Schoger, *Refactoring UI* (book TOC verified at https://www.refactoringui.com/; free chapter "Building Your Color Palette" at https://refactoringui.com/previews/building-your-color-palette). Section titles below are the book's own; the one-line rules are condensed from the book (numbers marked ⚠️ are from the book but not re-verified online — the full text is paywalled). Motto on the site: "Design with tactics, not talent."

**Process**
- **"Start with a feature, not a layout."** Don't open with the app shell (sidebar + top bar + empty canvas). Design the actual job — e.g. "rename a file and see it update in the list" — then build chrome around it.
- **"Detail comes later" / "Don't design too much."** Grayscale and plain boxes first; colour, shadows and icons last. Ship the simplest version of a feature, then iterate.
- **"Choose a personality."** Font, colour, radius and copy carry personality: serif = classic/elegant, rounded sans = playful, neutral sans = plain; small radius = neutral, large = playful, 0 = formal/serious ⚠️. Decide on purpose, then apply it everywhere.
- **"Limit your choices."** Predefine scales for font size, weight, line height, colour, spacing, width, shadow, radius, border width, opacity — then only pick from them.

**Hierarchy**
- **"Size isn't everything."** Use weight and colour before size: ~2 weights (400–500 normal, 600–700 emphasis; avoid < 400 in UI) and 2–3 text colours (primary dark, secondary grey, tertiary lighter grey) ⚠️.
- **"Don't use grey text on colored backgrounds."** Grey on blue looks dead. Pick a text colour with the *same hue* as the background and adjust saturation/lightness; don't use white at reduced opacity (it lets images/patterns bleed through).
- **"De-emphasize to emphasize."** If the active nav item doesn't pop, soften the inactive ones instead of shouting louder. (Linear's 2026 refresh did exactly this with its sidebar — §8.1.)
- **"Labels are a last resort."** Format data so it explains itself (`jane@acme.com`, `$1,240`, "12 left in stock"); when a label is needed, make it the de-emphasised partner of the value.
- **"Separate visual hierarchy from document hierarchy."** A section title is often just a label: small, semibold, secondary colour — not a huge `<h2>`.
- **"Balance weight and contrast."** Solid icons look heavier than text beside them → give the icon a softer colour. A 1 px border that looks too faint → make it 2 px rather than darker.
- **"Semantics are secondary."** Button styling follows hierarchy, not meaning: primary = solid, secondary = outline/low-contrast fill, tertiary = text link. A destructive action that isn't the page's main action is *not* big and red; save the bold red for the confirmation step.

**Layout & spacing**
- **"Start with too much white space,"** then remove until it feels right.
- **"Establish a spacing and sizing system."** Non-linear; neighbouring values differ by ≥ ~25 %: `4 8 12 16 24 32 48 64 96 128 192 256 384 512 640 768` px ⚠️ (Tailwind's default scale descends from this).
- **"You don't have to fill the whole screen" / "Grids are overrated."** Give elements the width they need; fixed-width sidebars + flexible content beats percentage columns; use `max-width`.
- **"Relative sizing doesn't scale."** Don't derive everything from `em`; a heading's ratio to body text and a button's padding shouldn't scale linearly.
- **"Avoid ambiguous spacing."** More space *between* groups than *within* them — a label sits closer to its own field than to the field above.

**Text**
- **"Establish a type scale."** Hand-picked, e.g. `12 14 16 18 20 24 30 36 48 60 72` px ⚠️; avoid fractional modular-scale values.
- **"Use good fonts."** Neutral sans/system font is a safe start; filter font catalogues for families with many weights (≥ 10 styles) as a crafting signal ⚠️; small UI text wants a tall x-height and looser spacing; display fonts have tighter spacing and short x-height.
- **"Keep your line length in check"** (≈ 45–75 characters, `max-width: 20–35em`) ⚠️. **"Baseline, not center"** when mixing sizes on one line. **"Line-height is proportional"** — small text and long lines need more; big headings need ~1.0–1.2.
- **"Not every link needs a color"** in link-dense UI (use weight/darker colour; underline on hover). **"Align with readability in mind"** — left-align prose, centre only ≤ 2–3 lines, right-align numbers in tables. **"Use letter-spacing effectively"** — tighten large headings, loosen ALL CAPS.

**Color** (see §3) — "You need more colors than you think": "8-10 shades" of grey, "5-10" shades of the primary, accents with shades too — "as many as ten different colors with 5-10 shades each for a complex UI"; "True black tends to look pretty unnatural"; "don't get clever using CSS preprocessor functions like 'lighten' or 'darken'… That's how you end up with 35 slightly different blues"; pick the base as "a shade that would work well as a button background", then darkest (text) and lightest (tinted background), then fill 700/300, then 800/600/400/200; "Trust your eyes, not the numbers" (preview page). Also: "Don't let lightness kill your saturation" (raise saturation toward the ends of the scale); "Greys don't have to be grey" (tint toward blue for cool, yellow/orange for warm); "Accessible doesn't have to mean ugly" (flip to dark text on a light tint instead of white on mid-tone); "Don't rely on color alone."

**Depth** — "Emulate a light source" (light from above: raised = lighter top edge + shadow below; inset = inner shadow at top); "Use shadows to convey elevation" (≈ 5 shadow tokens: button → dropdown → modal ⚠️); **"Shadows can have two parts"**: a larger soft shadow with real Y offset (direct light) + a tight, darker one with ~0 offset (ambient occlusion); the tight one fades as elevation rises; "Even flat designs can have depth" (lighter = closer); "Overlap elements to create layers."

**Finishing touches** — "Supercharge the defaults" (icons instead of bullets, styled checkboxes); "Add color with accent borders" (top of a card, side of an alert, under the active tab); "Decorate your backgrounds" sparingly; **"Don't overlook empty states"** (they're a first impression; hide filters/tabs that do nothing yet); **"Use fewer borders"** (use a shadow, a background shift, or more space instead); "Think outside the box" (menus with sections/icons, radio buttons as selectable cards). Images: "Everything has an intended size" — don't blow up 16–24 px icons to 3×; put them in a shape or use a larger-size icon set ⚠️; "Beware user-uploaded content" (fixed aspect + `object-fit`, inset shadow instead of border so edges don't bleed).

## 2. Typography for UI

### 2.1 Body text numbers (Butterick) — and why desktop chrome differs
Matthew Butterick, *Practical Typography* (https://practicaltypography.com/typography-in-ten-minutes.html, https://practicaltypography.com/summary-of-key-rules.html — site was refusing connections 2026-11-02; read via web.archive.org): point size "15-25 pixels on the web"; line spacing "120–145% of the point size" (CSS: unitless, e.g. `1.3`); line length "45–90 characters (including spaces)" or "2–3 lowercase alphabets"; "Use 5–12% extra letterspacing with all caps and small caps"; "Kerning should always be turned on"; "All caps are fine for less than one line of text"; "Use bold or italic as little as possible, and not together"; curly quotes; real ellipsis `…`; "Use centered text sparingly."
- **Apply to *content* panes** (documents, notes, articles, long descriptions, chat transcripts). **Not to chrome**: desktop UI text is smaller by convention — macOS body 13 pt, Windows 14 epx (see macos.md / windows.md). A 16 px web-style body in a Mac sidebar is a "port smell".
- Butterick says avoid system fonts for *documents*; for app chrome the opposite is true (§2.6). No conflict once you separate chrome from content.

### 2.2 Apple: optical size, tracking, leading (WWDC20 "The details of UI typography", Loïc Sander)
https://developer.apple.com/videos/play/wwdc2020/10175/
- SF originally had two cuts: "SF Text for small sizes below 20 points and SF Display for 20 points and above." Variable SF: "the design now transitions from Text to Display between 17 and 28 points." Small cuts have looser spacing and taller proportions.
- **Tracking must be size-specific**: "When type becomes smaller, letters tend to need more space between them"; "a tracking you provided for small sizes may not look good on large sizes." Use *tracking* (not kerning) to adjust spacing — kerning APIs break ligatures.
- **Leading**: tight/loose leading = −2 / +2 pt on iOS/macOS (body 22 → 20 tight / 24 loose). Apple applies more leading for Arabic and other tall scripts automatically — don't hard-code line heights that clip them.
- System handles optical size for "any custom variable font you might use, as long as it has an optical size axis." Prefer `.allowsTightening(true)` / `allowsDefaultTighteningForTruncation` over shrinking the font size.

### 2.3 Variable fonts and optical sizing on the web stack (Electron/Tauri)
- CSS `font-optical-sizing: auto` (default) maps the `opsz` axis to font-size for variable fonts that have one; override only on purpose: `font-variation-settings: "opsz" 32`.
- If your font has **no** `opsz` axis, emulate it: negative tracking on large sizes, slightly positive on 11–12 px. Example tokens (our synthesis — tune per font):
```css
--track-display: -0.022em;  /* ≥ 32px */
--track-title:   -0.012em;  /* 20–28px */
--track-body:     0;        /* 13–16px */
--track-small:   +0.01em;   /* 11–12px */
--track-caps:    +0.06em;   /* ALL CAPS / small caps: Butterick 5–12% */
```
- Inter ≥ 4.0 ships an optical-size axis / "Inter Display" (Linear adopted "Inter Display to add more expression to our headings", 2024 — https://linear.app/now/how-we-redesigned-the-linear-ui). The old Inter "dynamic metrics" page is gone (https://rsms.me/inter/dynmetrics/ → 404, archived at d.rsms.me) ⚠️.

### 2.4 Numbers, dates and small details
- **Tabular figures wherever numbers align or change**: tables, timers, file sizes, prices, counters, progress %: `font-variant-numeric: tabular-nums;` (SwiftUI `.monospacedDigit()`; WinUI `Typography.NumeralAlignment="Tabular"` ⚠️). Proportional figures in running prose. Vercel: "Tabular numbers for comparisons" (https://vercel.com/design/guidelines). Geist: Label 13 for secondary data — "Use tabular figures for numbers" (https://vercel.com/geist/typography).
- Consider `slashed-zero` for IDs/codes; `font-variant-numeric: lining-nums` if a serif defaults to old-style figures in UI.
- **Format with the platform, never by hand**: `Intl.NumberFormat`, `Intl.DateTimeFormat`, `Intl.RelativeTimeFormat`, `Intl.ListFormat` (web); `.formatted()` / `FormatStyle` (Swift). Respect the user's locale (Vercel: "Locale-aware formats"). Units: `10&nbsp;MB`; currency 0 or 2 decimals consistently in one context (Vercel copy rules).
- **`text-wrap`**: `balance` for headings/captions/empty-state titles, `pretty` for paragraphs (Josh Comeau's reset, updated 2026-06-03: https://www.joshwcomeau.com/css/custom-css-reset/). WebKit (Jen Simmons, 2025-04-08, https://webkit.org/blog/16547/better-typography-with-text-wrap-pretty/): "`pretty` can be applied to any text"; use `balance` only where you want equal line lengths; Safari's `pretty` evaluates the whole paragraph. Balance line caps: MDN says ≤ 6 lines Chromium / ≤ 10 Firefox; WebKit's post says Chromium = 4 ⚠️ (conflict). Both are progressive enhancement.
- **Font smoothing (macOS)**: Comeau keeps `-webkit-font-smoothing: antialiased` on `body` — his reasoning: macOS turned subpixel AA off system-wide in Mojave, yet browsers still default to it ⚠️ (his claim, not tested); no effect on Windows/Linux. Practitioner opinion; it makes light-on-dark text look less heavy. Animating/scaling text changes smoothing → animate a wrapper (Vercel).
- **Truncation**: single-line labels → `text-overflow: ellipsis` + full text in a tooltip/title; never truncate the distinguishing part (middle-truncate file names/paths: `report-2026…final.pdf`). Allow `overflow-wrap: break-word` for long URLs/IDs in content.
- Real typographic characters: `…` `’` `“ ”` `–` `—` `×` `⌘`. Sentence case for UI labels unless the platform says otherwise (macOS HIG uses title case for menu items and buttons — see macos.md).

### 2.5 Picking a typeface with character (without hurting legibility)
Checklist (synthesis of Refactoring UI "Use good fonts", Butterick, Anthropic skill):
1. **Job first**: is this font for chrome (labels, menus, tables at 11–14 px) or for content/headings (16 px+)? Character goes mostly in the second.
2. **Legibility tests at 11–13 px on a 1× Windows display at 100 % scaling** (worst case): distinct `Il1`, `0O`, `rn/m`; open apertures (`a e c s`); tall x-height; no hairline strokes.
3. **Completeness**: ≥ 4 weights + italics, tabular figures (`tnum`), case-sensitive punctuation, arrows, your languages (Latin Extended, Cyrillic, Greek, CJK fallback). Variable font with `wght` (+ `opsz` ideally).
4. **License** allows app embedding (desktop apps bundle fonts — web-font licences often don't cover this ⚠️).
5. **Pairing**: one family is enough. If two, make them clearly different (Anthropic: "use one family or two, and if two, make them clearly distinct"): serif display + sans UI, or sans UI + mono for code/data. Mono only where content *is* code, IDs, or aligned data — Anthropic lists "a monospace face for small data labels" as a slop tell.
6. **Avoid the default-without-decision**: Inter/Roboto/system are fine choices *when chosen*; the tell is no type scale, no weight discipline, no tracking adjustments, every heading the same size.

### 2.6 System font for chrome, brand font for content (desktop rule)
- **Chrome** (menus, toolbars, sidebars, tables, form controls, dialogs, tooltips, status bars): the platform UI font at the platform size — SF Pro (macOS), Segoe UI Variable (Windows 11), the desktop's font on Linux (GNOME/KDE; see linux.md). CSS stack for web-tech shells: `font: 13px/1.38 system-ui, -apple-system, "Segoe UI Variable Text", "Segoe UI", "Adwaita Sans", Cantarell, "Noto Sans", sans-serif;` ⚠️ (verify `system-ui` mapping per OS; set the size per platform).
- **Content and identity** (document titles, empty-state headlines, onboarding, the editor surface, marketing/about window): your brand/display face. Apple HIG Branding: "use a custom font for headlines and subheadings while using system fonts for body copy and captions" (§4.6). Bear goes further — its custom Bear Sans runs in editor *and* UI, but it was engineered for small-size legibility (§8.6); Linear uses Inter + Inter Display everywhere because that *is* its identity.
- Native frameworks: SwiftUI `.font(.system(.body))` for chrome; `.font(.custom("…", size:, relativeTo: .body))` for content so it still scales (WWDC20).

## 3. Color systems

### 3.1 Use a perceptual color space (OKLCH / LCH / Lab), not HSL
- HSL lightness lies: Stripe — "at the same level of mathematical lightness, yellow appears lighter than blue"; they rebuilt their palette in CIELAB (Koopersmith & Miner, 2019-10-15, https://stripe.com/blog/accessible-color-systems). Evil Martians — "HSL lightness is not consistent across hue axes" (Sitnik & Turner, https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl, page dated 2025-09-17).
- OKLCH syntax `oklch(L C H / a)`: L 0–1, C 0 to < 0.37, H 0–360 (red ≈ 20, yellow ≈ 90, green ≈ 140, blue ≈ 220, purple ≈ 320). "All browsers support `oklch()`" and relative colours (Evil Martians changelog 2024-07-13) → safe in Electron, WebView2, WKWebView, WebKitGTK.
- Hover/pressed by moving **L only**: `oklch(from var(--accent) calc(l - 0.05) c h)` (use decimals, `%` doesn't work in that `calc`). P3 colours go in `@media (color-gamut: p3)` with an sRGB base value. Chrome/Safari *clip* out-of-gamut colours rather than mapping them — keep chroma modest for UI.
- Refactoring UI says "Ditch hex for HSL" (2018); in 2026 the same advice reads "ditch hex for OKLCH" — the principle (think in hue/lightness/saturation, define shades up front) is unchanged.

### 3.2 A 12-step scale with jobs (Radix Colors)
Source: https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale
| Steps | Job |
|---|---|
| 1 | App background |
| 2 | Subtle surfaces: sidebars, cards, code blocks, striped rows, canvas |
| 3 / 4 / 5 | Component bg: normal / hover / pressed-or-selected (3 = hover when the component is transparent at rest) |
| 6 / 7 / 8 | Borders: non-interactive separators / interactive components / stronger + focus rings + hovered borders |
| 9 / 10 | Solid fills ("the purest step", highest chroma) / their hover |
| 11 / 12 | Low-contrast text / high-contrast text — "guaranteed to Lc 60" and "Lc 90" APCA on step 2 of the same scale |
- Most step-9 colours are designed for white text; **Sky, Mint, Lime, Yellow, Amber step 9 need dark text.**
- Greys: pure `gray`, or tinted `mauve` (purple), `slate` (blue), `sage` (green), `olive` (lime/grass), `sand` (yellow/amber/orange) — pick the grey whose hue is closest to your accent. "Be careful when using saturated grays for your app background, especially in dark mode." Text: gray 11/12 "for apps", accent 11/12 feels more marketing (https://www.radix-ui.com/colors/docs/palette-composition/composing-a-palette).
- Stripe's rule of thumb for any numbered scale: colours "at least five levels apart" pass small-text contrast; "four levels apart for icons and large text"; for badges shift "both the background and the text color up one level" to keep contrast consistent across hues.

### 3.3 Linear's approach: generate themes from three inputs
- 2024 redesign (Karri Saarinen et al., 2024-03-28, https://linear.app/now/how-we-redesigned-the-linear-ui): moved theme generation from HSL to **LCH** ("perceptually uniform"); "instead of having to define 98 specific variables for each theme, we defined three: **base color, accent color, and contrast**." Contrast is a dial → "super high-contrast themes for users who need it for accessibility." LCH also drives surface elevation (background → panels → dialogs → modals). They *limited* "how much chrome (blue in our case)" leaked into neutrals for "a more neutral and timeless appearance", and made text and neutral icons "darker in light mode and lighter in dark mode." Explorations were done "mostly with opacities of black and white."
- 2026 refresh (Charlie Aufmann & Maxime Heckel, 2026-03-12, https://linear.app/now/behind-the-latest-design-refresh): moved from "a cool, blue-ish hue" to a "warmer gray that still feels crisp, but less saturated" (warn: "too warm" looks muddy). Built the colour-picker tool with Claude Code; exported tokens as JSON → Figma plugin.
- **Copyable pattern**: let the user pick base + accent (+ contrast); derive every surface/border/text token by moving L in OKLCH/LCH; keep neutral chroma tiny (≈ 0.002–0.012).

### 3.4 Token sketch (OKLCH, tinted neutrals, hue 255) — contrast computed by us
```css
:root { /* light */
  --n1: oklch(0.995 0.002 255); /* #fcfdff app bg            */
  --n2: oklch(0.982 0.003 255); /* #f8f9fb sidebar / subtle   */
  --n3: oklch(0.962 0.004 255); /* #f1f3f5 control bg         */
  --n4: oklch(0.945 0.005 255); /* #ebedf0 hover              */
  --n5: oklch(0.925 0.006 255); /* #e4e6ea pressed / selected */
  --n6: oklch(0.900 0.007 255); /* #dbdee3 separators         */
  --n7: oklch(0.865 0.008 255); /* #cfd3d8 control border     */
  --n8: oklch(0.780 0.010 255); /* #b3b8be strong border      */
  --n9: oklch(0.640 0.012 255); /* #878d94 placeholder/icons/input border: 3.3:1 on n1 */
  --n10: oklch(0.600 0.012 255);/* #7b8187 */
  --n11: oklch(0.500 0.012 255);/* #5f646a secondary text: 5.9:1 on n1, 4.8:1 on n5 */
  --n12: oklch(0.230 0.012 255);/* #191d23 primary text: 16.6:1 */
  --accent: oklch(0.55 0.17 255);      /* #1570d1 — white label 4.9:1 */
  --accent-hover: oklch(from var(--accent) calc(l - 0.04) c h);
  --accent-text: oklch(0.50 0.15 255); /* #1762b6 links on n1: 6.0:1 */
  --accent-tint: oklch(0.95 0.03 255); /* selected-row bg */
}
@media (prefers-color-scheme: dark) { :root {
  --n1: oklch(0.170 0.004 255); /* #0e0f11 window bg (not #000) */
  --n2: oklch(0.195 0.005 255); /* #131517 */
  --n3: oklch(0.225 0.006 255); /* #1a1c1f raised panel / control */
  --n4: oklch(0.250 0.007 255); /* #1f2225 hover */
  --n5: oklch(0.280 0.008 255); /* #26292d popover / selected */
  --n6: oklch(0.310 0.009 255); /* #2d3135 separators */
  --n7: oklch(0.355 0.010 255); /* #383c41 control border */
  --n8: oklch(0.440 0.012 255); /* #4e5359 strong border */
  --n9: oklch(0.600 0.012 255); /* #7b8187 icons/input border: 4.9:1 on n1 */
  --n11: oklch(0.760 0.010 255);/* #adb1b7 secondary: 8.9:1 */
  --n12: oklch(0.950 0.005 255);/* #eceff2 primary: 16.5:1 (not pure white) */
  --accent-text: oklch(0.78 0.11 255); /* #87bafd — lighter + less chroma: 9.6:1 */
  --accent-tint: oklch(0.30 0.05 255);  /* selected-row bg */
  /* keep --accent fill dark enough for a white label; #4087de would only give 3.7:1 */
}}
```
Semantic layer on top (components never use raw steps): `--bg-app --bg-sidebar --bg-control --bg-hover --bg-selected --border-subtle --border-control --border-focus --text-primary --text-secondary --text-disabled --accent-solid --accent-text --danger-solid --danger-text …`. Values above verified with a WCAG 2 contrast script (OKLCH→sRGB); borders n6–n8 are 1.3–2.5:1, so **when a border is the only thing showing where an input is, use n9 or darker (≥ 3:1, WCAG 1.4.11).**

### 3.5 Neutrals, accent discipline, meaning
- Almost everything is grey (Refactoring UI). Tint greys slightly toward the accent (or toward warm for "calm" products — Linear 2026). Raise chroma a touch at the light/dark ends so the temperature survives.
- **One accent, used sparingly**: primary button, selection, focus, links, one key data point. On macOS honour the user's accent colour for selection/focus (see macos.md). Linear removed "colored team icon backgrounds" in 2026 because colour everywhere competed for attention.
- Semantic colours (danger/success/warning/info) get their own scales; never re-use the brand accent as "success".
- Never colour alone for status (Refactoring UI; Vercel "Redundant status cues").
- Text on coloured fills: same-hue darker/lighter text, not grey and not `rgba(255,255,255,.6)` (Refactoring UI).

### 3.6 Dark mode
- **Not pure black.** Material's baseline dark surface is `#121212` — light text on dark grey has less glare than on black (https://m2.material.io/design/color/dark-theme). Pure `#000` is reserved for OLED/"true black" options and full-screen media.
- **Elevation = lighter surface**, not bigger shadow: Material M2 overlays white at increasing opacity as elevation rises; M3 uses a surface tint. Our scale: each level up ≈ +0.025–0.04 L.
- **Desaturate and lighten accents** for text/icons on dark (Material uses the 200 tone of the primary); keep solid fills dark enough for their label.
- **Primary text not pure white** (≈ L 0.93–0.96); secondary ≈ L 0.72–0.78. Borders become *lighter* than the surface, not darker; shadows nearly vanish — use a 1 px light inner/outer border (`inset 0 0 0 1px oklch(1 0 0 / .06)`) to separate layers.
- **Re-check every pair** in dark mode; contrast doesn't invert linearly. Dim large white images/illustrations.
- `color-scheme: light dark` on `:root` so native scrollbars/form controls follow (Vercel). Offer System / Light / Dark — never force one.

### 3.7 Contrast standard (status Nov 2026)
- **Ship to WCAG 2.2 AA**: 4.5:1 text, 3:1 large text, 3:1 UI component boundaries and icons. APCA is a better perceptual model and Radix/Vercel use it, but "The contrast algorithm used in WCAG 3 is yet to be determined" (WCAG 3 editor's draft, April 2026); APCA was dropped from the draft in July 2023; WCAG 3 is "years away" (Adrian Roselli, https://adrianroselli.com/2026/04/wcag3-contrast-as-of-april-2026.html). Use APCA as a second opinion (e.g. thin light text in dark mode), not instead of WCAG 2.

## 4. Depth, shape, detail

### 4.1 Pick one separation tool per boundary: space → background shift → border → shadow
Order of preference (Refactoring UI "Use fewer borders"; Linear 2026 "Structure should be felt not seen"):
1. **Space** (group by proximity — Fluent: "Space can group content without lines or dividers", https://fluent2.microsoft.design/layout).
2. **Background shift** (sidebar on n2, content on n1; selected row on n5).
3. **Hairline border** (n6 for structure, n7 for controls).
4. **Shadow** — only for things that *float* above the window: menus, popovers, tooltips, dragged items, sheets, toasts. Cards sitting in a pane rarely need one.
- Linear 2026: dividers had "quietly proliferated across the platform, sometimes appearing without clear reason" → fewer separators, softer contrast (https://linear.app/now/behind-the-latest-design-refresh).
- Before → after: `.panel{border:1px solid #e5e7eb; box-shadow:0 1px 3px rgba(0,0,0,.1)}` on every block → panes separated by n1/n2 backgrounds + one n6 hairline between sidebar and content; shadow only on the popover.

### 4.2 Shadows that look real
- **Two parts** (Refactoring UI): a soft offset shadow (direct light) + a tight low-offset one (ambient occlusion). Vercel: "at least two layers." Josh Comeau (https://www.joshwcomeau.com/css/designing-shadows/): one light source for the whole app (offsets all point the same way, y ≈ 2× x or x = 0); higher = bigger offset + bigger blur + lower opacity; tint shadows with the background hue instead of black ("pure transparent black… desaturates the background"); don't animate layered shadows (expensive) — animate opacity of a pseudo-element instead.
```css
--shadow-color: 220 15% 20%;           /* tinted, not pure black */
--elev-1: 0 0.5px 1px hsl(var(--shadow-color) / .10),
          0 1px 2px  hsl(var(--shadow-color) / .06);                 /* buttons, inputs (optional) */
--elev-2: 0 1px 2px  hsl(var(--shadow-color) / .08),
          0 4px 8px  hsl(var(--shadow-color) / .08),
          0 0 0 0.5px hsl(var(--shadow-color) / .12);                /* menus, popovers */
--elev-3: 0 2px 4px  hsl(var(--shadow-color) / .06),
          0 8px 16px hsl(var(--shadow-color) / .08),
          0 24px 48px hsl(var(--shadow-color) / .12),
          0 0 0 0.5px hsl(var(--shadow-color) / .14);                /* sheets, dialogs, command palette */
/* dark mode: shadows barely read — keep them but add a light edge */
--elev-2-dark: 0 4px 16px oklch(0 0 0 / .5), inset 0 0 0 1px oklch(1 0 0 / .07);
```
(The values are our synthesis following Comeau + Vercel; the 0.5 px ring is the "crisp border" Vercel describes. Windows' native elevation ladder — control 2, card 8, flyout 32, dialog 128 — is in windows.md.)
- **Inset/pressed**: `inset 0 1px 2px hsl(var(--shadow-color)/.12)`; raised buttons may take a 1 px lighter top highlight `inset 0 1px 0 oklch(1 0 0/.12)` (Refactoring UI "Emulate a light source").

### 4.3 Hairlines on HiDPI
- On 2× displays a 1 px CSS border is 2 device px — often heavier than native separators. Use a translucent border so it adapts to any surface: `border: 1px solid oklch(0 0 0 / .08)` (light), `oklch(1 0 0 / .08)` (dark) — Vercel: "semi-transparent borders improve edge clarity."
- True hairlines: `@media (min-resolution: 2dppx) { .sep { border-width: 0.5px } }` or `box-shadow: 0 0 0 0.5px …` ⚠️ (engines differ in how they round sub-pixel borders; check on 1×, 1.25×, 1.5× Windows scaling where 0.5 px can vanish or snap). Native: `NSBox` separator / `Divider()` / WinUI `MenuFlyoutSeparator` draw the platform's own hairline — prefer them.
- Separators inset to the text start (not edge-to-edge) in lists read lighter; full-bleed only between major regions.

### 4.4 Radius: a small scale, concentric nesting
- **Scale** (pick ≈ 4 values + full): e.g. `--r-xs 4` (checkbox, tag), `--r-sm 6` (buttons, inputs, menu items), `--r-md 8–10` (popovers, cards), `--r-lg 12–16` (sheets, dialogs, windows), `--r-full`. Primer: small 3, **medium 6 (default)**, large 12 (`@primer/primitives` 11.10, `radius.css`). Platform window/control radii differ — macOS 26 and Windows 11 values are in macos.md / windows.md; match the OS for anything that touches the window edge.
- **Concentric**: inner radius = outer radius − padding (min ~2–4). A 12 px popover with 4 px padding → 8 px item highlight. Vercel: "Child radius ≤ parent radius & concentric so curves align." Apple: standard toolbar components "have corner radii that are concentric with bar corners. If you need to create a custom component, ensure that its corner radius is also concentric" (https://developer.apple.com/design/human-interface-guidelines/toolbars).
```css
.menu      { --pad: 4px; border-radius: 12px; padding: var(--pad); }
.menu-item { border-radius: calc(12px - var(--pad)); }  /* 8px */
```
- **Radius encodes hierarchy**: bigger containers, bigger radius. "One border-radius on everything regardless of hierarchy" is an Anthropic-listed tell (§6.1). Huge radii (20–24 px) on small controls read as mobile/toy.

### 4.5 Optical alignment and icons
- **Align by what the eye sees**: Vercel — "Adjust ±1px when perception beats geometry"; HIG Icons — asymmetric icons (e.g. download arrow, play triangle) may need padding to look centred. Text aligns on baselines/cap height, icons on their visible bounds.
- **One icon family, one stroke, one corner style.** HIG: icons need "a consistent size, level of detail, stroke thickness (or weight), and perspective"; "match the weights of interface icons and adjacent text." SF Symbols: nine weights mapped to SF font weights; three scales "defined relative to the cap height" (HIG SF Symbols). Raycast's 2022 redesign drew its own outline set with "a bolder stroke width" and shared rules for stroke and corner radii (Thomas Paul Mann, 2022-07-19, https://www.raycast.com/blog/a-fresh-look-and-feel). Figma UI3: "200 expressive icons hand-drawn by designer Tim Van Damme" (https://www.figma.com/blog/behind-our-redesign-ui3/). Sketch Copenhagen: "over 700 new icons" (§8).
- **Icon size relative to text** (desktop): 16 px icon beside 13 px text; 20 px beside 15–17 px; toolbar glyphs ~16–18 px in a 28–32 px target ⚠️ (synthesis; Windows uses Fluent 16/20 sizes — see windows.md). Icon box ≈ text line-height so rows don't jump.
- Web icon sets drawn on a 24 grid with `stroke-width: 2` look heavy at 16 px; scale stroke down (`1.5`) or use a non-scaling stroke so all sizes share one visual weight ⚠️ (Lucide exposes `absoluteStrokeWidth`; docs page moved, not re-verified). Vercel: "a thin-stroke icon may need a bolder stroke next to medium-weight text."
- Don't scale small icons up 3× for "feature" illustrations — "Everything has an intended size" (Refactoring UI).

### 4.6 Brand inside native chrome (Apple HIG Branding, refined 2026-09-09)
- "Apply your app's accent color judiciously… Minimize its use on controls and instead use it intentionally for primary actions or status indicators… consider moving it into the content layer."
- "It can work well to use a custom font for headlines and subheadings while using system fonts for body copy and captions."
- "Express your brand with familiar components… ensure that details like sizing, placement, and behavior continue to preserve a familiar experience." "Ensure branding always defers to content." (https://developer.apple.com/design/human-interface-guidelines/branding)

## 5. Density & layout for desktop

### 5.1 Density is a feature — offer it, don't fake it
- Desktop users sit 50–70 cm away with a precise pointer; information density is expected. Linear 2026: "preserving that rich density of information without letting the interface feel overwhelming." The trick is **quiet chrome**: dim navigation, fewer separators, smaller icons, one accent — not bigger padding.
- **Control-height ladder** (Primer, `@primer/primitives` 11.10 `size.css`): xsmall 24 · small 28 · **medium 32** · large 40 · xlarge 48 px; inline padding 12 px (8 at xsmall); gap 4–8. Stack spacing presets: condensed 8 / normal 16 / spacious 24. A good default for a web-tech desktop app: 28 px rows/controls in dense views (tables, sidebars), 32 px default, 40 px only for hero CTAs. Platform-native sizes (macOS control sizes, Windows compact 24/standard 32 ⚠️) are in the platform files.
- **Two densities max** ("Comfortable" and "Compact") via one token switch — change row height, vertical padding and font-size by one step, never the type family or icon set. Raycast ships a "Compact Mode" that "blends all other elements for a minimal appearance" (2022 blog).
- Fluent spacing ramp (https://fluent2.microsoft.design/layout): 0, 2, 4, 6, 8, 10, 12, 16, 20, 24, 28, 32, 36, 40, 48, 52, 56 — "The base unit is four pixels"; 2/6/10 exist to optically align icons. Fluent: "use spacers as a tool for creating consistency, rather than blindly using consistent spacers"; "Too much dense information can also be disorienting."

### 5.2 Grids and alignment
- A desktop window is not a 12-column marketing page. Use a **fixed-width sidebar + flexible content (+ optional fixed inspector)**: Refactoring UI "Grids are overrated" (fixed sidebar, flexible main). Primer split pages: "The pane region of a split page layout is always flushed to the left"; full pages cap at 1280 px; padding 16 (24 at ≥ 1280) (https://primer.style/product/getting-started/foundations/layout/).
- **One leading edge per region**: sidebar icons, labels, section headers and the search field share left edges; the content title aligns with the first column of the table under it. Linear's 2024 redesign spent time "aligning labels, icons, and buttons, both vertically and horizontally in the sidebar and tabs."
- **4 px grid** for everything, 2 px allowed inside controls for optical fixes (Fluent).
- Fluent alignment: "Align objects (images, icons) centrally and align text left." Numbers right-aligned in tables, with tabular figures.

### 5.3 Typical desktop regions (starting numbers — tune per platform)
| Region | Width / height | Notes |
|---|---|---|
| Sidebar (source list) | 200–260 px default, user-resizable 160–400, collapsible | Dimmer than content (Linear 2026 made it "a few notches dimmer"); row 24–32 px; section headers small + secondary colour, not caps-eyebrows |
| List / middle column | 280–400 px | Two-line rows: title (primary) + meta (secondary, tabular nums) |
| Content / editor | flexible; **prose `max-width: 65–75ch`**, centred or left-aligned within the pane | Butterick 45–90 chars; Anthropic "less than 80 characters"; tables and canvases use full width |
| Inspector | 240–320 px, right side, resizable | Labels left (secondary), values right; group with section headers + space, not boxes |
| Toolbar / title bar | platform height (see macos.md / windows.md) | Max ~5–7 visible actions; overflow menu for the rest |
| Status bar | 22–28 px, 11–12 px text, secondary colour | Counts, sync state, cursor position; tabular nums; clickable segments with hover states |
(Widths are our synthesis of common Mac/Windows pro apps ⚠️ — the platform HIGs give few hard numbers.)

### 5.4 Density done well — what to copy
- **Linear**: hierarchy by *dimming* (inactive sidebar items and nav recede: "Don't compete for attention you haven't earned"), compact icon-only tabs, consistent header action placement, fewer icons and no decorative icon backgrounds.
- **GitHub Primer**: explicit control-size tokens and condensed/normal/spacious stack presets; default radius 6; tables with tight rows but generous column gutters.
- **Figma UI3**: optional labels — "Turn on labels to quickly understand what each control does, or turn them off to focus on your work"; resizable panels; "Minimize UI". They *reverted* floating panels: they "cramped the canvas", and "The nail in the coffin was learning that they slowed people down" (Jenny Xie, 2024-10-01, https://www.figma.com/blog/our-approach-to-designing-ui3/). Lesson: fixed, resizable panels beat floaty novelty in tools.
- **Sketch Copenhagen (2025)**: fixed sidebar ("felt less distracting in the context of a canvas-based design tool"); context-aware toolbar; Liquid Glass only on toolbar/minimap/notifications, *not* sidebars or Inspector.

## 6. Anti-slop: what credible sources say

### 6.1 Anthropic `frontend-design` skill — three versions, and the lesson in between
Source: https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md (history: 2025-12-04, 2026-06-09, **2026-09-03** "avoid generic design defaults", PR #1713).

- **2025 version** (and the cookbook prompt, https://github.com/anthropics/claude-cookbooks/blob/main/coding/prompting_for_frontend_aesthetics.ipynb): "You tend to converge toward generic, 'on distribution' outputs… what users call the 'AI slop' aesthetic." Named tells: "overused font families (Inter, Roboto, Arial, system fonts)", "purple gradients on white backgrounds", "predictable layouts", "cookie-cutter design". It pushed *bold* moves: extreme weights ("100/200 weight vs 800/900, not 400 vs 600"), "size jumps of 3x+", gradient meshes, noise, grain — and warned "You still tend to converge on common choices (Space Grotesk, for example)". Three strategies that worked: (1) steer each design dimension separately (type, color, motion, backgrounds), (2) name inspirations ("IDE themes and cultural aesthetics"), (3) call out the defaults explicitly.
- **The 2026 correction** — the anti-slop prompt created *new* slop. The Sept 2026 skill says AI design "clusters around" five looks, all "defaults rather than choices":
  1. warm cream background (~`#F4F1EA`) + high-contrast serif display + terracotta/clay accent (~`#D97757`, "Anthropic's own Claude-interaction accent, so on a user's brief it reads as a tell");
  2. near-black background + one acid-green or vermilion accent;
  3. broadsheet layout: hairline rules, zero radius, dense newspaper columns;
  4. "the SaaS-card kit: content chopped into identical rounded cards, one border-radius on everything regardless of hierarchy, the same soft grey shadow (rgba(0,0,0,.1)) under each, and gradient washes as decoration";
  5. "template chrome": tracked-out ALL-CAPS eyebrow above every heading; meta strings joined with middle dots ("A · B · C"); "WORD — fragment" labels; tinted near-black (`#0B0B0B`, `#111`) standing in for black; monospace for small data labels; "→" appended to link/button text.
- **Typographic tells it lists:** accenting one word in a headline (italic/bold/colour); all-caps labels; "unnecessary typographic labels above content"; numbered markers (01/02/03) when the content isn't a sequence. "Structural devices… encode useful information about the content rather than decorate it."
- **Motion tell:** "fade-and-slide-up entrances on each section and hover transitions on every card are the generic default and read as AI-generated." Motion that answers a person's action is welcome.
- **Process it prescribes (copy this):** before code, write a token plan — palette as **4–6 named hex values**, typefaces + roles, a layout concept with ASCII wireframes and alignment, and principles. Then "work through a similar prompt to see if you arrive somewhere similar"; if so, revise and say why. "Spend your boldness in one place." "Remove one accessory" (Chanel). Quality floor "without announcing it": responsive, visible focus, reduced motion, accessible contrast. Screenshot and critique your own output.
- **Desktop caveat (our synthesis):** the 2025 "never system fonts" rule is wrong for desktop *chrome* — native-feeling chrome needs the system UI font (see §2.6). Character goes in content, headings, empty states, icon, and one signature element — not in re-skinned menus and buttons.

### 6.2 Vercel Web Interface Guidelines (living list; repo updated 2026-10-05)
Source: https://vercel.com/design/guidelines · https://github.com/vercel-labs/web-interface-guidelines (README + AGENTS.md). Installable review skill: `npx skills add https://github.com/vercel-labs/agent-skills --skill web-design-guidelines`. Items most relevant to desktop web-tech apps (paraphrased tightly; quotes marked):

- **Interactions:** keyboard works everywhere (WAI-ARIA APG patterns); `:focus-visible` rings, `:focus-within` for groups; sticky bars never cover the focused element; visual target = hit target, expand to ≥ 24 px if smaller; loading buttons keep their label + show a spinner; spinners/skeletons get a ~150–300 ms show-delay and ~300–500 ms minimum visible time; optimistic updates with rollback/Undo; "Rename…", "Saving…" use an ellipsis; confirm destructive actions **or** offer Undo; "Delay the first tooltip in a group; subsequent peers have no delay"; `overscroll-behavior: contain` in modals/drawers; **desktop rubber-banding: `overscroll-behavior: none` on `<html>` inside `@media (pointer: fine)`** (added 2026-10-05); autofocus the single primary input on desktop; "No dead zones"; disable selection + `inert` while dragging; every gesture has a click + keyboard alternative; links are `<a>`; aria-live for async updates; locale-aware shortcuts with platform symbols.
- **Animations:** honor `prefers-reduced-motion`; CSS > WAAPI > JS; animate `transform`/`opacity` only; "Never `transition: all`"; interruptible; correct `transform-origin`; SVG transforms on `<g>` with `transform-box: fill-box`.
- **Layout:** "Optical alignment. Adjust ±1px when perception beats geometry"; "Every element aligns with something intentionally"; balance icon/text lockups (thin icon next to medium text may need a bolder stroke); test ultra-wide (zoom to 50 %); "No excessive scrollbars… On macOS set 'Show scroll bars' to 'Always' to test what Windows users would see"; let CSS size things, don't measure in JS.
- **Content:** inline help first, tooltips last; skeletons mirror final layout; no dead ends; "All states designed. Empty, sparse, dense, & error states"; curly quotes; avoid widows/orphans; `font-variant-numeric: tabular-nums` for comparisons; don't rely on colour alone; icon-only buttons get `aria-label`; `…` not `...`; resilient to very long user content; locale-aware dates/numbers/currency; `translate="no"` on brand/code tokens; non-breaking spaces: `10&nbsp;MB`, `⌘&nbsp;K`.
- **Forms:** Enter submits single-field forms; ⌘/Ctrl+Enter submits textareas; never pre-disable submit; don't block keystrokes, validate instead; errors next to fields, focus first error; placeholders are example values ending with `…`; warn on unsaved changes; trim trailing whitespace; **Windows `<select>`: set `background-color` and `color` explicitly** (dark-mode contrast bug).
- **Design:** "Layered shadows. Mimic ambient + direct light with at least two layers"; "Crisp borders. Combine borders & shadows; semi-transparent borders improve edge clarity"; "Nested radii. Child radius ≤ parent radius & concentric"; "Hue consistency. On non-neutral backgrounds, tint borders/shadows/text toward the same hue"; "Interactions increase contrast" (hover/active/focus more contrast than rest); `color-scheme: dark` on `<html>` so scrollbars match; animate a wrapper, not the text node (smoothing changes); avoid gradient banding.
- **Vercel-only (brand choices, not universal):** Title Case headings/buttons (Chicago), `&` over "and", numerals for counts ("8 deployments"), space between number and unit, currency always 0 **or** 2 decimals in a context, error messages say how to fix.
- ⚠️ "Prefer APCA over WCAG 2" is Vercel's opinion; WCAG 2.x is still the legal/conformance bar (see §3.7).

### 6.3 Other credible voices on AI sameness (2025–2026)
- **shadcn (component-kit author), Dec 2025** — "somewhere along the way, all apps started looking the same. I guess the defaults were a little too good. My bad." → `npx shadcn create`: pick component library, icons, base colour, theme, fonts (https://ui.shadcn.com/docs/changelog/2025-12-shadcn-create). Since then the project ships alternative *styles* that change "the geometry, spacing, and feel of the components", e.g. **Luma** (Mar 2026: "Rounded geometry. Soft elevation. Breathable layouts. Inspired by macOS Tahoe, minus the glass.", https://ui.shadcn.com/docs/changelog/2026-03-luma), Sera, Rhea; Base UI became the default primitive layer (Jul 2026). Lesson: the kit is fine; *shipping its stock theme* is the tell.
- **Tailwind v4 defaults that matter for desktop** (https://tailwindcss.com/docs/upgrade-guide): "Buttons now use `cursor: default` instead of `cursor: pointer`" (matches desktop convention — don't add the hand back on app buttons); border colour defaults to `currentColor` (so you *must* pick a border token); `ring` is 1 px. shadcn added pointer cursor only as an opt-in setup flag (Apr 2026, https://ui.shadcn.com/docs/changelog/2026-04-pointer-cursor).
- **Adam Wathan (Tailwind), Aug 2025** — publicly apologised for making every Tailwind UI button `bg-indigo-500`, widely cited as the origin of the AI indigo/purple default ⚠️ (secondhand reports; original post not fetched).
- **Linear (2026)** — design principles that double as anti-slop rules: "Don't compete for attention you haven't earned"; "Structure should be felt not seen" (§3.3, §5.4).
- **Apple HIG Branding (refined 2026-09-09)** — accent "judiciously", brand colour into content, custom font for headlines + system for body, familiar components (§4.6).
- **Mac community 2026** — "There's no native look anymore" (Tonsky) and Brent Simmons' "That About Wraps It Up for Stock Mac UI" (2026-09-22) argue custom UI is now acceptable on Mac — *as long as behaviour stays native*. Full discussion in macos.md §10; our rule: custom pixels OK, custom behaviour not.
- Practitioner essays (opinion, lower weight): "AI design isn't ugly, it's fluent, and that's the problem" (uxdesign.cc, 2025/26 ⚠️ paywalled) — the same stack everywhere: Inter + shadcn + Lucide + Tailwind spacing; a "mediocre version of good design, applied the same way everywhere."

**Synthesis — what "slop" actually is:** not a font or colour, but *unexamined defaults* + *decoration without information* + *missing states*. Every source above converges on: decide the tokens up front, make structure carry meaning, spend boldness in one place, and finish the boring states.

## 7. Slop tell → why it reads generic → do instead

| Slop tell | Why it reads as generic | Do instead (desktop) |
|---|---|---|
| Indigo/violet accent, purple→blue gradients | The training-data default (Tailwind UI indigo ⚠️, Anthropic cookbook "purple gradients on white") — says "no decision made" | Derive the accent from the subject/brand; one accent used sparingly (§3.5); on macOS let selection follow the user's accent |
| Inter/Roboto/system everywhere, one size, one weight | Not the font — the missing type scale and hierarchy | System font for chrome *on purpose*; a characterful face for content/headings if the brand wants it; real scale + 2 weights + size-specific tracking (§2) |
| The 2026 "anti-slop" slop: cream `#F4F1EA` + serif + terracotta; black + acid green; broadsheet hairlines | The look models fall into *when told to avoid* the purple look (Anthropic skill, Sept 2026) | Pick colours from the product's world; run the "would a similar prompt give the same plan?" check |
| Everything in identical rounded cards with the same `rgba(0,0,0,.1)` shadow | "SaaS-card kit" (Anthropic); flattens hierarchy; looks like a web dashboard, not an app | Panes + lists + background shifts; shadows only for floating layers; radius by hierarchy (§4) |
| Glassmorphism / blur on everything | Decoration that costs legibility and battery; fights the OS's own materials | Use the platform material only where the OS does (sidebar, toolbar, popovers); never glass on content or glass-on-glass (macos.md, windows.md) |
| Centered hero layout inside an app window ("Welcome to X" + big CTA) | Marketing-page pattern; apps open to work, not a pitch | Open to the user's last state; first-run = a useful empty state in the real layout |
| Gradient text, glowing borders, animated gradient backgrounds | Attention without information | Solid text colours; colour only where it means something |
| Emoji as icons; mixed icon sets; random stroke widths | Inconsistent weight/metrics; emoji render differently per OS | One icon family, one stroke, sized to the text; platform symbols where possible (§4.5) |
| ✨ sparkle icon + purple for every AI feature | Now the universal "AI" badge; says nothing about *what* it does | Name the action ("Summarize", "Draft reply"); use the normal accent and a specific icon |
| Badge/pill soup: status pills, "New", "Beta", counts on everything | Everything shouts → nothing does | Plain text status with a small colour dot + label; badges only for actionable counts |
| Tracked-out ALL-CAPS eyebrows over every heading; "01 / 02 / 03" markers; "A · B · C" meta; "→" on every link | Anthropic "template chrome"; structure that encodes nothing | Section labels only when they help scanning (sentence case, secondary colour); numbers only for real sequences |
| Oversized radii (20–24 px) on small controls; one radius everywhere | Mobile/toy feel; ignores hierarchy | Radius scale 4/6/8/12 + concentric nesting (§4.4) |
| Grey-on-grey low contrast "for elegance" | Fails WCAG; looks washed out, esp. on Windows at 1× | ≥ 4.5:1 text, ≥ 3:1 control boundaries; de-emphasise with weight/size before contrast (§3.7) |
| Grey text on coloured backgrounds; white at 60 % opacity | Dead-looking, muddy (Refactoring UI) | Same-hue lighter/darker text |
| Uniform 16/24 px gaps everywhere | No grouping → no hierarchy (Refactoring UI "Avoid ambiguous spacing") | Tighter within groups, looser between (e.g. 4–8 inside, 16–24 between, 32+ between sections) |
| Fake data: "John Doe", "Lorem ipsum", `$1,234`, identical rows | Hides wrapping/truncation bugs; reads as a template | Realistic, varied content: long names, missing avatars, 0/1/999+ counts, RTL/accents |
| Generic 3D blob / "people with laptops" illustrations | Stock look, unrelated to the product | Show the product's own objects; a small, specific glyph; or nothing |
| `transition: all 0.3s` + fade-up on every element; hover-lift on every card | Janky (animates layout), slow, and the "generated" signature (Vercel; Anthropic) | Animate only `transform`/`opacity`, only in response to input; see motion.md |
| No hover / pressed / focus / selected / disabled states; `outline: none` | Feels dead or like a web page; inaccessible | Design all states; hover/active *increase* contrast (Vercel); visible `:focus-visible` ring |
| Pointer (hand) cursor on buttons, `user-select` everywhere | Web habit; desktop buttons use the arrow (Tailwind v4 now defaults to it) | `cursor: default` on controls; text selectable only in content |
| Default shadcn/Tailwind theme untouched (zinc, 0.5rem radius, stock shadows) | Its own author says "all apps started looking the same" | Run `shadcn create`/your own tokens; change radius, neutrals, type, icon set, density |
| Toasts for everything ("Saved!"), modal for every confirmation | Web-app reflex; interrupts | Inline status, Undo, status bar text (interaction.md) |
| Dark mode = inverted colours or `#000` + neon | Glare, vibrating accents, invisible borders | Dark greys, lighter elevations, desaturated accents, re-checked contrast (§3.6) |

## 8. Case studies: crafted desktop apps (copyable techniques)

### 8.1 Linear (web + Electron desktop)
Sources: 2024 redesign (https://linear.app/now/how-we-redesigned-the-linear-ui), 2026 refresh (https://linear.app/now/behind-the-latest-design-refresh, changelog https://linear.app/changelog/2026-03-12-ui-refresh).
- Theme = **base + accent + contrast** in LCH (98 variables → 3); contrast slider produces accessible high-contrast themes.
- Neutrals: limit how much accent hue leaks into greys; 2026 moved from cool blue-grey to a "warmer gray… less saturated".
- Hierarchy by **dimming chrome**: sidebar "a few notches dimmer"; "Don't compete for attention you haven't earned."
- Remove decoration: fewer, softer dividers; "colored team icon backgrounds" removed; icon sizes reduced; compact icon-only desktop tabs with "rounded corners and smaller icon and text sizing".
- **Predictable action placement**: share / copy link / open PR always in the same header spot across views.
- Pixel alignment of labels, icons, buttons in sidebar and tabs; Inter Display for headings, Inter for the rest; "relied on Apple standards" for native feel.
- Process: ship behind feature flags with an in-app toggle; build your own colour tool; two designers, ~2 months (2026).

### 8.2 Figma (UI3, 2024)
- Canvas first: "focus the canvas less on our UI and more on your work"; slim bottom toolbar; resizable/collapsible panels; optional labels; "Minimize UI".
- Rejected hover-only UI ("too unstable") and later floating panels ("slowed people down"). Replaced an icon-hidden blend-mode control (users had to wait for a tooltip) with an inline dropdown.
- Muscle memory is a design constraint: kept W/H below X/Y because moving them "disrupted muscle memory too much".
- Hand-drawn custom icon set (200) as a signature; labels kept identical to screen-reader labels.
- "Craft and flow don't have easy metrics, so you have to listen to users a lot" (Marcin Wichary).

### 8.3 Sketch (Copenhagen, Nov 2025 — https://www.sketch.com/blog/a-tour-of-copenhagen/)
- Explicit **adopt / adapt / go custom** decision per area for macOS 26: glass only in toolbar, minimap, canvas notifications; custom (non-glass) sidebar and Inspector.
- Popovers → movable detached panels that persist across selection; context-aware toolbar; Command Bar (S) and shortcuts surfaced in tooltips and menus.
- Document-tab icons encode state (saved, edited, local, workspace, library) — icons that carry information.
- 700+ new icons; still "looks good, with some subtle differences, on earlier macOS versions."

### 8.4 Things 3 (Cultured Code)
- Things 3 won an Apple Design Award at WWDC 2017 (Cultured Code's second; https://en.wikipedia.org/wiki/Things_(software); culturedcode.com says "honored twice"). Identity lives in a few signature elements: the blue Magic Plus button (drag it to where the to-do should go), the app icon, generous whitespace.
- OS 26 update (2025-09-15, https://culturedcode.com/things/blog/2025/09/things-for-os-26/): refreshed curvature across "windows, to-dos, dialogs, and controls"; "wider spacing that feels a bit more relaxed"; sidebar "a touch of glass" with "a hint of color"; Magic Plus "ever so slightly deforms its shape" when dragged; icon in Default/Dark/Tinted/Clear — "familiar at a glance and unmistakably Things". Lesson: refresh by *adjusting* (radius, spacing, material), keep the signature.
- Things uses its own toolbar rather than NSToolbar (cited by Brent Simmons 2026; see macos.md).

### 8.5 Raycast
- 2022 redesign (https://www.raycast.com/blog/a-fresh-look-and-feel): bigger search field "to reflect its importance"; bigger leading icons for scanning; a bottom **action bar** that shows the current title/toast on the left and context actions *with their shortcuts* on the right — teaches the keyboard; toasts inside the window; custom outline icon set with shared stroke and corner rules; **Compact Mode**; keycap app icon.
- Windows (2025-11-20, https://www.raycast.com/blog/raycast-for-windows): "familiar keyboard shortcuts… a design that fits right in… We built it to feel like it belongs here, not like something ported over." Same identity, platform behaviour.

### 8.6 Bear (Shiny Frog)
- Custom typeface **Bear Sans** (2023, https://blog.bear.app/2023/08/learn-about-our-new-custom-font-bear-sans/): Avenir "can be fatiguing to read at smaller body text sizes" — fixed with more width variation, more stroke contrast, larger apertures, tighter spacing, larger x-height, true italics. Used in editor *and* UI; goal: "sit silently, supporting your prose." Lesson: if you pick a characterful font, tune it for legibility at small sizes or confine it to large text.

### 8.7 Arc / Dia (The Browser Company), Panic (Nova, Transmit), Craft, Apple
- **Arc** ⚠️ (from memory; no first-party design write-up fetched): one bold signature — vertical tab sidebar tinted by a per-Space colour theme with the web page inset as a rounded card — while menus and shortcuts stay standard. Arc development stopped in May 2025 in favour of the simpler, AI-first Dia (beta June 2025); Atlassian announced buying The Browser Company in Sept 2025 for ~$610 M (https://heise.de/-10632710).
- **Panic Nova**: praised as a "Mac-assed" code editor (MacStories review, https://www.macstories.net/reviews/nova-review-panics-code-editor-demonstrates-why-mac-like-design-matters/); themes are CSS-like and can follow light/dark automatically ⚠️ (from secondhand copy of Panic's text). Panic's apps pair native behaviour with a playful, illustrated identity (icons, About windows) — personality at the edges, not in the controls.
- **Craft**: Apple's *Mac App of the Year* 2021 (App Store Awards — not an ADA; https://www.businesswire.com/news/home/20211202005370/en/). Document-as-blocks with deliberate content typography inside a native sidebar/shortcut skeleton ⚠️ (description from memory).
- **Apple's own apps / ADA**: ADA criteria and 2025–2026 Mac-relevant winners are in macos.md §10 ("Visuals and Graphics": "skillfully drawn interfaces… distinctive and cohesive theme"; "Interaction": "perfectly tailored to their platform").

**Common pattern across all of them:** (1) native behaviour and layout skeleton; (2) quiet, dim chrome; (3) **one** signature element (Magic Plus, keycap/action bar, hand-drawn icons, tinted sidebar, custom font); (4) custom icon set with strict rules; (5) density with restraint; (6) they evolve by refinement, not reinvention.

## 9. Pixel-level polish checklist
Run this on screenshots at 1× and 2×, light and dark, before calling a screen done (Anthropic: "a picture is worth 1000 tokens").

**Alignment & rhythm**
- [ ] Every gap is a spacing token; groups tighter inside than between; nothing "almost" aligned (1–2 px misses are the worst).
- [ ] One leading edge per region; icons, labels, inputs and headers share it. Text baselines align across adjacent columns/controls.
- [ ] Icons optically centred (play/download/chevrons nudged ±1 px); icon box = text line-height; icon weight matches text weight.
- [ ] Radii from the scale; nested radii concentric; no 20 px pills on 24 px controls.
- [ ] Hairlines crisp at 1× and 2× (and Windows 125/150 %); separators from tokens, never ad-hoc greys.

**Type**
- [ ] ≤ 4 sizes and ≤ 2–3 weights per view; tracking adjusted by size; ALL CAPS only for tiny labels, with +5–12 % letterspacing (or not at all).
- [ ] Tabular figures in tables, timers, counters, sizes, prices; numbers right-aligned in columns.
- [ ] Locale-formatted dates/numbers/currency; `…` not `...`; curly quotes; non-breaking space in `10 MB`, `⌘ K`.
- [ ] Headings `text-wrap: balance`; paragraphs `pretty`; prose ≤ 75ch.
- [ ] Truncation: ellipsis + full text on hover (tooltip/`title`); middle-truncate paths and file names; nothing clipped mid-glyph.
- [ ] Consistent capitalisation (platform: macOS title case for menus/buttons, Windows/GNOME sentence case — see platform files); consistent nouns across button → toast ("Publish" → "Published").

**Colour & depth**
- [ ] All text ≥ 4.5:1 (large ≥ 3:1), control boundaries/icons ≥ 3:1 — in light *and* dark *and* increased-contrast modes.
- [ ] One accent with a meaning; no grey text on coloured fills; semantic colours not reused for decoration.
- [ ] Shadows only on floating layers, layered and tinted; dark mode adds a light edge instead of heavier shadow.
- [ ] Dark mode parity: every surface, illustration, chart, focus ring and selection colour designed for dark; no pure black/white unless intentional.

**States & behaviour**
- [ ] Hover, pressed, focus-visible, selected, selected-but-window-inactive, disabled, drag-over states for every interactive element; interaction *raises* contrast.
- [ ] Focus ring visible, not clipped by `overflow: hidden`, follows the platform/user accent.
- [ ] Selection colour (`::selection`, list selection) uses the accent/system highlight; inactive-window selection goes grey.
- [ ] Cursor conventions: arrow on buttons and menu items, I-beam only on editable/selectable text, resize cursors on splitters, grab/grabbing for draggable canvases.
- [ ] Scrollbars: native or `color-scheme`-aware; test with macOS "Show scroll bars: Always" (Vercel) — no double scrollbars, no layout jump when they appear (`scrollbar-gutter: stable`).
- [ ] No layout shift: skeletons match final layout; images/avatars have reserved size; spinners delayed 150–300 ms, shown ≥ 300–500 ms (Vercel); button width doesn't change when label → "Saving…".
- [ ] Empty, first-run, loading, partial, error, offline, permission-denied and "too much data" states designed with real copy and a next step.
- [ ] Real content: long names, 0/1/many, missing images, long words/URLs, RTL and accented text, huge numbers.
- [ ] Window at minimum size, half-screen, and ultra-wide: nothing overlaps, prose stays capped, sidebars collapse sensibly.
- [ ] Reduced motion / reduced transparency / increased contrast respected (motion.md, accessibility.md).
- [ ] Final pass: remove one accessory (Anthropic). Is there exactly one memorable thing?

## 10. Practitioner notes from hand-picked sources

Takeaways from sources the skill's author recommended, cross-checked against the platform guidelines. **[STD]** = backed by platform or standards guidance; **[TASTE]** = a practitioner's taste call (use judgment). Where a source got a platform rule wrong, the item says so.

Sources:
- Kole Jain, [Everything you need to Design macOS Apps EXACTLY like Apple](https://www.youtube.com/watch?v=Vy0KKvZJRH8) (Dec 2025)
- Kole Jain, [EVERYTHING you need to know to build a Dashboard UI in 8 minutes](https://www.youtube.com/watch?v=B7k5rOgmOGY) (Aug 2025)
- uxpeak, [UX Design Thinking Behind The Most Loved Apps](https://www.youtube.com/watch?v=U7jTCgIWS4w) (Oct 2026)
- Benji Taylor, [Stageshow](https://benji.org/stageshow) (agent skill for product-UI demos, MIT)
- Sahil Jada, [font picks to "unslop" designs](https://x.com/BySahilJada/status/2116834000765681757) (Nov 2026)
- Vercel, [Introducing Geist Serif](https://vercel.com/blog/introducing-geist-serif) (Oct 2026) and [Geist typography](https://vercel.com/geist/typography)
- Julien Thibeaut (ibelick), [ui-skills](https://github.com/ibelick/ui-skills) (MIT)

1. **The app should feel like part of the system, not a place you visit** — summon-anywhere panels, menu bar extras, drag in *and out*, Esc/Return, quiet confirmations. (Kole Jain macOS [00:00–01:00]) [TASTE, fits HIG "Stay out of the way"]
2. **Global hotkeys must never reuse a standard shortcut** (⇧⌘S = Duplicate/Save As) — make them rebindable and check for conflicts. (correction to Kole Jain [01:00]; HIG Keyboards) [STD]
3. **Remove traffic lights only on transient launcher-style panels** (Spotlight/Raycast type, closed with Esc/click-away); real windows keep the system frame, and web shells mark drag regions and leave the top ~38–52 pt uncluttered. (Kole Jain [01:00], [03:02]; Stageshow chrome rules) [STD]
4. **Content first: what's the least UI that lets the user's content shine?** Empty state with one next action; filters and metadata appear when there's content or a selection — but stay in the menus, disabled. (Kole Jain [03:02]; ui-skills baseline-ui; NN/g) [STD]
5. **Dark mode isn't an inversion:** use bigger steps between surfaces in dark mode and smaller ones in light; in dark mode show depth with lighter surfaces, not shadows. Follow the system appearance, with **no in-app theme switch** (default to "System" if one is required). (Kole Jain [04:04–05:05]; Stageshow craft; HIG Dark Mode) [STD + TASTE for step sizes]
6. **Every shortcut needs visible feedback, but high-frequency keyboard actions respond instantly**: no slow animation on actions people repeat many times a day. (Kole Jain [06:05]; motion.md; Stageshow "UI feedback stays as quick as the real product") [STD]
7. **Optimistic UI only with a rollback path**: update right away, then reconcile; on failure, restore the item and say so. Pair deletes with Undo (⌘Z / Ctrl+Z) instead of a confirm dialog; confirm only when the action truly can't be undone. (Kole Jain both videos; corrects ui-skills' AlertDialog rule; HIG Undo, NN/g) [STD]
8. **Never use toasts for errors, and avoid web-style toasts in Mac main windows**: show errors next to their source; on Mac, confirm in place (highlight the new row); on Windows/GNOME, an undo toast/InfoBar is native. (Kole Jain dashboard [05:02]; ui-skills a11y; platform notes) [STD]
9. **Put things where each platform expects them**: Mac search in the trailing toolbar (not a bottom bar), Settings in a ⌘, window (not a popover or sidebar item); Windows keeps Settings at the bottom of NavigationView. (Kole Jain corrections) [STD]
10. **Dashboards: do one thing well**: the user's most important information goes top-left, type is smaller with tighter steps than marketing pages, a strict grid, one primary action, charts with axes/grid lines and a date range, multi-select that reveals bulk actions. (Kole Jain dashboard; Few; NN/g) [STD]
11. **Hierarchy test: "if you can't say what someone should read first, they can't either."** Name steps up, key metric gets the weight, everything else steps back, one shape language per screen. (uxpeak [01:00–02:00]) [STD]
12. **Show consequences before commit**: result counts on the apply button ("Show 41 homes"), a count on each filter option, a histogram behind range sliders, and filters that show all choices at once (no per-filter pages). On desktop, a live non-modal filter panel. (uxpeak [09:04–14:09]) [STD for counts/feedback; TASTE for histogram]
13. **Make the system translate the user's terms into its own** (monthly budget → max price) and give control where no default fits everyone (card vs list view), while still choosing a strong default. (uxpeak [03:00], [13:07]; Tesler; NN/g defaults) [TASTE]
14. **Restraint budget**: about 3–7 meaningful strings per focal area; one big number; say it once; one accent colour per view; no default gradients, purple "AI" colour, sparkles or glow. (Stageshow craft; ui-skills baseline-ui) [TASTE, consistent with HIG "one prominent action"]
15. **Icons from one deliberate set at one size and stroke** (SF Symbols on Mac, Fluent on Windows, Adwaita on GNOME; otherwise Phosphor/Tabler etc.; never Lucide on autopilot or hand-drawn glyphs); icon-only buttons get a label plus a tooltip that shows the shortcut. (Stageshow; ui-skills; HIG) [STD + TASTE for set choice]
16. **Spacing micro-rules**: ≥12 px text inset from container edges; row padding 12 px (8 px dense); ≥8 px between a control and the edge above; fixed 8–12 px gaps; no near-tangent edges (1–3 px apart); concentric radii (outer = inner + padding). (Stageshow craft; ui-skills Playbook; HIG concentric corners) [TASTE + STD for concentric]
17. **Optical alignment**: centre labels on cap height (`text-box: trim-both cap alphabetic`); centre the digits and let the currency sign hang outside; nudge play triangles; use `tabular-nums` for any numbers that change or line up. (Stageshow; ui-skills; Vercel guidelines) [TASTE]
18. **Nothing pops; change only what changed**: keep elements mounted through exit, let neighbours make room as items arrive, roll only the digits that changed, keep button states in one fixed-size slot, anchor popovers to their trigger, size them before the first frame, and on scale-in animate only the surface while the text just fades. (Stageshow motion) [TASTE, consistent with motion.md]
19. **Don't copy marketing-demo pace into app UI**: Stageshow's 0.3 s popovers and 0.8–2.7 s story curves are tuned for video. App menus/popovers stay ≤150–200 ms, feedback ≤200 ms, and only transform/opacity animate. (Stageshow vs motion.md; ui-skills baseline-ui) [STD]
20. **One type system, several voices**: system/UI sans runs the product chrome, and an expressive display face (e.g. Geist Serif, OFL) is reserved for headings, empty states and onboarding. Pair faces with matching x-height/cap height (or `size-adjust`), and tighten tracking as size grows (Geist: −0.02 em at 14–20 px → −0.06 em at 40–72 px). (Vercel Geist Serif + type scale; Sahil Jada post) [TASTE; licensing STD]
21. **Bundle fonts locally and check licences**: OFL fonts (Geist family, Figtree) are safe to embed; Fontshare/ITF fonts (Switzer) need their licence checked; unverifiable fonts (Brodine) should be skipped. Desktop apps never load fonts from a CDN at runtime. (Sahil Jada post; Geist README) [STD for licensing]
22. **Separate Label and Copy styles**: one-line UI labels get tight leading (14/20, 13/16) and paragraphs get looser leading (14/20 → 16/24). Buttons use medium weight. Native Mac sticks to SF text styles at a 13 pt body. (Geist typography; macos.md) [STD for Mac; TASTE for Geist values]
23. **Write a DESIGN.md token plan before coding**: colours, typography (fontFamily/size/lineHeight/weight/letterSpacing), radii, spacing, plus Do/Don't rules backed by evidence. It can be checked with `npx @google/design.md lint`. (ui-skills create-design-md) [TASTE/tooling]
24. **For a focused "improve this" pass (not a full audit): prove, falsify, cap**: each finding needs a cited rule, proof that it actually reaches the screen, and exactly one fix. Try to disprove each finding, report at most 3, and write self-contained plans with stop conditions. Use the same output format as the rule checks: quote the line, say why it matters, give the fix. (ui-skills improve-ui / baseline-ui) [TASTE, strong method]

## Unverified / open questions
- **Refactoring UI specifics** (spacing scale 4…768, type scale 12…72, line length 45–75 chars/20–35em, ≥10-styles font filter, personality/radius mapping, 5 shadow tokens): from the book; only the TOC and the colour-palette preview were fetchable (Medium "7 tips" article blocked by Cloudflare). Tailwind's defaults match the scales.
- **Practical Typography** read via web.archive.org (live site refused connections on 2026-11-02).
- **`text-wrap: balance` line cap in Chromium**: MDN says 6 lines; WebKit's April 2025 post says 4. Not tested.
- **Inter dynamic-metrics formula** page is 404 (moved to d.rsms.me archive); Inter 4 opsz axis behaviour not re-verified.
- **Sub-pixel hairlines** (`0.5px` borders) rendering across Chromium/WebKit/WebKitGTK at fractional Windows scaling — not tested.
- **Icon-to-text size pairs** (16/13, 20/15–17) and region widths in §5.3 are synthesis from common pro apps, not from a single primary source.
- **Lucide `absoluteStrokeWidth`** docs URL moved (404); behaviour from memory.
- **Adam Wathan "indigo" apology** (Aug 2025): only secondhand reports found; original X post not fetched.
- **uxdesign.cc "AI design isn't ugly, it's fluent"**: paywalled/403; summarized from search snippets only.
- **Arc design details, Panic Nova theming, Craft description**: from memory/secondary sources; no first-party design write-ups fetched.
- **Material dark-theme page** (m2.material.io) is JS-rendered; #121212 and elevation-overlay facts confirmed via search snippets + Flutter docs, not the page text.
- **WinUI `Typography.NumeralAlignment`** property name for tabular figures — from memory.
- **System font CSS stack** — whether `system-ui` resolves to Segoe UI Variable on Windows 11 in WebView2, and "Adwaita Sans" naming on GNOME 48+, not verified here (see windows.md / linux.md).
- **Evil Martians OKLCH article** shows "2025-09-17" as its date though the piece originally appeared earlier (≈ 2022) — date shown is the page's current stamp.
- **Open question**: Anthropic's Sept 2026 skill flags "a monospace face for small data labels" as a tell, while Vercel/Geist recommend mono/tabular for data. Reconciliation used here: mono for code/IDs/aligned numbers where it carries meaning; not as decoration for every small label.
- **Open question**: Linear/Vercel/Radix lean on APCA; WCAG 3 contrast is undecided (April 2026 draft). We ship to WCAG 2.2 and use APCA as a second check.

## Sources (primary, fetched 2026-11-02)
Anthropic frontend-design skill (3 versions) https://github.com/anthropics/skills/tree/main/skills/frontend-design · Anthropic cookbook https://github.com/anthropics/claude-cookbooks/blob/main/coding/prompting_for_frontend_aesthetics.ipynb · Vercel guidelines https://vercel.com/design/guidelines + https://github.com/vercel-labs/web-interface-guidelines · Geist typography https://vercel.com/geist/typography · Refactoring UI https://www.refactoringui.com/ · Practical Typography https://practicaltypography.com/ · WWDC20 10175 https://developer.apple.com/videos/play/wwdc2020/10175/ · Radix Colors https://www.radix-ui.com/colors/docs/ · Evil Martians OKLCH https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl · Stripe https://stripe.com/blog/accessible-color-systems · Linear https://linear.app/now/how-we-redesigned-the-linear-ui, https://linear.app/now/behind-the-latest-design-refresh · Josh Comeau https://www.joshwcomeau.com/css/designing-shadows/, https://www.joshwcomeau.com/css/custom-css-reset/ · WebKit text-wrap https://webkit.org/blog/16547/better-typography-with-text-wrap-pretty/ · MDN text-wrap · Primer primitives 11.10 (unpkg) + https://primer.style/product/getting-started/foundations/layout/ · Fluent 2 layout https://fluent2.microsoft.design/layout · Figma UI3 posts · Sketch Copenhagen · Things OS 26 · Raycast 2022 + Windows 2025 · Bear Sans · shadcn changelog · Tailwind v4 upgrade guide · Adrian Roselli WCAG3 contrast (Apr 2026) · Apple HIG (Branding, Icons, SF Symbols, Toolbars).
