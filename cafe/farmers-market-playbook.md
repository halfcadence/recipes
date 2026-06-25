# Farmers-Market Validation Playbook
### Half Cadence — first move, before any lease

*Sell canelés at a Seattle farmers market for 6–8 weekends. Answer four questions with money, not opinion: is the demand real, does the price hold, do drinks attach, is the waste survivable. This gates the whole [`plan.md`](./plan.md) thesis. Run this before signing anything.*

---

## 0. Read this first — the regulatory constraint that shapes everything

**A canelé is almost certainly a potentially hazardous (TCS) food under Washington law, which means you should plan to bake it in a permitted commercial/commissary kitchen and sell under a temporary food permit — NOT under the home-kitchen Cottage Food permit. There is a narrow, cheap path to confirm whether a home-kitchen route is open; pursue it in parallel, but do not build the plan on it.**

First, get the term right, because it's easy to misread. **"Potentially hazardous food" — now called TCS (Time/Temperature Control for Safety) — is a microbiology classification, not a freshness/quality one.** It asks one question: can pathogens (Salmonella, Staph, Listeria, botulism) grow or form toxin in the finished food at room temperature? That turns on two physical properties: **pH** (acidic? ≤ 4.6 = safe) and **water activity** (dry? aw ≤ 0.85 = safe). Hit *either* threshold and the food is automatically non-TCS. It has nothing to do with whether the item stales or "keeps for a day" — that's a separate axis.

**Why a canelé lands on the TCS side (medium confidence):**

- **RCW 69.22.010** gates the *entire* cottage-food program on the food being **non-potentially-hazardous**. That gate is decided by the finished product's pH and water activity — **not** by what product category you name it into.
- A canelé is a baked flour-egg-milk **batter** (eggs fully cooked at ~525°F), structurally a cousin of the madeleine/financier/far breton. It is near-neutral (~pH 6–7; the only acid is a splash of rum) and, by deliberate design, has a **moist, custardy interior** whose water activity is almost certainly **> 0.85, plausibly > 0.92.** Under the FDA Food Code interaction tables for heat-treated foods, pH > 4.6 **and** aw > 0.85 lands in TCS (or "Product Assessment required" — presumptively TCS until proven otherwise).
- This is exactly where the canelé differs from its drier batter-cake cousins: a madeleine or financier finishes dry enough to clear the aw bar; the canelé's signature wet interior is what fails it.

**What this corrects from earlier drafts:** a prior version shoved the canelé into WAC 16-149-130's "custard pie" prohibition. That was the wrong route. WAC 16-149-130 bars cream/custard/meringue **pies** and cakes/pastries with cream, cream-cheese, or fresh-fruit **fillings/garnishes**, plus anything with uncooked eggs. A canelé has **none** of these — no filling, no garnish, no frosting, eggs fully baked — so it is **not** squarely named in the prohibition, and WAC 16-149-120 would plausibly read it as an allowed "cake/pastry." So don't lean on the categorical "it's a custard pie" argument; it doesn't hold. The reason a canelé is still barred is the **TCS gate (moisture + near-neutral pH)**, which the category argument cannot defeat.

**What would actually settle it — proof, not intuition:**

1. **Lab water-activity test on the finished interior** (~$40/sample; pH ~$6.50). If aw ≤ 0.85, the canelé flips to non-TCS outright (pH won't help — it's near-neutral). For a moist canelé this is unlikely, which is why the working assumption is "TCS."
2. **Written WSDA determination.** WA cottage approval is discretionary and per-product: you submit the specific recipe + label, a Public Health Advisor reviews it for "low risk," and lists it on your permit (or doesn't). A favorable lab number strengthens the argument but does not bind their call. Email **cottagefoods@agr.wa.gov** / call **(360) 902-1876**; describe it honestly as a baked flour-egg-milk batter (compare to a financier/madeleine, **not** a custard pie) and ask whether they will list it.

**The safe operational route (reviewer-independent — works regardless of how the TCS question resolves): a Public Health — Seattle & King County (PHSKC) Temporary Food Establishment permit, with canelés baked in a permitted commercial/commissary kitchen — NOT a home kitchen.** This is the plan's primary path. See §1. Not a WSDA Food Processor license (that's for shelf-stable packaged goods sold wholesale/off-site — the wrong tool here).

