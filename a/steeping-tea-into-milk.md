---
title: Steeping Tea into Milk
category: articles
permalink: /a/steeping-tea-into-milk
---

How to infuse tea (or coffee, or spices) into the liquid of a recipe without throwing off its ratios — and why the fix scales to any batch size.

## The problem

When you steep tea directly in the milk a recipe calls for, the leaves drink some of it. Strain them out and you're left with *less* milk than you started with — and a batter that's now short on liquid, which in something ratio-sensitive like a canelé means a thicker, drier crumb. The flavor's there, but the math has quietly shifted.

The naive fix — "just add a splash more milk to make up for it" — works, but only if you guess the loss correctly. Guess low and the batter's still tight; guess high and you've diluted everything.

## How much does tea actually absorb?

Less settled than you'd hope. There's no clean published figure for tea-leaf liquid retention. The closest documented anchors are adjacent:

| | Liquid retained per gram dry |
|---|---|
| Brewing grain (malt) | ~1× |
| Spent coffee grounds | ~2× |
| Tea leaves | ~2–4× (estimate) |

Tea leaves are lighter and more porous than coffee grounds and expand more as they rehydrate, so they hold proportionally more. But the spread is wide and depends on the cut:

- **Broken, CTC, or bagged tea** sits on the low end, ~2–3×.
- **Large whole leaf** can reach ~4× because it unfurls and traps more liquid.

So for 14g of loose Earl Grey, expect to lose roughly 30–55g of milk. The honest answer is you can't pin it to a single number — which is exactly why the method below doesn't rely on one.

## The fix: steep, then measure back

Instead of guessing the loss, **start with extra liquid and measure back to your target after straining.**

1. Decide the liquid your recipe actually needs (the *target*).
2. Start with more than that — enough to cover the worst-case absorption.
3. Steep the tea in it, then strain the leaves out.
4. Weigh the strained liquid and measure out exactly the target amount. Top up with fresh milk if you came up short.

Now absorption can't hurt you. If the leaves drank 40g or 55g, it doesn't matter — you weigh what's left and take exactly what the recipe wants. The exact absorption rate stops being something you have to know and becomes something you simply absorb (so to speak) into the buffer.

How much extra to start with:

```
start = target + (k × tea weight)
```

Use **k ≈ 4** as a safe buffer. Worst case you have a little extra to discard; that's fine. The only failure mode is starting with too little and not having enough to reach the target — so err high.

## Why it scales to any batch size

This is the nice part: the buffer is *proportional*, so it carries to a bigger batch unchanged.

To keep flavor constant across batch sizes, you scale the tea with the liquid — the tea is always the same fraction `r` of the target liquid. And absorption is `k × tea weight`. Put those together and the starting liquid is:

```
start = target × (1 + k × r)
```

That multiplier `(1 + k × r)` has no batch size in it. It depends only on how strong you steep (`r`) and how much the leaves drink (`k`). Make 12 canelés or 24 or 200 — you start with the same proportional excess every time.

**Worked example — single vs big batch:**

| | Target milk | Tea | Buffer (4×) | Start with | Then measure back to |
|---|---|---|---|---|---|
| 12-mold | 340g | 14g | ~56g | ~400g | 340g |
| 24-mold | 745g | ~31g | ~124g | ~870g | 745g |

Same ratio, same flavor strength, same method. The big batch just has bigger numbers — you steep ~31g of leaf in ~870g of milk, strain, and measure 745g back out.

## What tea to use

Here's the freeing part: for baking, **cheap tea is the right tea.** You're burying the leaf under sugar, milk, and a caramelized shell, so nuance is wasted — what you want is a brisk, tannic, assertive black tea that reads through everything else. The qualities that make a tea "low grade" for sipping are exactly what you want here:

- **Broken leaf, fannings, and dust** — the small bits inside ordinary tea bags — have more surface area, so they extract faster and stronger. That bold, slightly bitter punch is what survives the oven.
- **Bagged supermarket black is fine.** Just slit open a few bags and weigh the loose leaf. Lipton, Tetley, Twinings, Red Rose — all work.
- **Don't waste good tea.** Fine first-flush Darjeeling, single-estate anything, delicate greens — their subtlety vanishes in baking. Save those for the cup.
- **Skip cheap flavored blacks.** Bargain "vanilla" or "tropical" blacks lean on synthetic oils that can taste chemical. Plain black is safer; add your own flavor.

For **Hong Kong milk tea**, Ceylon is the undisputed backbone — practically every authentic recipe agrees. But cafés (cha chaan teng) rarely use a single tea; they brew a proprietary blend of grades for body, color, and aroma. The common homemade approximation is **Ceylon plus a plain Lipton-style black, roughly 1:1** — Ceylon for bold flavor and aroma, Lipton for mellow consistency — often with some orange pekoe and broken grades for fast, strong extraction and deep reddish color. Steep it hard and astringent; that bite is the signature.

Practical picks:

- [Lipton Yellow Label loose black](https://www.amazon.com/Lipton-Yellow-Label-Tea-loose/dp/4639725043) — the classic HK-blend workhorse.
- [Harney & Sons Orange Pekoe (Ceylon & India blend)](https://www.amazon.com/Harney-Sons-Orange-Pekoe-Ceylon/dp/B08X14VF1L) — a good single bag of brisk loose leaf.
- [Moon Tea 100% Ceylon loose leaf](https://www.amazon.com/MOON-TEA-Traditional-Premium-Ceylon/dp/B0DTKPD1TZ) — marketed for milk and bubble tea.
- [Twinings Ceylon tea bags](https://www.amazon.com/Twinings-Individually-Refreshing-Caffeinated-Packaging/dp/B003TQ780C) — proof that bags are perfectly fine; just open and weigh.

## Beyond tea

The same steep-and-measure-back approach works for anything you infuse into a recipe's liquid:

- **Coffee / espresso** steeped or bloomed into milk or cream (`k` ≈ 2).
- **Whole spices** — cardamom, cinnamon, star anise — simmered and strained.
- **Fresh herbs and aromatics** — bay, lemongrass, thyme — which can hold a surprising amount of liquid for their weight.

In every case: start over, steep, strain, weigh, and measure back to the amount the recipe needs. You get the flavor of a long infusion with none of the ratio drift.

This is the method used in the [Earl Grey]({{ '/r/earl-grey-canele' | relative_url }}), [Hong Kong Milk Tea]({{ '/r/hong-kong-milk-tea-canele' | relative_url }}), and [Thai Tea]({{ '/r/thai-tea-canele' | relative_url }}) canelés.

## Sources

- [Tea Epicure — Kinetics of Steeping Tea](https://teaepicure.com/kinetics-of-steeping-tea/)
- [Home Brewing Stack Exchange — water loss to grain absorption](https://homebrew.stackexchange.com/questions/16160/how-can-i-stop-losing-so-much-water-during-brew)
