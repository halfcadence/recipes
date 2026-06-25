# Copper & Cream — brand kit

Working brand assets for the café concept. Everything extends the recipe site's existing two-ink Risograph system — no new colors, no new fonts. See [`../plan.md`](../plan.md) for the full business + UX plan.

## Tokens (do not deviate)

| Token | Hex | Use |
|---|---|---|
| Blue | `#0078bf` | Primary ink. Wordmark, body, all small type. |
| Fluorescent Pink | `#ff48b0` | Accent ink. The `&`, fills, the sold-out strike. |
| Overprint | `#cc2464` | Blue × pink multiply. Earned by overlap — never a flat fill except for section labels / the honesty line. |
| Cream | `#fbfaf8` | The only ground. |
| Midnight | `#435060` | De-emphasized type (dates, sublines). |
| Light gray | `#88898a` | Empty dots, sold-out name. |

**Type:** Bricolage Grotesque (600) for the wordmark and headlines; monospace for everything else — prices, times, flavor names, wayfinding. (Matches the recipe site exactly.)

**Voice:** imperative, numeric, honest, no adjectives, no exclamation points. `Rest 48 hours. Bake at 525. Eat today.`

## Assets

| File | What it is |
|---|---|
| `logo.svg` | Primary wordmark — canelé-glyph colophon + "copper & cream" (blue words, pink `&`) + monospace subline. |
| `today-board.svg` | **The hero artifact.** The daily flavor board: fixed all-star band + rotating roster with a remaining-count dot grid and a pink sold-out strike. This is simultaneously the in-store board, the menu, and the day's Instagram post. Re-typeset every morning. |
| `flavor-vanilla.svg` | All-star glyph — the master mark: pink rectangle body + blue circle dome. |
| `flavor-chocolate.svg` | All-star glyph — the inverse: blue body + pink dome. |
| `flavor-milk-tea.svg` | All-star glyph — pink body + blue base band (the milk layer). |
| `flavor-pour-over.svg` | All-star glyph — blue dripper triangle + pink drip. |

The flavor glyphs are lifted directly from the recipe site's existing illustrations (`canele.svg`, `chocolate-canele.svg`, `hong-kong-milk-tea-canele.svg`, `iced-pour-over.svg`), so the café and the recipes read as one hand. New rotating flavors follow the site's illustration rules: max 2 primary shapes, blue/pink only, `viewBox="0 0 200 200"`, multiply on the overlapping shape.

## Rendering

These are riso-spec SVGs. To preview as PNG:

```
convert -density 150 -background "#fbfaf8" today-board.svg today-board.png
```

For real signage/packaging, lock `#0078bf` and `#ff48b0` to Pantone/spot equivalents and proof on actual cream stock — Fluorescent Pink drifts to muddy magenta in 4-color digital and backlit signage. Never set prices in pink alone (fails contrast on cream); use blue or overprint-dark.

## The daily ritual

1. Set today's counts → re-typeset `today-board.svg` (swap names, reset dot grids).
2. Print on cream at A2. Hang it.
3. Photograph it → that's the day's social post. Caption in the recipe voice.
4. As flavors sell out, knock down dots; at zero, strike the name in pink.
5. The board, the website `/today` page, and the counts must never disagree.