**Pursue the cottage path in parallel, as upside only.** If WSDA lists the recipe, you gain a low-cost home-kitchen channel. If they decline or demand testing, you're already operational via the commissary and lose nothing. **Do not delay launch waiting on a cottage reclassification — realistically it won't come, and the commissary path doesn't need it.**

> **Confidence:** That a canelé is **TCS / barred from cottage food** is MEDIUM confidence — it rests on the finished interior's water activity being > 0.85, which is very likely but unproven without a lab test. The **commissary + temporary-permit path is HIGH confidence** as the safe default regardless of outcome. The permit *dollar figures* below are corrected to live PHSKC/WSDA fee schedules where confirmed and flagged as ranges where not; **call PHSKC and your target market manager to confirm current numbers and the required cold-holding plan before you commit.**

---

## 1. Regulatory path — the cheapest legal route

| Path | Legal for canelés? | Cost | Why |
|---|---|---|---|
| **Cottage Food permit** (WSDA) | **Probably not** (TCS) | **$355 / 2 yr**¹ | The canelé's moist, near-neutral interior almost certainly clears no non-TCS threshold (§0), so it's gated out of cottage food. *Cheap upside path:* a ~$40 water-activity test + a written WSDA determination could open a home-kitchen channel — pursue in parallel, don't wait on it. |
| **WSDA Food Processor license** | Wrong tool | ~$200/yr base² | For packaged, shelf-stable goods processed for off-site/wholesale sale. A canelé sold fresh at a booth is food service, regulated by the local health jurisdiction (PHSKC), not processing. |
| **King County Temporary Food Establishment permit + commissary** | **YES — this is the route** | see §2 | PHSKC permits short-term/recurring food service. Bake in a permitted kitchen, hold/transport safe, sell at the booth under the temp permit. |

**The route, in order:**

1. **Lock a permitted commissary / commercial kitchen.** You may not bake canelés for sale in a home kitchen — that route is closed (cottage food excludes the product). Rent a shared/commissary kitchen by the hour or a kitchen-share membership. PHSKC operates a **commissary locator (kingcounty.gov/commissary)** as an optional resource to help find low-cost kitchen space — it is a finder, not a permit issuer. Budget **$15–35/hr** or **$300–700/mo** for a membership (verify locally; Seattle rates vary widely, and this is often the largest single line).
2. **Get the King County Temporary Food Establishment permit.** PHSKC defines "temporary" as operating at one location with a fixed menu **for less than 21 days, OR up to 3 days/week for an approved recurring event such as a farmers market** — a weekly market qualifies (verified verbatim). Fees are **tiered by complexity, not a flat number**³: Minimal $126 single / $252 unlimited; **Moderate $315 single / $756 (5-event) / $882 unlimited; Complex $441 single / $819 (5) / $1,008 unlimited.** A cold-held TCS product like a canelé will land in **Moderate or Complex** — budget toward or above the top of the old "$200–900" estimate. Multi-event/unlimited packages also require a **Certified Booth Operator (CBO) course, ~$126.** Apply through the market's farmers-market coordinator packet; markets often coordinate vendor permits as a group.
3. **Food worker cards** for everyone handling food: **$10 each, valid 2 years** (3 years on renewal; WA state card, taken online). Confirmed.
4. **Confirm the market itself is permitted** and ask its manager which permit tier they operate under and what they require of a hot-baked, refrigeration-after-bake (TCS) vendor — including the **cold-holding plan PHSKC will require**, since canelés are TCS once baked. Some markets restrict TCS foods or require specific holding setups.

> **Cost reality:** the permit + commissary + cards is the real cost of being legal — call it **$900–2,000 over a 6–8 week test** (a TCS product lands in the Moderate/Complex permit tier and likely adds the ~$126 CBO course). This is the price of the answer. It is far cheaper than a $150k lease on an unvalidated guess.

---

## 2. Booth costs — all-in to run ~6–8 test weekends

Estimates. Confirm the starred lines (market fee, permit, commissary) with the specific market and PHSKC before paying.

