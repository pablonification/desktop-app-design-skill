---
type: llm
focus: trace
weight: 1
---

The fixes remove 'transition: all' and the staggered 0.6 s fade-up entrance on the stat cards (or shorten them to purposeful, short transitions on transform/opacity), and any movement that remains is covered by reduced-motion handling (prefers-reduced-motion and/or MotionConfig reducedMotion="user"); passes if no movement animations remain at all
