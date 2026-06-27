# Half Cadence — brand kit

Working brand assets for the café concept. Everything extends the recipe site's existing two-ink Risograph system — no new colors, no new fonts. See [`../plan.md`](../plan.md) for the full business + UX plan and [`../site/`](../site/) for the website.

**The name.** A *half cadence* in music is a phrase that stops on the dominant chord — unresolved, hanging, pulling you toward the next. That's the daily-drop / sell-out model stated as a name: *we never resolve; come back tomorrow.* It also ties the café to the owner's existing `halfcadence` recipe site and handle, so it's one brand for free.

## Tokens (do not deviate)

| Token | Hex | Use |
|---|---|---|
| Blue | `#0078bf` | Primary ink. Wordmark words, body, all small type. |
| Fluorescent Pink | `#ff48b0` | Accent ink. The `/` caesura, fills, the sold-out strike. |
| Overprint | `#cc2464` | Blue × pink multiply. Earned by overlap — never a flat fill except for section labels / the honesty line. |
| Cream | `#fbfaf8` | The only ground. |
| Midnight | `#435060` | De-emphasized type (dates, sublines). |
| Light gray | `#88898a` | Empty dots, sold-out name. |

**Type:** Bricolage Grotesque (600) for the wordmark and headlines; monospace for everything else — prices, times, flavor names, wayfinding. (Matches the recipe site exactly.)

**Voice:** imperative, numeric, honest, no adjectives, no exclamation points. `Rest 48 hours. Bake at 525. Eat today.`

**The wordmark mechanic:** "half / cadence" — words in blue, the **`/` caesura in pink**. The slash performs the two-ink rule *and* the unresolved-phrase idea in one mark. The canelé glyph (pink rectangle body + blue circle dome) sits as a colophon beside it.

## Assets

| File | What it is |
|---|---|
| `logo.svg` | Primary horizontal wordmark — canelé-glyph colophon + "half / cadence" + monospace subline. |
| `stamp.svg` | Circular mark for the IG avatar, stickers, and the rubber stamp — glyph + stacked wordmark + `EAT TODAY`. |
| `today-board.svg` | **The hero artifact.** The daily flavor board: fixed all-star band + rotating roster with a remaining-count dot grid and a pink sold-out strike. Simultaneously the in-store board, the menu, and the day's Instagram post. Re-typeset every morning. |
| `cup-band.svg` | Wrap/sleeve band for cups — repeating canelé glyph + `POUR OVER · ~4 MIN · WORTH IT`. |
| `bag-mockup.svg` | Mockup of the kraft 4×6" single-serve bag with the two-ink stamp on the face (see [`../canele-bags`](../../a/canele-bags.md)). Idealized — a real pigment-stamp impression has more texture. |
| `bag-mockup-glassine.svg` | The gift version — translucent glassine showing the dark fluted shell, with the brand on a stamped **kraft band** (you can't stamp slick glassine directly). |
| `bag-mockup-flatbottom.svg` | A flat-bottom (SOS) kraft bag that **stands up** — box-like prism, fold-top + seal sticker, stacked wordmark on the face. |
| `bag-mockup-triangle.svg` | A flat kraft bag with the top **rolled into a triangular prism** (candy-bag fold) — stands on its bottom seam. |
| `flavor-vanilla.svg` | All-star glyph — the master mark: pink rectangle body + blue circle dome. |
| `flavor-chocolate.svg` | All-star glyph — the inverse: blue body + pink dome. |
| `flavor-milk-tea.svg` | All-star glyph — pink body + blue base band (the milk layer). |
| `flavor-pour-over.svg` | All-star glyph — blue dripper triangle + pink drip. |
| `box-label.svg` | Gift-box label — wordmark + "box of __ / flavors" fill-in + the "eat today" honesty line. |
| `eat-today-card.svg` | The card that tucks into every box: *eat today, don't refrigerate, the shell goes soft.* |
| `loyalty-card.svg` | Punch card — ten blue canelé-glyph outlines; each visit gets a pink dome stamp; the tenth is free. The stamp performs the two-ink rule every visit. |
| `gen-riso/canele-riso.png` | Nova Canvas riso print — the fluted canelé silhouette on cream, pink/blue two-ink with halftone grain. The warm, classic version. |
| `gen-riso/canele-riso-bold.png` | Same fluted canelé, pink-ground bold poster variant (blue overprint). |
| `gen-riso/cadence-bars-riso.png` | Nova Canvas abstract riso print — blue bars + pink caesura slash (the "cadence" motif). A poster/wall option. |

The flavor glyphs are lifted directly from the recipe site's existing illustrations (`canele.svg`, `chocolate-canele.svg`, `hong-kong-milk-tea-canele.svg`, `iced-pour-over.svg`), so the café and the recipes read as one hand. New rotating flavors follow the site's illustration rules: max 2 primary shapes, blue/pink only, `viewBox="0 0 200 200"`, multiply on the overlapping shape.

## Rendering

These are riso-spec SVGs. To preview as PNG:

```
convert -density 150 -background "#fbfaf8" today-board.svg today-board.png
```

For real signage/packaging, lock `#0078bf` and `#ff48b0` to Pantone/spot equivalents and proof on actual cream stock — Fluorescent Pink drifts to muddy magenta in 4-color digital and backlit signage. Never set prices in pink alone (fails contrast on cream); use blue or overprint-dark.

## The daily ritual

1. Set today's counts → re-typeset `today-board.svg` (swap names, reset dot grids), or edit the `TODAY` object in [`../site/today.html`](../site/today.html) — same data, two surfaces.
2. Print the board on cream at A2. Hang it.
3. Photograph it → that's the day's social post. Caption in the recipe voice.
4. As flavors sell out, knock down dots; at zero, strike the name in pink.
5. The printed board, the website `/today` page, and the counts must never disagree.