| Line | Low | Expected | High | Note |
|---|---|---|---|---|
| **Market stall fee*** (per day) | $35 | $55 | $75 | Seattle markets: flat daily fee, often **+5–8% of sales** or a seasonal membership. Confirm structure. |
| Stall fee × 7 days | $245 | $385 | $525 | Plus any % of sales. |
| **Temp food permit*** (recurring/multi-event) | $315 | $756 | $1,008 | PHSKC **Moderate/Complex** tier for a TCS product (corrected from "$200–900").³ Add CBO course below if buying a 5-event/unlimited package. |
| **Certified Booth Operator course** (if 5+/unlimited package) | — | $126 | $126 | Required for multi-event/unlimited permit tiers.³ |
| **Commissary kitchen*** (6–8 wk) | $400 | $800 | $1,400 | Hourly ($15–35/hr) or short membership ($300–700/mo); ~3–5 hr bake per market day. Often the largest line. |
| Food worker cards (×2) | $20 | $20 | $20 | $10 each, valid 2 yr. Confirmed. |
| 10×10 pop-up tent (white, weighted) | $120 | $180 | $260 | Most markets require a tent + weights. |
| Tent weights (4× 25lb) | $40 | $70 | $100 | Required; wind. |
| Folding table(s) + cream cloth | $60 | $110 | $180 | |
| **Refrigeration / cold-hold** (cooler + ice, or 12V cooler) | $40 | $120 | $300 | Canelés are TCS once baked; hold cold or sell within a safe window. **Confirm the holding plan with PHSKC.** |
| Handwashing setup (5-gal jug + spigot, catch bucket, soap, towels) | $35 | $60 | $90 | **Required** at the booth. |
| Probe thermometer | $15 | $25 | $40 | Required; log temps. |
| Display (cream trays, tiered stand, glyph cards) | $60 | $120 | $220 | The riso "today" board lives here (§3). |
| Hand pour-over + batch setup (V60/Kalita, gooseneck kettle, hand grinder, batch urn, jugs) | $200 | $400 | $700 | Hand pour-over + batch only — **no Poursteady.** On-brand theater, cheap. |
| Square reader + stand | $50 | $80 | $120 | Card + tap; logs every txn (data, §5). |
| Signage / riso posters / box cards | $40 | $90 | $160 | Reprint the "today" board each week. |
| Packaging (kraft window boxes, liners, cups, sleeves, stamps) | $80 | $180 | $320 | Reuse the brand stamps; near-zero recurring. |
| Ingredients (6–8 wk, ~170/day target × 7) | $300 | $550 | $900 | ~$0.62 fully-loaded/unit × volume + drink supplies. |
| Contingency (~12%) | — | $300 | — | |
| **ALL-IN, 6–8 weekends** | **~$2,200** | **~$3,900** | **~$6,200** | One-time gear (tent, kettle, reader) carries forward to the café. |

**Bottom line: budget ~$3,900 to buy the answer.** Roughly half is reusable equipment, not sunk. Being legal — permit + CBO + commissary + cards — is ~$900–2,000 of the total, the real price of certainty.

---

## 3. The booth — the riso "today" board, made portable

The stall is a scaled-down [`plan.md`](./plan.md) §13 drop. Same glyphs, same honesty line, same sell-out ritual. The board is the menu, the marketing, and the operational truth. (See [`brand/today-board.svg`](./brand/today-board.svg) for the template.)

```
            COPPER & CREAM
            [canelé glyph]
   ─────────────────────────────────
   TODAY        sat 27 jun    sold from 9
   ─────────────────────────────────
   [▮●] chocolate    $4.25   ● ● ● ● ○ ○
   [●▮] vanilla      $4.25   ● ● ● ● ● ●
   [▮▬] milk tea     $4.50   ● ● ● ○ ○ ○
   [▲●] pour over    $5.00   hand-poured ~4 min
   ─────────────────────────────────
   TODAY ONLY
   [glyph] earl grey   $4.50  ● ● ○ ○ ○
   [glyph] matcha      $5.00  SOLD OUT  (pink strike)
   ─────────────────────────────────
   Best within hours. We sell out. Come early.
```

