# Canelé — Cost of Production per Unit

**Batch:** 24 canelés (~75g each, 1815g batter), the [Big-Batch Canelé](../r/big-batch-canele.md). **Prices:** Fred Meyer / Kroger Seattle (groceries) + Amazon (vanilla, fleur de sel), mid-2026, mid-range store-brand. Low-confidence prices flagged `~?`.

## 1. Line items

| Ingredient | Qty used | Unit price | Line cost |
|---|---|---|---|
| Whole milk | 745 g | $0.00104/g | $0.78 |
| Heavy cream | 85 g | $0.0069/g | $0.59 |
| Unsalted butter | 100 g | $0.0101/g | $1.01 |
| Vanilla beans (2 pods) | 2 pods | $0.60/pod `~?` | $1.20 |
| Granulated sugar | 375 g | $0.00165/g | $0.62 |
| Fleur de sel | 4 g | $0.11/g `~?` | $0.44 |
| Eggs (2 whole + 5 yolks = 7 eggs) | 7 eggs | $0.25/egg `~?` | $1.75 |
| Aged rum | 88 g (~93.6 ml) | $0.043/ml WA out-the-door `~?` | $4.03 |
| AP flour | 185 g | $0.00132/g `~?` | $0.24 |
| Cornstarch | 33 g | $0.0044/g `~?` | $0.15 |
| **Batch total** | | | **$10.80** |

**Notes on the math**
- **Rum:** the price source is per-*milliliter*; the recipe specs 88 *grams*. At rum density ~0.94 g/ml that's ~93.6 ml → $4.03 at the WA out-the-door rate ($0.043/ml, which already includes WA's 20.5% spirits sales tax + $3.77/L liter tax). If you cost rum at its pre-tax base (~$0.030/ml), the line drops to **$2.81** and the batch to **$9.58**. WA's spirits tax alone moves the per-canelé number by ~$0.05.
- **Eggs:** all 7 eggs drawn from the carton are charged at full price ($1.75). The recipe leaves **2 whites** unused — if you reuse them (financiers, macarons), a mass-based credit is ~$0.32, netting eggs to ~$1.43 and the batch to ~$10.47. Not discounted above.
- Fleur de sel at $0.11/g is the specialty tin; swapping plain sea salt ($0.0075/g) drops that line from $0.44 to ~$0.03 — see sensitivity.

## 2. Per-canelé (ingredients)

- **Batch total: $10.80** (rum at WA out-the-door)
- **÷ 24 = ~$0.45 / canelé**
- (Rum at pre-tax base → batch $9.58 → **~$0.40 / canelé**.)

## 3. Fully-loaded per-canelé

Add nonstick baking spray at ~$0.02–0.05 per mold (≈1 g/use; cans are ~5 oz, not 170 g — negligible at batch scale):

- **~$0.47–0.48 / canelé** (ingredients + spray, rum at WA rate)

**NOT included** (see [`plan.md`](./plan.md) §6 for these): labor (loaded ~$25.56–27/hr at the $21.30 wage floor), oven gas/electric (high-heat 525°F runs are gas-heavy), copper mold wear + seasoning, packaging (kraft-window boxes, liners, riso cards), and ~10% waste. The plan rolls these into its $0.62 fully-loaded figure.

## 4. Sensitivity — what dominates

Two volatile lines drive ~half the batch cost:

1. **Rum — $4.03 (37% of batch).** The single biggest line, and the most tax-sensitive (WA spirits tax adds ~$1.20 to the line / ~$0.05 per canelé vs. base). Dropping to a floor-priced bottle (~$22 base) trims ~$0.40 off the batch (~$0.02/canelé). Small per-unit lever, largest absolute one.
2. **Eggs — $1.75 (16%).** Volatile retail prices (floor ~$2.09 to promo spikes ~$4.00/dozen swing this ±$0.50/batch). Reusing the 2 whites recovers ~$0.32.
3. **Vanilla beans — $1.20 (11%).** At $0.60/pod (medium confidence). **Switching to 16g vanilla extract** removes the bean line entirely; extract for this batch runs only ~$1–2 even at retail, so it's roughly a wash to a small saving — but flavor, not cost, should decide.

A cheaper-salt swap (fleur de sel → plain sea salt) saves ~$0.41/batch (~$0.017/canelé) on its own.

Floor scenario (base-tax rum + reused whites + plain salt): batch ≈ **$8.4**, ~**$0.35/canelé**.

## 5. Profit per canelé

Using **~$0.48/canelé** (ingredients + baking spray, WA rum, no packaging/labor/rent). This is **contribution margin** — what lands in your pocket baking at home for friends or a pop-up, where you pay no rent and no wage.

| Price | Profit/canelé | Margin | Per batch (24) |
|---|---|---|---|
| **$2.50 friends & family** | **$2.02** | 81% | **~$48** |
| **$4.00 retail** | **$3.52** | 88% | **~$84** |

- **Even the F&F price clears ~$2/canelé.** Ingredients are so cheap that a steep discount is still very profitable — the $2.50 price isn't charity, it's ~$48/batch.
- **Boxing it** subtracts ~$0.10–0.20/unit (6/dozen kraft box + liner + card) or ~$0.40–0.60 if individually windowed. A bare bag for F&F: ~$0.
- **This is NOT net business profit.** Once the model carries labor (the $21.30/hr wage floor — the biggest line), rent, and ~10% waste, net falls to the café-benchmark ~5–12% of revenue — the "profitability is a demand bet" flag in [`plan.md`](./plan.md) §9. At the home/F&F/pop-up level there's no wage or rent being paid, so contribution ≈ take-home.

## 6. Bottom line

**~$0.45/canelé in ingredients from a Seattle grocery (~$0.47–0.48 fully-loaded for spray; ~$0.40 if rum is costed pre-tax).** This lands right on the plan's assumed **~$0.44 ingredient** estimate — the recompute validates it — but sits well under the plan's **~$0.62 fully-loaded** figure, which is intentionally higher because it carries packaging + 10% waste that this ingredient-only sheet does not. At $4 retail that's ~$3.50 contribution per unit; at $2.50 F&F, ~$2.00.

---

*Confidence: milk, cream, butter, sugar are high (corroborated figures); vanilla, salt, eggs, rum, flour, cornstarch, spray are medium (estimated from ranges — Kroger/Fred Meyer block scraping). All flagged `~?` in the table. The conclusion (~$0.45/canelé) is robust to these because the high-confidence dairy/sugar lines and the dominant rum line anchor most of the cost.*
