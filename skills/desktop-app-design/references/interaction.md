# Interaction design and usability for desktop apps

Read this for heuristics (Nielsen, Shneiderman, Tognazzini, Norman, ISO 9241), the laws behind pointing and choice (Fitts, steering, Hick, KLM), desktop patterns (command palettes, menus, selection, drag and drop, tables, settings, dialogs, errors, empty states, onboarding, autosave), and a user-centered evaluation process an agent can run without real users. Every rule cites its source inline; ⚠️ marks claims that couldn't be fully verified (collected at the end). Researched November 2026 — platform details change, so re-check anything version-specific.

Contents: 1. Heuristic sets · 2. Laws with numbers · 3. Desktop-app posture & design philosophy · 4. Desktop interaction patterns · 5. User-centred process an agent can actually run · 6. Top 25 desktop usability rules · 7. Heuristic evaluation template · Unverified / open questions · Key sources

## 1. Heuristic sets (exact wording + desktop application)

### 1.1 Nielsen's 10 usability heuristics (current NN/g wording)
Source: https://www.nngroup.com/articles/ten-usability-heuristics/ (first published 24 Apr 1994; wording refined 2020 by Kate Moran & Feifei Liu; last reviewed 30 Jan 2024). NN/g: "the 10 heuristics themselves have remained relevant and unchanged since 1994" — derived from a factor analysis of 249 usability problems (Nielsen, CHI '94).

| # | Name | Exact definition (NN/g) | Desktop application |
|---|---|---|---|
| 1 | Visibility of System Status | "The design should always keep users informed about what is going on, through appropriate feedback within a reasonable amount of time." | Status bar / sync indicator / save state always glanceable; every click acknowledged ≤0.1 s; long jobs show progress + Cancel. |
| 2 | Match Between the System and the Real World | "The design should speak the users' language. Use words, phrases, and concepts familiar to the user, rather than internal jargon. Follow real-world conventions, making information appear in a natural and logical order." | Menu/command names use the user's domain nouns+verbs ("Export as PDF…", not "Run render pipeline"); no internal IDs, enum names or HTTP codes in UI. |
| 3 | User Control and Freedom | "Users often perform actions by mistake. They need a clearly marked 'emergency exit' to leave the unwanted action without having to go through an extended process." | Multi-level Undo/Redo (⌘Z/⇧⌘Z, Ctrl+Z/Ctrl+Y); Esc closes any dialog/popover/mode; Cancel on every long op. |
| 4 | Consistency and Standards | "Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform and industry conventions." | Internal (same verb, icon, shortcut everywhere) + external (OS menu structure, standard shortcuts, platform button order). |
| 5 | Error Prevention | "Good error messages are important, but the best designs carefully prevent problems from occurring in the first place. Either eliminate error-prone conditions, or check for them and present users with a confirmation option before they commit to the action." | Disable impossible commands, constrain inputs, sensible defaults; NN/g tip: "Prevent high-cost errors first, then little frustrations." |
| 6 | Recognition Rather than Recall | "Minimize the user's memory load by making elements, actions, and options visible. The user should not have to remember information from one part of the interface to another. Information required to use the design (e.g. field labels or menu items) should be visible or easily retrievable when needed." | Full menu bar, visible labels, recent files, command palette with fuzzy search, autocomplete, persistent column headers. |
| 7 | Flexibility and Efficiency of Use | "Shortcuts — hidden from novice users — may speed up the interaction for the expert user so that the design can cater to both inexperienced and experienced users. Allow users to tailor frequent actions." | Keyboard shortcuts for every frequent command, command palette, customizable toolbar, saved views/filters, macros. |
| 8 | Aesthetic and Minimalist Design | "Interfaces should not contain information that is irrelevant or rarely needed. Every extra unit of information in an interface competes with the relevant units of information and diminishes their relative visibility." | NN/g: "doesn't mean you have to use a flat design". Density is fine for experts if every element earns its place; hide rarely used options behind progressive disclosure. |
| 9 | Help Users Recognize, Diagnose, and Recover from Errors | "Error messages should be expressed in plain language (no error codes), precisely indicate the problem, and constructively suggest a solution." | Inline error next to the field/object, plus a one-click fix ("Reconnect", "Choose another folder"); error code only as copyable detail. |
| 10 | Help and Documentation | "It's best if the system doesn't need any additional explanation. However, it may be necessary to provide documentation to help users understand how to complete their tasks." | Searchable Help menu, contextual "?" links, keyboard-shortcut reference, task-focused steps. |

NN/g tips worth enforcing: "no action with consequences to users should be taken without informing them" (#1); "Support Undo and Redo" (#3); "Offer help in context, instead of giving users a long tutorial to memorize" (#6); slips = "unconscious errors caused by inattention", mistakes = "conscious errors based on a mismatch between the user's mental model and the design" (#5). Same URL.

### 1.2 Severity ratings 0–4 (Nielsen)
Source: https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/
- Severity is "a combination of three factors": **frequency** ("common or rare?"), **impact** ("easy or difficult to overcome?"), **persistence** ("one-time problem … or will users repeatedly be bothered?"), plus market impact.
- Scale (exact): **0** = "I don't agree that this is a usability problem at all" · **1** = "Cosmetic problem only: need not be fixed unless extra time is available on project" · **2** = "Minor usability problem: fixing this should be given low priority" · **3** = "Major usability problem: important to fix, so should be given high priority" · **4** = "Usability catastrophe: imperative to fix this before product can be released".
- Ratings from one evaluator are "too unreliable to be trusted"; "the mean of a set of ratings from three evaluators is satisfactory for many practical purposes." Rate after finding (not during), independently, ~30 min.
- Agent rule: ship-blocker = any 4; fix all 3s before polish; never spend time on 1s while 3s exist.

### 1.3 Shneiderman's Eight Golden Rules (6th-edition wording)
Source: https://www.cs.umd.edu/users/ben/goldenrules.html (from *Designing the User Interface*, 6th ed., Pearson 2016, §3.3.4; original list 1985). Shneiderman: the rules "require validation and tuning for specific design domains."
1. **Strive for consistency.** "Consistent sequences of actions should be required in similar situations; identical terminology should be used in prompts, menus, and help screens…" Exceptions (e.g. delete confirmation) "should be comprehensible and limited in number." → Same verb in menu, button, tooltip, palette and docs.
2. **Seek universal usability.** "Novice to expert differences, age ranges, disabilities, international variations, and technological diversity…" "Adding features for novices, such as explanations, and features for experts, such as shortcuts and faster pacing, enriches the interface design." → Ship both menus *and* shortcuts; support OS text scaling and screen readers.
3. **Offer informative feedback.** "For frequent and minor actions, the response can be modest, whereas for infrequent and major actions, the response should be more substantial." → Toggle = state change only; export of 2 GB = progress + completion notification.
4. **Design dialogs to yield closure.** "Sequences of actions should be organized into groups with a beginning, middle, and end." → Multi-step flows end with an explicit done state ("Exported 312 files — Show in Finder").
5. **Prevent errors.** "gray out menu items that are not appropriate"; "users should not have to retype an entire name-address form if they enter an invalid zip code"; "Erroneous actions should leave the interface state unchanged." → Never clear a form on error.
6. **Permit easy reversal of actions.** "This feature relieves anxiety, since users know that errors can be undone, and encourages exploration." Units: single action, data-entry task, or group. → Undo groups match user intent (one "Replace All" = one undo step).
7. **Keep users in control.** "Experienced users strongly desire the sense that they are in charge… They don't want surprises or changes in familiar behavior." → No auto-rearranging menus, no surprise focus steals, no layout jumps.
8. **Reduce short-term memory load.** "…designers avoid interfaces in which users must remember information from one display and then use that information on another display." (Shneiderman still cites "seven plus or minus two chunks" — see §2.9 for the modern 4±1 correction.)

### 1.4 Tognazzini's First Principles of Interaction Design (Revised & Expanded, 5 Mar 2014)
Source: https://asktog.com/atc/principles-of-interaction-design/ — Tog designed Apple's first human interface (1978). Principles most relevant to desktop (exact principle titles in quotes):
- **Anticipation** — "Bring to the user all the information and tools needed for each step of the process." Don't make users leave the current screen to gather data.
- **Autonomy / status** — "Use status mechanisms to keep users aware and informed"; "Keep status information up to date and within easy view"; "Ensure status information is accurate" (his example: an update progress bar saying ~5 min that actually takes an hour).
- **Consistency levels** — strictness rises from platform look → suite → app look → small visible structures → invisible structures → **"Interpretation of user behavior"** (the most important: "Shortcut keys must maintain their meanings"). "Over time, strive for continuity, not consistency." "The most important consistency is consistency with user expectations" (Buxton). "Make objects that act differently look different" (a trash can that instantly destroys must not look like a trash can).
- **Defaults** — "Defaults within fields should be easy to 'blow away'" (auto-select field content on focus); "Not everything should have a default. If there isn't a predictable winner, consider not offering any default"; say "Restore Initial Settings", not "Default"; make the **scope** of a reset obvious (this tab vs. whole app).
- **Discoverability** — "Any attempt to hide complexity will serve to increase it"; "If the user cannot find it, it does not exist"; "There is no 'elegance' exception to discoverability"; "With the exception of small mobile devices, controls do not belong in the middle of the content area." **Active Discovery:** mention a feature at the earliest moment it's needed, repeat at spaced intervals, stop once adopted.
- **Efficiency** — "Look at the user's productivity, not the computer's"; "Keep the user occupied"; cost-of-change = hourly wage × 3 (overhead) × users × task time × productivity delta. "The great efficiency breakthroughs … are to be found in the fundamental architecture of the system, not in the surface design."
- **Error messages** must "Explain what's wrong", "Tell the user specifically what to do about it", "Leave open the possibility the message is improperly being generated by a deeper system malfunction."
- **Explorable interfaces** — "Always allow 'Undo'": without undo you need "a bunch of confirmation dialogs"; "A perfect user is a slow user"; "Always allow a way out"; Cancel in wizards must say where the user can finish later.
- **Fitts's law** — "Use large objects for important functions … small objects for functions you would prefer users not perform"; "Even a one-pixel boundary can result in a 20% to 30% slow-down for tools along the edge"; Mac menu bar "approximately five times faster" than in-window menus (Tog's claim ⚠️ see §2.1); "Multiple Fitts": total time = sum of all targets, so cut the number of targets.
- **Latency** — "Acknowledge all button clicks by visual or aural feedback within 50 milliseconds"; "Trap multiple clicks of the same button"; push work to background threads. His delay table: **0.5–2 s** busy cursor/indicator · **>2 s** tell the potential length of wait · **>5 s** animated progress indicator ("Process must end by the time indicator is full!") · **>10 s** keep users informed & entertained · **>15 s** also play a sound + strong visual on completion "so users know to return".
- **Protect Users' Work** — "Ensure that users never lose their work. This principle is all but absolute." Calls for continuous save.
- **Readability** — "Menu and button labels should have the key word(s) first, forming unique labels"; "Test all designs on your oldest expected user population."
- **Simplicity** — "Avoid the 'Illusion of Simplicity'"; "Use Progressive Revelation to flatten the learning curve"; "Do not simplify by eliminating necessary capabilities."

