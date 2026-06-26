# Experiment — structure % × cornstarch (custardier, still sets)

**Two questions, one bake:**
1. The custardy canelé sits at **12.2% structure** (flour + cornstarch as % of batter). Will **10%** bake up custardier and still set + unmold cleanly?
2. **Does it even need the cornstarch?** Traditional canelés are *all flour* — no starch. This recipe swaps ~15% of the flour for cornstarch to soften the crumb. Is that worth it, or do you prefer the classic all-flour chew?

Both questions are the *same lever*: how much gluten-forming structure is in the batter. Flour brings gluten (chew, set); cornstarch brings set *without* gluten (tender). So test them together as a 2×2 rather than guessing twice.

**Short answer from the math:** 10% should work. The [`batter-analysis`](../.kiro/skills/batter-analysis.md) skill puts the custardy sweet spot at **8–14% structure**, collapse risk only **below 7%**. So 10% is comfortably in-range — softer than now, with margin before it won't release. The recipe's "12% is about as custardy as you can go" note is conservative.

## The cornstarch question

Classic Bordeaux canelé = flour, milk, butter, sugar, egg, vanilla, rum. **No cornstarch.** This repo's "custardy" version adds it deliberately: cornstarch has no gluten, so replacing ~15% of the flour lowers the gluten that toughens the crumb → softer, more pudding-like interior. It's a modern tweak toward custardy, not the canon. Whether you *want* it is a taste call — which is exactly what the all-flour arms below settle.

## The lever: structure % (rows) × starch type (columns)

## The four arms (single batch, 821g, 12 molds — cheaper to test first)

Everything except flour/cornstarch stays identical (340g infused milk, 38g cream, 45g butter, 170g sugar, eggs, rum, vanilla). Each arm needs ~3 molds, so one 12-mold batch covers all four.

| Arm | Flour | Cornstarch | Structure % | Tests |
|---|---|---|---|---|
| **A — control** | 85g | 15g | 12.2% | today's custardy recipe |
| **B — low, hold starch** | 65g | 15g | 10.0% | *custardier, cornstarch held* (the softest bet) |
| **C — all-flour, traditional** | 100g | 0g | 12.2% | the classic chew — *do you even want cornstarch?* |
| **D — all-flour, low** | 80g | 0g | 10.0% | traditional texture, less of it |

Reading the grid: **A vs C** answers the cornstarch question at equal structure. **A vs B** answers the 10% question with cornstarch. **C vs D** answers it without. B is the most custardy, C is the most traditional.

> **Big-batch equivalents (1815g, 24 molds)** if you'd rather scale one winner later: A = 185g flour / 33g cornstarch; B = 144g / 33g; C = 218g / 0g; D = 177g / 0g.

## How to run it

Bake all four arms on the **same tray, same bake** to kill oven variance — that's the whole point of a side-by-side.

1. Make one base batch through the milk/egg/sugar/rum stage. **Split the wet base into 4 equal portions** *before* adding flour (weigh them — ~same grams each).
2. Into each portion, whisk its arm's flour + cornstarch from the table (scale to ¼ batch: e.g. Arm A = ~21g flour + ~4g cornstarch per quarter). Strain each.
3. Rest all four the same 24–48h, labeled.
4. Fill 3 molds per arm at the same weight (70g). **Map which mold position is which arm** (photo the tray).
5. Bake 525°F / 11 min → 375°F / 50–55 min. Don't open the oven.
6. Unmold immediately. **Make-or-break: do B and D (the 10% arms) release cleanly, or slump/tear?**

## What to watch + likely outcomes

| Signal | Likely at 10% | What it means |
|---|---|---|
| **Unmolding** | Should still release; may be slightly more delicate | If it tears or won't hold shape → 10% is your floor; back off toward 11% |
| **Interior** | More open, wetter, more pudding-like custard | The goal — confirms custardier |
| **Crust** | Same dark shell (sugar/heat-driven, not flour) | Structure doesn't set the crust, so it shouldn't change |
| **Mushrooming/collapse** | Low risk at 10%, but a thinner batter sets slower | If it mushrooms then flattens → the shell set too slow; keep the 525°F shock hot, don't open the oven |
| **Slumping after unmold** | The real risk — sags as it cools | If so, the interior never set enough → 10% too low *for your oven*, or hold the shock longer |

Also taste **A vs C** for the cornstarch verdict: does the cornstarch's tenderness read as *better*, or just *softer*? If C (all-flour) tastes more like the canelé you want, drop the cornstarch — simpler pantry, simpler batter, and more traditional.

**Compensations if a 10% arm is too soft to unmold:**
- Bump that arm back to **11%** (single: 73g flour, cornstarch held; or 90g all-flour) — splits the difference.
- Or keep 10% but **extend the second stage 3–5 min** / push to **385–400°F** to drive more set without adding flour.
- The recipe's existing fallback — "if too soft to unmold, bump flour to 100g" — goes the opposite way; this experiment deliberately probes lower, so expect to land in **10–11%** as your custardy floor.

## After the bake

- If **B holds** (10%, cornstarch): update the [Canelé](../r/canele.md) analysis to note 10% as a viable custardier target, maybe spin an "extra-custardy" variant.
- If you prefer **C** (all-flour): that's a real finding — drop the cornstarch from the base recipe and note the traditional texture is the house style.
- If the 10% arms slump but 11% holds: you've pinned the practical floor for *your* oven and molds (which run hotter/cooler than any published number) — more useful than any recipe's generic advice.

Log which mold position was which arm + a photo of the cut interiors, so the result is reproducible.

---

*Basis: [`canele.md`](../r/canele.md) (821g, 12.2% structure), [`big-batch-canele.md`](../r/big-batch-canele.md) (1815g, 12.0%), and the custardy/cakey/collapse thresholds in `.kiro/skills/batter-analysis.md` (custardy 8–14%, collapse <7%). "Cornstarch sets without gluten" and the traditional all-flour formula are from the canelé recipe's own notes + the classic Bordeaux canelé.*
