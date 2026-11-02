# Motion and microinteractions for desktop apps

Read this before adding any animation, transition, hover/press feedback, loading state or other microinteraction. Covers when not to animate, duration and easing numbers per platform, springs, perceived performance, reduced motion, and per-stack code. Every rule cites its source inline; ⚠️ marks claims that couldn't be fully verified (collected at the end). Researched November 2026 — platform details change, so re-check anything version-specific.

Contents: 0. TL;DR rules · 1. What motion is for — and when not to animate · 2. Microinteractions model · 3. Timing & easing numbers · 4. Springs · 5. Perceived performance & waiting · 6. Practitioner craft · 7. Implementation per stack · 8. Reduced motion done right · 9. Desktop microinteraction catalog · Recent changes worth knowing · Unverified / open questions

## 0. TL;DR rules (read first)
1. **Every input gets a visible response within 100 ms** (Nielsen 0.1 s); motion may *continue* after, but must never delay the result or block the next input (Apple HIG: "Let people cancel motion").
2. **Don't animate high-frequency or keyboard-driven actions** (typing, arrow-key navigation, command palette, tab cycling, selection). Animate *spatial/state changes the user must track* and *feedback*.
3. **Desktop durations are short**: micro 80–150 ms · menus/popovers ≤150–200 · panels/dialogs 200–300 · nothing routine > 400 ms. Exits ~15–50 % faster than entrances. Bigger/farther = longer.
4. **Easing**: entrances decelerate (`cubic-bezier(0,0,0,1)` Windows/Fluent, `(0.05,0.7,0.1,1)` M3, `(0.23,1,0.32,1)` practitioner); on-screen moves standard (`(0.2,0,0,1)`); system-driven exits accelerate; user-dismissals are fast fades. Linear only for opacity-only fades, progress and spinners.
5. **Prefer interruptible motion**: springs (Apple: duration + bounce 0; ζ = 1 − bounce) or CSS *transitions*, never restart-from-zero keyframes for re-triggerable UI. Hand gesture velocity to the spring.
6. **Bounce is rare**: bounce 0 by default, ≤0.15–0.3 only after momentum gestures or for playful brand moments; > 0.4 "may feel too exaggerated" (WWDC23).
7. **Origin-aware**: popovers/menus scale (0.96–0.97 → 1) from their trigger; never from `scale(0)`; things leave the way they came (symmetric paths).
8. **Animate only `transform`/`opacity`**; never `transition: all`; fit the 8.3 ms frame at 120 Hz; layout changes via FLIP/layout animations.
9. **Respect reduced motion on every platform and live-update it**: replace slides/zooms/parallax/bounce with cross-fades or nothing; keep opacity, color, progress and direct-manipulation tracking.
10. **Use the platform's built-ins first** (WinUI transitions, AdwNavigationView, SwiftUI presets, native menus/sheets) — they already encode timing, accessibility and input-type nuance.
11. **Waiting**: nothing < 1 s; spinner after 150–300 ms delay and ≥300–500 ms visible; skeletons for page loads < 10 s; percent-done + estimate ≥ 10 s; accelerate progress toward the end, no late stalls (Harrison 2007).
12. **One signature moment, everything else quiet** (Saffer) — delight belongs in rare interactions.

## 1. What motion is for — and when not to animate

**Motion is for** (NN/g, Laubheimer 2020, https://www.nngroup.com/articles/animation-purpose-ux/): **feedback** ("a short animation can ensure that users see the feedback"), **state change** (mode, loading), **spatial metaphor / navigation** (up/down a hierarchy, forward/back), **preventing disorientation** ("Accordions, anchor links, and menu overlays can be disorienting or confusing if the change appears instantaneously"), **signifiers** (direction hints how to dismiss), **attention**. Not for "time-filling visual stimulations", not to hijack attention; "Gratuitous animations distract and annoy". Apple HIG Motion (updated 2025-09-09, https://developer.apple.com/design/human-interface-guidelines/motion): "Add motion purposefully… Don't add motion for the sake of adding motion"; "Make motion optional" (never the only carrier of information); "Aim for brevity and precision in feedback animations"; "generally avoid adding motion to UI interactions that occur frequently"; "Let people cancel motion… don't make people wait for an animation to complete". Windows: Connected · Consistent · Responsive · Delightful · Resourceful ("Avoid custom animations where possible") (https://learn.microsoft.com/windows/apps/design/signature-experiences/motion). GNOME: use motion to explain spatial change; widgets must not jump/disappear without animation when resizing (see linux.md §5).

**Research basis**
- **Chang & Ungar 1993**, "Animation: from cartoons to the user interface", UIST '93, pp. 45–55, DOI 10.1145/168642.168647 (PDF: https://bibliography.selflanguage.org/_static/animation.pdf). Static UIs "startle and confuse users"; cartoon principles in 3 groups — **solidity** (objects move continuously, never "sudden materializations and disappearances"; drag the real object, not an outline; motion blur for fast moves), **exaggeration** (anticipation: "a small contrary motion"), **reinforcement** (slow-in/slow-out — "pacing the middle of transitions faster than the endpoints", arcs for non-interactive travel, follow-through "vibrate into place"). Principles drawn from Thomas & Johnston, *Disney Animation: The Illusion of Life* (1981) — the "12 principles"; in productivity UI keep only slow-in/out, arcs, follow-through (tiny), staging, timing; skip squash-and-stretch/exaggeration except for playful moments.
- **Tversky, Morrison & Bétrancourt 2002**, "Animation: can it facilitate?", IJHCS 57(4):247–262, DOI 10.1006/ijhc.2002.1017 — skeptical review; Heer & Robertson summarise it as "finding no benefit for communicating the workings of complex systems" (with an exception for transitions). ⚠️ The commonly cited reading — animated conditions often won only because they showed *more* information or allowed interaction — is from memory, abstract paywalled. Two principles (quoted via Heer & Robertson 2007): **Congruence** — "the structure and content of the external representation should correspond to the desired structure and content of the internal representation"; **Apprehension** — it "should be readily and accurately perceived and comprehended". ⇒ animate *changes the user must track*, keep motion simple and slow enough to perceive, don't expect motion to teach.
- **Heer & Robertson 2007**, "Animated Transitions in Statistical Data Graphics", IEEE TVCG 13(6):1240–1247, DOI 10.1109/TVCG.2007.70539 — animated transitions "significantly improve graphical perception" vs. instant. Guidelines: group similar transitions (common fate), **minimize occlusion**, maximize predictability (slow-in/slow-out), **use simple transitions** (translation/expand easier than rotation), **stage complex transitions** (e.g. rescale axis first, then values; stagger to reduce occlusion), avoid aggressive multi-stage "do-everything" sequences, "Make transitions as long as needed, but no longer" (~1 s for data-vis; their tests used 1.25 s and 2 s — data-viz only; UI chrome must be far shorter).

**When NOT to animate** (merge of the above + practitioners in §6)
1. **High-frequency actions** — typing, list arrow-key navigation, tab switching via shortcut, command-palette toggle, selection changes, hover on dense lists. Apple: avoid motion on frequent interactions; Emil Kowalski: 100+×/day → "No animation. Ever."
2. **Keyboard-initiated actions** — keyboard users are fast and expect instant response; animate at most a ≤100 ms opacity change (practitioner consensus, §6).
3. **Anything that blocks input** — never make the user wait for a transition before the next click/keypress lands; queue nothing, retarget instead (WWDC18).
4. **Animation as the only signal** of state (fails reduced-motion users, screen readers).
5. **Several things competing** — NN/g: "The number of simultaneous animations is overwhelming"; one primary motion per moment, others subordinate.
6. **Looping/autoplay** decoration in productivity UI; WCAG 2.2.2: moving content > 5 s needs pause/stop/hide (Vercel guidelines restate it).
7. **Scroll-jacking, parallax, zooming backgrounds** — vestibular triggers (§8).

## 2. Microinteractions model (Dan Saffer, *Microinteractions: Designing with Details*, O'Reilly 2013, ISBN 978-1-4493-4268-6)
Primary source used: Saffer's own article "Microinteractions: Why details matter" (Smart Design, https://smartdesignworldwide.com/ideas/microinteractions-details-matter/). ⚠️ microinteractions.com (the book's old site) now 301-redirects to an unrelated domain — do not link it. O'Reilly excerpt pages returned 403; chapter map from the O'Reilly TOC via search: ch.2 Triggers ("Bring the data forward"), ch.3 Rules ("Don't start from zero"), ch.4 Feedback, ch.5 Loops & Modes.
- **Definition**: "Microinteractions are the contained product moments that do one small task." (toggle a setting, copy a link, rename a file, mute).
- **Trigger** — "what starts a microinteraction": *manual* (click, shortcut, drag) or *system* (file finished syncing, new message). Make manual triggers look like what they do; show current state on the trigger itself (a toggle shows on/off; a sync button shows "syncing"). *Bring the data forward*: put the key datum on the trigger (unread count on the icon, branch name on the button).
- **Rules** — "determine the flow… by defining the sequence of events"; they are invisible, so users learn them only via feedback. *Don't start from zero*: "you usually know something" about the user/platform/context — prefill last-used values, remember the last folder/view, default the export format to the one used last time, smart defaults by context.
- **Feedback** — "Feedback (and the lack of feedback) is how we understand the Rules". Match feedback to the significance of the event; prefer modifying existing UI (label changes "Copy" → "Copied") over adding new UI (toast). Use the least intrusive channel first: visual → sound → haptic.
- **Loops & modes** — loops govern "how long the microinteraction goes on for, if it repeats, and how it changes over time" (e.g. auto-dismiss after N s, progressive reduction: hide hints after the user has learned them). Modes only "for a critical but infrequent action" that would otherwise disrupt the flow; avoid modes otherwise.
- **Signature moments** — "microinteractions that have been elevated to be part of the brand" (Facebook Like). A desktop app may have **one or two** (e.g. a satisfying "inbox zero" or "build passed" moment); everything else stays quiet and fast.
- Agent checklist per microinteraction: *What triggers it? What's the one task? What does the user already know/what do we know (don't start from zero)? What changes on screen within 100 ms? What happens on repeat/second time? What if it fails? What if reduced motion is on?*