### 1.5 Norman — *The Design of Everyday Things* (Revised & Expanded, Basic Books, 2013)
Publisher page: https://www.hachettebookgroup.com/titles/don-norman/the-design-of-everyday-things/9780465072996/ (subtitle on the page: "The essential guide to human-centered design"). The two characteristics of good design are **discoverability** (can I figure out what actions are possible and how?) and **understanding** (what does it all mean?). Concepts below are from ch. 1–5 of the book (book text not online; definitions paraphrased ⚠️ — verify wording if quoted).

| Concept | Meaning | Desktop rule |
|---|---|---|
| **Affordance** | A relationship between object and agent: what actions are possible. | Don't argue about "affordances" — design the cues (next row). |
| **Signifier** | Any perceivable cue that signals what action is possible and where. Norman (2008): "Forget affordances: what people need, and what design must provide, are signifiers." https://jnd.org/signifiers-not-affordances/ | Clickable things look clickable (button shape, link style, hover state, resize cursor, drag handle ⋮⋮). Don't hide controls until hover unless they're also reachable via menu/keyboard. |
| **Mapping** | Relationship between controls and their effects; "natural mapping" uses spatial analogy. NN/g #2 example: stovetop knobs laid out like burners. | Put a control next to what it affects; toolbar order mirrors pipeline order; zoom slider left=out/right=in; panel toggle icons show which side opens. |
| **Constraints** | Physical, cultural, semantic, logical limits that reduce possible actions. | Disable invalid commands (and say why in tooltip), date pickers that can't pick end<start, typed inputs, drop targets that only accept valid types. |
| **Forcing functions** | Strong constraints: interlocks, lock-ins (prevent leaving with unsaved work), lockouts. | "Quit with unsaved changes?" is a lock-in — better: autosave so it's not needed (§4.20). |
| **Feedback** | Immediate, informative communication of the result of an action; too much feedback is as bad as too little. | Every action produces a visible result within 0.1 s; don't add sounds/toasts to routine actions. |
| **Conceptual model** | The user's explanation of how the system works, built from the "system image" (UI, docs, behavior). | One consistent object model: if it's a "project" in the sidebar, it's a "project" in menus, errors and docs. |
| **Gulf of execution / evaluation** | Execution = "Taking action to accomplish a specific goal"; evaluation = "Understanding the state of the system" (NN/g, 2018: https://www.nngroup.com/articles/two-ux-gulfs-evaluation-execution/). Seven stages of action: goal → plan → specify → perform → perceive → interpret → compare. | Bridge execution with visible commands, signifiers, palette search; bridge evaluation with state shown in place (selection highlight, dirty-document dot, sync badge). |
| **Slips vs mistakes** | Slips: "Slips occur when users intend to perform one action, but end up doing another"; often experts on autopilot. Mistakes: "users have goals that are inappropriate for the current problem" — wrong mental model (https://www.nngroup.com/articles/slips/). | Slips → constraints, good defaults, forgiving formats, undo, separate destructive from frequent controls. Mistakes → follow conventions, show previews of wide-scope actions, show context, gather user data (https://www.nngroup.com/articles/user-mistakes/). |

NN/g: "The designer is at fault for making it too easy for the user to commit the error… The answer is to redesign the system to be less error prone." https://www.nngroup.com/articles/slips/

### 1.6 ISO 9241-110:2020 — Interaction principles (2nd ed., published 2020-05-28, 32 pp.)
Catalogue: https://www.iso.org/standard/75258.html (iso.org blocks scripted fetch; metadata verified via national store https://online.standard.no/en/iso-9241-110-2020 and the STN EN ISO preview https://normy.normoff.gov.sk/norma/131625/nahlad). Scope: principles "formulated in general terms (i.e. independent of situations of use, application, environment or technology)"; "does not cover the specifics of every application domain (e.g. safety critical systems, collaborative work, artificial intelligence features)". Changes from 2006: "the principle of individualization has been merged into the principle of controllability; a new principle on user engagement has been developed." Sources it draws on include Nielsen, Molich, Tognazzini, Bastien, Dzida. The 7 principles (exact clause titles) and their sub-recommendation groups (from the table of contents), with desktop application (full definitions paywalled ⚠️):
1. **5.1 Suitability for the user's tasks** — identifying suitability; *optimizing effort in task accomplishment*; *defaults supporting the task*. → Count steps for top tasks; pre-fill with last-used values.
2. **5.2 Self-descriptiveness** — *presence and obviousness of the information*; *clear indication of processing status*. → Labels, tooltips, visible state, progress.
3. **5.3 Conformity with user expectations** — appropriate system behaviour and responses; *consistency (internal and external)*; *changes in the context of use*. → Platform conventions; same command behaves the same in every window.
4. **5.4 Learnability** — *discovery*; *exploration*; *retention*. → Menus reveal shortcuts; safe exploration via undo; stable layout so learned positions persist.
5. **5.5 Controllability** — *interruption by the user*; *flexibility*; *individualization*. → Cancel/pause any long job; multiple ways to do a task; customizable toolbars/shortcuts.
6. **5.6 Use error robustness** — *use error avoidance*; *use error tolerance*; *use error recovery*. → Constraints, forgiving input, undo, autosave/versions.
7. **5.7 User engagement** (new in 2020) — *motivating the user to use the system*; *trustworthiness of the system*; *increasing user involvement*. → Honest status, no dark patterns, transparent data handling.
The intro lists problems the principles prevent: "additional unnecessary steps", "misleading information", "insufficient and poor information on the user interface", "unexpected responses", "navigational limitations during use", "inefficient error recovery". Annex A = checklist.

### 1.7 ISO 9241-210:2019 — Human-centred design for interactive systems (2nd ed., July 2019; confirmed 2025)
Catalogue: https://www.iso.org/standard/77520.html (status "confirmed 2025" seen in search snippet of the ISO page ⚠️). Scope: "requirements and recommendations for human-centred design principles and activities throughout the life cycle of computer-based interactive systems". Annex B = conformance checklist.
- **Six principles** (widely quoted from the 2010/2019 text; exact 2019 wording not verifiable — ⚠️): (a) design based on an explicit understanding of users, tasks and environments; (b) users involved throughout design and development; (c) design driven and refined by user-centred evaluation; (d) the process is iterative; (e) design addresses the whole user experience; (f) team includes multidisciplinary skills and perspectives.
- **Activities** (confirmed headings via https://blog.rheinwerk-computing.com/how-to-do-ux-design-a-guide-to-the-iso-9241-210-standard): **Plan the human-centred design process → Understand and specify the context of use → Specify the user requirements → Produce design solutions → Evaluate the design** → iterate until requirements are met.
- Agent mapping: context of use = §5.1 "users + JTBD"; requirements = measurable usability targets (§5.2); design solutions = prototypes; evaluate = heuristic eval + walkthrough + KLM (§5.4–5.6), then real-user test.

## 2. Laws with numbers (and what they mean on a desktop)

### 2.1 Fitts's law — pointing time
- **Formula** (Fitts 1954, https://doi.org/10.1037/h0055392; Shannon form popularized by MacKenzie): MT = a + b·log₂(D/W + 1). Time grows with distance D, shrinks with target width W; logarithmic, so 2× farther ≠ 2× slower. For rectangles use the smaller dimension (MacKenzie & Buxton 1992, per https://www.nngroup.com/articles/fitts-law/).
- **Screen edges and corners are "infinite" targets with a mouse** — the pointer stops at the edge, so users don't decelerate. NN/g: "In MacOS, application menus are shown at the very top of the screen… users will not need to slow down." Edge advantage is **absent on touchscreens** (Avrahami CHI '15: edge targets *slower*). https://www.nngroup.com/articles/fitts-law/
- **Tog's "five magic pixels"** (Ask Tog, Feb 1999): the fastest pixel is "the current location of the mouse pointer. Popup menus make use of this pixel… zero travel" — this is why **context menus open at the pointer**; the other four are the screen corners. https://asktog.com/columns/022DesignedToGiveFitts.html
- **Never put a dead zone between a control and the screen edge**: "Ensure that the user can click on the very first row of pixels along the edge of the screen… There should be no buffer zone" (same page); "Even a one-pixel boundary can result in a 20% to 30% slow-down" (https://asktog.com/atc/principles-of-interaction-design/). Applies to full-screen/maximized apps: edge-docked toolbars, tab strips, and the top-right close button of a maximized window must extend to the pixel edge. Practitioner claim ⚠️: Mac menu bar "at least five times faster" than in-window menus (Tog's own Apple test, not a published study).
- **Desktop rules**: label + icon targets are bigger (whole row clickable, not just icon) — NN/g; place sequential controls close (OK/Submit next to last field); order linear menus by frequency (first item closest to handle); in **context menus put the most-used items near the top** (closest to the pointer); don't crowd small targets; invisible padding helps but users still slow down for the visible size. https://www.nngroup.com/articles/fitts-law/
- **"Multiple Fitts"**: total time = sum over all targets → fewer clicks beats bigger buttons (Tog).

### 2.2 Steering law — moving through tunnels (Accot & Zhai 1997)
- "Beyond Fitts' law: models for trajectory-based HCI tasks", CHI '97, pp. 295–302, https://doi.org/10.1145/258549.258760. T = a + b·(A/W): time is **linear** in tunnel length/width (much steeper than Fitts's log).
- NN/g (2024): "long, narrow tunnels take more time to navigate than short, wide tunnels"; affected widgets: cascading menus, sliders, scroll bars, scrubbers. https://www.nngroup.com/articles/steering-law/
- **Rules**: keep dropdowns short; "Avoid hierarchical menus, particularly… more than two-levels deep"; if you must cascade, use a **short hover delay or "a vector-based triangular system to allow for some diagonal movement error"** (safe triangle / menu-aim); pad menu rows; supplement sliders with a numeric field + steppers for precision; let users click anywhere on a slider track (NN/g steering-law). Tog specified the Mac's original "<"-shaped buffer in the mid-'80s; he says OS X replaced it with a Windows-style ~0.5 s timer (https://asktog.com/columns/022DesignedToGiveFitts.html). Open-source reference: jQuery-menu-aim detects mouse direction toward the submenu instead of timeouts (https://github.com/kamens/jQuery-menu-aim). ⚠️ Current macOS/Windows native menu behavior not re-tested here — for custom (Electron/Flutter/web) menus, implement safe-triangle yourself.
- NN/g menu checklist (2024): "Use Click-Activated (Rather Than Hover-Activated) Submenus"; "Avoid Multilevel Cascading Menus"; "Clearly Signify Submenus with a Caret or Arrow Icon"; hiding navigation under a hamburger "is not appropriate for desktop websites and apps"; application primary nav expected on the **left side**. https://www.nngroup.com/articles/menu-design/

### 2.3 Hick–Hyman law — choice time
- Hick 1952 (https://doi.org/10.1080/17470215208416600), Hyman 1953 (https://doi.org/10.1037/h0056940): RT = a + b·log₂(n + 1) for n equally likely alternatives; more generally RT is linear in the **information** (bits) of the choice, so unequal frequencies are faster.
- NN/g: "the more choices you present to your users, the longer it takes them to reach a decision. However, combining Hick's Law with other design techniques can make long menus easy to use." https://www.nngroup.com/videos/hicks-law-long-menus/
- **Desktop reading**: applies to choosing among *known* options; when users must *search/read* unfamiliar items, time is closer to linear in item count. So: group related menu items with separators, order predictably (frequency, workflow, or alphabetical for long lists), set strong defaults, put the 1 primary action visually first. Don't "fix" Hick by hiding needed commands (Tog: "Do not simplify by eliminating necessary capabilities").

### 2.4 Keystroke-Level Model (Card, Moran & Newell 1980)
- CACM 23(7):396–410, https://doi.org/10.1145/358886.358895. Predicts expert, error-free execution time by summing operators. Values (original 1980 / Kieras tutorial https://www.cs.umd.edu/~golbeck/INST631/KSM.pdf):

| Op | Meaning | Time |
|---|---|---|
| K | keystroke | CMN: 0.08–1.2 s; Kieras: expert 90 wpm 0.12 · skilled 55 wpm 0.20 · **average non-secretary 40 wpm 0.28 (use this)** · unfamiliar 1.2 |
| P | point with mouse | **1.1 s** (0.8–1.5) |
| B / BB | press-or-release / click | 0.1 / **0.2 s** |
| H | home hand keyboard↔mouse | **0.4 s** |
| M | mental preparation | **1.35 s** (CMN 1980); Kieras gives range 0.6–1.35 and recommends **1.2 s** |
| W(t) | waiting for system | measured |

- **Worked comparisons** (agent can compute): menu command via mouse from typing = H + M + P + BB + P + BB + H ≈ 0.4+1.2+1.1+0.2+1.1+0.2+0.4 = **4.6 s**; same command via shortcut (⌘S = 2K) = M + 2K ≈ 1.2+0.28×2 = **1.76 s**; via command palette (⌘K = 2K, type 4 chars, Enter) = M + 7K ≈ **3.2 s** (+1 M ≈ 4.4 s if the user must read the result list; needs no memorized shortcut). Right-click context menu while hand on mouse = M + BB + P + BB ≈ 2.7 s. Use these to justify shortcuts and to compare two flows.
- Limits: experts only, no errors, no learning; "Choosing how many Ms are involved, and where they appear, is the hardest part" (Kieras).

### 2.5 Response-time limits
- **0.1 s** "limit for having the user feel that the system is reacting instantaneously"; **1.0 s** "limit for the user's flow of thought to stay uninterrupted"; **10 s** "limit for keeping the user's attention focused" (Nielsen, *Usability Engineering* 1993, after Miller 1968 and Card et al. 1991). https://www.nngroup.com/articles/response-times-3-important-limits/
- Desktop specifics from the same page: 0.1 s = selecting a table column should highlight within 0.1 s, "Ideally, this would also be the response time for sorting the column"; >1 s show a busy indicator; >10 s needs "a percent-done indicator as well as a clearly signposted way for the user to interrupt"; 2–10 s: a full percent-done bar can be overkill — use a busy cursor + small changing number; for unknown-length work show "the absolute amount of work done" (e.g., name of each item processed). Animations must be timed by clock, not CPU speed.
- Tognazzini: acknowledge every click "within 50 milliseconds" and "trap multiple clicks" (§1.4).

### 2.6 Doherty threshold (≈400 ms)
- Origin: W. J. Doherty & A. J. Thadhani (spelling varies "Thadani"), *The Economic Value of Rapid Response Time*, IBM publication GE20-0752-0, 1982 — an IBM report, **not** a peer-reviewed paper (Laws of UX labels it "IBM Systems Journal" — likely inaccurate ⚠️). The IBM-hosted copy (vm.ibm.com/devpages/jelliott/evrrt.html) now returns 404 (checked 2026-11-02). Popular statement: "Productivity soars when a computer and its users interact at a pace (<400ms)…" https://lawsofux.com/doherty-threshold/
- Use: treat **≤400 ms** as the target for *system* response on frequent interactive commands (search-as-you-type results, view switches, filter application). Practitioner framing ⚠️; the 0.1/1/10 s limits are the better-supported rule.

### 2.7 Jakob's law
- "people spend most of their time using digital products other than yours. Users' experiences with those other products set their expectations." (in Heuristic #4, https://www.nngroup.com/articles/ten-usability-heuristics/). On desktop the "other products" are the OS and the user's other apps: standard menu order (File Edit View … Window Help), standard shortcuts (⌘/Ctrl+C/V/X/Z/S/F/W/Q/N/O/P/comma for Settings on Mac), standard dialogs (file pickers, print). Tog: "Shortcut keys must maintain their meanings."

### 2.8 Tesler's law (conservation of complexity)
- "for any system there is a certain amount of complexity which cannot be reduced" — attributed to Larry Tesler at Xerox PARC (mid-1980s), via Dan Saffer's *Designing for Interaction* interview (https://lawsofux.com/teslers-law/, secondary ⚠️). NN/g video (Nov 2025): "Shift Complexity to Simplify UX" https://www.nngroup.com/videos/teslers-law/
- Desktop rule: the app (not the user) absorbs complexity — infer file types, auto-detect encodings, remember last folder, smart defaults; but never remove capability (Tog "Illusion of Simplicity").

### 2.9 Miller's 7±2 is misused — use Cowan's 4±1
- Miller 1956 (https://doi.org/10.1037/h0043158) was about absolute-judgment span and chunking, not "menus must have ≤7 items." Cowan 2001 (https://doi.org/10.1017/S0140525X01003922): working-memory capacity ≈ **4 chunks** (3–5) when rehearsal/chunking are controlled.
- Rules: never require users to carry >3–4 items between screens (show them instead — Heuristic #6); chunk long numbers/IDs (Tog: phone numbers "broken up into smaller pieces"); menus and toolbars can be longer than 7 if grouped, since they're *recognized*, not recalled.

## 3. Desktop-app posture & design philosophy

### 3.1 Cooper et al., *About Face* (4th ed., Wiley, Sept 2014; Cooper, Reimann, Cronin, Noessel)
Publisher: https://www.wiley.com/en-us/About+Face%3A+The+Essentials+of+Interaction+Design%2C+4th+Edition-p-9781118766576 — TOC/index verified from Wiley excerpt PDFs (https://media.wiley.com/product_data/excerpt/71/11187665/1118766571-28.pdf): ch. 9 "Platform and Posture" ("Postures for the Desktop": sovereign pp. 208–213, transient pp. 213–217, daemonic pp. 217–218), ch. 10 "Optimizing for Intermediates" ("Perpetual Intermediates", "Inflecting the Interface", "Designing for Three Levels of Experience"), ch. 12 "Reducing Work and Eliminating Excise", ch. 15 "Preventing Errors and Informing Decisions" ("Using Rich Modeless Feedback", "Undo, Redo, and Reversible Histories", "What If: Compare and Preview"), ch. 21 "Eliminating Errors, Alerts, and Confirmations". Definitions below paraphrased from the book (⚠️ exact wording not checked; Wikipedia quotes the 3rd ed.: sovereign "monopolizes the user's attention for long periods of time"; transient "comes and goes, presenting a single, high-relief function" — https://en.wikipedia.org/wiki/Application_posture).

| Posture | What it is | Design rules |
|---|---|---|
| **Sovereign** | The user's main tool for hours (IDE, editor, DAW, mail, design tool). | Design for **maximized** windows and **perpetual intermediates**; conservative, low-saturation chrome so content dominates; dense information OK; rich keyboard + toolbar + palette access; persistent panels; remember layout per document/workspace. |
| **Transient** | Opened for one short job, then dismissed (color picker, quick-capture, launcher, calculator, file-share popover). | Big, obvious, self-explanatory controls; open where the user's attention is (near pointer/menu-bar icon); remember last position & values; one primary action; close on completion/Esc. |
| **Daemonic** | Runs in the background with no direct interaction (sync agents, backup, updaters, menu-bar/tray utilities). | Invisible when healthy; surface only state the user must act on; a tray/menu-bar icon reflecting status; settings reachable from it; never steal focus. |
| (Auxiliary/parasitic, 3rd ed.) | Persistent small helper beside a sovereign app (palettes, inspectors, mini players). | Compact, glanceable, doesn't fight the main window for focus. |

- **Perpetual intermediates**: most users neither stay beginners nor become experts; they plateau in the middle. Design primarily for intermediates, give beginners a fast on-ramp and experts accelerators ("inflect" the interface: frequent commands visible, rare ones one level deeper). NN/g agrees: "even users of complex applications tend to plateau at mediocre performance" (https://www.nngroup.com/articles/complex-application-design/).
- **Excise** = work the tool demands that doesn't advance the user's goal (window juggling, navigating to settings, confirming, re-entering data). Eliminate it before decorating.
- **Undo, don't confirm**: rich modeless feedback + reliable undo instead of modal confirmations; confirm only when the user would *likely* cancel. ("Don't stop the proceedings with idiocy" is a chapter title from earlier editions — ⚠️ not present in the 4th-ed TOC.)

### 3.2 Raskin, *The Humane Interface* (Addison-Wesley, March 2000)
Sources: Raskin Center summaries https://www.raskincenter.org/rchi/core-principles and https://www.raskincenter.org/jef/humane-interface/; Brown CS course notes https://cs.brown.edu/courses/csci0920/2005/bell.raskin.pdf.
- **Modes cause errors**: "A mode is a state of an interface in which the same user action produces different results." Goal: "every user action always has the same meaning, regardless of system state." "If a mode cannot be eliminated, convert it to a quasimode" — a mode held only while a key is held (Shift, Space-to-pan, ⌥-drag-to-copy). Desktop rules: show mode state prominently where the eyes are (cursor shape, status pill), make modes time-out or self-exit after one use (transient modes "can cause fewer errors"), let Esc always exit.
- **Habituation**: practiced actions become automatic and persist even after the UI changes; "Answering 'yes' to the prompt for confirming deleting a file becomes a habit, which defeats the purpose" (Brown notes). → Routine confirmations give *no* protection; use undo. Never move or repurpose learned commands; "An adaptive interface is a bad idea—it prevents users from habituating" → no auto-reordering menus.
- **Locus of attention**: "A routine confirmation prompt is not proportional if it interrupts a focused working state." Keep feedback in the content area, not in modal boxes.
- **Never lose work / universal undo**: "Users should not lose work"; continuous automatic save; "If all actions are reversible, users can explore freely." Raskin's "First Law" — "A computer shall not harm your work or, through inaction, allow your work to come to harm" (⚠️ widely quoted from the book; not verified online).
- **Monotony**: "There exists exactly one gesture to achieve a given effect" — tension with Nielsen #7 (multiple paths). Resolution for desktop: one canonical *method* per command (same name, same shortcut everywhere), but expose it through several *entry points* (menu, palette, context menu, toolbar) that all show the same shortcut.
- "Subjective impressions of speed are often wrong" → measure (KLM, stopwatch).

### 3.3 NN/g — 8 design guidelines for complex applications (Kate Kaplan, 8 Nov 2020)
https://www.nngroup.com/articles/complex-application-design/ — complex app = "any application supporting the broad, unstructured goals or nonlinear workflows of highly trained users in specialized domains".
1. **Promote learning by doing** — users want to start immediately ("paradox of the active user"); allow trial-and-error "without that experimentation resulting in loss of work"; live previews instead of long blind sequences.
2. **Help users adopt more efficient methods** — users "satisfice"; embed "in-context learning cues for accelerators" (e.g., tooltip suggesting drag-and-drop).
3. **Provide flexible and fluid pathways** — avoid rigid linear workflows; wizards with an interactive step map to jump back/forward without losing progress.
4. **Help users track actions and thought processes** — notes/annotations on data, history, resumability after interruptions (analyses can run "for hours, if not days").
5. **Coordinate transition among multiple tools and workspaces** — export to Excel/PowerPoint, "copy visuals as images", good clipboard formats.
6. **Reduce clutter without reducing capability** — "staged disclosure": show options only when relevant.
7. **Ease transition between primary and secondary information** — details in hover/side panel without leaving the screen.
8. **Make important information visually salient** — often by *removing* nonessential elements, not adding emphasis.

### 3.4 NN/g — accelerators for power users (18 Oct 2024)
https://www.nngroup.com/articles/ui-accelerators/
- Accelerators "should be additional, alternate ways to accomplish a task… Those users who never discover the accelerator should be able to complete the same task in another way."
- Discoverability: "readily available, yet easy to ignore"; reveal gradually; contextual hints "after a user performs the action in the standard way"; "Display Keyboard Shortcuts Inline… right-align shortcuts next to the corresponding action in a dropdown menu"; show shortcut in tooltips (but hover excludes keyboard/touch users); macros in multiple places; cheat sheet = "A last resort".
- "Do not override commonly known shortcuts, such as those for copy, paste, select all, and print"; allow custom shortcuts for experts; provide feedback and undo for accelerator-triggered actions.

## 4. Desktop interaction patterns (evidence-backed rules)
Platform specifics (exact menu layouts, native APIs) live in macos.md / windows.md / linux.md / cross-platform.md — this section is the cross-platform *why* and the numbers.

### 4.1 Keyboard-first design & command palettes (⌘K / Ctrl+K / Ctrl+Shift+P)
- **Every command reachable by keyboard**; mouse and keyboard redundant: "Users should be able to do everything with the keyboard that they can with the mouse, except actions for which fine motor skills are essential" (Microsoft Win7 UX guide, https://learn.microsoft.com/en-us/windows/win32/uxguide/inter-mouse). Visible focus indicator always: removing it "is catastrophic for keyboard users" (https://www.nngroup.com/articles/keyboard-accessibility/).
- **Why a palette**: KLM (§2.4) — palette ≈3–4 s vs menu-by-mouse ≈4.6 s, with no memorized shortcut; it's recognition (type a fragment, pick from list) instead of recall.
- **Palette design checklist** (Superhuman, Tim Boucher, 12 Oct 2021 — practitioner, https://blog.superhuman.com/how-to-build-a-remarkable-command-palette/; VS Code UX guidelines https://code.visualstudio.com/api/ux-guidelines/command-palette):
  1. One shortcut opens it from anywhere (⌘K or ⌘⇧P/Ctrl+Shift+P); same shortcut/Esc closes and **returns focus to the previously focused element**.
  2. Contains *every* command (single registry: each action = menu item + shortcut + palette entry).
  3. **Fuzzy, forgiving matching** ("opn" → Open), case-insensitive, with **aliases/synonyms** (show "Archive (Done)" so users learn your term).
  4. Before typing, show **recent/most-used** commands first; rank by default score + usage; boost context-relevant commands; hide only fully irrelevant ones.
  5. **Show each command's shortcut** in the result row so users "learn the shortcut for next time"; group by category ("File: …", "View: …"); clear verb-first names; no emoji (VS Code).
  6. Results update per keystroke within 0.1 s (§2.5); ↑/↓ + Enter; cut off the last visible row to signal more.
  7. Don't overwrite existing shortcuts (VS Code); palette supplements, never replaces, menus (accelerators must be optional — NN/g §3.4).
- **Search-everything vs command palette**: if the palette also searches content (files, records), separate sections or prefixes (`>` for commands like VS Code) so actions and objects don't mix confusingly ⚠️ practitioner convention.

### 4.2 Shortcut discoverability
- Show shortcuts **right-aligned in menus and context menus** (NN/g accelerators; "Show keyboard shortcuts in contextual menus… Seeing these shortcuts repeatedly will help users memorize" — https://www.nngroup.com/articles/contextual-menus/).
- Show the shortcut **in every toolbar tooltip** ("Bold (⌘B)"); tooltips must also appear on keyboard focus (NN/g tooltips: "Support both mouse and keyboard hover", https://www.nngroup.com/articles/tooltip-guidelines/). Microsoft: hover tooltip after ~1 s still pointing.
- Contextual hint **after** the user performs an action the slow way ("Tip: ⌘⇧L does this") — once, dismissible, never repeated after adoption (NN/g accelerators; Tog "Active Discovery").
- Provide a **shortcut cheat sheet** (Help › Keyboard Shortcuts, often bound to ⌘/ or ?) organized by workflow — NN/g calls it "a last resort" for discovery but useful for experts.
- Allow **rebinding** for pro tools; detect conflicts; never rebind OS-standard shortcuts (copy, paste, select all, print, undo, quit, close, settings).

### 4.3 Menus vs toolbars vs context menus

| Surface | Role | Rules |
|---|---|---|
| **Menu bar** (app/window menus) | Complete, searchable catalogue of every command; where users look when lost. | Every command lives here (even if also elsewhere), with shortcut; standard order; disabled (not hidden) when unavailable; ellipsis "…" when more input is needed. Hamburger-only menus are "not appropriate for desktop… apps" (https://www.nngroup.com/articles/menu-design/). |
| **Toolbar** | The ~5–12 most frequent commands for *this* document type. | Icon + label or icon + tooltip with shortcut; group with separators; customizable in sovereign apps; never the *only* path. |
| **Context menu** | Commands for the clicked object/selection, at the pointer (Fitts "prime pixel"). | NN/g (https://www.nngroup.com/articles/contextual-menus/): "Only include a focused set of actions" for the clicked thing; commands "also available from the application's main menu"; "List commands in frequency-of-use order"; "fewer than 10–12 items"; "Limit the use of submenus" (never a 3rd level); "Disable items that aren't relevant… Rather than hiding"; add a visible signifier (⋯ button) because right-click is hidden; don't use gear/hamburger icons for contextual menus. Right-click first **selects** the item under the pointer, then shows its menu (Microsoft). |
| **Inspector / properties panel** | Persistent, modeless editing of the selection's attributes. | Updates live with selection; changes apply immediately with undo (see 4.13). |
| **Command palette** | Search across all commands. | See 4.1. |

- Microsoft (Win7 guide): right-click, double-click and modifier-clicks "aren't intuitive… shouldn't be required to perform basic tasks"; "Never require users to click an object to determine if it is clickable"; "Make hover redundant". https://learn.microsoft.com/en-us/windows/win32/uxguide/inter-mouse

### 4.4 Selection & multi-select conventions
Source: Microsoft mouse guidelines (above) + platform convention; on macOS read Cmd for Ctrl.
- Click = select one (deselect others); **Shift+click = extend contiguous range** from the anchor; **Ctrl/⌘+click = toggle one item** without affecting others; drag on empty background = **marquee (rubber-band)** select; click on empty background = deselect all; **Ctrl/⌘+A = select all** (in the focused list/canvas, not the whole window); double-click = default action (open); arrow keys move selection, Shift+arrows extend.
- Text: double-click word, triple-click line/paragraph.
- Keep selection **visible and distinct from focus and hover** (three different states); show a count ("12 selected") and bulk actions bar when >1 selected (NN/g data tables: batch actions above/below the table, "single-click option to Select All").
- Don't lose selection on refresh/sort/filter; if filtered-out items stay selected, say so ("3 selected, 1 hidden by filter") ⚠️ practitioner rule.
- Microsoft: "Have clicks take effect on mouse button up" (lets users abandon by moving off); allow ~3 px movement on release; "Ignore redundant mouse clicks while your program is inactive"; "Use the Esc key to let users abandon compound mouse interactions such as moving, resizing, splitting, and dragging"; splitters ≥5 px wide; click targets ≥16×16 px; don't use Alt or Shift+Ctrl as mouse modifiers.

### 4.5 Drag and drop
NN/g (Feb 2020) https://www.nngroup.com/articles/drag-drop/ — direct manipulation "particularly useful for grouping, reordering, moving, or resizing objects", but "can be inefficient, imprecise, and even physically challenging".
- Signifiers: grab handle and/or **platform-standard cursor** change on hover (open hand / move / resize cursors) — "avoid creating new, custom icons".
- Feedback on grab: lift (shadow), outline, slight offset/angle, translucent ghost for files.
- **Preview the drop**: other items animate out of the way (~**100 ms**); trigger reshuffle when the **center** of the dragged object crosses the edge of the target (edge-to-edge feels "twitchy", cursor-based feels "mushy").
- **Magnetism**: drop zones active slightly beyond their visible border, clearly highlighted when active.
- Always pair with a precise alternative (arrow-key nudge, Cut/Paste, "Move to…" menu) and keyboard access (Tab to handle, Space to grab, arrows to move, Space to drop, Esc to cancel; announce to screen readers).
- Convention: drag within the same volume/container = move; across volumes = copy (Tog's Xerox Star story: "Dragging a document within a logical volume will move it. Dragging it from one logical volume to another will copy it" — https://asktog.com/atc/principles-of-interaction-design/); modifier (⌥/Ctrl) forces copy; show the "+" badge; Esc cancels; drop is undoable.
- Auto-scroll when dragging near the edge of a scrollable area; spring-loaded folders/tabs open after a hover delay ⚠️ platform convention.

### 4.6 Direct manipulation & inline editing
- Shneiderman (1983, "Direct Manipulation: A Step Beyond Programming Languages", *Computer* 16(8):57–69, https://doi.org/10.1109/MC.1983.1654471): continuous representation of the objects of interest; physical actions (or labeled buttons) instead of complex syntax; rapid, incremental, reversible operations whose impact is immediately visible (widely quoted wording; paper paywalled ⚠️). NN/g definition (Oct 2024): "users act on displayed objects of interest using physical, incremental, and reversible actions whose effects are immediately visible" https://www.nngroup.com/articles/direct-manipulation/
- Rules: live preview during drag/resize (≤0.1 s); numeric field next to every slider/handle for precision (steering law §2.2); snapping guides; undo for every manipulation; Microsoft: "where there is direct manipulation, there can be accidental manipulation and therefore the need for forgiveness".
- **Inline editing**: double-click or Enter/F2 to rename/edit in place; Enter commits, Esc reverts, Tab moves to next cell; edit state must look different (NN/g modes: "at least two visual indicators" — background + field border; https://www.nngroup.com/articles/modes/). Inline editing in table rows "works only if the table is narrow"; for wide records use a **nonmodal side panel** (NN/g data tables). Never lose an in-progress edit when focus leaves — commit or keep draft ⚠️ practitioner.

### 4.7 Data tables
NN/g (Apr 2022) https://www.nngroup.com/articles/data-tables/ — 4 core tasks: "Find record(s) that fit specific criteria · Compare data · View, edit or add a single row's data · Take action(s) on records".
- First column = **human-readable identifier**, "instead of a 'mystery meat' automatically generated ID".
- Default column order by importance; related columns adjacent.
- Filters "discoverable, quick, and powerful"; "clear visual indication that filters are active".
- "Freeze header rows and header columns (if the table is larger than the screen)"; help place-keeping with borders, zebra striping, or row hover highlight.
- Easy hide/reorder columns (not drag-only), with visible state ("15 columns hidden"); manual hide of rows; sort by any column.
- Single-record editing: avoid **modal** popups (they hide neighbouring records users copy from); prefer **nonmodal side panel or separate window**; accordions get left open and clutter.
- Actions: few inline actions per row; otherwise checkbox selection + batch action bar; "Select All".
- Sorting: click header = sort, click again = reverse, show arrow indicator; sorting should respond within 0.1 s ("users would feel that they are sorting the table", §2.5).
- Typography/format (typographic/practitioner convention; ⚠️ not in the NN/g article, no usability study found): **right-align numbers**, use tabular (monospaced) figures, same decimals per column, left-align text, units in header not cells; offer density (compact/comfortable) for sovereign apps.
- Virtualize long lists; never block the UI to load 10k rows; show row count ("1–50 of 3,204").

### 4.8 Dashboards
- Few's definition: "A dashboard is a visual display of the most important information needed to achieve one or more objectives, consolidated and arranged on a single screen so the information can be monitored at a glance." 13 pitfalls (Few, *Common Pitfalls in Dashboard Design*, Feb 2006, https://www.perceptualedge.com/articles/Whitepapers/Common_Pitfalls.pdf): exceeding a single screen · inadequate context for the data · excessive detail or precision · expressing measures indirectly · inappropriate display media · meaningless variety · poorly designed display media · inaccurate quantitative encoding · poor arrangement · ineffective highlighting of what's important · useless decoration · misused/overused color · unappealing display. Use flow: see big picture → focus on items needing attention → drill in.
- NN/g (2017) https://www.nngroup.com/articles/dashboards-preattentive/: encode quantities with **length and 2D position** (bars, lines, dots); avoid pies/donuts/gauges/treemaps for comparison ("area and angle" are hard to compare); color for categories/alerts, not magnitude.
- Rules: every number gets context (target, previous period, trend); the most important status top-left; alerts stand out by *removing* noise (NN/g complex-apps #8); hover for exact values without navigating (complex-apps #7); show "last updated" time. (Charting details → the dataviz skill.)

### 4.9 Search & filters
- Filter = excludes items; faceted navigation = "multiple filters that comprehensively describe a set of content" — more powerful but more interaction cost (https://www.nngroup.com/articles/filters-vs-facets/).
- **Batch vs interactive** (https://www.nngroup.com/articles/applying-filters/): if results can't update fast, "err on the side of batch filtering and include an Apply button"; or update after **1–2 s** of inactivity while still acknowledging each click immediately; don't scroll/jump the page while the user is mid-selection. On desktop with fast local data, apply instantly (≤0.1–0.4 s) and keep focus in the filter panel.
- Always show active filters as removable chips + "Clear all"; show result count; preserve query, filters, sort and scroll when returning from a detail view.
- Search field: visible (not icon-only) in sovereign apps; ⌘F/Ctrl+F focuses in-view find, ⌘K/palette for global; suggestions/autocomplete to prevent slips (NN/g slips); "no results" state says what was searched and offers to clear filters (§4.17).

### 4.10 Forms on desktop
- Labels **close to their fields**: above the field for short forms; NN/g allows **left labels for "extremely long desktop forms"** (https://www.nngroup.com/articles/web-form-design/). Eye-tracking: top labels ≈50 ms to field vs ≈500 ms for left-aligned labels (Penzo 2006, small study — from mobile notes ../research/ux-research.md). Never placeholder-as-label (https://www.nngroup.com/articles/form-design-placeholders/).
- Single column; logical sequence; explain format requirements up front ("Don't make users guess"); mark required/optional; no Reset/Clear buttons.
- **Tab order = visual order** (left→right, top→bottom); Enter submits single-line forms; Esc cancels dialogs; initial focus in the first field the user is most likely to type in (Microsoft: "Place the caret where users are most likely to type first").
- Errors (NN/g 10 guidelines, Dec 2024, https://www.nngroup.com/articles/errors-forms-design-guidelines/): inline validation where possible; success indicator only for complex fields; message next to the field; color + icon; "Don't Validate Fields Before Input is Complete"; summary never the *only* indicator; "Don't Use Tooltips to Report Errors"; extra help after repeated errors. Preserve all input on error (Tog, Shneiderman #5).
- Forgiving formats: accept spaces/dashes and normalize; auto-format as typed (https://www.nngroup.com/articles/slips/).
- Defaults: pre-fill the most likely value; Tog: no default if there's no predictable winner; field content auto-selected on focus so typing replaces it.

### 4.11 Settings / preferences
- Most people never change settings: Spool's team found **<5%** of several hundred Word users had changed any setting (programmers/designers changed >40% of options) — UIE, 2011, practitioner study https://archive.uie.com/brainsparks/2011/09/14/do-users-change-their-settings/. NN/g: users "rarely utilize fancy customization features, making it important to optimize the default" (https://www.nngroup.com/articles/the-power-of-defaults/). ⇒ **Defaults are the design**; settings are an escape hatch.
- Apply instantly (no OK/Apply) with visible effect and undo/revert, where the platform does so (macOS/GNOME convention — see platform notes); if a change is expensive or risky (e.g., display, sync location), preview + explicit confirm + auto-revert timer ⚠️ practitioner.
- Organize by user task, not by code module; searchable settings for >~20 options (VS Code/macOS System Settings pattern ⚠️ practitioner); every setting labeled with its effect; deep-link from feature to its setting and back.
- "Reset" says what and how much it resets — Tog: use "Restore Initial Settings", make scope (this tab vs all) unmistakable.
- Raskin warns preferences are often hidden modes ("Users often waste time trying to get their customizations right") — add a setting only when users genuinely differ, not to dodge a design decision.

### 4.12 Dialogs: modal vs nonmodal
- NN/g (2017) https://www.nngroup.com/articles/modal-nonmodal-dialog/: modal dialogs "interrupt the user's workflow", "cause users to forget what they were doing", "block the content in the background". Use modals only to (1) prevent/correct critical errors and irreversible loss, (2) request information **critical to continue** the current process, (3) fragment a complex occasional workflow, (4) ask for info that significantly reduces effort. Don't use for nonessential info; "Consider Nonmodal Dialogs Instead" when not critical.
- Desktop rules: prefer sheets/dialogs **attached to their document window** (window-modal) over app-modal; never nest modal on modal; Esc = Cancel; Enter = default (never the destructive button); buttons labeled with verbs; **follow platform button order** (Windows: OK first; Apple: OK last — "Do what the platform owner tells you to do", https://www.nngroup.com/articles/ok-cancel-or-cancel-ok/).
- Microsoft window rules (https://learn.microsoft.com/en-us/windows/win32/uxguide/win-window-mgt): owned windows open "centered" on owner (45% above / 55% below); contextual windows open **near the object** that launched them; program-initiated windows **don't take focus** — "flash the taskbar button three times… but don't do anything else"; user-initiated windows take focus only if rendered within **5 s**.

### 4.13 Confirmation vs undo
- NN/g (Nielsen 2018, reviewed Aug 2026) https://www.nngroup.com/articles/confirmation-dialog/: confirm only "actions with serious consequences — such as destroying users' work or costing large amounts of money", especially non-undoable ones; "Do not use confirmation dialogs for routine actions" (cry-wolf → automatic Yes); be **specific** (name the file/count: Windows' "these 2 items" is bad); buttons like **"Delete file" / "Keep file"** not Yes/No; **no default Yes**; for very dangerous ops require a **nonstandard action** (type the name/DELETE); optional "don't ask again" for educational confirms; "do go to great lengths to provide undo".
- Decision rule for agents: undoable → **just do it + show Undo** (toast/inline, and ⌘Z works); not undoable but recoverable (trash/versions) → do it + say where to recover; truly irreversible & costly → specific confirmation; catastrophic → typed confirmation. (Cooper, Raskin habituation, Tog "Always allow Undo" — §3.)
- Undo design: multi-level, named ("Undo Delete 3 Rows"), groups match user intent, survives save (ideally), covers settings and bulk ops; Redo; visible history for complex apps (About Face ch. 15 "Reversible Histories").

### 4.14 Error messages
NN/g (May 2023) https://www.nngroup.com/articles/error-message-guidelines/ — visibility: "Display the error message close to the error's source"; "noticeable, redundant, and accessible indicators" (bold, high-contrast, red + icon); severity-appropriate styling (warning ≠ error); "Avoid prematurely displaying errors". Communication: "human-readable language"; "Concisely and precisely describe the issue" (never "An error occurred"); "Offer constructive advice"; positive tone, don't blame ("invalid", "illegal"). Efficiency: "Preserve the user's input"; "Reduce error-correction effort" (offer the likely fix as a button); link to more detail sparingly. Tog adds: allow for "a deeper system malfunction" — offer "Copy details"/report. Desktop extras: errors from background jobs go to the job's row/status area plus a notification if the window is unfocused; error codes only in an expandable details section.

### 4.15 Status: indicators vs validations vs notifications
NN/g (Jan 2024) https://www.nngroup.com/articles/indicators-validations-notifications/: **indicators** are contextual, conditional, passive (unread bold, sync badge); **validations** are tied to user input and require action; **notifications** aren't triggered by the user's current action — **action-required** ones may be intrusive/modal, **passive** ones should be non-intrusive (badge, small nonmodal popover) and can be missed. Mobile notes: never put errors in a toast; toasts that carry anything important must persist long enough (WCAG 2.2.1).
- Desktop: OS notifications only when the app is **not focused** and the user would want to come back (job finished, mention, failure); in-app status otherwise; Tog: for >15 s jobs add "a noticeable sound & strong visual indication so users know to return".

### 4.16 Empty states (complex apps)
NN/g (Kaplan, Sept 2021) https://www.nngroup.com/articles/empty-state-interface-design/ — 3 uses: **communicate system status**, **provide learning cues** ("pull revelations", e.g. "Star your favorites to list them here"), **provide direct pathways** (Create button + Learn more; demo data). Never show "No records" while still loading ("trigger-happy users… never see the relevant content"); distinguish *nothing yet* / *no results for these filters* / *failed to load*.

### 4.17 Onboarding & help
- Tutorials "interrupt users, don't necessarily improve task performance, and are quickly forgotten"; users skip them (paradox of the active user); "What's New" modals at launch get dismissed unread (NN/g, Feb 2023, https://www.nngroup.com/articles/onboarding-tutorials/). Use **pull revelations**: contextual tips triggered by the related activity; easy to dismiss *and recall*; progressive detail; "No memorization!"; "Skip the obvious stuff".
- Tooltips (NN/g 2019): never for info "vital to task completion"; brief, not redundant with the label; mouse **and keyboard** triggered; consistent across all icons.
- Help (Heuristic #10, https://www.nngroup.com/articles/help-and-documentation/): proactive help short and contextual; reactive help (Help menu, docs) **comprehensive and searchable**, task-oriented steps; help menu search that also finds menu commands (macOS does this natively).
- First run: open into a useful state (sample/blank document or empty state with 1–2 primary actions), not a carousel; ask for permissions/accounts only when the feature needs them (mobile notes §7–8).

### 4.18 Progressive disclosure & wizards
- "Initially, show users only a few of the most important options… Offer a larger set of specialized options upon request"; "designs that go beyond 2 disclosure levels typically have low usability"; the advanced control must be visible with a clear label (strong information scent) (https://www.nngroup.com/articles/progressive-disclosure/). Classic desktop example: Print dialog → "Show Details".
- Staged disclosure in complex forms: reveal dependent options only when the triggering option is set (complex-apps #6).
- Wizards (https://www.nngroup.com/articles/wizards/): for novices or infrequent processes (setup, import); show the step list with current step highlighted; descriptive Next/Back labels; for repeat/expert tasks offer a single-form alternative; let users move back without losing data (complex-apps #3) and tell them where to resume if they cancel (Tog).

### 4.19 Loading & perceived performance
- Limits from §2.5. NN/g progress indicators (2014) https://www.nngroup.com/articles/progress-indicators/: give visual feedback **immediately** on input; "Use a progress indicator for any action that takes longer than about 1.0 second"; **looped spinner only for 2–10 s**, not <1 s (flash causes anxiety); **percent-done for ≥10 s** (or <10 s if processing a known count of items, e.g., "12 of 40 files"); text saying what is happening; time estimates rounded and padded; no static "Loading…". Myers (CHI '85, https://doi.org/10.1145/317456.317459): users prefer systems with percent-done indicators.
- Skeleton screens (NN/g, reviewed Sept 2026) https://www.nngroup.com/articles/skeleton-screens/: "used exclusively for full-page loads"; wireframe-like blocks mimicking the real layout; **don't** use frame-only skeletons (≈ spinner).
- Desktop specifics: Microsoft — busy pointer when blocked >1 s, "working in background" pointer when still responsive; don't combine with progress bars; progress windows in the lower-right of the active monitor. Never block the whole window for a background job — show it in a status bar/activity panel with Cancel; keep UI thread free (Tog "use multi-threading to push latency into the background").
- Optimistic UI for low-risk, high-success actions, with visible rollback on failure (mobile notes; practitioner).

### 4.20 Autosave, never losing data, offline & sync status
- Tog: "Ensure that users never lose their work. This principle is all but absolute." Raskin: "Users should not lose work"; continuous automatic save, universal undo. NN/g error messages: "Preserve the user's input".
- Rules: autosave documents and drafts continuously (debounced, e.g., after a pause) **and** on blur/quit; keep version history; crash recovery restores unsaved work on next launch; closing a window with only autosaved content needs no prompt; restore window/session state (macOS notes; Microsoft "Persistence"). If you must ask on quit, the buttons are "Save", "Don't Save", "Cancel" (verbs), never a default that discards.
- Show save/sync status as a quiet, always-visible **indicator** (Saved · Saving… · Offline — changes saved locally · Sync error ⟶ Retry), with last-sync time on hover; never color alone. Offline: keep working, queue changes, say what's unavailable (mobile notes §10, https://web.dev/articles/offline-ux-design-guidelines). Conflicts: show both versions and let the user choose/merge; never silently overwrite ⚠️ practitioner.

### 4.21 Multi-window & multi-monitor
Microsoft window-management guide (Win7, updated 2025) https://learn.microsoft.com/en-us/windows/win32/uxguide/win-window-mgt:
- **Persist** monitor, size, position and maximized state per window; if that monitor is gone, use last monitor → shrink to fit → move toward top-left → fall back to defaults. Never open off-screen.
- Default size "appropriate for its contents"; avoid near-maximized default restored sizes; set a **minimum size** below which content is unusable; bigger windows "must show progressively more information" (don't just add whitespace).
- Open new document windows cascaded from top-left; utilities centered; owned windows on their owner; respect user's Z-order; don't steal activation.
- Support opening documents/panels in separate windows or tabs for side-by-side comparison (NN/g data tables: users copy from neighbouring records; complex-apps #5 tool switching) ⚠️ practitioner extrapolation. Inspectors/palettes follow the active document window.

### 4.22 Toolbar & UI customization
- Allow toolbar customization in sovereign apps (add/remove/reorder, "Restore Default Set"); most users won't customize (<5%, §4.11), so the default set must be right. Customization ≠ personalization; NN/g found customizable sites score the same usability as regular ones; benefits only when there's a real need (https://www.nngroup.com/articles/customization-of-uis-and-products/).
- No adaptive/auto-rearranging menus or toolbars (Raskin: prevents habituation; Shneiderman #7 "They don't want surprises or changes in familiar behavior"). Recent/frequent lists are fine as **separate** sections.

### 4.23 Updates without disruption
- Don't interrupt work for updates or "What's New" (NN/g push revelations; Microsoft: program-initiated windows don't take focus). Download in background; install on quit/next launch or when idle; ask before restarting and never lose state across an update (restore windows, documents, undo where possible).
- Keep learned behavior stable: Tog "Over time, strive for continuity, not consistency" and "Make pages that have changed look changed"; never repurpose shortcuts or move high-frequency commands (Raskin habituation). Announce changes via a dismissible, recallable "What's New" entry in Help, and pull revelations at the changed feature.
- Status of update visible in the app menu/About and Settings ("Update ready — restart to install"), with release notes link ⚠️ practitioner synthesis.

## 5. User-centred process an agent can actually run (no real users yet)
Maps to ISO 9241-210 activities (§1.7). Steps 1–7 are agent-runnable; step 8 is what to hand to a human. Usability = effectiveness + efficiency + satisfaction for specified users, goals and context (ISO 9241-11:2018 definition — ⚠️ quoted from memory, not re-verified).

**Step 1 — Context of use (write it down, ≤1 page).**
- Users: 1–3 primary user types with experience level (novice / perpetual intermediate / expert — Cooper), frequency of use (daily-hours = sovereign posture; occasional = transient), environment (multi-monitor office, laptop on the go, shared screen), input (keyboard-heavy? pen? screen reader?).
- Jobs-to-be-done: "When [situation], I want to [motivation], so I can [outcome]" (common JTBD job-story template ⚠️ practitioner). NN/g: "Jobs-to-be-done focus on user problems and needs, while well-executed personas include the same information and also add behavioral and attitudinal details" — "Personas and Jobs-to-Be-Done Are Compatible" (https://www.nngroup.com/articles/personas-jobs-be-done/).
- **Top tasks**: list 5–10 tasks ranked by frequency × importance; the top 3 get the fewest steps, a shortcut, and a toolbar slot.

**Step 2 — Task analysis.** NN/g (Sept 2020) https://www.nngroup.com/articles/task-analysis/: gather (contextual inquiry, critical-incident interviews, diaries, activity sampling — or, for an agent, existing docs, support tickets, competitor workflows), then build a **hierarchical task analysis (HTA)**: goal → tasks → subtasks + "plans" (order/conditions; novices vs experts differ). Annotate each task with: count of steps, frequency, cognitive complexity, physical demands, time (KLM). "Do not rely solely on self-reported behavior… or simulations (remember: you are not the user!)".

**Step 3 — Usability requirements (measurable).** For each top task: target success rate, max steps/clicks, KLM time for expert path, max response time (0.1 s for direct manipulation, 1 s for navigation, progress UI >1 s), error-recovery path, keyboard-only completion = yes.

**Step 4 — Product design principles (3–5, product-specific).** Derive from the posture and users, e.g. "Content first, chrome quiet" (sovereign), "Never lose work", "Every command in menu + palette + shortcut", "Undo instead of confirm", "No surprises in familiar places". Each must be able to settle a real design dispute ⚠️ practitioner practice.

**Step 5 — Heuristic evaluation (self-run).** Procedure (NN/g, https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/): pick heuristics (Nielsen 10 + domain extras, e.g. §1.4/§1.6/§6); narrow scope (one task, one section, one user group, one device); **first pass to learn the flow, second pass to find violations**; record one issue per line with heuristic, location, evidence, fix; consolidate (affinity) and **rate severity separately after finding** (0–4, §1.2). Why many evaluators: "single evaluators found only 35 percent of the usability problems"; recommend "about five evaluators, but certainly at least three" (Nielsen 1994, https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/theory-heuristic-evaluations/; Nielsen & Molich CHI '90, https://doi.org/10.1145/97243.97281). **Agent adaptation** ⚠️: emulate 3–5 independent evaluators by doing separate passes with different lenses (novice first-run; daily expert/keyboard-only; screen-reader/high-zoom; error & edge cases; visual hierarchy) and only merge afterwards. Remember NN/g: a violation isn't automatically a bug — context and alternatives matter, "you should not bet that your design is one of the few exceptions".

**Step 6 — Cognitive walkthrough (learnability of new/unfamiliar workflows).** From Lewis, Polson, Wharton et al.: Polson, Lewis, Rieman & Wharton 1992, *IJMMS* 36:741–773 (https://doi.org/10.1016/0020-7373(92)90039-N); streamlined practitioner version by Wharton, Rieman, Lewis & Polson 1994 in Nielsen & Mack (eds.) *Usability Inspection Methods* (Wiley). At each step of a top task, answer (NN/g wording, Feb 2022, https://www.nngroup.com/articles/cognitive-walkthroughs/):
1. "Will users try to achieve the right result?"
2. "Will users notice that the correct action is available?"
3. "Will users associate the correct action with the result they're trying to achieve?"
4. "After the action is performed, will users see that progress is made toward the goal?"
Any "No" ⇒ the step **fails**; fix before shipping. Best for "complex applications and systems that require new design patterns", not for apps that use only standard patterns.

**Step 7 — Quantitative self-checks.**
- **KLM** (§2.4) for the expert path of each top task in 2 candidate designs; prefer the design that's faster *and* passes the walkthrough. Count Ms honestly (each decision/visual search ≈1.2 s).
- **Realistic-content test**: render every view with: 0 items, 1 item, typical, 10× typical, 10,000 rows; longest real names/paths/emails; non-Latin and RTL text; translated strings — IBM expansion figures via W3C: ≤10-char strings may grow **200–300%**, >70 chars ~**130%** (https://www.w3.org/International/articles/article-text-size); window at minimum size and on a 4K monitor; OS text-scaling 150–200%; dark/light; offline; slow network (3 s, 30 s responses); failed request; permission denied.
- **Keyboard-only pass**: complete each top task without the mouse; visible focus at every step; logical tab order; Esc closes every overlay.
- **Response-time audit**: every interaction acknowledged ≤0.1 s; anything >1 s shows progress; >10 s percent-done + Cancel.

**Step 8 — What to ask a human to test.**
- **Qualitative think-aloud test, ~5 users per round, then iterate**: Nielsen & Landauer (INTERCHI '93, https://doi.org/10.1145/169059.169166): problems found = N(1−(1−L)ⁿ), average **L = 31%** ⇒ 5 users ≈ 85% of problems; better "3 studies with 5 users each" than one with 15; for 2 groups use 3–4 per group, for ≥3 groups 3 per group (https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/). **Caveats**: L varies by product/task; Faulkner (2003, https://doi.org/10.3758/BF03195514) showed individual 5-user samples can find far fewer problems than the 85% average — treat 5 as a per-round minimum, not a guarantee; complex/expert desktop apps need representative domain users.
- Think-aloud: "Thinking aloud may be the single most valuable usability engineering method" (Nielsen; https://www.nngroup.com/articles/thinking-aloud-the-1-usability-tool/). Give realistic tasks (not "click X"), don't help, prompt "what are you thinking?", note where they hesitate.
- **Metrics** (for benchmarks you need **≥20–30 users** — NN/g, https://www.nngroup.com/articles/measuring-perceived-usability/): task success rate, time on task, error count, plus:
  - **SEQ** after each task: "Overall, how difficult or easy was the task to complete?" 1–7; historical average ≈ **5.3–5.6**; ask "why?" when <5 (Sauro, https://measuringu.com/seq10/; Sauro & Dumas CHI '09, https://doi.org/10.1145/1518701.1518946).
  - **SUS** after the session: 10 items, 5-point; score = (Σ(odd−1) + Σ(5−even)) × 2.5 → 0–100; **average 68** across 500 studies, **>80.3 ≈ top 10% (A)**, <51 ≈ bottom 15% (Brooke, "SUS: a 'quick and dirty' usability scale", 1996, in *Usability Evaluation in Industry*, Taylor & Francis; created 1986; https://measuringu.com/sus/; Bangor, Kortum & Miller 2008, https://doi.org/10.1080/10447310802205776). Don't alter wording/order.
  - NASA-TLX for high-consequence, trained-operator workflows (NN/g).
- Numbers from 5 users "should not inform design decisions" (NN/g) — use them to find problems, not to prove quality.

## 6. Top 25 desktop usability rules (checklist)
1. **Acknowledge every input within 0.1 s** (pressed state, selection highlight, cursor change); trap double-clicks/duplicate submits. (§2.5, Tog 50 ms)
2. **>1 s shows a busy indicator; >10 s shows percent-done + Cancel + what's happening**; long jobs never block the window. (§4.19)
3. **Never lose work**: continuous autosave, crash recovery, input preserved on every error, session/window state restored. (§4.20)
4. **Undo instead of confirm**: multi-level, named Undo/Redo for every data change; confirmations only for irreversible, costly actions — specific text, verb buttons, no default Yes. (§4.13)
5. **Every command lives in the menu bar** (or the app's complete command menu), with its shortcut shown; disabled not hidden. (§4.3)
6. **Full keyboard operation** with visible focus, logical tab order, Esc closes/cancels everything. (§4.1)
7. **Command palette** for apps with >~30 commands: fuzzy search, aliases, recents first, shortcuts shown. (§4.1)
8. **Don't override platform-standard shortcuts or dialog button order**; follow the OS menu structure. (§2.7, §4.12)
9. **Context menus open at the pointer**, contain only actions for the clicked object, ≤10–12 items, frequency-ordered, max one submenu level, all items also in the main menu. (§4.3)
10. **Use edges, corners and the pointer location** (Fitts); no dead pixels between edge controls and the screen edge in maximized/full-screen layouts; big targets for frequent actions, small/far for dangerous ones. (§2.1)
11. **No cascading menus deeper than 2 levels**; implement safe-triangle/menu-aim in custom menus; click-activated submenus. (§2.2)
12. **Standard selection model**: click, Shift-range, Ctrl/⌘-toggle, marquee, select-all, Esc/background-click deselect; selection, focus and hover visibly distinct. (§4.4)
13. **Drag and drop has signifiers, live preview, magnetism, Esc-cancel, undo, and a non-drag alternative.** (§4.5)
14. **Direct manipulation with precision fallback**: live preview + numeric field for every slider/handle. (§4.6)
15. **Tables**: human-readable first column, frozen headers, sortable columns, visible active-filter state, right-aligned tabular numbers, nonmodal side panel for record editing, batch actions. (§4.7)
16. **Errors**: next to the source, plain language, cause + fix button, no blame, error codes only in details. (§4.14)
17. **Status is glanceable**: save/sync/offline/background-job state always visible as quiet indicators; notifications only when unfocused and actionable. (§4.15, §4.20)
18. **Modals only for critical, blocking decisions**; window-modal over app-modal; never stacked; program-initiated windows never steal focus. (§4.12)
19. **Empty states explain status, teach, and offer the first action**; never "No items" while loading. (§4.16)
20. **No launch tutorials or What's-New modals**; contextual pull revelations, tooltips with shortcuts, searchable Help. (§4.17)
21. **Progressive disclosure ≤2 levels**, with clearly labeled "Advanced"/"Show Details"; staged disclosure in complex forms. (§4.18)
22. **Defaults do the work**: <5% of users change settings — optimize the default layout, toolbar and options; settings apply instantly and say what Reset resets. (§4.11)
23. **Modes are visible (≥2 indicators), escapable, and preferably quasimodal**; no adaptive/auto-reordering menus. (§3.2)
24. **Windows remember monitor/size/position, have sensible minimum sizes, show more content when bigger, and never open off-screen.** (§4.21)
25. **Speak the user's language and be consistent**: same verb/icon/shortcut for the same action everywhere (menu, toolbar, palette, docs); domain words, not internal jargon. (§1.1 #2/#4, Shneiderman #1)

## 7. Heuristic evaluation template (fill one row per issue)
Scope line first: `Product · user group · task · platform/window size · build/date · evaluator lens (novice / expert-keyboard / a11y / edge-case)`.

| ID | Task & step | Location (window › panel › control) | Observation (what happens, evidence/screenshot) | Heuristic(s) violated (N1–N10, S1–S8, ISO 5.x, DOET concept) | Frequency (rare/common) | Impact (easy/hard to overcome) | Persistence (once/repeated) | Severity 0–4 (mean of ≥3 independent ratings) | Recommendation (concrete fix) | Est. effort (S/M/L) | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| H-01 | Export › choose format | Export sheet › Format popup | "PNG" option silently drops layers; no warning | N1, N5, S5 | common | hard | repeated | 3 | Disable incompatible options with reason, or warn inline before export | S | open |

Cognitive-walkthrough companion row: `Task · step · Q1 right goal? · Q2 notices action? · Q3 associates action with goal? · Q4 sees progress? · Pass/Fail · fix`. KLM companion row: `Task · design A operators · time · design B operators · time · winner`.
Prioritize: all 4s before release; 3s next; batch 1–2s; re-test changed areas (NN/g: "the second study will both serve as quality assurance… and help provide deeper insights").

## Unverified / open questions
1. **ISO 9241-110:2020 principle definitions** — only clause titles/sub-headings and intro verified (STN EN preview); the definitional sentences are paywalled. iso.org returned 403 to scripted fetch.
2. **ISO 9241-210:2019 six principles** — wording given is the widely quoted 2010-era text; the 2019 text and the "confirmed 2025" status were seen only via search snippets/secondary pages.
3. **ISO 9241-11:2018 usability definition** — from memory.
4. **Norman DOET definitions** — paraphrased from the book (not online); only the "Signifiers, not affordances" essay (2008) and NN/g summaries were read.
5. **Cooper *About Face*** — chapter/section titles and page numbers verified from Wiley's 4th-ed TOC/index PDFs; posture definitions paraphrased; "Don't stop the proceedings with idiocy" not found in the 4th-ed TOC (likely 1st/2nd ed.).
6. **Raskin** — principles verified via Raskin Center and a Brown course summary, not the book; "First Law" quote not verified.
7. **Doherty threshold** — the IBM-hosted copy of Doherty & Thadhani (GE20-0752-0, 1982) is 404; "400 ms" is the popular label (Laws of UX), its "IBM Systems Journal" attribution looks wrong; treat as practitioner lore.
8. **Tog's "5× faster Mac menu bar"** and "1-pixel boundary = 20–30% slowdown" — Tog's own tests, not published studies.
9. **Native submenu safe-triangle behavior** on current macOS/Windows — NN/g (2024) says Apple reverted Tog's triangle; Tog (1999) says OS X uses a timer; not re-tested in 2026. Implement menu-aim in custom menus regardless.
10. **Spool's "<5% change settings"** — 2011 blog post about an older Word study; sample details not published.
11. **SUS original citation** — Brooke 1996 book chapter (Taylor & Francis) not checked against the publisher; MeasuringU says SUS was created in 1986.
12. **Practitioner-only rules** (marked ⚠️ inline): palette prefixes, selection-under-filter messaging, numeric alignment, settings search threshold (~20), auto-revert for risky settings, sync-conflict handling, multi-window extrapolation, update UX, "agent emulates multiple evaluators". No controlled studies found.
13. **Open question for the skill**: Nielsen #7 (multiple paths) vs Raskin's monotony (one gesture per effect) — resolved here as "one canonical command, many entry points, same name/shortcut everywhere"; no empirical test of this compromise found.
14. **Open question**: KLM operator values date from 1980s hardware/users; modern trackpads and high-DPI screens may change P (1.1 s). Use for *relative* comparison of designs only.

## Key sources (all fetched 2026-11-02 unless noted)
- NN/g: ten-usability-heuristics · how-to-rate-the-severity-of-usability-problems · how-to-conduct-a-heuristic-evaluation (+ theory-heuristic-evaluations) · response-times-3-important-limits · fitts-law · steering-law · menu-design · hicks-law-long-menus (video) · teslers-law (video) · complex-application-design · ui-accelerators · contextual-menus · drag-drop · data-tables · direct-manipulation · modes · empty-state-interface-design · modal-nonmodal-dialog · confirmation-dialog · error-message-guidelines · errors-forms-design-guidelines · web-form-design · indicators-validations-notifications · progress-indicators · skeleton-screens · progressive-disclosure · wizards · onboarding-tutorials · tooltip-guidelines · help-and-documentation · keyboard-accessibility · filters-vs-facets · applying-filters · dashboards-preattentive · the-power-of-defaults · customization-of-uis-and-products · ok-cancel-or-cancel-ok · slips · user-mistakes · two-ux-gulfs-evaluation-execution · task-analysis · personas-jobs-be-done · cognitive-walkthroughs · why-you-only-need-to-test-with-5-users · thinking-aloud-the-1-usability-tool · measuring-perceived-usability (all under https://www.nngroup.com/articles/ or /videos/).
- Authors: https://www.cs.umd.edu/users/ben/goldenrules.html · https://asktog.com/atc/principles-of-interaction-design/ · https://asktog.com/columns/022DesignedToGiveFitts.html · https://jnd.org/signifiers-not-affordances/ · https://www.raskincenter.org/rchi/core-principles · https://www.perceptualedge.com/articles/Whitepapers/Common_Pitfalls.pdf · https://blog.superhuman.com/how-to-build-a-remarkable-command-palette/
- Platform guides: https://learn.microsoft.com/en-us/windows/win32/uxguide/inter-mouse · https://learn.microsoft.com/en-us/windows/win32/uxguide/win-window-mgt · https://code.visualstudio.com/api/ux-guidelines/command-palette
- Papers (DOIs verified via api.crossref.org): Fitts 1954 10.1037/h0055392 · Hick 1952 10.1080/17470215208416600 · Hyman 1953 10.1037/h0056940 · Miller 1956 10.1037/h0043158 · Cowan 2001 10.1017/S0140525X01003922 · Card, Moran & Newell 1980 10.1145/358886.358895 · Shneiderman 1983 10.1109/MC.1983.1654471 · Myers 1985 10.1145/317456.317459 · Nielsen & Molich 1990 10.1145/97243.97281 · MacKenzie & Buxton 1992 10.1145/142750.142794 · Polson et al. 1992 10.1016/0020-7373(92)90039-N · Nielsen & Landauer 1993 10.1145/169059.169166 · Nielsen 1994 10.1145/191666.191729 · Accot & Zhai 1997 10.1145/258549.258760 · Faulkner 2003 10.3758/BF03195514 · Bangor et al. 2008 10.1080/10447310802205776 · Sauro & Dumas 2009 10.1145/1518701.1518946
- Books (publisher pages): Norman DOET rev. ed. 2013 (Basic Books, ISBN 9780465072996) · Cooper et al. *About Face* 4th ed. 2014 (Wiley, ISBN 9781118766576) · Raskin *The Humane Interface* 2000 (Addison-Wesley) · Shneiderman et al. *Designing the User Interface* 6th ed. 2016 (Pearson).