- **A2 cream sheet, reprinted each market morning.** Dots knocked down by hand as counts deplete; pink overprint strike at zero.
- Photograph the fresh board at open → the day's Instagram post. The market is also a brand-on-substrate test (does Fluorescent Pink survive print/sun? — [`plan.md`](./plan.md) experiment #8).
- Cap quantities visibly. **Selling out is the product.** But forecast so all-stars don't vanish before the mid-morning crowd — sell-out should read as craft, not as running short.

---

## 4. Pricing protocol — A/B test, $4.25–4.50 vs $5.00

The single highest-leverage number. A $0.50 cut plus weaker attach is most of the gap between the base and downside cases in [`plan.md`](./plan.md). Test it for real; do not guess.

**Design: two price tiers, randomized by market-day, on the all-star flavors.**

- **Tier A (low):** all-stars **$4.25**, premium/rotating **$4.50**.
- **Tier B (high):** all-stars **$5.00**, premium/rotating **$5.00**.
- **Hold drinks constant** across both tiers (pour-over $5.00, batch $3.50) so the canelé price is the only thing moving.

**Randomize / sequence to kill confounds:**

1. **Alternate tiers by market-day in a pre-drawn random order** (flip a coin per week before the season; do not let weather or mood pick). Over 6–8 weekends you get ~3–4 days per tier.
2. **If you can work two markets in one weekend, run A at one and B at the other on the same day** — same weather, same week, cleaner read. Rotate which market gets which tier across weekends to cancel location effect.
3. **Keep everything else fixed:** same open time, same flavor lineup, same board, same staffing. Only price moves.
4. **Never change price mid-day.** One tier per booth per day.

**Sample size — what makes it trustworthy:**

- You are not running a clinical trial; you are looking for a **clear, large effect**. With ~170 units/day target, **3 days per tier ≈ ~500 units per price point** — enough to see a real conversion or sell-out-time difference if one exists.
- **The decisive metric is units sold and time-to-sellout at each price, not a p-value.** If $5.00 sells through at the same volume and time as $4.25, price up. If $5.00 visibly slows the line, stretches sell-out past noon, or leaves units unsold, the market is telling you $4.25–4.50 is the number.
- **Watch the balk point:** count people who read the board, see the price, and walk. A jump in balk rate at $5.00 is the signal even if totals look similar.

**Decision rule:** open the café at the **highest tier that clears modeled volume without raising the balk rate or pushing sell-out past mid-morning.** Per the plan's honesty flag: $4.25–4.50 is the defensible open; $5.00 is earned only if sell-outs are consistent, and likely only on rotating/premium flavors.

---

## 5. Daily tracking sheet — log every market day

One row per market day. Square exports the transaction-level data; you add the rest by hand. This is the evidence file that decides go/no-go.

**Schema (columns):**