## 3. Timing & easing numbers

### 3.1 Durations — rules of thumb
- **Range**: "most animations should be in the range of 100–500 ms"; simple feedback (checkbox, toggle) ≈ **100 ms**; substantial changes (modal) **200–300 ms**; 400 ms only for "big movements across large screens"; "At 500ms, animations start to feel like a real drag" (NN/g, Laubheimer 2020, https://www.nngroup.com/articles/animation-duration/). Find "the shortest time that an animation can take without being jarring".
- **Desktop is faster than mobile**: "Desktop animations should be faster and simpler than their mobile counterparts. These animations should last **150ms to 200ms**" — because pointer moves are small and desktop transitions are less noticeable (Material 1 spec, 2017 snapshot: https://web.archive.org/web/2017/https://material.io/guidelines/motion/duration-easing.html). Same page: mobile ≈ 300 ms (enter **225**, exit **195**, large/full-screen **375**); tablet +30 % (390); wearables −30 % (210); ">400ms may feel too slow".
- **Exit shorter than enter** (~15–50 % shorter): M2 nav drawer 250 open / 200 close, card 300 expand / 250 collapse, dialog fade **150 in / 75 out**, switch **100**, selection controls 100, shape change 200, detailed icon animation 500 (M2 "Speed", https://web.archive.org/web/2019/https://material.io/design/motion/speed.html). Windows: expand 300 / contract 150; exits 167 (motion-in-practice; see windows.md §9).
- **Distance/size scales duration**: Windows 167 small/near · 250 normal · 333 large/far; Material: small area (icons, selection controls) short, medium (chips, bottom sheets) 250/200, large (cards, persistent sheets) 300/250.
- **Frequency shrinks duration** toward zero (NN/g: "the more frequent the animation, the more subtle and shorter"; §1, §6).
- **Desktop default ladder (synthesis, use unless the platform says otherwise)**: micro feedback (hover/press/color) **80–150 ms** · tooltip/small popover **120–150 ms** · menu/dropdown/select **150–200 ms** open, ≤150 close · panel/sidebar/disclosure **200–250 ms** · dialog/sheet **200–300 ms** in, 150–200 out · page/view transition **250–350 ms** · nothing in routine UI > **400 ms**.

### 3.2 Platform token tables (verified)
| System | Durations | Curves |
|---|---|---|
| **Windows 11** (WinUI; https://learn.microsoft.com/windows/apps/design/motion/timing-and-easing) | `ControlFasterAnimationDuration` **83** (fades), `ControlFastAnimationDuration` **167**, `ControlNormalAnimationDuration` **250**; **333** for large moves | enter/"Fast Out, Slow In" `cubic-bezier(0,0,0,1)`; exit/"Slow Out, Fast In" `cubic-bezier(1,0,1,1)`; point-to-point `(0.55,0.55,0,1)`; fade linear 83 ms |
| **Fluent 2** web/React tokens (fluentui `packages/tokens`) | ultraFast 50 · faster 100 · fast 150 · normal 200 · gentle 250 · slow 300 · slower 400 · ultraSlow 500 | `curveDecelerateMid (0,0,0,1)`, `curveAccelerateMid (1,0,1,1)`, `curveDecelerateMax (0.1,0.9,0.2,1)`, `curveEasyEase (0.33,0,0.67,1)`, … (full list in windows.md §9) |
| **Material 3** (material-web `tokens/versions/v0_192/_md-sys-motion.scss`) | short1–4 **50/100/150/200** · medium1–4 **250/300/350/400** · long1–4 **450/500/550/600** · extra-long1–4 **700/800/900/1000** | `emphasized` / `standard` `(0.2,0,0,1)` · `emphasized-decelerate (0.05,0.7,0.1,1)` · `emphasized-accelerate (0.3,0,0.8,0.15)` · `standard-decelerate (0,0,0,1)` · `standard-accelerate (0.3,0,1,1)` · `legacy (0.4,0,0.2,1)` (= old "standard"), `legacy-decelerate (0,0,0.2,1)`, `legacy-accelerate (0.4,0,1,1)` |
| **M3 Expressive springs** (Compose `MotionScheme`, androidx `tokens/StandardMotionTokens.kt`, `ExpressiveMotionTokens.kt`; mass 1) | *standard*: spatial fast/default/slow = ζ 0.9, k **1400/700/300**; effects (color/opacity) ζ 1.0, k 3800/1600/800 · *expressive*: spatial ζ 0.6/0.8/0.8, k 800/380/200; effects as standard | "spatial" springs (position/size) may overshoot; "effects" springs (color, opacity) never do |
| **GNOME / libadwaita** (source `src/*.c`) | toasts show/hide **300**, replace 500; tab overview 400; `AdwTimedAnimation` example 250 | `AdwTimedAnimation` default easing `ADW_EASE_OUT_CUBIC` (`adw-timed-animation.c`); springs: nav view ζ 1, m 1, k **1000**; sidebars/flap/carousel ζ 1, m 0.5, k 500; bottom sheet ζ 0.8, k 400; floating sheet ζ 0.62, k 500 |
| **Qt Widgets** (`qcommonstyle.cpp`) | `SH_Widget_Animation_Duration` **200** | — |
| **Apple** | No public duration tokens. SwiftUI default = spring `response 0.55, dampingFraction 1.0`; presets d 0.5 (§4). Core Animation implicit default 0.25 s ⚠️ (long-standing, not in current docs) | Use springs (bounce 0) rather than Béziers |

### 3.3 Easing
- **Ease-out (decelerate) for entrances** — "Most frequently, you'll want to use an ease-out animation" (NN/g); Windows/Fluent `(0,0,0,1)`; M3 `emphasized-decelerate`.
- **Exits**: platform systems use **accelerate** (ease-in) for elements leaving *for good* — Windows `(1,0,1,1)`, M3 `emphasized-accelerate` — combined with a short duration and a fade. NN/g: ease-in/in-out "sometimes used for elements leaving the screen" but "can feel unresponsive if the start is slow". Practitioner (Kowalski): ease-out for exits too, never ease-in. **Rule for agents**: user-triggered dismiss (close menu, Esc a dialog) → fast fade/ease-out ≤150 ms so it feels instant; system-driven departure (toast auto-dismiss, item moving off) → accelerate is fine.
- **On-screen move/morph (A→B, both visible)**: standard / ease-in-out — Windows point-to-point `(0.55,0.55,0,1)`, M3 `standard (0.2,0,0,1)`, Kowalski `(0.77,0,0.175,1)`.
- **Linear only** for opacity-only fades (Windows 83 ms fade), progress, spinners/rotation, marquee. "Completely linear motion looks weird and unnatural" (NN/g).
- CSS built-ins are weak: `ease-out` = `(0,0,0.58,1)`. Prefer `(0,0,0,1)`/`(0.23,1,0.32,1)`/`(0.05,0.7,0.1,1)` for entrances.
- Specify ms, not frames; specify curves as cubic-bezier or named platform curves (NN/g).

### 3.4 Tooltips, menus, hover — platform timings (verified in source/docs)
| | First show | "Warm" next tooltip | Notes |
|---|---|---|---|
| Win32 common controls (https://learn.microsoft.com/windows/win32/controls/ttm-setdelaytime) | `TTDT_INITIAL` = double-click time (**500 ms** default) | `TTDT_RESHOW` = 1/5 (**100 ms**) | autopop = 10× (5000 ms) |
| GTK 4 (`gtk/gtktooltip.c`) | `HOVER_TIMEOUT` **500 ms** | `BROWSE_TIMEOUT` **60 ms** | browse mode ends `BROWSE_DISABLE_TIMEOUT` 500 ms after leaving |
| Qt Widgets (`qapplication.cpp`, `qcommonstyle.cpp`) | `QStyleHints::toolTipWakeUpDelay` (new API in 6.12; historically 700 ms ⚠️) | **20 ms** while fall-asleep timer runs | `SH_ToolTip_FallAsleepDelay` 2000 ms |
| macOS AppKit | ~1 s ⚠️ (`NSInitialToolTipDelay` user default, undocumented) | instant-ish ⚠️ | system-drawn; don't reimplement |
| Web (Vercel/Kowalski) | delay first (~400–700 ms is common practice ⚠️) | **0 ms delay and 0 ms animation** | tooltip anim 125 ms ease-out |
**Menus/popovers**: open **instantly or ≤150 ms** (pointer users have already committed); close with a quick fade (≤150 ms) or instantly when an item is chosen. macOS menus appear instantly and fade out after selection (the chosen item blinks first) — observed system behaviour ⚠️ (not documented in HIG). Never animate a context menu's open when it was triggered by keyboard.
**Hover**: respond on the next frame (no delay) for color/background; transition ≤ 100–150 ms in, can be slightly slower out (e.g. 150 ms in / 250 ms out lets quick cursor sweeps over lists not "flicker") (practitioner ⚠️). Delayed hover *reveals* (preview cards) need intent delay (NN/g: "Hover-triggered previews may need a slight delay").

## 4. Springs

### 4.1 Why springs (Apple, WWDC23 "Animate with springs", https://developer.apple.com/videos/play/wwdc2023/10158/)
- Goal: **continuous position *and* velocity**. Linear has velocity jumps at start/end — "be cautious about using them, especially for movement"; OK for "a repeating spinning indicator".
- Bézier ease-in-out has no way to take an initial velocity → jerks when a gesture hands off or the animation is retargeted. "Springs are the only type of animation that maintains continuity both for static cases and cases with an initial velocity."
- Retargeting mid-flight: the spring "uses the velocity it had when it was retargeted as the initial velocity towards its new destination" → interruptions feel smooth. This is *the* reason to use springs for anything the user can re-trigger quickly (hover/press, toggles, panels, drag).
- Multi-property springs may finish at different times — that's fine/desired.
- Apple's 2-param model: **duration** (perceptual, not settling time) + **bounce** (−1…1). bounce > 0 = bouncy (underdamped), 0 = smooth (critically damped), < 0 = flattened (overdamped). Don't wait for the settling duration for UI changes; use SwiftUI's completion handler (it uses the perceptual duration).
- Tuning recipe (verbatim intent): pick **duration first** for pacing, then add bounce. bounce 0 = "smooth, gradual"; ~0.15 = brisk, not visibly bouncy; ~0.3 = noticeably bouncy; "be cautious about using values higher than around 0.4". "When you're not sure, use a spring with bounce 0." Add bounce for playful UIs or **at the end of a gesture** (momentum).

### 4.2 Conversion formulas (duration *d*, bounce *b* → mass/stiffness/damping)
The session's code-sample text on developer.apple.com is garbled (reads "damping = 1 - 4π × bounce ÷ duration"). **Verified numerically against the macOS 26 SDK `SwiftUI.Spring` (local `swift` run, 2026-11-02):**
```
mass      = 1
stiffness = (2π / d)²                         // b ≥ 0
damping   = (1 − b) · 4π / d                   // b ≥ 0  (b=0 → critical: 4π/d)
// b < 0 (flattened): ζ = 1/(1+b); damping = 4π / (d·(1+b)); stiffness = (2π/d)² · (2ζ² − 1)
// dampingRatio = 1 − b for b ≥ 0;  response == duration
```
SDK output: `.smooth` = d 0.5, b 0 → k 157.9, c 25.13, settling 0.80 s · `.snappy` = d 0.5, **b 0.15** (ζ 0.85) → c 21.36, settling 0.88 s · `.bouncy` = d 0.5, **b 0.30** (ζ 0.70) → c 17.59, settling 1.04 s. `Animation.default` (iOS 17/macOS 14+) = `spring(response: 0.55, dampingFraction: 1.0)` (was `easeInOut` before) (https://developer.apple.com/documentation/swiftui/animation/default). `interactiveSpring` defaults `response 0.15, dampingFraction 0.86, blendDuration 0.25` (https://developer.apple.com/documentation/swiftui/animation/interactivespring(response:dampingfraction:blendduration:)).
In code, let the API convert: `Spring(duration: 0.5, bounce: 0.2).stiffness` (SwiftUI), `CASpringAnimation(perceptualDuration:bounce:)`, `UIView.animate(duration:bounce:)` (WWDC23 code samples).

### 4.3 Fluid-interface rules (WWDC18 "Designing Fluid Interfaces", https://developer.apple.com/videos/play/wwdc2018/803/)
- **Response**: "people are really, really sensitive to latency… look for delays everywhere" — remove timers/delays; detect all candidate gestures from the start and cancel the losers once intent is clear, rather than waiting.
- **Interruptible & redirectable**: users must be able to reverse mid-animation ("I could just turn back immediately"). Never lock input for the length of a transition.
- **Spatial consistency**: things leave and return along **symmetric paths** (slid in from the right → leave to the right).
- **Hint in the direction** of the result (Control Center modules grow toward their final state while pressed).
- **Lightweight input, amplified output**: on release, compute a *projected* end point from the throw velocity + the scroll view's deceleration rate ("leaning on that familiarity people have with scrolling"), snap to the target nearest the **projected** point, and hand the velocity to a spring. Slide formula ⚠️ (not in transcript text): `projected = pos + (velocity/1000) · rate / (1 − rate)`, `rate ≈ 0.998` (UIScrollView `.normal`).
- **Rubber-banding** at boundaries instead of hard stops; smooth hand-off between tracking objects.
- Spring params for designers = **damping ratio** (100 % = no overshoot … 0 % = oscillates forever) and **response** (how fast it heads to target) — "we like to avoid using duration when we're describing elastic behaviors". "Start with 100% damping"; add overshoot only when "the gesture that's driving the motion itself has momentum" (Now Playing: present 100 %, swipe-dismiss **80 %**).
- Frame content matters, not just fps: too large a jump between adjacent frames "strobes"; higher refresh allows faster movement; motion blur/stretch encode velocity.
- Heavier things get more "mass" (apps) than light things (photos) — a consistent physical vocabulary.

### 4.4 Spring APIs on other stacks (same physics: mass m, stiffness k, damping c; ζ = c / (2√(k·m)))
| Stack | API & defaults (verified) | Notes |
|---|---|---|
| **Motion** (motion.dev, ex-Framer Motion) — source `packages/motion-dom/src/animation/generators/spring.ts` (main, Nov 2026) | `{ type: "spring", visualDuration: 0.3, bounce: 0.25 }` or `{ stiffness, damping, mass }`. Source defaults: **stiffness 100, damping 10, mass 1**; duration 800 ms; **bounce 0.3** (docs page says 0.25 ⚠️ mismatch); `restSpeed` 2 / `restDelta` 0.5 (0.01/0.005 for tiny ranges). `visualDuration` → `k = (2π / (1.2·visualDuration))²`, `c = 2ζ√k`, ζ = 1−bounce ("maps bounce to a damping ratio as SwiftUI does"; negative bounce = overdamped). Physics options override time options. | **Default transitions when you pass nothing**: `x/y/rotate` → spring k 500, c 25 (underdamped); `scale` → k 550, critically damped when target is 0 else c 30; opacity/color → tween 0.3 s `ease: [0.25, 0.1, 0.35, 1]`; >2 keyframes → 0.8 s (`utils/default-transitions.ts`). Set an explicit transition for product UI. `spring(...)` `toString()` emits `"<ms>ms linear(...)"` for CSS. |
| **CSS `linear()`** | Chrome 113 · Firefox 112 · Safari 17.2 (MDN BCD) → OK in WebView2, WKWebView on macOS 14.2+/Safari 17.2+, WebKitGTK (current). | Fixed duration; **no velocity carry-over on interrupt** (Comeau, https://www.joshwcomeau.com/animation/linear-timing-function/, 2025-10-28, upd. 2026-05-05). Generate, don't hand-write (Archibald/Argyle "linear() easing generator", Easing Wizard). Fallback via `@supports (animation-timing-function: linear(0, 1))`. |
| **GNOME libadwaita** `AdwSpringAnimation` (https://gnome.pages.gitlab.gnome.org/libadwaita/doc/main/class.SpringAnimation.html; `adw-spring-params.c`) | `adw_spring_params_new (damping_ratio, mass, stiffness)` (critical damping = 2√(m·k)); `_new_full (damping, mass, stiffness)`; `initial-velocity` for gesture hand-off; `epsilon` 0.001; `clamp` stops at target (no overshoot); `estimated-duration` read-only. | Stock values in §3.2. Under reduced motion the bottom sheet switches to ζ 1.0 and nav view to a crossfade — **except while a swipe gesture is active** (`adw-navigation-view.c`: `use_crossfade = !gesture_active && adw_get_reduce_motion(...)`). |
| **WinUI / Windows App SDK** `SpringNaturalMotionAnimation` (https://learn.microsoft.com/windows/apps/develop/composition/spring-animations, 2026-03) | `compositor.CreateSpringVector3Animation()` / `CreateSpringScalarAnimation()`; `DampingRatio`, `Period` (time of one oscillation), `FinalValue`, `InitialValue`, `InitialVelocity`. **Windows design team values**: Offset normal ζ 0.8 / 50 ms, dampened 0.85 / 50 ms, less-dampened 0.65 / 60 ms; Scale/Size normal 0.7 / 50 ms, dampened 0.8 / 50 ms, less-dampened 0.6 / 60 ms. | Feed into `InteractionTrackerInertiaNaturalMotion` for velocity-aware gesture release. Windows docs frame springs as "livelier… pops" — use sparingly in calm Windows UI. |
| **Flutter** `SpringDescription` (https://api.flutter.dev/flutter/physics/SpringDescription-class.html) | `SpringDescription(mass:, stiffness:, damping:)`, `.withDampingRatio(mass:, stiffness:, ratio = 1.0)`, **`.withDurationAndBounce(duration = 500 ms, bounce = 0.0)`** (Apple-style; version added ⚠️). Drive with `AnimationController.animateWith(SpringSimulation(spring, from, to, velocity))`. | |
| **Qt Quick** `SpringAnimation` (https://doc.qt.io/qt-6/qml-qtquick-springanimation.html) | `spring` (useful 0–5.0, default 0 = off), `damping` (0–1.0, default 0), `mass` 1.0, `epsilon` 0.01, `modulus`, `velocity` (max). | Not the same parametrisation as Apple's; tune by eye (e.g. `spring: 3; damping: 0.3` for follow-the-cursor). |
| **Jetpack Compose / M3** | `spring(dampingRatio, stiffness)`; M3 tokens in §3.2. | Useful as reference values even off-Android. |

**Converting Apple-style (d, bounce) for any engine**: `m = 1; k = (2π/d)²; c = (1−bounce)·4π/d; ζ = 1−bounce`. Example d 0.35 s, bounce 0.15 → k 322.3, c 30.5, ζ 0.85. WinUI `Period` is *not* Apple's duration (Microsoft: "the time it takes the spring to perform a single oscillation"; its recommended 50–60 ms values are much shorter than Apple durations) — don't convert, start from Microsoft's table and tune by eye ⚠️.

**Pre-computed `linear()` springs** (sampled from the Apple formula above, 25 points, settle ε 0.002 — use the settle time as the CSS duration):
```css
:root{
  /* d 0.30 s, bounce 0 (smooth) — settle ≈ 400 ms */
  --spring-smooth: linear(0, 0.049, 0.158, 0.285, 0.412, 0.526, 0.624, 0.706, 0.772, 0.825, 0.867, 0.899, 0.924, 0.943, 0.957, 0.968, 0.976, 0.983, 0.987, 0.991, 0.993, 0.995, 0.996, 0.997, 1);
  /* d 0.35 s, bounce 0.15 (snappy) — settle ≈ 450 ms, 0.6 % overshoot */
  --spring-snappy: linear(0, 0.047, 0.154, 0.287, 0.423, 0.548, 0.658, 0.749, 0.822, 0.878, 0.92, 0.951, 0.972, 0.987, 0.996, 1.002, 1.005, 1.006, 1.006, 1.006, 1.005, 1.004, 1.003, 1.003, 1);
}
.panel{ transition: transform 400ms var(--spring-smooth); }
```

## 5. Perceived performance & waiting

### 5.1 Response-time limits
- **0.1 s** — "about the limit for having the user feel that the system is reacting instantaneously"; **1 s** — "the limit for the user's flow of thought to stay uninterrupted"; **10 s** — "the limit for keeping the user's attention focused" (Nielsen 1993, https://www.nngroup.com/articles/response-times-3-important-limits/, citing Miller 1968, AFIPS FJCC, DOI 10.1145/1476589.1476628, and Card, Robertson & Mackinlay 1991).
- ⇒ Every click/keypress must produce a visible change within **100 ms** (pressed state, optimistic result, or at least a cursor/state change); motion that *starts* within that frame is fine even if it lasts 200 ms.
- **Doherty threshold (400 ms)** — traces to Walter J. Doherty & Ahrvind J. Thadhani, "The Economic Value of Rapid Response Time" (IBM report, 1982; report no. GE20-0752-0 ⚠️ unverified), building on Thadhani 1981 "Interactive user productivity", IBM Systems Journal 20(4):407–423, DOI 10.1147/sj.204.0407 and Doherty & Kelisky 1979, IBM Sys J 18(1), DOI 10.1147/sj.181.0143 — productivity studies of *system response time on mainframe terminals*, not a perceptual constant. Kent Beck: "No research says 'human attention starts to slip at exactly 400 milliseconds'… a practically motivated threshold" (https://newsletter.kentbeck.com/p/the-precious-eyeblink). Treat "<400 ms" as an engineering target, cite 0.1/1/10 for perception.
- WWDC18: "people are really, really sensitive to latency… look for delays everywhere" (§4.3).

### 5.2 Progress indicators
- **Myers 1985**, "The importance of percent-done progress indicators for computer-human interfaces", CHI '85, pp. 11–17, DOI 10.1145/317456.317459 (PDF https://www.cs.cmu.edu/~bam/papers/percentdoneCHI85.pdf): "people prefer to have progress indicators" — **86.1 %** of subjects preferred the version with a percent-done indicator (p = 0.0006 on semantic-differential ratings); the predicted preference for *constant* response time was **not** significant.
- **NN/g thresholds** (Sherwin 2014, https://www.nngroup.com/articles/progress-indicators/): immediate visual acknowledgement always; **< 1 s → no indicator** ("distracting"); **2–10 s → looped/indeterminate**; **≥ 10 s → percent-done + time estimate**, offer Cancel; "Updating 3 of 50" counts; never static "please wait"; never "don't click twice" warnings — show the first click registered.
- **Harrison, Amento, Kuznetsov & Bell 2007**, "Rethinking the progress bar", UIST '07 pp. 115–118, DOI 10.1145/1294211.1294231 (PDF https://chrisharrison.net/projects/progressbars/ProgBarHarrison.pdf): 9 progress functions over 5.5 s; bars with **pauses near the end** (Late Pause, Wavy) were perceived **slower** than linear; **accelerating** bars (Power, Fast Power — fastest progress near the end) perceived **faster**. Design: "progress can be downplayed in the beginning and accelerated towards the end"; cache early progress to smooth later stalls; put slow/variable stages (network) **first**.
- **Harrison, Yeo & Hudson 2010**, "Faster progress bars: manipulating perceived duration with visual augmentations", CHI '10 pp. 1545–1548, DOI 10.1145/1753326.1753556 (PDF https://chrisharrison.net/projects/progressbars2/ProgressBarsHarrison.pdf): pulsation with **increasing** frequency beats decreasing; ribbing moving **backwards** (against progress) beats still/forward; best = "animated ribbing that move[s] backwards in a decelerating manner" → perceived duration **−11 %** vs solid bar.
- Determinate vs indeterminate on Windows: determinate `ProgressBar` when known; indeterminate `ProgressBar` = non-blocking; `ProgressRing` = blocking (windows.md §8).

### 5.3 Spinners, skeletons, optimistic UI
- **Flicker control**: delay showing a spinner **~150–300 ms**, then keep it **≥ 300–500 ms** once shown (Vercel guidelines). NN/g skeletons: "< 1 second… skeleton screens or spinners aren't necessary" (https://www.nngroup.com/articles/skeleton-screens/, Tankala 2023, reviewed 2026-09).
- **Skeletons** for full-view/structured content loads < 10 s; spinners for a single module (one card/video); progress bar for downloads/uploads/conversions; avoid "frame-display" skeletons (only header/footer). Skeleton must match the final layout (same heights) so the swap causes **zero layout shift**; cross-fade content in over 150–200 ms; a subtle pulse/shimmer (1.5–2 s loop) is optional and must stop under reduced motion. "Skeleton screens do not replace performance-optimization efforts."
- **Optimistic UI**: "Update the UI immediately when success is likely; reconcile on server response… On failure, show an error & roll back or provide Undo" (Vercel). Pair destructive actions with **undo instead of confirm** (GNOME HIG principle "Allow destructive actions to be undone instead of asking for confirmation").
- Faster-spinning spinners make waits *feel* shorter (Kowalski, practitioner); Apple's indeterminate indicators and Windows ProgressRing already tuned — use them.

## 6. Practitioner craft (opinions from respected practitioners — not standards)

### 6.1 Emil Kowalski (Sonner, Vaul; emilkowal.ski, animations.dev; his own agent skills repo https://github.com/emilkowalski/skills — `skills/review-animations/STANDARDS.md`)
- **Frequency decides** (STANDARDS.md): 100+×/day (shortcuts, command-palette toggle) → "No animation. Ever."; tens/day (hover, list nav) → remove or drastically reduce; occasional (modals, drawers, toasts) → standard; rare/first-time (onboarding, celebrations) → delight allowed. "Never animate keyboard-initiated actions" (also https://emilkowal.ski/ui/you-dont-need-animations — Raycast's palette has no open animation).
- **Easing**: enter/exit → ease-out; on-screen move/morph → ease-in-out; hover/color → `ease`; constant motion → linear. "**Never `ease-in` on UI**" (it delays the moment the user is watching). Built-ins are weak; his tokens: `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)`, `--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1)`, `--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1)`. **Conflict:** differs from Windows/Material, which use *accelerate* curves for exits (§3) — on native Windows follow the platform; in custom web-tech UIs a fast ease-out exit is defensible.
- **Durations**: button press 100–160 ms · tooltips/small popovers 125–200 · dropdowns/selects 150–250 · modals/drawers 200–500 · "UI animations stay under 300ms" ("A 180ms dropdown feels more responsive than a 400ms one") (https://emilkowal.ski/ui/7-practical-animation-tips).
- **Physicality**: press = `scale(0.97)` on `:active` with `transition: transform 160ms ease-out` (range 0.95–0.98). "Never `scale(0)`" → enter from `scale(0.9–0.97)` + `opacity: 0` (tip example: 0.93). **Origin-aware popovers**: `transform-origin` at the trigger (Radix `--radix-dropdown-menu-content-transform-origin`, Base UI `--transform-origin`); modals exempt (center).
- **Tooltips**: delay the first; once one is open, neighbours open with **no delay and no animation** (Base UI `[data-instant] { transition-duration: 0ms }`); tooltip anim `125ms ease-out`, from `opacity:0; scale(0.97)`.
- **Interruptibility**: CSS *transitions* retarget mid-flight; `@keyframes` restart from zero → use transitions (or springs) for anything re-triggerable (toasts, toggles).
- **Springs**: prefer `{ type: "spring", duration: 0.5, bounce: 0.2 }`; keep bounce 0.1–0.3, mostly 0 in UI; bounce for drag-to-dismiss/playful. Decorative mouse-follow → `useSpring`, not raw pointer position.
- **Asymmetric timing**: slow where the user decides (hold-to-confirm 2 s linear), fast where the system responds (release 200 ms ease-out).
- **Stagger** 30–80 ms per item; never block interaction during it.
- **Blur bridge**: if a crossfade shows two states, add `filter: blur(2px)` during it (keep < 20 px; costly in Safari).
- **Gestures**: dismiss on velocity (`|distance|/ms > ~0.11`), not only distance; rubber-band past edges; pointer capture during drag; ignore extra pointers once dragging.
- **Perf**: "Only animate `transform` and `opacity`"; don't drive children via a CSS variable on the parent (style recalc for all children); Motion's `x`/`y`/`scale` shorthands run on rAF (main thread) and can drop frames under load — a full `transform` string can be hardware-accelerated (⚠️ practitioner claim; check Motion's current docs). CSS/WAAPI keep running when JS is busy.
- **Debug**: play at 2–5× slower; DevTools Animations panel; review with fresh eyes next day.
- **Reduced motion** "means fewer and gentler animations, not zero".

### 6.2 Rauno Freiberg — "Invisible Details of Interaction Design" (July 2023, https://rauno.me/craft/interaction-design)
- **Frequency × novelty**: "When so commonly executed, the interaction novelty is also diminished" — the 100th repetition of an animated keyboard action feels like lag.
- **Kinetic physics**: thrown things keep momentum and angle ("the gesture retains the momentum and angle at which it was thrown").
- **Interruptibility**: criticises iOS Settings because "swiping back immediately does not interrupt the animation".
- **Metaphors**: "Great interaction design rewards learning by reusing metaphors" (paging like a book).
- **Spatial consistency**: motion shows where things live (app switcher order, origin of audio).
- "Truly fluid gestures are immediately responsive"; destructive actions commit at gesture *end*, lightweight overlays can trigger mid-gesture.

### 6.3 Vercel Web Interface Guidelines — Animation & loading (https://vercel.com/design/guidelines)
- "Provide a reduced-motion variant." · "Prefer CSS, avoid main-thread JS-driven animations when possible" (CSS > WAAPI > JS libs) · animate `transform`/`opacity`, avoid `width/height/top/left` · "Only animate when it clarifies cause & effect" or "adds deliberate delight" · "Choose easing based on what changes (size, distance, trigger)" · "Animations are cancelable by user input" · no autoplay except muted non-essential loops; motion > 5 s needs pause/stop/hide · "Anchor motion to where it 'physically' starts" (transform-origin) · **never `transition: all`** — list properties · SVG: animate `<g>` wrappers with `transform-box: fill-box; transform-origin: center`.
- Loading: spinner **show-delay ~150–300 ms** and **minimum visible ~300–500 ms** to avoid flicker; loading buttons keep their label + indicator; "Saving…" ends with an ellipsis.
- Optimistic: "Update the UI immediately when success is likely; reconcile on server response." On failure show an error and roll back or offer Undo.
- Tooltips: "Delay the first tooltip in a group; subsequent peers have no delay." Hover/active/focus states have more contrast than rest. `:focus-visible` over `:focus`.

### 6.4 Josh W. Comeau (joshwcomeau.com)
- "A friendly introduction to spring physics" (2020, updated 2025-11-03): springs are for *motion*, not color/opacity; mass = inertia, tension = snappiness, friction = settling.
- "linear()" article (2025-10-28, updated 2026-05-05, https://www.joshwcomeau.com/animation/linear-timing-function/): `linear()` "only draws straight lines between a set of provided points"; generate it (Linear() Easing Generator by Jake Archibald & Adam Argyle; Easing Wizard); interrupted CSS transitions reverse "without carrying over the element's current velocity"; ~88 % global support in Oct 2025 → `@supports (animation-timing-function: linear(0, 1))` fallback; gate the transition inside `@media (prefers-reduced-motion: no-preference)`.

### 6.5 Apple (WWDC26 "Principles of great design", https://developer.apple.com/videos/play/wwdc2026/250/)
- Craft = "Responsive animations that feel fluid and provide immediate, natural feedback". "The way to make a design delightful isn't by adding confetti or tacking on extra flourishes at the end of your process."

## 7. Implementation per stack

### 7.0 Performance rules (all stacks)
- Frame budget **16.7 ms @ 60 Hz, 8.3 ms @ 120 Hz** (ProMotion MacBook Pros, many Windows laptops); budget includes your JS/Swift work + layout + paint. "It's not just about framerate. It's what's in the frames" — large per-frame jumps strobe (WWDC18).
- Animate **compositor-only properties**: `transform` (translate/scale/rotate) and `opacity` (+ `filter`/`clip-path` in modern engines, costlier). Never animate `width/height/top/left/margin/padding` per frame; use FLIP (measure → invert with transform → play) or the platform's layout animation (SwiftUI, Motion `layout`, View Transitions). Vercel: "never `transition: all`".
- `will-change: transform` only on elements *about to* animate (add on hover/pointerdown, remove after) — each promoted layer costs GPU memory.
- Don't read layout (`getBoundingClientRect`, `offsetHeight`) between writes in the same frame (layout thrash); batch reads, then writes, inside `requestAnimationFrame`.
- Prefer CSS transitions/WAAPI (run off the main thread) for fixed motion; JS springs for interruptible/gesture-driven motion (Kowalski, Vercel: "CSS > Web Animations API > JavaScript libraries").
- Measure: Chrome/Edge DevTools Performance + Animations panel (slow to 10–25 %), Safari Web Inspector Timelines, Xcode Instruments (Animation Hitches / Core Animation), Windows: PresentMon/WPA, GTK Inspector (`GTK_DEBUG=interactive`) FPS overlay.

### 7.1 Web tech (Electron / Tauri / WebView2 / WKWebView / WebKitGTK)
Engines: Electron = Chromium (current); Tauri = WebView2 (Chromium) on Windows, **WKWebView = the OS's Safari version** on macOS, **WebKitGTK** on Linux — feature-detect, don't UA-sniff.
```css
:root{ --ease-out: cubic-bezier(0.23,1,0.32,1); --ease-in-out: cubic-bezier(0.77,0,0.175,1);
       --dur-1: 100ms; --dur-2: 150ms; --dur-3: 200ms; --dur-4: 250ms; }
.btn{ transition: background-color var(--dur-1) ease, transform 160ms var(--ease-out); }
.btn:active{ transform: scale(.97); }
@media (hover:hover) and (pointer:fine){ .row:hover{ background: var(--hover-bg); } }

/* Enter/exit for top-layer UI incl. display:none (no JS) */
[popover], dialog{
  opacity:0; transform: scale(.96); transform-origin: var(--origin, top left); /* popover: at its trigger */
  transition: opacity 150ms var(--ease-out), transform 150ms var(--ease-out),
              display 150ms allow-discrete, overlay 150ms allow-discrete;
}
dialog{ transform-origin: center; }                                    /* modals: centered (Kowalski) */
[popover]:popover-open, dialog[open]{ opacity:1; transform:none; }
@starting-style{ [popover]:popover-open, dialog[open]{ opacity:0; transform:scale(.96); } }

@media (prefers-reduced-motion: reduce){
  *,*::before,*::after{ transition-duration:0.01ms !important; animation-duration:0.01ms !important; animation-iteration-count:1 !important; scroll-behavior:auto !important; }
  /* then opt specific opacity/color transitions back in — see §8 */
}
```
Support (MDN BCD, Nov 2026): `@starting-style` Chrome 117 / Firefox 129 / Safari 17.5; `transition-behavior: allow-discrete` Chrome 117 / Safari 17.4 / Firefox 129 (partial); `overlay` **Chromium only** (Safari/Firefox ignore it — harmless); popover API Chrome 114 / Firefox 125 / Safari 17; `interpolate-size: allow-keywords` (animate to `height:auto`) **Chromium 129+ only** → elsewhere use `grid-template-rows: 0fr → 1fr`.
**View Transitions (same-document)**: `document.startViewTransition(update)` — Chrome/Edge 111, Safari 18.0, Firefox 144 (Baseline since Oct 2025); cross-document Chrome 126 / Safari 18.2. Spec default `animation-duration: 0.25s` (https://drafts.csswg.org/css-view-transitions-1/). WebKitGTK ships them since 2.46 (https://webkitgtk.org/2024/10/04/webkitgtk-2.46.html), **but** a WebKitGTK 2.52.6 segfault when `startViewTransition()` forces accelerated compositing with `WEBKIT_DISABLE_DMABUF_RENDERER=1` (a common Tauri/NVIDIA workaround) led Stirling-PDF to drop VT on Linux (open PR, Oct 2026: https://github.com/Stirling-Tools/Stirling-PDF/pull/8680). ⇒ wrap it:
```js
const reduce = matchMedia('(prefers-reduced-motion: reduce)');
function transition(update){
  if (!document.startViewTransition || reduce.matches || window.__skipViewTransitions /* host flag set by Tauri/Rust on Linux, not UA sniffing */) return update();
  return document.startViewTransition(update);
}
/* CSS: ::view-transition-group(*){ animation-duration:200ms; animation-timing-function:cubic-bezier(.2,0,0,1) } */
```
**Motion for React** (`npm i motion`, `import { motion, AnimatePresence, MotionConfig, useReducedMotion } from "motion/react"`):
```jsx
<MotionConfig reducedMotion="user" transition={{ type:"spring", visualDuration:0.25, bounce:0 }}>
  <AnimatePresence initial={false}>
    {open && <motion.div key="menu" initial={{opacity:0, scale:.96}} animate={{opacity:1, scale:1}}
                exit={{opacity:0, transition:{duration:.12}}} style={{transformOrigin:"var(--origin)"}} />}
  </AnimatePresence>
  {items.map(i => <motion.li key={i.id} layout />)}   {/* reorder/add/remove via FLIP */}
</MotionConfig>
```
`reducedMotion="user"` (default is `"never"`!) disables transform and layout animations; "Other animations, like `opacity` and `backgroundColor`, will persist" (https://motion.dev/docs/react-motion-config).

### 7.2 SwiftUI (macOS 14+)
```swift
// these lines type-check against the macOS 26 SDK inside a View (swiftc -typecheck, 2026-11-02)
@Environment(\.accessibilityReduceMotion) private var reduceMotion
withAnimation(.snappy(duration: 0.25)) { isExpanded.toggle() }           // explicit
Text(count, format: .number).contentTransition(.numericText(countsDown: delta < 0)) // macOS 13+
  .animation(.snappy, value: count)                                          // implicit, scoped to value
Image(systemName: "checkmark.circle").symbolEffect(.bounce, value: copiedTick)      // SF Symbols effects
.matchedGeometryEffect(id: item.id, in: ns)                                  // shared-element move
Image(systemName: copied ? "checkmark" : "doc.on.doc").contentTransition(.symbolEffect(.replace)) // copy → ✓
TextField("Password", text: $pw)                                             // error shake (skip if reduceMotion)
  .keyframeAnimator(initialValue: 0.0, trigger: reduceMotion ? 0 : errorTick) { v, x in v.offset(x: x) } keyframes: { _ in
    KeyframeTrack { LinearKeyframe(8, duration: 0.05); LinearKeyframe(-7, duration: 0.07); LinearKeyframe(5, duration: 0.07)
                    LinearKeyframe(-3, duration: 0.07); SpringKeyframe(0, duration: 0.1) } }   // ≈0.36 s
withAnimation(.smooth) { … } completion: { … }                               // perceptual-duration completion (iOS 17/macOS 14)
NSHapticFeedbackManager.defaultPerformer.perform(.alignment, performanceTime: .now) // Force Touch trackpad
```
`PhaseAnimator`/`KeyframeAnimator` macOS 14+ ("avoid performing any expensive operations directly within content" — it runs every frame). Haptics: "Call this method only in response to user-initiated actions… visual feedback… should accompany the feedback" (`perform(_:performanceTime:)` docs); patterns `.generic`, `.alignment` (snapping to guides), `.levelChange` (pressure levels). WWDC26: `.reorderable()` on `ForEach` + `.reorderContainer()` on the parent gives system lift/drop animations in any container (List, LazyVGrid, stacks) (https://developer.apple.com/videos/play/wwdc2026/269/).
**AppKit**: `NSAnimationContext.runAnimationGroup({ ctx in ctx.duration = 0.2; ctx.timingFunction = CAMediaTimingFunction(name: .easeOut); ctx.allowsImplicitAnimation = true; view.animator().alphaValue = 1 }, completionHandler: nil)`; macOS 15+: `NSAnimationContext.animate(.spring(duration: 0.3)) { view.frame = f }` takes a **SwiftUI `Animation`** (listed on the NSAnimationContext doc page). Reduce motion: `NSWorkspace.shared.accessibilityDisplayShouldReduceMotion` + `NSWorkspace.accessibilityDisplayOptionsDidChangeNotification` on `NSWorkspace.shared.notificationCenter` ("avoid large animations, especially those that simulate the third dimension"). Frame-synced work: `NSView.displayLink(target:selector:)` → `CADisplayLink` in sync with the view's display (not invoked while hidden).

### 7.3 WinUI 3 / Windows App SDK
- Prefer built-ins: page transitions (`EntranceNavigationTransitionInfo`, `DrillInNavigationTransitionInfo`, `SlideNavigationTransitionInfo`, `SuppressNavigationTransitionInfo`), `ConnectedAnimationService` (`PrepareToAnimate`/`TryStart`), list `ItemContainerTransitions` (`AddDeleteThemeTransition`, `RepositionThemeTransition`, `EntranceThemeTransition`), `AnimatedIcon` (Lottie) — details in windows.md §9.
```xml
<Border x:Name="Card">
  <Border.OpacityTransition><ScalarTransition Duration="0:0:0.083"/></Border.OpacityTransition>
  <Border.TranslationTransition><Vector3Transition Duration="0:0:0.167"/></Border.TranslationTransition>
</Border>  <!-- now setting Card.Opacity / Card.Translation animates implicitly -->
```
```csharp
var ui = new Windows.UI.ViewManagement.UISettings();
bool motion = ui.AnimationsEnabled;                 // Settings › Accessibility › Visual effects › Animation effects
var s = compositor.CreateSpringVector3Animation(); s.DampingRatio = 0.8f; s.Period = TimeSpan.FromMilliseconds(50);
s.FinalValue = new Vector3(0, 0, 0); visual.StartAnimation("Offset", s);
```
Chromium (Electron/WebView2) derives `prefers-reduced-motion` on Windows from `SPI_GETCLIENTAREAANIMATION` (= Animation effects), re-read on `WM_SETTINGCHANGE` (Chromium `ui/gfx/animation/animation_win.cc`).

### 7.4 GTK 4 / libadwaita
```c
AdwAnimationTarget *t = adw_property_animation_target_new (G_OBJECT (revealer_child), "opacity");
AdwAnimation *a = adw_timed_animation_new (GTK_WIDGET (self), 0.0, 1.0, 200, t);
adw_timed_animation_set_easing (ADW_TIMED_ANIMATION (a), ADW_EASE_OUT_CUBIC);
adw_animation_play (a);   /* auto-skips to end if widget unmapped or gtk-enable-animations = FALSE */

AdwSpringParams *p = adw_spring_params_new (1.0, 1.0, 1000.0);           /* ζ, mass, stiffness */
AdwAnimation *sp = adw_spring_animation_new (w, from, to, p, t);
adw_spring_animation_set_initial_velocity (ADW_SPRING_ANIMATION (sp), velocity); /* from the swipe */
```
Prefer stock `AdwNavigationView`, `AdwDialog`, `AdwBottomSheet`, `GtkRevealer`, `GtkStack` transitions — they already honour reduced motion (libadwaita 1.9 / GTK 4.23+, see linux.md §5). Reduced-motion: `GtkSettings:gtk-interface-reduced-motion` (`GtkReducedMotion`, **GTK 4.22+**; https://docs.gtk.org/gtk4/property.Settings.gtk-interface-reduced-motion.html), libadwaita helper `adw_get_reduce_motion()` (internal); CSS `@media (prefers-reduced-motion: reduce)`. Distinct from `gtk-enable-animations` (= "animations off entirely").

### 7.5 Qt
```qml
Rectangle { id: card
  Behavior on opacity { NumberAnimation { duration: 150; easing.type: Easing.OutCubic } }
  Behavior on x { SpringAnimation { spring: 3; damping: 0.3 } }   // follows a moving target
}
```
Widgets: `QPropertyAnimation(widget, "pos")` + `QEasingCurve::OutCubic`; style default animation 200 ms. Reduced motion: `QGuiApplication::styleHints()->accessibility()->motionPreference()` + `motionPreferenceChanged` (`QAccessibilityHints`, accessor since 6.10, property **since 6.12**, https://doc.qt.io/qt-6/qaccessibilityhints.html; on Linux fed by portal `reduced-motion` and GNOME `enable-animations`; on Android "Remove animations").

### 7.6 Flutter
Implicit: `AnimatedContainer`, `AnimatedOpacity`, `AnimatedSwitcher`, `AnimatedSize`, `TweenAnimationBuilder` (duration + `Curves.easeOutCubic`, or M3 tokens `Durations.short4`/`medium2`… and `Easing.emphasizedDecelerate` from `package:flutter/material.dart`). Explicit: `AnimationController(vsync: this, duration: …)`; physics: `controller.animateWith(SpringSimulation(SpringDescription.withDurationAndBounce(duration: Duration(milliseconds: 300)), 0, 1, velocity))`. Reduced motion: `MediaQuery.disableAnimationsOf(context)` (rebuilds only when that flag changes); `AccessibilityFeatures.reduceMotion` = "certain animations be simplified and parallax effects removed". Which desktop OS settings feed these flags is undocumented ⚠️ — on Linux read the portal yourself.

## 8. Reduced motion done right
**Who/why**: vestibular disorders, migraine, motion sensitivity, attention disorders. WCAG 2.3.3 *Animation from Interactions* (AAA): motion triggered by interaction can be disabled unless essential; WCAG 2.2.2 *Pause, Stop, Hide* (A): auto-moving content > 5 s needs a control; WCAG 2.3.1: no more than 3 flashes/second.
**Replace, don't just delete** (Kowalski: "fewer and gentler animations, not zero"; Apple: Liquid Glass under Reduce Motion "decreases the intensity of some effects and disables any elastic properties" — WWDC25 "Meet Liquid Glass", https://developer.apple.com/videos/play/wwdc2025/219/):
| Normal | Reduced |
|---|---|
| Slide / push / drill-in page transitions | Cross-fade 150–200 ms (libadwaita does exactly this) or instant |
| Zoom / scale-from-origin popovers, modal scale-in | Opacity fade ≤150 ms, no scale |
| Parallax, background zoom, scroll-linked motion, auto-scrolling, smooth `scroll-behavior` | Off (static); jump scroll |
| Spring overshoot / bounce / shake | Critically damped or none; error = color + icon + text |
| Looping decorative animation, shimmer skeletons, animated illustrations | Static frame; skeleton without shimmer |
| Large-distance motion, 3-D flips, rotation | Fade |
| **Keep**: opacity, color/background changes, focus rings, progress bars and spinners (essential status), pressed states, text/number updates | — |
| **Keep direct manipulation**: content that tracks the pointer/finger during drag/swipe (libadwaita keeps the slide while `gesture_active`) | — |
**Read the setting everywhere — and listen for changes at runtime:**
| Platform | Read | Change signal |
|---|---|---|
| Web/Electron/Tauri | `matchMedia('(prefers-reduced-motion: reduce)')` (Chrome 74, Firefox 63, Safari 10.1) | `mql.addEventListener('change', …)` |
| macOS AppKit | `NSWorkspace.shared.accessibilityDisplayShouldReduceMotion` (10.12+) | `NSWorkspace.accessibilityDisplayOptionsDidChangeNotification` (workspace notification center) |
| SwiftUI | `@Environment(\.accessibilityReduceMotion)` | automatic |
| Windows | `UISettings.AnimationsEnabled` (Settings › Accessibility › Visual effects › Animation effects); Win32 `SystemParametersInfo(SPI_GETCLIENTAREAANIMATION)` | `UISettings.AnimationsEnabledChanged` (fires off UI thread) / `WM_SETTINGCHANGE` |
| GNOME/GTK | `GtkSettings:gtk-interface-reduced-motion` (4.22+), `gtk-enable-animations`; CSS media query | `notify::` on the property |
| Any Linux (Flatpak/KDE/Electron main process) | Portal `org.freedesktop.portal.Settings` → `org.freedesktop.appearance` / `reduced-motion` (u: 0 no-pref, 1 reduce) | `SettingChanged` signal (linux.md §8) |
| Qt 6.12+ | `QAccessibilityHints::motionPreference` | property notify |
| Flutter | `MediaQuery.disableAnimationsOf(context)`, `AccessibilityFeatures.reduceMotion` | rebuild |
Electron on Linux: Chromium's mapping from the portal/GNOME key is unverified ⚠️ → read the portal in the main process and set a `data-reduce-motion` attribute on `<html>`; style with `:root[data-reduce-motion] …` *and* the media query.
**Pattern (web)** — opt-in motion rather than opt-out, so the default is safe:
```css
.sheet{ transition: opacity 150ms ease-out; }                         /* everyone gets the fade */
@media (prefers-reduced-motion: no-preference){
  .sheet{ transition: opacity 150ms ease-out, transform 250ms var(--ease-out); }
  .sheet[data-state=closed]{ transform: translateY(8px) scale(.98); }
}
```
Also offer an in-app "Reduce motion" toggle (System / On / Off) in Settings for apps with heavy motion (Fluent 2: ship a "no motion" option).

## 9. Desktop microinteraction catalog
Numbers are defaults to start from (synthesised from §1–§8; individual sources cited inline). "Instant" = same frame, no transition. Under reduced motion apply §8.

| Interaction | Recommended behaviour | Numbers |
|---|---|---|
| **Hover** (rows, buttons, toolbar items) | Background/color tint only; no movement, no scale on dense UI; gate with `@media (hover:hover) and (pointer:fine)`. Show affordances (row actions) on hover *and* on focus/selection. | in 0–100 ms `ease`; out ≤150 ms; hover *reveal* of previews/cards after ~300–500 ms intent delay ⚠️ |
| **Press / active** | Darken/tint immediately; optional `scale(0.97)` for prominent buttons (Kowalski; range 0.95–0.98); never on list rows/menu items. | press feedback 0 ms (same frame); release 100–160 ms ease-out |
| **Focus ring** | Appears **instantly** on keyboard focus (`:focus-visible`), never fades in (it's keyboard-driven); may move instantly between items. macOS: use the system focus ring (it has its own animation). | 0 ms; 2 px ring + offset; never `outline: none` without replacement |
| **Toggle / switch / checkbox / radio** | Knob slides, track tints; checkmark may draw. State is readable mid-animation; click again mid-flight = retarget (spring/transition, not keyframes). | ~100 ms (NN/g "roughly 100 ms"; M2 switch 100 ms) or spring d 0.2–0.25, bounce 0 |
| **Button async (loading)** | Keep the label, add a spinner/progress inside, lock width (no layout jump), disable re-submit. Don't show the spinner for fast responses. | show spinner after 150–300 ms; keep ≥300–500 ms once shown (Vercel); end with "Saving…" |
| **Copy to clipboard** | Modify the trigger, don't add UI: icon swaps to ✓ (SwiftUI `.contentTransition(.symbolEffect(.replace))` / `symbolEffect`), tooltip/label "Copied". Announce via a11y live region. | swap 100–150 ms; revert after ~1.5–2 s ⚠️ practitioner |
| **Inline edit / rename (F2, Enter, double-click)** | Swap label↔field in place with **no** motion (keyboard-driven); select the editable part (filename without extension); Esc cancels, Enter/blur commits; brief success tint optional. | 0 ms swap; optional 150 ms background flash on commit |
| **Drag & drop — lift** | Start only after the platform threshold (macOS drag image after "about three points"; Windows `GetSystemMetrics(SM_CXDRAG)`; GTK `gtk-dnd-drag-threshold` default 8 px, https://docs.gtk.org/gtk4/property.Settings.gtk-dnd-drag-threshold.html). Translucent drag image, slight lift (scale 1.02–1.04 + shadow); multi-item → stack + count badge. | lift 100–150 ms; image tracks pointer 1:1 every frame (no easing/lag — Chang & Ungar "solidity") |
| **Drag — targets & insertion** | Highlight **only valid** targets on hover; insertion line/gap between items; siblings slide apart to make room; auto-scroll near edges; spring-load folders/tabs after a hover pause. | siblings 150–200 ms spring (bounce 0); spring-loading ~500–700 ms hover ⚠️ |
| **Drag — drop / cancel / fail** | Drop: item settles into place, stays **selected** (HIG). Cancel (Esc) or invalid drop: animate back to source if visible, or "scale up and fade out… evaporating" (HIG drag-and-drop). Undoable. | settle 150–250 ms; snap-back 200–300 ms ease-out/spring |
| **List reorder** | Pointer: live sibling displacement (above). Keyboard (Alt/⌥+↑↓): move instantly or ≤150 ms and keep focus on the moved row. SwiftUI 2026: `.reorderable()` + `.reorderContainer()`; web: Motion `layout`; WinUI `RepositionThemeTransition`. | 150–200 ms |
| **Add list item** | New row expands from 0 height then fades/slides in from its source (e.g. from the "+" or the composer); scroll it into view; highlight briefly. Skip animation for bulk inserts (> ~5–10 rows) or initial load. | height 150–200 ms + fade 150 ms; highlight fade-out 1–2 s |
| **Remove list item** | Fade out, then collapse the gap (two stages, Heer & Robertson "staging"); move focus/selection to the next item; offer Undo. | fade 100–150 ms → collapse 150–200 ms |
| **Optimistic update + undo toast** | Apply instantly; show toast "Deleted 3 items — Undo"; reconcile; on failure revert with an error message (Vercel). Prefer undo over confirm dialogs (GNOME principle). | toast timeout ≈ 5 s (libadwaita `AdwToast:timeout` default 5; scale by Windows `UISettings.MessageDuration`) |
| **Toast enter/exit** | Enter and leave via the **same edge** (Kowalski/Sonner); stack, don't overlap; **pause timer while hovered or focused** (libadwaita: toasts "cannot disappear while being hovered… or have keyboard focus inside"). | libadwaita show/hide 300 ms; web 200–300 ms in, 150–200 out; `translateY(100%)`→0 + fade |
| **Number / count change** | `font-variant-numeric: tabular-nums` so width doesn't jitter; roll digits (`contentTransition(.numericText(countsDown:))`) only for small, meaningful changes; large jumps update instantly. | 200–300 ms spring; none for live-updating streams (> ~2 updates/s) |
| **Loading → content** | Reserve final layout (skeleton same size) → cross-fade content in; **zero layout shift**; don't animate each item separately on large lists (stagger max 30–80 ms × first ~6 items). | nothing < 1 s; cross-fade 150–200 ms |
| **Sidebar collapse/expand** | Animate the sidebar's width/offset and let content reflow once (or overlay + slide on narrow windows); remember state; shortcut toggle (⌃⌘S / Ctrl+B) may animate since it's a spatial change, but keep it short. | 200–250 ms standard curve / spring d 0.25 bounce 0; libadwaita uses spring ζ 1, m 0.5, k 500 |
| **Panel / split resize (user drag)** | **No animation** — follow the pointer 1:1 at display rate; snap/collapse thresholds animate; double-click divider to reset (animated). | 0 ms tracking; snap 150–200 ms |
| **Menu / dropdown / context menu** | Opens at the pointer/trigger, **origin-aware** scale 0.96→1 + fade or simply instant; native menus: let the OS do it. Close on selection instantly or ≤100 ms fade; hover highlight inside menus is instant. Keyboard-opened → instant. | open 0–150 ms; close 0–100 ms |
| **Popover / tooltip** | Popover: origin-aware scale 0.96–0.97 + fade. Tooltip: delay first (platform: 500 ms Win32/GTK), then warm mode with **no delay & no animation** for neighbours (Win32 reshow 100 ms, GTK 60 ms, Qt 20 ms). | popover 120–150 ms; tooltip fade 100–125 ms |
| **Modal / dialog / sheet** | Backdrop fade + panel fade/scale 0.96→1 (centered origin) or the platform sheet (macOS sheets slide from the title bar — system-managed); focus moves into the dialog on open, back to the trigger on close. | in 200–250 ms ease-out; out 150 ms; M2 dialog fade 150 in / 75 out |
| **Command palette (⌘K / Ctrl+K)** | **No open animation** (Raycast) or ≤100 ms opacity; input focused on the first frame; results update instantly as you type; selection highlight jumps instantly with ↑↓. | 0–100 ms |
| **Tab switch** | Content swaps instantly (or ≤100–150 ms cross-fade); the selected-tab indicator may slide when *clicked*; keyboard tab cycling (Ctrl+Tab) instant. Fluent 2: top-level nav = quick fade, not slide. | indicator 150–200 ms; content 0–150 ms |
| **Page / view navigation (drill-in, back)** | Forward = new view enters from the direction of the hierarchy, back = symmetric reverse (WWDC18 spatial consistency); Windows: `DrillInNavigationTransitionInfo` / `EntranceNavigationTransitionInfo`; GNOME `AdwNavigationView`. | 250–300 ms in; exits faster (Windows fwd: fade-out 150 → slide-in 300) |
| **Success** | Inline confirmation where the action happened (✓ morph on the button, row tint). Celebrations only for rare milestones (signature moment). Never block the next action. | 200–400 ms; confetti-class effects only for rare events |
| **Error** | Field-level: red border/icon + message + a11y announcement; optional horizontal **shake** like the macOS login password field (observed system behaviour ⚠️, no documented values): 3–4 decaying oscillations, ±6–10 px. Keep focus in the field, select its contents. Under reduced motion: no shake. | shake 300–400 ms total; message fade-in 150 ms |
| **Empty → first item** | Empty-state illustration fades out as the first item appears in the same region (no jump to a different layout); focus the new item. | fade 150 ms; item enter 200 ms |
| **Window open / app launch** | Let the OS animate windows (don't fake zooms). Show a ready first frame: Electron `new BrowserWindow({ show:false, backgroundColor })` + `once('ready-to-show', () => win.show())` "will have no visual flash" (Electron docs); restore last size/position; no splash animation unless startup > ~1 s. | first meaningful frame target < 1 s ⚠️ practitioner |

## Recent changes worth knowing (2025–2026)
- **Firefox 144 (Oct 2025) shipped same-document View Transitions** → Baseline across Chromium/WebKit/Gecko (MDN BCD). WebKitGTK has had them since 2.46, but see the 2.52.6 crash workaround (§7.1).
- **WebKitGTK crash (Oct 2026)**: `document.startViewTransition()` segfaults WebKitGTK 2.52.6 under `WEBKIT_DISABLE_DMABUF_RENDERER=1` (and on Debian/Ubuntu NVIDIA hosts) — Tauri/Linux apps should guard or skip VT (https://github.com/Stirling-Tools/Stirling-PDF/pull/8680, open).
- **GTK 4.22 `gtk-interface-reduced-motion`** + libadwaita 1.9 (GNOME 50, Mar 2026) stock widgets swap slides for crossfades; GTK 4.23/GNOME 51 (Sep 2026) `GtkStack`/`GtkRevealer`/`GtkSpinner` comply (linux.md §1, §5).
- **Qt 6.12**: `QAccessibilityHints::motionPreference` (portal `reduced-motion` + GNOME `enable-animations` on Linux) and `QStyleHints::toolTipWakeUpDelay`.
- **Liquid Glass (macOS 26, 2025)**: system motion responds "with greater emphasis" to touch but "a more subdued effect" with a trackpad (HIG Motion, 2025-09-09); Reduce Motion disables the material's elastic behaviour. **WWDC26**: SwiftUI `.reorderable()`/`.reorderContainer()` system lift/drop animations in any container.
- **Motion (motion.dev)** spring generator now maps `bounce` exactly like SwiftUI, including **negative bounce = overdamped** (source comment, main branch 2026); `visualDuration` is the recommended time knob.
- **Material 3 Expressive** (2025) added a spring-based "motion scheme" (Compose `MotionScheme.standard()` / `.expressive()`; *spatial* springs for position/size/scale, *effects* springs for alpha/color) alongside the older duration/easing tokens — values in §3.2 come from androidx source.
- **Emil Kowalski published his animation rules as agent skills** (https://github.com/emilkowalski/skills, `review-animations/STANDARDS.md`) — a ready-made, citable rubric for agents.
- **Microinteractions.com** (Saffer's book site) now redirects to an unrelated domain — cite Saffer via Smart Design / O'Reilly instead.

## Unverified / open questions
- ⚠️ WWDC18 momentum-projection formula `(velocity/1000)·rate/(1−rate)` is from slide memory; the transcript only describes it.
- ⚠️ Motion spring default `bounce`: source says **0.3**, docs page says 0.25. Motion `x`/`y` shorthand "not hardware-accelerated" is a practitioner claim (Kowalski) — check current Motion performance docs.
- ⚠️ Qt tooltip wake-up default (historically 700 ms) — now delegated to `QStyleHints::toolTipWakeUpDelay`, default not shown in docs. macOS tooltip initial delay (~1 s, `NSInitialToolTipDelay`) undocumented.
- ⚠️ macOS menu close fade + selected-item blink, sheet behaviour, and the login-window password **shake** are observed system behaviours with no documented durations; the shake values given (300–400 ms, ±6–10 px, 3–4 oscillations) are practitioner estimates.
- ⚠️ Core Animation implicit default 0.25 s is long-standing lore, absent from current CATransaction docs.
- ⚠️ Doherty & Thadhani 1982 IBM report number (GE20-0752-0) not verified; only the related IBM Systems Journal papers' DOIs were.
- ⚠️ Chromium's Linux source for `prefers-reduced-motion` (portal vs GNOME key) not verified; Windows mapping (`SPI_GETCLIENTAREAANIMATION`) is verified in Chromium source.
- ⚠️ Flutter: which desktop OS settings feed `disableAnimations`/`reduceMotion`, and the release that added `SpringDescription.withDurationAndBounce`.
- ⚠️ WinUI `SpringNaturalMotionAnimation.Period` exact mathematical definition (damped vs undamped period) — Microsoft only says "time it takes the spring to perform a single oscillation".
- ⚠️ Material 3 guidance pages (m3.material.io) are JS-only and could not be read; M3 numbers come from material-web token source v0_192 and androidx Compose tokens. M2/M1 desktop numbers come from archived pages (2017/2019).
- ⚠️ Saffer's book text (O'Reilly, 403) not read directly — model taken from Saffer's own Smart Design article; chapter-to-principle mapping from the O'Reilly TOC via search.
- ⚠️ Tversky et al. 2002 abstract paywalled — principles quoted via Heer & Robertson 2007, which quotes them verbatim.
- ⚠️ Practitioner-only numbers in §9: hover-reveal intent delay 300–500 ms, copy-confirmation revert 1.5–2 s, spring-loading hover 500–700 ms, first-tooltip web delay 400–700 ms, first meaningful frame < 1 s.
- Open: no platform publishes desktop *hover* timing; no study compares ease-out vs ease-in for exits on desktop specifically (platforms and practitioners disagree, §3.3).
