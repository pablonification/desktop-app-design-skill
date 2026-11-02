# Emotional design, delight, personality and trust

Read this to decide how the app should feel and to make that feeling concrete: the personality brief (3 adjectives + 1 anti-adjective), "familiar structure, distinctive details", the signature moment, trust and voice, and the line between persuasion and manipulation. Backed by Norman, Walter, Kano, and peer-reviewed research on aesthetics, first impressions, trust and memory. Every rule cites its source inline; ⚠️ marks claims that couldn't be fully verified (collected at the end). Researched November 2026 — platform details change, so re-check anything version-specific.

Contents: 0. TL;DR — rules to act on · 1. Norman — *Emotional Design*: visceral, behavioral, reflective · 2. Walter — *Designing for Emotion*: needs hierarchy, persona, personality · 3. Other frameworks · 4. Aesthetics research: does beauty make things feel usable? · 5. First impressions, prototypicality & standing out · 6. Trust & credibility · 7. Peak-end rule & memory · 8. Delight · 9. Personality & voice · 10. Ethics boundary: persuasion vs manipulation · 11. Agent playbook · Unverified / open questions · Sources

## 0. TL;DR — rules to act on

1. **Basics first, then pleasure.** Functional → reliable → usable → pleasurable (Walter; NN/g). Surface delight on a broken base backfires; bad usability makes the app *look* worse after use (Tuch et al. 2012).
2. **Polish is measurable.** "Craftsmanship" is its own facet of perceived beauty and showed the biggest gap between a crafted and a sloppy version (d = 1.60) (Moshagen & Thielsch 2010). Kill every alignment, radius, icon-style, clipping and jank defect.
3. **You're judged in 17–50 ms**, and that snap judgment covers appeal, usability *and* trustworthiness (Lindgaard 2006/2011; Tuch et al. 2012). Make the first frame of the first window excellent.
4. **Familiar structure, distinctive details.** Typical-for-its-category + low complexity is rated most beautiful; atypical layouts lose at every complexity level (Tuch 2012; MAYA). Be distinctive in type, color, icon, motion signature, copy, empty states — not in navigation, controls, shortcuts, chrome.
5. **Two trust gates:** design gets you *rejected* fast (94% of rejection comments were about design), content/substance gets you *trusted* (83% of trust comments were about content) (Sillence et al. 2004). Need both.
6. **Trust = competence + benevolence + integrity** (McKnight 2002): it works and never loses data; it acts in my interest; it tells the truth (honest saved/sync/progress states, honest pricing, data transparency).
7. **Peaks and ends shape memory**; duration barely does (Kahneman 1993; meta-analysis r = .58 for peak-end, duration ≈ 0). But the overall average predicts as well — make the whole good, then invest in first success, completions, error recovery, quit, trial end.
8. **Stressful moments get the plainest UI**; relaxed moments can carry expressive flourishes (Norman 2002).
9. **Delight respects time:** the more frequent the moment, the less ornament. Never block input. Deep delight (faster/easier than expected) > surface delight (confetti). Delighters decay into expectations (Kano).
10. **Voice: trust first, warmth second.** Casual, conversational, moderately enthusiastic tone tested best; humor is risky; trust explained ~52% of desirability vs ~8% for friendliness (NN/g 2016). Same voice everywhere; tone shifts with emotional stakes.
11. **One persona, one signature moment.** 3 adjectives + 1 anti-adjective drive type, color, motion, copy, sound; one ownable moment tied to the core value (§11).
12. **Never manipulate.** Subtle dark patterns work *and* don't trigger backlash — that's why they're dangerous (Luguri & Strahilevitz 2021). Equal-weight choices, ask once, cancel as easy as subscribe (DSA Art. 25; FTC 2022).

## 1. Norman — *Emotional Design* (2004): visceral, behavioral, reflective

Source status: book (Donald A. Norman, *Emotional Design: Why We Love (or Hate) Everyday Things*, Basic Books, 2004; jnd.org lists "Published: 2004" and a chapter "Three Levels of Design: Visceral, Behavioral and Reflective") **not read directly** — levels below are from NN/g's summary (Fessenden, "The 3 Pillars of User Delight", 27 Nov 2022) and consistent secondary summaries. Norman's precursor essay *was* read: Norman 2002, "Emotion & design: attractive things work better", *Interactions* 9(4):36–42, doi:10.1145/543434.543435 (jnd.org copy).

Norman 2002, directly quoted: "Positive affect enhances creative, breadth-first thinking"; "Positive affect makes people more tolerant of minor difficulties"; "Anxiety focuses the mind"; "it is essential that products designed for use under stress follow good human-centered design"; "Products designed for more relaxed, pleasant occasions can enhance their usability through pleasant, aesthetic design." (Norman bases this on affect psychology, e.g. Isen's work, plus the Kurosu/Tractinsky ATM studies in §4 — not on direct experiments with software.)

**Design rule from this:** the more stressful the moment (error, data at risk, payment, deadline), the *plainer and more obvious* the UI must be — strip decoration, raise clarity. Save expressive flourishes for calm moments (first launch, empty states, completion).

| Level | What it is | Desktop-app moves |
|---|---|---|
| **Visceral** — the instant, pre-conscious reaction to appearance, sound, feel (NN/g: features that "instinctively spark positive affect") | First window, app icon, launch, type and color, sound | App icon crafted at every size (16 px Finder list to 1024 px), not a generic glyph on a gradient. First window opens at a sensible size/position, already populated (sample doc or a designed empty state), no flash of unstyled content, no spinner wall. One confident typographic voice; restrained palette with one accent; real materials of the platform (vibrancy/Mica/libadwaita) rather than flat web grey. Pixel-snapped strokes and icons; crisp at 1× and 2×. |
| **Behavioral** — pleasure and effectiveness of *use*: understandable, controllable, fast, feels good in the hand (NN/g: delight when a task is "easier than expected") | Every interaction, keyboard, feedback, performance | Instant response to input (< 100 ms), keyboard-first with standard shortcuts, undo everywhere, direct manipulation, drag-and-drop that does the expected thing, menus complete and correctly greyed. The "feel" is mostly speed + predictability; motion only to explain change (see `motion.md`). This is where most trust is earned (§6). |
| **Reflective** — conscious meaning: self-image, values, memories, "what does using this say about me", story you tell others | About box, brand, values, the app's point of view, how it ends, what people share | A clear stance stated once (e.g. "Local-first. Your files stay on your Mac."), honored everywhere. Craft visible in places only enthusiasts check (About window, icon details, keyboard cheat-sheet, changelog voice). Respect for the user's data and attention (export, no lock-in, no nags). Good endings (§7) because memory is reflective. |

Norman's central point (all summaries agree): the levels operate together and conflict — an app can win visceral and lose behavioral (pretty but slow), or win behavioral and lose reflective (efficient but you're embarrassed by it). Design all three; when they conflict in a tool, behavioral wins.

## 2. Walter — *Designing for Emotion*: needs hierarchy, persona, personality

Source status: Aarron Walter, *Designing for Emotion*, A Book Apart; 1st ed. 17 Oct 2011, **2nd ed. 22 Jun 2020** (107 pp., ISBN 978-1-952616-49-5; chapters: Emotional Design; Designing for Humans; Personality; Empathy and Inclusion; Emotional Engagement; Trust, Fear, and Forgiveness; The Business of Emotional Design) — per publisher page, which now says "A Book Apart no longer sells or distributes books" (contact author). Book **not read directly**; read the author's own excerpt "Personality in Design" (A List Apart, 18 Oct 2011) and NN/g's account of the hierarchy.