- `date` / `market` / `price_tier` (A or B)
- `weather` (temp °F, rain y/n, wind) — confounds demand, log it
- `foot_traffic` (market's headcount if published, else your tally of passers-by/hr at peak)
- `open_time` / `selltout_time` per flavor (or "unsold")
- `units_total` and `units_by_flavor` (chocolate / vanilla / milk tea / pour over / each rotating)
- `time_to_sellout_minutes` (open → last unit, per flavor and overall)
- `drinks_total` and `drinks_by_type` (espresso / hand pour-over / batch / tea)
- `drink_attach` = drinks ÷ canelé transactions (target ~0.8–1.0)
- `avg_ticket` ($ per transaction)
- `balk_count` (read board, saw price, left — tally at peak hour)
- `preorders` (if you stand up a one-page reserve form) vs walk-up share
- `waste_units` (baked, unsold, given away or tossed) and `waste_pct` = waste ÷ baked
- `rush_balk` (people who left the line because hand pour-over was slow — tests the espresso-vs-slow-bar mix)
- `notes` (what sold first, what dragged, weather/event context)

**Tally the metrics that Square can't see** (balk, foot traffic, rush-balk) with a clicker and a 15-minute peak-hour count — don't try to log all day.

---

## 6. Go / no-go thresholds — tied to the model

Lean needs the equivalent of **~170 canelé/day + ~140 drinks/day**, drink attach **~0.8–1.0**, and waste **trending under ~12%**, at a **defensible price ($4.25–4.50)**. Translate the market day to a Lean café day: a strong weekend-market day should *exceed* a weekday café day, because the market concentrates demand. Be honest about that adjustment.

**GO — start scouting a Lean lease (do NOT jump to Full):**

- Sustained sell-through near **~120–170 units/day** by the back half of the test, **without cutting price below $4.25**.
- Sell-outs land **mid-morning, not at open** (real demand, not under-baking).
- Drink attach **≥ ~0.8** across espresso + hand pour-over + batch; rush-balk low. *(If hand pour-over alone bottlenecks the line, that confirms the espresso-led bar from the revised §5 — not a no-go.)*
- Waste **trending ≤ 12%** once pre-order + drop discipline is running.
- **$5.00 holds** on at least the rotating/premium flavors without raising the balk rate.

**ITERATE — extend the test, change one variable, do not lease yet:**

- Volume in the **~70–120/day** band, or sell-through only at **$4.25 with $5.00 clearly balking**.
- Drink attach **~0.5–0.8** — workable but margin-thin; test espresso, tea, or batch-only pricing.
- Waste **stuck 12–20%** — tighten forecast, pre-orders, and caps; re-run 3–4 more weekends.
- Good units but bad weather/foot-traffic confounds → get clean weeks before deciding.

**STOP — do not sign a lease; the demand bet has failed:**

- Volume **under ~70/day** at the back half of the test even at $4.25.
- Can't move units without dropping **below $4.00** (kills the sub-15% COGS margin thesis entirely).
- Waste **persistently >20%** despite caps and pre-orders (each 5 pts ≈ ~1 pt net margin; 20%+ erases the advantage).
- Drink attach **<0.5** AND canelé volume weak → neither leg of the revenue model stands.

> The market is the cheapest "no" you will ever get. A clear STOP here saves ~$150k. A clear GO is worth far more than the ~$3,900 it cost.

---

## 7. Sequencing

- **Weeks -3 to -1:** Confirm the cottage-food exclusion is understood (it is — §0). Call PHSKC, lock a commissary, secure the temp permit (Moderate/Complex tier + CBO course if multi-event), get food worker cards, book the market(s), draw the random price-tier schedule, confirm the cold-holding plan.
- **Weeks 1–2:** Shake out the booth. Don't trust this data — it's setup noise. Fix the holding/handwashing/queue flow.
- **Weeks 3–8:** Run the A/B price test clean. Log every day (§5). Push pre-orders and the sell-out ritual.
- **After:** Score against §6. GO → tour ~700–1,000 SF 2nd-gen Cap Hill spaces ([`plan.md`](./plan.md) §3) and open **Lean**. ITERATE → one more block of weekends. STOP → keep the day job, keep the tent.

---

*Footnotes (regulatory, verified against current WA/King County sources):*
*¹ The WSDA Cottage Food permit is **$355 for two years** (covers a home-kitchen inspection and up to $35,000 gross annual sales; a failed initial inspection adds a $125 reinspection fee). The exclusion rests on the **TCS gate** (moist, near-neutral interior → aw > 0.85), not on the "custard pie" category — see §0. A lab aw test + WSDA determination could in principle open it; treat as upside, not the plan.*
*² The WSDA Food Processor license base fee (~$200/yr) was not independently confirmed; the reasoning for excluding it (it governs packaged/wholesale processing, not booth food service) stands regardless of the exact fee.*
*³ King County Temporary Food Establishment permit fees are tiered: Minimal $126 single / $252 unlimited; Moderate $315 / $756 (5) / $882 unlimited; Complex $441 / $819 (5) / $1,008 unlimited. A cold-held TCS product lands in Moderate or Complex; multi-event/unlimited packages add a ~$126 Certified Booth Operator course. The "temporary = one location, fixed menu, <21 days or up to 3 days/week for an approved recurring event such as a farmers market" definition is verified verbatim. Food worker card ($10, valid 2 years) is confirmed. Confirm exact tier, the CBO requirement, and the required cold-holding plan directly with PHSKC and the market manager before paying.*
