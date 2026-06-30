# Experiment — start temp & steel handling (dial-in the oven, not the batter)

**Question:** with a preheated baking steel in a non-convection oven, what's the right **start temp**, and how do you handle the **second stage** so the steel's coast-down doesn't scorch the bottoms? Settles the "is 525 / 550 even needed, and do I take the pan off the steel?" thread.

**Sequencing — do this AFTER the [structure experiment](./experiment-10pct-structure.md).** Lock the batter at 12% structure first. This experiment moves *oven* variables; if you change batter and oven in the same bake you won't know which knob did what. One variable at a time.

## The physics you're testing

A charged steel is a thermal flywheel. It (1) restores the effective shock temp that a cold tray craters, so the *dial* can come down from 525, and (2) keeps radiating after you drop the dial, so the second stage runs **hotter than the dial** for a while and the bottoms can over-darken. Two knobs fall out of that:

- **Start temp** — how much shock. Steel delivers it reliably, so you likely don't need 525 (small batches work at 450). Floor is the *high regime*: you can't go low-only (350–375°F never caramelizes the crust — see [baking-steel-notes](./baking-steel-notes.md)).
- **Second-stage handling** — once the shell sets (~11 min), the steel's aggressive bottom heat is a scorch liability. Lift the tray off it, or let it coast.

## The grid (steel in, ~½″, preheated 45–60 min)

Bake small sets (3–6 molds) so you can run several arms cheaply. Hold everything else fixed: same rested batter, 75g fill, fridge-cold, ~11-min shock, second stage 350°F (see below), rotate once late.

### Part A — start temp ladder

All arms drop to **350°F** for the second stage (the Perfect Loaf canelé-on-steel number) — *not* 375–400. Reasoning: the steel coasts hot after the temp drop, so a lower set point counteracts it; 350 + hot-coasting-steel ≈ the old 375–400 + a non-coasting oven, and it's the documented steel profile. The start temp is the variable here.

| Arm | Profile | Watching for |
|---|---|---|
| A1 | **525 → 350** (current shock, lower 2nd stage) | baseline — darkest shell, known-good shock |
| A2 | **500 → 350** | shell still dark? mushroom still controlled? |
| A3 | **475 → 350** | the likely steel sweet spot — enough shock, gentler |
| A4 | **450 → 350** | the full Perfect-Loaf profile — does a *full custardy tray* still brown dark + set here? |

**Judge on, in order:** (1) does it mushroom / cul-blanc? (2) is the shell a deep mahogany, or going pale/blonde — **on the top and sides, not just the bottom** (the steel browns the base; in a fanless oven the top/sides only see the dial-temp air, so they're where a too-low start shows up first)? (3) interior set. Stop going lower at the arm where the *top* shell turns pale or mushrooming returns.

*Hypothesis: ~475–500 → 350 is the sweet spot. 450→350 is the documented profile and may well work — but The Perfect Loaf is a different (likely firmer) batter and setup; our custardy, low-structure batter is the most mushroom-prone and wants a touch more shock, and a full 24-mold fanless tray lags the top/sides more than their bake did. So test 450 rather than adopt it on faith — if it browns dark on top at full tray, take it (gentlest, least-scorchy, most hands-off); if it's blonde on top, step up.*

### Part B — second-stage handling (run at your Part-A winner temp)

**Default to leaving the tray on the steel the whole bake — that's how real canelé-on-steel recipes work** (The Perfect Loaf bakes directly on the steel start to finish, 450→350°F, never lifts it). Opening the door to relocate a tray mid-bake fights the whole point of the steel (heat recovery in a fanless oven), and moving up toward the top element risks over-browning the *top*. And a too-dark *bottom* is forgiving on a canelé — it wants a dark crust anyway — so the scorch risk is smaller here than on a cookie. So test the no-fuss options first; only reach for lifting if bottoms actually come out **burnt** (not merely dark).

| Arm | After the ~11-min shock | Watching for |
|---|---|---|
| B1 *(default)* | Tray **stays on the steel**, drop to **350°F**, let the steel coast (don't reheat) | bottoms dark-but-fine, or actually burnt? |
| B2 | Stays on steel, drop to 350°F, **second sheet pan slid under the tray** as a buffer | does the buffer alone tame the bottom? (no door-shuffle) |
| B3 *(only if B1/B2 burn)* | Tray **lifted one rack up, off the steel** | bottoms even now — but did the top over-brown / did the open door cost you? |

**Judge on:** is the bottom *burnt* (bitter, hard) or just dark (fine — a canelé wants dark)? Only escalate B1 → B2 → B3 if the previous arm actually scorches. Most likely **B1 is enough** — coasting at 350 is the whole fix. *Hypothesis: B1 wins; the lift is a remedy you probably never need.*

## What you're NOT changing

- **Don't shorten the 11-min shock** as a knob here — that time is about *when the shell sets*, and it's harder to judge than temp or tray position. Hold it fixed; move temperature (Part A) and tray position (Part B) instead.
- **Don't run 550 with a steel** — that's double-compensation and scorches. 550 is the *no-steel* number only.

## Logging

| Arm | Start °F | 2nd stage | On/off steel | Mushroom? | Shell color (pale→mahogany 1–5) | Bottom vs sides (even? darker?) | Interior set | Notes |
|---|---|---|---|---|---|---|---|---|
| A1 | 525 | 350 | on | | | | | |
| A2 | 500 | 350 | on | | | | | |
| A3 | 475 | 350 | on | | | | | |
| A4 | 450 | 350 | on | | | | | |
| B1 | (winner) | 350, coasting | on | | | | | |
| B2 | (winner) | 350, coasting | on + buffer pan | | | | | |
| B3 | (winner) | 350 | lifted off | | | | | |

Photograph bottoms + a cut interior per arm; bottom scorch and shell color are hard to score from memory.

## Likely landing (the hypothesis to beat)

**Steel in, tray on it the whole bake: start ~475–500°F → at ~11 min, drop to 350°F and let the steel coast (never reheat) → finish.** (450→350 is the documented Perfect-Loaf profile and may work outright — test it as arm A4; step up to 475–500 only if the top shell comes out blonde.) No door-shuffle, no lifting — that's how real canelé-on-steel recipes run, and a dark bottom is on-brand for a canelé. Only add a buffer pan, or lift the tray, if bottoms come out genuinely *burnt*. Your oven + steel mass set the exact numbers — this experiment finds them; don't trust a generic recipe number over your own logged result.

---

*Cross-refs: [`../r/big-batch-canele.md`](../r/big-batch-canele.md) (the oven notes this dials in), [`baking-steel-notes.md`](./baking-steel-notes.md) (why the steel coasts hot + the caramelization floor), [`experiment-10pct-structure.md`](./experiment-10pct-structure.md) (do that first — one variable at a time).*