- **Hierarchy of user needs** (Walter, adapted from Maslow; as presented by NN/g "A Theory of User Delight", Fessenden, 5 Mar 2017): **functional → reliable → usable → pleasurable**. Pleasure only counts once the lower layers hold; NN/g: "a product can be delightful only if it is usable", and "no one's ever said, 'I'm thrilled this beautiful product doesn't work as well as I expected.'" (Walter's excerpt itself places personality at the "pleasure" layer, after functionality, reliability and usability.) Critique: the Maslow mapping is loose (commentators find no real correspondence between layers) — treat it as a priority order, not psychology. Jordan (2000) proposed a similar functionality → usability → pleasure ladder (⚠️ secondary).
- **Design persona** (ALA excerpt): a document that defines the product's personality so visual design, copy and interaction stay consistent. Sections: brand name; overview; personality image (a person/mascot embodying it); **brand traits — 5–7 traits plus one trait to avoid**; personality map (axes: unfriendly↔friendly, submissive↔dominant); voice (and how it shifts by situation); copy examples; visual lexicon (color, type, style, mood board); engagement methods.
- **"This, but not that" traits** (MailChimp example, ALA excerpt): "Fun, but not childish." "Funny, but not goofy." "Powerful, but not complicated." "Hip, but not alienating." "Easy, but not simplistic." "Trustworthy, but not stodgy." "Informal, but not sloppy." Mascot used sparingly, for humor only — never to deliver feedback, stats or task help. **Move:** write traits as pairs; the "but not" half is what stops overshooting.
- **Authenticity:** contrived personality backfires — audiences notice and may "never trust your brand"; "Personality is a risk, but … the rewards are worth it" (ALA excerpt).
- The 2nd edition's chapter "Trust, Fear, and Forgiveness" (TOC) matches §6/§7 here: emotional goodwill buys forgiveness for occasional failure — but only if the basics usually work (⚠️ content not read).

## 3. Other frameworks (Jordan, Anderson, Csikszentmihalyi, Kano)

**Jordan, *Designing Pleasurable Products*** (Patrick W. Jordan, Taylor & Francis, 2000; ⚠️ not read — Open University course + library records). Four pleasures, adapted from anthropologist Lionel Tiger:
- *Physio* (senses): crisp type rendering, satisfying sound on completion, smooth 120 Hz scrolling, trackpad haptics where the OS supports them.
- *Socio* (relationships/status): beautiful shareable exports, good collaboration presence, an app people recommend without embarrassment.
- *Psycho* (cognitive/emotional): low mental load, feeling of mastery, "it just did what I meant".
- *Ideo* (values, taste): local-first, privacy, accessibility, sustainability, craft — values users want to align with.
**Move:** for each app, name which pleasure is primary (a pro tool: psycho; a journal: ideo + physio) and spend effort there.

**Anderson, *Seductive Interaction Design*** (Stephen P. Anderson, New Riders, 2011; publisher sample pages + TOC read). Premise: usable is necessary but not enough — chapter 1 "Beyond usability". Sections: (1) *Aesthetics, Beauty, and Behavior* ("Are you easily understood?", "Are you attractive?", "Who do you remind people of?" — associations and trust); (2) *Playful Seduction* — humor "when appropriate", surprise mixed with rewards, "Delighters", curiosity / information-gap theory, self-expression; (3) *The Subtle Art of Seduction* — small first steps, endowed-progress effect, fewer options, less text, defaults, framing, "An Eye for Details" (role-play the interaction, script the narrative, look for micromoments, minimize choices per moment); (4) *The Game of Seduction* — challenge, status, scarcity. **Use sections 1–3; treat section 4's scarcity and status mechanics with suspicion** in a tool — they sit next to the dark patterns in §10.

**Csikszentmihalyi, *Flow*** (Harper & Row, 1990; ⚠️ via secondary summaries). Conditions of flow: clear goals, immediate feedback, challenge matched to skill, deep concentration, sense of control, loss of self-consciousness, altered sense of time. NN/g ties *deep delight* to flow (§8). For tools:
- *Clear goals:* every view has one obvious primary purpose; the current task/state is visible (document title, mode, selection).
- *Immediate feedback:* every keypress/click acknowledged within 100 ms; live preview instead of apply-and-wait.
- *Challenge ↔ skill:* progressive disclosure, then accelerators (shortcuts, command palette, scripting) so experts keep growing (see `interaction.md` §3.4).
- *Protect concentration:* no unsolicited modals, toasts, update nags or "what's new" during work; batch notifications; focus/distraction-free mode.
- *Control:* undo, non-destructive edits, predictable autosave.

**Kano model** (Kano, Seraku, Takahashi & Tsuji 1984, "Attractive quality and must-be quality", *Hinshitsu (J. Japanese Society for Quality Control)* 14(2):147–156; DOI 10.20684/quality.14.2_147 resolves via doi.org to J-STAGE — registered with JaLC, not Crossref; paper itself not read). Categories: **must-be** (absence → anger; presence → no credit: never losing data, launching fast, native shortcuts), **one-dimensional/performance** (more = better: speed, sync reliability, search quality), **attractive/delighters** (unexpected, absence not missed), plus indifferent and reverse. **Decay:** delighters migrate to performance and then must-be over time (Kano's later "life cycle of quality" work, ⚠️ not read; widely accepted). Examples: dark mode, command palettes, live collaboration, "Saved" indicators were once delighters and are now expected. **Moves:** (1) audit must-bes first — they are invisible when present and unforgivable when absent; (2) delighters must be refreshed, and copying the category's current delighters only gets you to "expected"; (3) beware *reverse* qualities — features some users actively dislike (forced animations, chatty mascot, sounds on by default).

## 4. Aesthetics research: does beauty make things feel usable?

**Bottom line for an agent:** looks shape the *first* judgement of quality and usability; real use then pulls judgement back toward actual usability — and bad usability drags perceived beauty down. Polish is a multiplier on working software, not a substitute.

| Study (DOI verified via Crossref) | What they did | What they found (precisely) | Caveats |
|---|---|---|---|
| Kurosu & Kashimura 1995, CHI '95 companion pp. 292–293, doi:10.1145/223355.223680 | 26 ATM keypad/screen layouts rated for beauty and "apparent usability" | Apparent usability correlated with beauty (r ≈ .59, reported in secondary sources); apparent usability "strongly affected by the aesthetic aspects rather than the inherent usability" (abstract) | No actual use; ⚠️ participant count differs between secondary sources (156 vs 252) — couldn't read full text |
| Tractinsky 1997, CHI '97, doi:10.1145/258549.258626 | Replicated Kurosu in Israel with the same 26 layouts | Aesthetics–apparent-usability correlation held (even stronger) across cultures | Still pre-use ratings |
| Tractinsky, Katz & Ikar 2000, *Interacting with Computers* 13(2):127–145, doi:10.1016/S0953-5438(00)00031-X | Simulated ATM, aesthetics and actual usability manipulated, ratings before/after use | Pre-use beauty ↔ usability correlation stayed strong after use; aesthetics affected post-use perceived usability, "whereas the degree of actual usability had no such effect" (abstract) | Small simple tasks; later work reversed it (below) |
| Sonderegger & Sauer 2010, *Applied Ergonomics* 41:403–410, doi:10.1016/j.apergo.2009.09.002 (author PDF read) | 60 adolescents, functionally identical simulated phones, appealing vs unappealing skin | Appealing phone rated more usable **and** tasks were faster: mean completion 147.7 s vs 198.5 s | Teens 14–17, one product; performance effect not widely replicated |
| Hassenzahl 2004, *Human–Computer Interaction* 19(4):319–349, doi:10.1207/s15327051hci1904_2 | 4 MP3-player skins, before/after use | Beauty depended mostly on **identification** (hedonic: "communicate important personal values to relevant others"); goodness depended on usability + hedonic; after use, perceived usability and goodness changed with actual usability problems, while beauty and hedonic ratings "remained stable over time" (abstract) | Skins, not whole apps |
| Tuch, Roth, Hornbæk, Opwis & Bargas-Avila 2012, *Computers in Human Behavior* 28(5):1596–1607, doi:10.1016/j.chb.2012.03.024 | 80 people, online shop in 2×2 (aesthetics × usability), rated before/after | "Aesthetics does not affect perceived usability. In contrast, usability has an effect on post-use perceived aesthetics" — frustration from poor usability lowered beauty ratings (abstract via search summary; full text paywalled) | One shop; strong usability manipulation |

Measurement models worth knowing:
- **Pragmatic vs hedonic quality** (Hassenzahl, Burmester & Koller 2003, AttrakDiff, doi:10.1007/978-3-322-80058-9_19): pragmatic = helps me do the task (clear, controllable, efficient); hedonic = stimulation (novel, interesting) + identification (says something about me). Hassenzahl & Tractinsky 2006 (*Behaviour & IT* 25(2):91–97, doi:10.1080/01449290500330331) frame UX as beyond the instrumental: hedonic needs, affect and the experiential, temporal nature of use. **Move:** design both — a tool must be pragmatically excellent *and* give something to identify with (a point of view, craft you're proud to show).
- **Classical vs expressive aesthetics** (Lavie & Tractinsky 2004, *IJHCS* 60(3):269–298, doi:10.1016/j.ijhcs.2003.09.002): classical = orderly, clear, symmetric, pleasant (close to usability experts' rules); expressive = creative, original, fascinating, sophisticated. The classical dimension is "more closely related to perceived usability" (quoted via EduTech Wiki ⚠️ full text not read). **Move:** get classical right everywhere (alignment, spacing, contrast); spend expressive budget in a few chosen places.
- **VisAWI** (Moshagen & Thielsch 2010, *IJHCS* 68(10):689–709, doi:10.1016/j.ijhcs.2010.05.006; author preprint read): 7 studies, 84 → **18 final items**, four facets under one general aesthetics factor (facets intercorrelate .60–.74): **Simplicity** ("clarity, orderliness, homogeneity, grouping, and balance"), **Diversity** ("visual richness, dynamics, variety, creativity, and novelty"), **Colorfulness** (individual colors and their composition), **Craftsmanship** ("whether the site was designed with skill and care using modern technologies"; "the skillful and coherent integration of all relevant design dimensions"; modern tech "to avoid the impression of being outdated"). Two findings that matter: (1) in a pleasing-vs-deliberately-distorted version of the same site, the **largest difference was on Craftsmanship (d = 1.60)**, smallest on Diversity (d = 0.49); (2) after people actually used sites, perceived usability correlated moderately with **Simplicity and Craftsmanship**, but not with Diversity or Colorfulness. Craftsmanship is the research name for "polish" — and it's the facet most tied to perceived quality, whereas novelty/colour are not. (A short VisAWI-S exists — Moshagen & Thielsch 2013 ⚠️ not opened.)

Desktop moves from this section:
1. Ship nothing with visible craft defects: misaligned baselines, inconsistent radii, mixed icon styles, off-grid spacing, clipped text, jank. These are "craftsmanship" failures users rate within a glance.
2. Don't rely on beauty to hide friction — Tuch 2012 shows bad usability makes the app *look* worse after use.
3. Use visual polish where judgments form fast: first window, empty state, settings, About box, app icon.
4. Give the app an identity people want to be associated with (Hassenzahl's identification) — a coherent point of view, not decoration.

## 5. First impressions, prototypicality & standing out

**The key tension:** users like what is *simple* and *typical for its category*. Novelty helps only while the design still reads as a recognisable member of its category. So: **familiar structure, distinctive details.**

- **50 ms** — Lindgaard, Fernandes, Dudek & Brown 2006, *Behaviour & IT* 25(2):115–126, doi:10.1080/01449290500330448: visual-appeal ratings of homepages at 50 ms correlated highly with ratings at 500 ms; "visual appeal can be assessed within 50 ms". Lindgaard et al. 2011 (*ACM TOCHI* 18(1), doi:10.1145/1959022.1959023) extended this: at 50 ms, judgments of perceived usability and **trustworthiness** were also "largely driven by visual appeal", though they rely on somewhat different visual attributes.
- **17 ms, prototypicality** — Tuch, Presslaber, Stöcklin, Opwis & Bargas-Avila 2012, *IJHCS* 70(11):794–811, doi:10.1016/j.ijhcs.2012.06.003 (author preprint read): 119 real company-site screenshots × visual complexity (VC: low/med/high) × prototypicality (PT: low/high). Both VC and PT affected beauty ratings at 50 ms and even at **17 ms**. Very large effects: study 1 ηp² VC = .58, PT = .81; study 2 VC = .52, PT = .55. Interaction: low PT sites were judged unattractive at *every* complexity level; high-PT, low-VC sites were most beautiful. Their conclusion: "Designs that contradict what users typically expect … may trigger a suboptimal first impression and impair users' expectations." Limits (authors'): passive viewing of screenshots, young Swiss sample, company sites only.
- **MAYA** — Hekkert, Snelders & van Wieringen 2003, *British Journal of Psychology* 94:111–124 ("Most advanced, yet acceptable"): for product designs, typicality and novelty both predicted preference and together explained ~56% of it; they suppress each other, so the sweet spot is maximum novelty that keeps typicality (doi:10.1348/000712603762842147; findings via search summaries, full text not read). Tuch 2012 explicitly links its result to this: "novelty only affects aesthetic judgments given high PT."
- **Complexity & color, not universal** — Reinecke et al. 2013, CHI, pp. 2049–2058, doi:10.1145/2470654.2481281 (full text read): 450 sites, 548 volunteers; computational colorfulness + complexity models plus demographics explain **48%** of variance in 500 ms appeal ratings (adj. R² = .48). Complexity mattered far more than colorfulness; high complexity caused the largest drop, low ≈ medium. People **over 45 preferred lower complexity** more than other ages; **PhD holders were most negatively affected by high colorfulness**; gender had no interaction. Even Webby-award sites averaged only 4.21–6.57/9 with wide spread — no universal "best". Follow-up (Reinecke & Gajos 2014 CHI, ~2.4 M ratings, ~40 k people): country differences exist (e.g. Russians and Finns penalised complexity most).
- **Processing fluency** — Reber, Schwarz & Winkielman 2004, *Personality and Social Psychology Review* 8(4):364–382, doi:10.1207/s15327957pspr0804_3: "The more fluently perceivers can process an object, the more positive their aesthetic response." Fluency is raised by figure–ground contrast, symmetry, repetition, **prototypicality**, and priming. This is the mechanism behind the 17 ms results: easy-to-process = liked = feels true/trustworthy.

What "prototypical" means for a desktop app (my synthesis — not tested on desktop software directly):
- Category conventions users already hold: a mail client has a sidebar → list → reading pane; an editor has a document canvas with toolbar/inspector; a launcher is a single centred field with a result list. Keep these.
- Platform conventions: menu bar / title-bar placement, window controls, standard shortcuts, settings window shape (see `macos.md`, `windows.md`, `linux.md`).
- Distinctiveness goes into the *details* that do not change how the app is operated (see §11b).
- Keep visual complexity low by default (density can be user-adjustable — power users accept density, first impressions punish it). Respect older/expert audiences' lower tolerance for clutter and loud color.

## 6. Trust & credibility

**Two-gate model (the most useful single idea here):** looks decide whether people *reject* you fast; substance decides whether they *trust* you over time.
- **Sillence, Briggs, Fishwick & Harris 2004**, CHI pp. 663–670, doi:10.1145/985692.985776 (full text read): 15 women researching menopause/HRT over 4 weeks. Of comments explaining **rejection/mistrust, 94% were about design** (inappropriate name, complex busy layout, lack of navigation aids, boring design esp. colour, pop-up ads, slow intros, small print, too much text, corporate look and feel, poor search) vs 6% content. Of comments explaining **trust/selection, 83% were about content** (informative, unbiased, relevant, clear simple language) vs 17% design. Rejected sites were often "not explored further than the homepage". Small qualitative sample; health context.
- **Seckler, Heinz, Forde, Tuch & Opwis 2015**, *Computers in Human Behavior* 45:39–50, doi:10.1016/j.chb.2014.11.064 (abstract/highlights via search only): distrust is "mostly an effect of graphical and structural design issues"; trust rests on social factors (reviews, recommendations); privacy issues raised distrust, security signs raised trust; distrustful experiences = missing honesty and benevolence.
- **Fogg et al. 2003**, DUX '03 pp. 1–15, doi:10.1145/997078.997097: 2,684 people compared live sites; **"design look" was mentioned in 46.1% of credibility comments** — the most-mentioned factor; next were information structure and information focus (abstract). Caveat: a parallel expert study (Stanford, Tauber, Fogg & Marable 2002, 15 health/finance experts) ranked design look only 6th, behind name, information source, company motive — experts discount looks; novices lean on them (ranking via secondary page ⚠️).
- **Stanford Guidelines for Web Credibility** (Fogg, 2002; credibility.stanford.edu/guidelines) — 10 rules; the desktop-relevant ones: make claims verifiable; show a real organisation behind it; make it easy to contact you; "look professional (or appropriate for your purpose)"; "easy to use — and useful"; show it's updated; "use restraint with any promotional content"; **"avoid errors of all types, no matter how small they seem"** (typos, broken links, downtime).
- **Kim & Moon 1998**, *Interacting with Computers* 10(1):1–29, doi:10.1016/S0953-5438(97)00037-4: cyber-banking UIs; 14 visual design factors in four groups (title, menu, main clipart, colour) significantly affected feelings of trustworthiness, symmetry, awkwardness, elegance; two redesigned interfaces successfully *induced* different levels of trustworthiness. I.e. perceived trustworthiness is designable through visual choices (Korean sample, 1990s aesthetics — use the principle, not the specific colours).
- **Lindgaard et al. 2011** (doi:10.1145/1959022.1959023): trustworthiness judgments at 50 ms are "largely driven by visual appeal."
- **McKnight, Choudhury & Kacmar 2002**, *Information Systems Research* 13(3):334–359, doi:10.1287/isre.13.3.334.81: trust = disposition to trust + institution-based trust (structural assurances: platform, guarantees) + trusting beliefs (**competence, benevolence, integrity**) + trusting intentions (willingness to depend on it). Map to software: competence = it works and never loses data; benevolence = it acts in my interest (no dark patterns, no surprise upsells); integrity = it tells the truth (honest states, honest pricing, honest data use); institution-based = signed/notarised binary, store listing, known company, clear privacy policy.

Desktop trust builders (each maps to the evidence above):
1. **Competence signals:** zero craft defects in the first window; no layout shift on load; native-feeling controls, correct shortcuts; fast cold start (or an honest, branded launch state); crash-free first session.
2. **Data-safety cues:** autosave with visible, quiet confirmation ("Saved · 2 s ago" / "All changes saved"); undo for everything destructive; version history/restore; explicit "where is my data" (local path, cloud, sync state) in settings; export in open formats; on quit with unsaved/unsynced work, say exactly what will happen.
3. **Honest states:** progress that reflects real work (determinate where possible); offline/sync/conflict states named plainly; never show "Saved" before it's persisted; failures say what happened, what's safe, what to do (see `interaction.md` §4.14).
4. **Integrity & benevolence:** say what leaves the device and why, before it does (telemetry opt-in or clear opt-out, permission prompts with a one-line reason); pricing and trial end dates shown plainly; cancel/uninstall as easy as start; no nags.
5. **Institutional cues:** code-signed/notarised builds (unsigned-app OS warnings are a trust killer at the very first moment), real company name + contact in About/Help, changelog that shows the app is maintained, privacy policy link.
6. **Copy quality:** zero typos, consistent capitalisation and terminology (Stanford guideline 10). Errors in copy read as errors in the product.

Trust breakers (avoid absolutely): glitches/jank on first run; layout shift; lost or silently overwritten data; "Saved" lies; surprise network calls or permissions; dark patterns (§10); fake urgency/scarcity timers; ads or upsell modals in a paid tool; inconsistent visual language (looks stitched together); off-brand system dialogs in the middle of a polished flow; updates that move things without explanation.

## 7. Peak-end rule & memory

People don't remember an experience as the sum of its moments. Memory overweights the **most intense moment** and the **end**, and largely ignores **duration**.

- **Kahneman, Fredrickson, Schreiber & Redelmeier 1993**, *Psychological Science* 4(6):401–405, doi:10.1111/j.1467-9280.1993.tb00589.x (full text read): 32 male students; short trial = hand in 14 °C water 60 s; long trial = same 60 s **plus** 30 s while water warmed to ~15 °C. **22 of 32 (69%) chose to repeat the long trial**; among the 21 who felt the end ease off by ≥2 points, 17 (81%) chose it. More total pain, better memory, because of a better ending.
- **Fredrickson & Kahneman 1993**, *JPSP* 65(1):45–55, doi:10.1037/0022-3514.65.1.45: film clips; "Effects of film duration on retrospective evaluations were small"; evaluations behaved like "a weighted average of 'snapshots' … as if duration did not matter."
- **Redelmeier & Kahneman 1996**, *Pain* 66(1):3–8, doi:10.1016/0304-3959(96)02994-6: colonoscopy (n = 154) and lithotripsy (n = 133); remembered total pain correlated with peak pain and pain in the last 3 min (both p < .005); long procedures weren't remembered as worse.
- **Redelmeier, Katz & Kahneman 2003**, *Pain* 104(1–2):187–194, doi:10.1016/S0304-3959(03)00003-4 (RCT, n = 682): adding a short, milder ending lowered final-moment pain (1.7 vs 2.5/10), whole-experience unpleasantness (4.4 vs 4.9 on 10 cm VAS) and ranking (4.1 vs 4.6), and slightly raised return rates (OR 1.41, p = .038). **Note how small the memory effects are** in a real setting.
- **Meta-analysis — Alaybek, Dalal et al. 2022**, *OBHDP* 170:104149, doi:10.1016/j.obhdp.2022.104149 (abstract via RePEc): 174 effect sizes; peak-end effect on retrospective evaluations is large (r = .581, 95% CI .487–.661); **duration effect ≈ nil**; but the peak-end effect was **similar in size to the overall average** of the experience. So "peak-end beats the average" is *not* established — make the whole thing good, then invest extra at peaks and ends.
- **In HCI — Cockburn, Quinn & Gutwin 2015**, CHI pp. 357–366, doi:10.1145/2702123.2702139: two 5-page sequences with identical total work (25 sliders). Manipulating only the peak *or* only the end did **not** significantly change preference; manipulating **both together** did. Effects in UI are real but modest; don't over-engineer.

Design moves for a desktop app (my synthesis, grounded in the above):
1. **Identify the peaks** — the most intense moments: first success ("it worked!"), a big export/render/build finishing, a long-awaited sync completing, recovering lost work, and the *negative* peaks: crash, data-loss scare, payment failure. Reduce negative peaks first (they dominate memory and NN/g's delight article notes negativity bias).
2. **Design the ends** — end of onboarding, end of a long task, end of a session (quit), end of a trial, uninstall. Make each end calm and conclusive: "Export finished — 214 photos · Show in Finder"; a clean quit that confirms everything is saved; a trial-end screen that's respectful and offers export, not a hostage note.
3. **Finish long operations strong:** if a task takes time, let the final moments feel fast and clear (progress that doesn't stall at 99%, a crisp completion state, a notification if the window is in the background). Tie into the OS (Dock/taskbar progress, notification on completion).
4. **Error recovery is an "end":** after an error, the last thing the user sees should be the fix working ("Reconnected — all 3 changes synced"), not the error.
5. **Don't pad.** Duration neglect does *not* license making things slower or adding ceremony; Alaybek shows the overall average matters as much as peaks.

## 8. Delight (and calm)

**NN/g, "A Theory of User Delight"** (Therese Fessenden, 5 Mar 2017, read):
- *Surface delight* "is local and contextual; it is usually derived from largely isolated interface features" (animations, microcopy, imagery, sound). *Deep delight* "is holistic, and is achieved once all user needs are met" — users reach flow; the interface supports the task without getting in the way.
- Investing in surface delight before the foundation risks poor returns; forced humor/gimmicks "seem insincere"; slow decorative animation is cited as a delight failure. Negativity bias: bad moments are remembered more than good ones.
**NN/g, "The 3 Pillars of User Delight"** (Fessenden, 27 Nov 2022, read): visceral, behavioral, reflective (Norman's levels); "A two-legged stool cannot stand on its own"; **"You cannot impose joy"** — read the user's emotional state (playful UI during an insurance claim annoys); "the key to lasting delight is not to always look for opportunities to excite or entertain the user."

**Apple Design Awards — "Delight and Fun"** (developer.apple.com/design/awards, 2026 page, read): "memorable, engaging, and satisfying experiences enhanced by Apple technologies." Sibling categories show what Apple counts as craft: *Interaction* — "intuitive interfaces and effortless controls that are perfectly tailored to their platform"; *Visuals and Graphics* — "skillfully drawn interfaces, and high-quality animations with a distinctive and cohesive theme"; *Innovation* — "novel use of Apple technologies that sets them apart in their genre". 2026 Delight and Fun finalists include Panic's *Blippo+* (macOS). Note the formula: delight *through platform technology*, cohesive theme, tailored to platform — not delight by ignoring the platform.

**Calm technology:**
- Weiser & Brown, "Designing Calm Technology" (Xerox PARC, 21 Dec 1995, read via calmtech.com) and "The Coming Age of Calm Technology" (1996; in *Beyond Calculation*, Springer 1997, pp. 75–85, doi:10.1007/978-1-4612-0685-9_6): "Calm technology engages both the center and the periphery of our attention, and in fact moves back and forth between the two." Result: "to put us at home, in a familiar place."
- Amber Case's 8 principles (calmtech.com, read; Calm Tech Institute launched May 2024): "Technology should require the smallest possible amount of attention"; "should inform and create calm"; "should make use of the periphery"; "should amplify the best of technology and the best of humanity"; "can communicate, but doesn't need to speak"; "should work even when it fails"; "The right amount of technology is the minimum needed to solve the problem"; "should respect social norms".
- Desktop translation: status lives in the periphery (menu-bar extra / tray icon state, Dock/taskbar badge and progress, subtle title-bar or status-bar indicators) and only escalates to the centre (notification, alert) when the user must act. Notifications are rare, actionable and grouped. Graceful degradation: offline still works; sync failures don't block editing.

**Delight that respects time — rules:**
1. Foundation first: functional → reliable → usable, *then* pleasurable (Walter/NN/g). If a must-be is broken, don't ship a delighter.
2. **Frequency rule:** the more often a moment occurs, the less ornament it gets. Keyboard actions and things seen 100×/day: no decorative animation (see `motion.md` §6.1). Rare moments (first launch, first success, milestone, year-end export) can afford a flourish.
3. Never block: delight must not delay input. Any celebratory animation is interruptible, short, skippable, and respects Reduce Motion; sounds respect system mute/alert volume and are off or subtle by default for frequent events.
4. Prefer *deep* delight (it was faster/easier than expected; it remembered my context; it fixed my mistake) over *surface* delight (confetti).
5. Delight should be discoverable but not demanded: hidden niceties (option-click alternates, a thoughtful About box, a clever empty state) reward exploration without taxing everyone.
6. Refresh delighters; they decay (Kano). Today's delighter is next year's expectation.
7. Context check (NN/g "You cannot impose joy"): no jokes in errors involving data loss, money, security, health.

## 9. Personality & voice

**NN/g four tone dimensions** (Kate Moran, "The Four Dimensions of Tone of Voice", 17 Jul 2016, read): **formal ↔ casual, serious ↔ funny, respectful ↔ irreverent, matter-of-fact ↔ enthusiastic** — each a spectrum. Advice: pick a position on each; refine with "a handful" of tone words plus **anti-tone words** (e.g. authoritative, not pedantic); don't push to extremes; vary tone by context while keeping personality; tone is also carried by visual and interaction design.
**Evidence on effect** (Moran, "The Impact of Tone of Voice on Users' Brand Perception", 7 Aug 2016, read): 100 US adults, 4 pairs of near-identical text samples. "Casual, conversational, and moderately enthusiastic tones performed best" (e.g. casual bank: +0.7 friendliness, +0.3 trust, +0.4 recommend on 5-point scales). A playful insurance sample was friendlier but *less* trustworthy. Humor: mixed — "extremely risky, because when it fails, you annoy and alienate your users." **Trustworthiness explained ~52% of variance in desirability; friendliness added only ~8%** — so voice should optimise for trust first, warmth second. Effects are small (0.3–0.7 points); small sample; text-only.
**Mailchimp Content Style Guide — Voice and Tone** (styleguide.mailchimp.com, practitioner, read): voice = "plainspoken", "genuine", "translators", "Our humor is dry." "You have the same voice all the time, but your tone changes." "It's always more important to be clear than entertaining." "Forced humor can be worse than none at all." Match tone to the reader's emotional state (relieved vs confused vs upset).

Microcopy by state (one personality, tone modulated by emotional stakes):

| State | Emotional stakes | Tone setting | Example (calm/precise/warm notes app) |
|---|---|---|---|
| Empty state (first run) | Curious, low stakes | Most personality allowed | "Nothing here yet. Press ⌘N to start a note — it saves as you type." |
| Success, routine | Low | Almost silent | Status bar: "Saved" (no toast) |
| Success, peak (§7) | High positive | Warm, specific, brief | "Exported 214 notes to Markdown. Show in Finder" |
| Loading / waiting | Mild impatience | Matter-of-fact, honest | "Importing 1,240 of 3,000 notes…" |
| Error, recoverable | Anxious | Serious, specific, no jokes | "Couldn't sync — you're offline. Your edits are saved on this Mac and will sync when you reconnect." |
| Destructive confirm | High | Plain, exact consequence | "Delete 'Q3 plan'? You can restore it from Trash for 30 days." |
| Data loss / crash recovery | Very high | Calm, reassuring, factual | "We restored your unsaved changes from 2 minutes before the app quit." |

Personality must be **consistent across channels**: type (geometric vs humanist vs mono), color temperature, corner radii, icon stroke, motion character (springy vs linear vs none), copy, sound (soft click vs none), haptics (Force Touch trackpad), and even what the app *refuses* to do. Inconsistency reads as inauthentic — Walter's warning in §2. Write the persona once (§11a) and check every surface against it.

## 10. Ethics boundary: persuasion vs manipulation

Emotional design uses the same levers as manipulation (attention, affect, defaults, framing). The line: **persuasion helps users do what they already want and leaves them able to choose otherwise; manipulation benefits the maker by deceiving, pressuring, or hiding.**

- **Gray, Kou, Battles, Hoggatt & Toombs 2018**, CHI, doi:10.1145/3173574.3174108: dark patterns = where "user value is supplanted in favor of shareholder value"; corpus of 118 practitioner-identified examples (count via secondary summaries ⚠️); five strategies: **nagging, obstruction, sneaking, interface interference, forced action**. Warns designers "could easily become complicit in manipulative or unreasonably persuasive practices."
- **Mathur et al. 2019**, *Proc. ACM HCI* 3(CSCW), pp. 1–32, doi:10.1145/3359183 (abstract via OpenAlex): ~53 K product pages from ~11 K shopping sites; **1,818 dark-pattern instances, 15 types, 7 categories; 183 sites deceptive; 22 third parties selling dark patterns "as a turnkey solution."**
- **Luguri & Strahilevitz 2021**, *Journal of Legal Analysis* 13(1):43–109, doi:10.1093/jla/laaa006 (abstract read): mild dark patterns made people "more than twice as likely" to sign up for a dubious service; aggressive ones "almost four times" (≈11% control → 26% mild → 42% aggressive, per author's CPPA slides); aggressive ones caused backlash, **mild ones did not** — the dangerous ones are the subtle ones. Hidden information, trick questions, obstruction worked best; "must act now" messages did not increase purchases. Less-educated users were more susceptible.
- **FTC staff report "Bringing Dark Patterns to Light"** (15 Sep 2022): four buckets — misleading consumers/disguising ads (incl. fake countdown timers, false scarcity); making it hard to cancel; burying key terms and junk fees (drip pricing); tricking people into sharing data (privacy defaults, confusing toggles). (The separate 2024 "Click-to-Cancel" rule was vacated by the 8th Circuit on 8 Jul 2025, *Custom Communications v. FTC*; state laws like California's auto-renewal law and ROSCA still apply.)
- **EU Digital Services Act, Art. 25** (Reg. (EU) 2022/2065): providers of online platforms "shall not design, organise or operate their online interfaces in a way that deceives or manipulates" users or materially impairs free, informed decisions; Commission guidance may target giving options disproportionate visual prominence, "repeatedly requesting that the recipient … make a choice where that choice has already been made", and "making the procedure for terminating a service more difficult than subscribing to it." (Applies to online platforms; practices covered by the UCPD/GDPR are excluded from Art. 25 but regulated there. Treat it as the bar for any desktop app with accounts/subscriptions.)

Agent rules (do not cross):
1. Equal visual weight for "Accept"/"Decline", "Subscribe"/"Not now"; no confirmshaming ("No thanks, I like losing work").
2. Ask once; remember the answer (no nagging re-prompts for ratings, upgrades, notifications, telemetry).
3. Cancel/downgrade/uninstall/export as easy as sign-up; no emotional guilt walls before cancel.
4. No fake urgency/scarcity, no fake progress, no fake "someone is viewing this" social proof.
5. Privacy-protective defaults; plain-language toggles (no double negatives); state what data leaves the device.
6. No sneaking: no pre-checked add-ons, no silent trial→paid conversion without a clear reminder before the charge.
7. Delight never used to distract from a cost or consequence (no confetti on the payment screen hiding the renewal terms).
8. Test: "Would we be comfortable if the user saw exactly why we designed it this way?" If not, it's manipulation.

## 11. Agent playbook

### 11a. Personality brief: 3 adjectives + 1 anti-adjective → concrete decisions

Write this before any UI code (it's a compressed Walter design persona, §2). Each adjective must change at least one decision in each column; the anti-adjective names the failure you're most likely to drift into.

Adjective lexicon (starting points, not rules):

| Adjective | Type | Color | Motion | Copy | Sound / haptics |
|---|---|---|---|---|---|
| calm | generous line-height (1.5+), moderate sizes, few weights | low saturation, warm or neutral greys, one muted accent | few animations, ease-out 150–250 ms, no bounce | matter-of-fact, quiet; status not toasts | none by default |
| precise | strict 4/8 px grid, tabular numerals, aligned baselines | hairline separators, exact semantic colors | linear/critically-damped, no overshoot | exact numbers and names ("214 notes", not "your notes") | none, or a crisp single tick |
| warm | humanist sans or text serif for content | warm paper whites / warm darks, soft accent (terracotta, ink-blue) | soft ease, slightly longer on rare moments | second person, contractions, casual | soft, low-pitched |
| fast | compact, strong contrast, large input text | high contrast, one vivid accent for the active item | appear instantly; ≤100 ms; no entrance animation on summoned UI | terse; keyboard hints inline | optional subtle tick, off by default |
| confident | clear hierarchy, larger headings, fewer type sizes | decisive accent, solid fills for primary action | decisive, no hesitation; no spinners where optimistic UI works | declarative, no hedging ("Done." not "It looks like it may have worked") | — |
| playful | rounded or characterful display face *only* in rare moments | brighter secondary palette in illustrations/empty states | springs with slight overshoot (bounce ≈ 0.1–0.2) on rare moments only | wit in empty/onboarding states only; never in errors | optional, playful, off for frequent events |

**Worked example 1 — notes app: calm, precise, warm; anti-adjective: *cute***
- Type: content in a text serif (e.g. system serif on macOS, or a licensed text face) at 15–17 pt, line-height ~1.55; chrome in the system UI font; tabular numerals for counts/dates.
- Color: warm off-white canvas and warm near-black dark mode; one muted ink-blue accent for selection/links; no gradients; follows system accent if user prefers.
- Motion: sidebar/panel transitions 180–220 ms ease-out, no overshoot; typing, switching notes and search results: zero animation; Reduce Motion → cross-fades only.
- Copy: matter-of-fact + casual + respectful + low enthusiasm (NN/g dimensions). "Saved" in the status area; "Moved to Trash · Undo"; errors name what's safe first ("Your note is saved on this Mac.").
- Sound: none. Haptics: none.
- Icon: a tactile paper/notebook object with one precise detail (a ribbon, a ruled margin), crafted at all sizes.
- Signature moment (§11c): reopening the app puts you back exactly — same note, cursor and scroll — instantly, with a 1-line quiet confirmation the first time ("Picked up where you left off").
- Anti-*cute* guardrails: no mascot, no emoji in UI strings, no confetti, no exclamation marks.

**Worked example 2 — keyboard launcher: fast, confident, playful; anti-adjective: *noisy***
- Type: large grotesk/geometric sans in the query field (20–24 pt), compact result rows, monospace keycaps for shortcuts.
- Color: platform material panel (vibrancy/Mica/libadwaita), high-contrast text, one vivid accent only on the selected row.
- Motion: panel appears on hotkey with no entrance animation (or ≤ 100 ms fade); the selection highlight moves with a snappy spring (tiny overshoot is the *only* playful motion in daily use); results never animate in a way that delays Enter.
- Copy: casual + moderately enthusiastic, humor reserved for no-results and onboarding ("No results for 'calcualtor' — did you mean Calculator?"); terse elsewhere.
- Sound: off by default; optional soft tick.
- Signature moment: first-run hotkey setup ends with the user pressing *their* hotkey and the panel appearing instantly — the product's promise (speed) demonstrated, not described.
- Anti-*noisy* guardrails: no toasts, tips, "what's new" banners or update prompts inside the panel; notifications only for things the user started.

### 11b. "Familiar structure, distinctive details"

Rule: be prototypical where users *operate* the app; be distinctive where users *perceive* it. Evidence: low-prototypicality designs are judged less beautiful within 17–50 ms at every complexity level (Tuch et al. 2012); novelty pays only while typicality holds (Hekkert et al. 2003, MAYA); fluency → liking (Reber et al. 2004); see Jakob's law in `interaction.md` §2.7.

| Safe to make distinctive | Risky — stay conventional (platform/category norms) |
|---|---|
| Typography (content face, display moments) | Navigation structure & information architecture for the category |
| Color palette & accent, illustration style | Control behavior (buttons, checkboxes, text fields, sliders, scroll) |
| Iconography style (consistent stroke/grid) | Keyboard shortcuts (⌘/Ctrl+S, Z, F, comma for settings, etc.) |
| Motion *signature* on rare moments | Window chrome: traffic lights / caption buttons, drag regions, double-click title bar, snap layouts |
| Copy & voice | Menu bar structure and standard menu items; context menus |
| Sound design (subtle, optional) | Standard dialogs: open/save/print/permissions |
| App icon (crafted, platform-shaped) | Text editing behaviors (selection, cursor movement, IME, spell check) |
| Empty states & onboarding moment | Focus rings, tab order, accessibility semantics |
| About window, changelog, export/print output, templates | Settings window shape and location; drag-and-drop semantics |
| Loading/launch state, completion states | Notification behavior and system integration |

Gray zone (allowed only if every native behavior survives): custom title bars (must keep drag area, window controls, double-click, snap/tiling), custom-drawn controls (must keep keyboard, focus, screen-reader roles, high-contrast modes). Keep default visual complexity low (density can be a user setting) — complexity penalties are largest for older and expert users (Reinecke et al. 2013).

### 11c. One signature moment per app

A signature moment is the single, ownable instant people remember and describe to others. Criteria:
1. **Tied to the core value** (the reason the app exists), ideally at a *peak* or an *end* (§7).
2. **Deep before surface:** it demonstrates the value (speed, safety, clarity) rather than decorating it.
3. **Rare or naturally bounded**, so it doesn't grate on the 100th time; if frequent, it must be ≤ 300 ms and non-blocking.
4. **Multi-sensory but degradable:** visual + motion + copy (+ optional sound) that still works with Reduce Motion, sound off, and a screen reader.
5. **On-persona:** every element traceable to the 3 adjectives.
6. **Tested at occurrence #1 and #100** — still pleasant, or does it need to fade/shorten after first time?
Process: list peaks/ends → pick the one closest to core value → design it across channels → cut anything that delays the user.

### 11d. Trust checklist (ship-blocking)

- [ ] First window: no layout shift, no flash of unstyled/blank content, no jank, correct size/position, populated or designed empty state.
- [ ] Craft audit: grid alignment, consistent radii/strokes/icon style, no clipped/overflowing text in any language, crisp at 1×/2×, dark mode and high-contrast correct.
- [ ] Zero typos; consistent terms and capitalisation; no placeholder or lorem text.
- [ ] Autosave or explicit save that never loses work; visible but quiet saved state; undo for destructive actions; version history or Trash where feasible.
- [ ] "Saved"/"Synced" only after it's true; offline, syncing, conflict and error states named plainly with next steps.
- [ ] Errors: what happened, what's safe, what to do; no humor in high-stakes errors.
- [ ] Data transparency: where data lives, what leaves the device and why, telemetry choice, export in an open format.
- [ ] Permissions requested in context with a one-line reason; app works (degraded) if refused.
- [ ] Signed/notarised builds; real company/contact in About; changelog; privacy policy.
- [ ] Pricing/trial honest: end date shown, reminder before charge, cancel as easy as subscribe.
- [ ] No dark patterns (§10 rules 1–8); no fake urgency; no nagging; equal-weight choices.
- [ ] Interruptions: no unsolicited modals during work; notifications only for user-initiated or truly urgent events.
- [ ] Updates: never interrupt work; explain anything that moved.
- [ ] Stress moments (errors, payments, data at risk) are the *plainest* screens in the app (Norman 2002).

### 11e. Emotional QA pass (run after building, before calling it done)

1. **First 60 seconds:** launch cold; screenshot the first frame and the first 3 s — would it survive a 50 ms glance next to category leaders (prototypical? low complexity? crafted)?
2. **Peaks & ends:** walk the first success, the longest operation, an error-and-recovery, quit, trial end. Is each end calm and conclusive?
3. **Persona check:** pick 5 random surfaces (an error, empty state, settings page, About, a tooltip). Do type, color, motion, copy all express the 3 adjectives and avoid the anti-adjective?
4. **Frequency check:** list every animation/sound; anything seen daily that's decorative → remove or shorten.
5. **Ethics check:** run §10's test — would we be comfortable showing the user why each prompt/default exists?

## Unverified / open questions

- ⚠️ **Books not read directly:** Norman *Emotional Design* (2004), Walter *Designing for Emotion* (2nd ed. 2020), Jordan *Designing Pleasurable Products* (2000), Csikszentmihalyi *Flow* (1990), Amber Case *Calm Technology* (O'Reilly, ~2015). Claims rest on author excerpts (Walter ALA 2011, Norman *Interactions* 2002), publisher pages/TOCs, NN/g, and secondary summaries. Anderson: only publisher sample pages/TOC.
- ⚠️ Kurosu & Kashimura 1995: r ≈ .59 and participant count (156 vs 252 in different secondary sources) not checked against the full paper (ACM PDF blocked).
- ⚠️ Tuch, Roth et al. 2012 (CHB) and Seckler et al. 2015: findings from abstracts/highlights via search, not full text (ScienceDirect blocked).
- ⚠️ Lavie & Tractinsky 2004 "classical more related to perceived usability" — quoted via a wiki, full text not read.
- ⚠️ Hekkert et al. 2003 numbers (typicality/novelty r > .75, 56% joint variance) via search summaries only.
- ⚠️ Fogg 2003: only the 46.1% "design look" figure is verified (abstract); other category percentages and the expert-study ranking come from a secondary page.
- ⚠️ Gray et al. 2018 corpus size (118) via secondary summaries; the five strategy names are consistent across sources.
- ⚠️ Kano "life cycle of attractive quality" (delighters decaying to must-be) — Kano's later work not read; Kano 1984 DOI resolves via doi.org/JaLC, not Crossref.
- ⚠️ Moshagen & Thielsch 2013 VisAWI-S (short form) not opened.
- **Generalisation gap (open question):** almost all aesthetics/first-impression/trust evidence is from **websites, ATMs, phones and MP3 skins**, mostly young Western or East-Asian student samples, passive screenshot viewing. Nothing found that tests prototypicality or peak-end directly on **desktop productivity apps** used daily for months. Long-term use likely shifts weight from visual appeal to pragmatic quality (Hassenzahl 2004: goodness tracked usability over time; beauty stayed stable).
- **Replication notes:** "What is beautiful is usable" (Tractinsky 2000) was reversed under strong usability manipulation (Tuch et al. 2012); NN/g warns beauty only masks *minor* problems. Sonderegger & Sauer's speed benefit (147.7 s vs 198.5 s) is one study with teens. Peak-end: effects in UI are modest and needed both peak and end manipulated (Cockburn et al. 2015); meta-analysis finds peak-end ≈ overall average.
- **Cultural/age variation:** complexity and color preferences vary by age, education and country (Reinecke 2013/2014) — no universal "beautiful". Calibrate to the target audience.
- Lists of "emotional design principles" circulating online (some AI-generated) misattribute ideas to Anderson and Walter — don't trust them without the book.

## Sources

DOIs checked at api.crossref.org/works/<doi> on 2026-11-02 (all resolved; Kano's via doi.org/JaLC).

Papers
- Alaybek, B., Dalal, R. S., et al. (2022). All's well that ends (and peaks) well? A meta-analysis of the peak-end rule and duration neglect. *OBHDP* 170:104149. doi:10.1016/j.obhdp.2022.104149
- Cockburn, A., Quinn, P., & Gutwin, C. (2015). Examining the peak-end effects of subjective experience. CHI '15, 357–366. doi:10.1145/2702123.2702139
- Fogg, B. J., et al. (2003). How do users evaluate the credibility of Web sites? DUX '03, 1–15. doi:10.1145/997078.997097
- Fredrickson, B. L., & Kahneman, D. (1993). Duration neglect in retrospective evaluations of affective episodes. *JPSP* 65(1):45–55. doi:10.1037/0022-3514.65.1.45
- Gray, C. M., Kou, Y., Battles, B., Hoggatt, J., & Toombs, A. L. (2018). The dark (patterns) side of UX design. CHI '18. doi:10.1145/3173574.3174108
- Hassenzahl, M. (2004). The interplay of beauty, goodness, and usability in interactive products. *HCI* 19(4):319–349. doi:10.1207/s15327051hci1904_2
- Hassenzahl, M., Burmester, M., & Koller, F. (2003). AttrakDiff. *Mensch & Computer 2003*, 187–196. doi:10.1007/978-3-322-80058-9_19
- Hassenzahl, M., & Tractinsky, N. (2006). User experience – a research agenda. *Behaviour & IT* 25(2):91–97. doi:10.1080/01449290500330331
- Hekkert, P., Snelders, D., & van Wieringen, P. C. W. (2003). 'Most advanced, yet acceptable'. *Br. J. Psychology* 94(1):111–124. doi:10.1348/000712603762842147
- Kahneman, D., Fredrickson, B. L., Schreiber, C. A., & Redelmeier, D. A. (1993). When more pain is preferred to less. *Psychological Science* 4(6):401–405. doi:10.1111/j.1467-9280.1993.tb00589.x
- Kano, N., Seraku, N., Takahashi, F., & Tsuji, S. (1984). Attractive quality and must-be quality. *Hinshitsu* 14(2):147–156. doi:10.20684/quality.14.2_147
- Kim, J., & Moon, J. Y. (1998). Designing towards emotional usability in customer interfaces. *Interacting with Computers* 10(1):1–29. doi:10.1016/S0953-5438(97)00037-4
- Kurosu, M., & Kashimura, K. (1995). Apparent usability vs. inherent usability. CHI '95 companion, 292–293. doi:10.1145/223355.223680
- Lavie, T., & Tractinsky, N. (2004). Assessing dimensions of perceived visual aesthetics of web sites. *IJHCS* 60(3):269–298. doi:10.1016/j.ijhcs.2003.09.002
- Lindgaard, G., Fernandes, G., Dudek, C., & Brown, J. (2006). Attention web designers: You have 50 milliseconds… *Behaviour & IT* 25(2):115–126. doi:10.1080/01449290500330448
- Lindgaard, G., Dudek, C., Sen, D., Sumegi, L., & Noonan, P. (2011). Visual appeal, trustworthiness and perceived usability of homepages. *ACM TOCHI* 18(1). doi:10.1145/1959022.1959023
- Luguri, J., & Strahilevitz, L. J. (2021). Shining a light on dark patterns. *J. Legal Analysis* 13(1):43–109. doi:10.1093/jla/laaa006
- Mathur, A., et al. (2019). Dark patterns at scale. *Proc. ACM HCI* 3(CSCW):1–32. doi:10.1145/3359183
- McKnight, D. H., Choudhury, V., & Kacmar, C. (2002). Developing and validating trust measures for e-commerce. *ISR* 13(3):334–359. doi:10.1287/isre.13.3.334.81
- Moshagen, M., & Thielsch, M. T. (2010). Facets of visual aesthetics. *IJHCS* 68(10):689–709. doi:10.1016/j.ijhcs.2010.05.006 (preprint: uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/moshagen_2010.pdf)
- Norman, D. A. (2002). Emotion & design: Attractive things work better. *Interactions* 9(4):36–42. doi:10.1145/543434.543435 (jnd.org/emotion-design-attractive-things-work-better/)
- Reber, R., Schwarz, N., & Winkielman, P. (2004). Processing fluency and aesthetic pleasure. *PSPR* 8(4):364–382. doi:10.1207/s15327957pspr0804_3
- Redelmeier, D. A., & Kahneman, D. (1996). Patients' memories of painful medical treatments. *Pain* 66(1):3–8. doi:10.1016/0304-3959(96)02994-6
- Redelmeier, D. A., Katz, J., & Kahneman, D. (2003). Memories of colonoscopy: a randomized trial. *Pain* 104(1–2):187–194. doi:10.1016/S0304-3959(03)00003-4
- Reinecke, K., et al. (2013). Predicting users' first impressions of website aesthetics… CHI '13, 2049–2058. doi:10.1145/2470654.2481281 (PDF: kgajos.seas.harvard.edu/papers/reinecke13aesthetics.pdf); Reinecke & Gajos (2014) CHI, iis.seas.harvard.edu/papers/reinecke14visual.pdf
- Seckler, M., Heinz, S., Forde, S., Tuch, A. N., & Opwis, K. (2015). Trust and distrust on the web. *CHB* 45:39–50. doi:10.1016/j.chb.2014.11.064
- Sillence, E., Briggs, P., Fishwick, L., & Harris, P. (2004). Trust and mistrust of online health sites. CHI '04, 663–670. doi:10.1145/985692.985776
- Sonderegger, A., & Sauer, J. (2010). The influence of design aesthetics in usability testing. *Applied Ergonomics* 41(3):403–410. doi:10.1016/j.apergo.2009.09.002 (author PDF: sonar.ch)
- Tractinsky, N. (1997). Aesthetics and apparent usability. CHI '97, 115–122. doi:10.1145/258549.258626
- Tractinsky, N., Katz, A. S., & Ikar, D. (2000). What is beautiful is usable. *Interacting with Computers* 13(2):127–145. doi:10.1016/S0953-5438(00)00031-X
- Tuch, A. N., Roth, S. P., Hornbæk, K., Opwis, K., & Bargas-Avila, J. A. (2012). Is beautiful really usable? *CHB* 28(5):1596–1607. doi:10.1016/j.chb.2012.03.024
- Tuch, A. N., Presslaber, E. E., Stöcklin, M., Opwis, K., & Bargas-Avila, J. A. (2012). The role of visual complexity and prototypicality regarding first impression of websites. *IJHCS* 70(11):794–811. doi:10.1016/j.ijhcs.2012.06.003 (preprint: research.google.com/pubs/archive/38315.pdf)
- Weiser, M., & Brown, J. S. (1995). Designing calm technology (Xerox PARC); (1997) The coming age of calm technology, in *Beyond Calculation*, 75–85. doi:10.1007/978-1-4612-0685-9_6

Practitioner / regulatory
- NN/g: Fessenden, "A Theory of User Delight" (2017-03-05) nngroup.com/articles/theory-user-delight/ · Fessenden, "The 3 Pillars of User Delight" (2022-11-27) nngroup.com/articles/pillars-user-delight/ · Moran, "The Four Dimensions of Tone of Voice" (2016-07-17) nngroup.com/articles/tone-of-voice-dimensions/ · Moran, "The Impact of Tone of Voice on Users' Brand Perception" (2016-08-07) nngroup.com/articles/tone-voice-users/ · Moran, "The Aesthetic-Usability Effect" (2024-02-03) nngroup.com/articles/aesthetic-usability-effect/
- Walter, A., "Personality in Design", A List Apart (2011-10-18) alistapart.com/article/personality-in-design/ · abookapart.com/products/designing-for-emotion
- Anderson, S. P., *Seductive Interaction Design* sample pages: ptgmedia.pearsoncmg.com/images/9780321725523/samplepages/0321725522.pdf
- Mailchimp Content Style Guide, Voice and Tone: styleguide.mailchimp.com/voice-and-tone/
- Stanford Guidelines for Web Credibility (Fogg, 2002): credibility.stanford.edu/guidelines/
- Calm Tech principles (Amber Case): calmtech.com · Weiser & Brown 1995: calmtech.com/papers/designing-calm-technology
- Apple Design Awards 2026 categories: developer.apple.com/design/awards/
- FTC, "Bringing Dark Patterns to Light" (staff report, 2022-09-15): ftc.gov press release "FTC Report Shows Rise in Sophisticated Dark Patterns…" · 8th Cir. vacatur of Click-to-Cancel rule, *Custom Communications v. FTC* (2025-07-08), via law-firm alerts (lw.com, gtlaw.com)
- EU Digital Services Act, Reg. (EU) 2022/2065, Art. 25: eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R2065 (text read via eu-digital-services-act.com)
