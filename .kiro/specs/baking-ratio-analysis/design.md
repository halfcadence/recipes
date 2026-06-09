# Design Document

## Overview

This feature adds a styled "Analysis" section to baking recipe pages that breaks each recipe down into functional components (fat, sugar, structure solids, liquid, egg/protein) as a percentage of total batter/dough weight, with a benchmark comparison and a plain-language takeaway. The intent is pedagogical: reading these sections across recipes teaches how ratio shifts drive texture.

The design reuses existing assets rather than inventing new machinery:
- **`batter-analysis` skill** stays the single source of truth for ingredient decomposition values and texture benchmarks.
- **Recipe markdown** carries the analysis content authored per-recipe (the numbers are computed once and written into the page; there is no runtime calculation engine).
- **Site SCSS theme** provides the styling tokens; we add one styled block, mirroring the existing `.notes` pattern.
- **Steering + checklist** are updated so the convention is documented and enforced going forward.

The key design decision: the Analysis section is **authored static content** (a markdown block in each recipe), computed by following the skill's rules — not a Jekyll plugin or JS calculator. This matches how the site already works (everything is hand-authored markdown rendered by Jekyll/minima) and keeps the build simple, while the skill guarantees the numbers are produced consistently.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ batter-analysis skill (.kiro/skills/batter-analysis.md)       │
│  • ingredient decomposition table  ← SINGLE SOURCE OF TRUTH   │
│  • texture benchmarks by baked-good type                      │
│  • output format + correctness rules                          │
└───────────────┬───────────────────────────────────────────────┘
                │ (rules followed when authoring)
                ▼
┌─────────────────────────────────────────────────────────────┐
│ Recipe page  r/<slug>.md                                       │
│   ## Ingredients   (existing table — the input data)           │
│   ## Steps         (existing)                                  │
│   ## Analysis      (NEW styled block: component table +        │
│                     benchmark compare + takeaway)              │
│   ## Notes         (existing)                                  │
└───────────────┬───────────────────────────────────────────────┘
                │ rendered by
                ▼
┌─────────────────────────────────────────────────────────────┐
│ Jekyll build  →  styled via assets/main.scss (.analysis block)│
│   light/dark/print aware, uses existing theme tokens          │
└─────────────────────────────────────────────────────────────┘
                ▲
                │ documented + enforced by
┌─────────────────────────────────────────────────────────────┐
│ steering.md  →  baking-recipe convention + New Recipe Checklist│
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Analysis block markup (in recipe markdown)

A new section authored between Steps and Notes, wrapped in a styled div so it reads as distinct from instructions. It mirrors the existing `<div class="notes" markdown="1">` pattern.

```markdown
## Analysis

<div class="analysis" markdown="1">

Total batter weight: **856g**

| Component | Amount | % |
|---|---|---|
| Structure solids (flour + starch) | 100g | 11.7% |
| Fat (butter + cream + yolk fat) | 78g | 9.1% |
| Sugar | 170g | 19.9% |
| Liquid (milk + cream water + rum + egg water) | 486g | 56.8% |
| Egg/protein | 22g | 2.6% |

**Custardy vs cakey:** structure at ~12% sits in the custardy range (8–14%); fat at ~9% keeps it rich. Reducing flour further trades cleaner unmolding for a softer set.

</div>
```

Rationale for placement (Steps → Analysis → Notes): the analysis is reference/teaching content that a reader consults after understanding the recipe but it's more structured than the prose Notes, so it sits just above them. This is a fixed convention (Req 4.1).

### 2. `.analysis` SCSS styling

Add a styled block to `assets/main.scss` parallel to `.notes`. It MUST:
- Use existing theme tokens (section color, Midnight text, paper background) — no new arbitrary grays/colors (Req 4.4).
- Be de-emphasized relative to Steps but distinct from Notes (e.g. a thin left rule or tint in the section color, or a labeled header) so the two read differently.
- Render correctly in light mode, dark mode (Midnight-derived), and print (Req 4.5).
- Keep the component table readable on narrow screens.

Approach: reuse the table styling already applied to recipe tables; wrap the block with a subtle background tint or top/bottom rule keyed off the active section color variable. Dark mode handled by the existing themed mixins so no separate color list is introduced.

### 3. `batter-analysis` skill (extended, source of truth)

Already contains the decomposition table, benchmarks, output format, and correctness rules. Changes needed:
- Add an explicit subsection describing the **on-page Analysis block** format (the markdown above), so authoring a recipe's section is deterministic.
- Add any missing ingredient decompositions encountered during rollout before use (Req 2.6) — e.g. glutinous rice flour and white/brown sugar blends for butter mochi; eggs-as-leavening note for clafoutis.
- Keep decomposition values identical to what recipe pages display (Req 3.1–3.3).

### 4. Steering convention + checklist

`steering.md` updates:
- New subsection "Analysis (baking recipes)" under recipe conventions: defines what qualifies as a baking recipe, the fixed placement, the internal structure (table → benchmark compare → takeaway), one-decimal display, and a pointer to the skill as source of truth.
- Extend the **New Recipe Checklist**: add a step "For baking recipes (batter/dough), add an `## Analysis` section computed via the batter-analysis skill."

### 5. Rollout tracking

A simple tracking list (in the tasks doc and/or a checklist note in steering) of qualifying recipes and their analysis status. No code artifact required; sequencing is canelés → cookies/shortbread → clafoutis/mochi → cakes/chiffon/brownies (Req 5.5).

## Data Models

### Qualifying-recipe rule

A recipe qualifies for an Analysis section when ALL hold:
- `category: sweets` (or a future baked category), AND
- it is a batter or dough that is **baked or set** (canelé, cake, cookie, brownie, chiffon, quick bread, clafoutis, mochi), AND
- it is NOT a no-bake/assembled sweet (jelly, panna cotta, affogato, drinks).

Disqualifying examples on the current site: coffee jelly, tea jelly, matcha affogato, bay leaf panna cotta, salted caramel sauce, strawberry milk (no-bake / non-batter / drinks).

Borderline-but-included (analyzed via their primary batter/custard component): purin (custard base), tarte-tatin (the batter/caramel-set, or noted as pastry-led), french-silk-pie (filling). For these, the Analysis labels which component is analyzed.

Qualifying examples (initial inventory):
- Canelés: canele, custardy-canele, chocolate-canele, chocolate-canele-ferrandi, white-chocolate-matcha-canele, white-chocolate-matcha-canele-ferrandi, eggnog-canele
- Cookies/shortbread: double-chocolate-chip-cookies, matcha-white-choco-cookies, brown-butter-hojicha-cookies, matcha-shortbread, matcha-latte-cookies, vietnamese-coffee-marble-cookies
- Brownies: chocolate-brownies, matcha-brownies
- Cakes/chiffon: chocolate-gateau-au-chocolat, matcha-gateau-au-chocolat, orange-chocolate-gateau-au-chocolat, hojicha-gateau-au-chocolat, vanilla-bean-gateau-au-chocolat, earl-grey-chiffon-cake, matcha-chiffon-cake
- Other batter / custard / pastry: cherry-clafoutis, crispy-butter-mochi, purin (custard base), tarte-tatin, french-silk-pie (filling)

### Component model (per recipe)

Computed by the skill's rules, expressed as:

```
total_batter_weight = Σ incorporated ingredient grams
component[fat|sugar|structure|liquid|protein] = Σ decomposed contributions
percent[c] = component[c] / total_batter_weight   (display 1 decimal)
```

Excluded from total: beeswax (mold coat), dusting/finishing sugar not in the batter (Req glossary / 6.2).

## Error Handling

- **Missing decomposition**: if a recipe contains an ingredient absent from the skill table, the skill table MUST be extended first (Req 2.6). The analysis is not authored with a guessed value.
- **Sum mismatch**: component grams must sum within tolerance of total batter weight, and percentages to ~100% (Req 6.1–6.2). If they don't, the decomposition or arithmetic is wrong and must be corrected before publishing.
- **Out-of-benchmark component**: not an error — the takeaway must explicitly acknowledge it (Req 6.3).
- **Build failure**: Jekyll build must pass after each batch (Req 6.4); malformed tables or div wrappers are caught here.
- **Excluded-item ambiguity**: items like dusting sugar or beeswax are excluded from the denominator and that exclusion is implicit in the stated total; where a finishing component is significant (e.g. sugar coating on marble cookies), note whether it's counted.

## Correctness Properties

These are invariants every published Analysis section must satisfy. They are the formal specification the rollout is verified against (see Testing Strategy for how each is checked).

### Property 1: Mass conservation
For any recipe, the sum of component gram amounts equals the stated total batter weight within rounding tolerance (±2g). `Σ component_grams ≈ total_batter_weight`.

**Validates: Requirements 6.1**

### Property 2: Percentage closure
The displayed component percentages sum to approximately 100% (within rounding tolerance), accounting for any explicitly excluded finishing items. `Σ percent[c] ≈ 100%`.

**Validates: Requirements 6.2**

### Property 3: Single denominator
Within one recipe, every component percentage uses the same `total_batter_weight` denominator.

**Validates: Requirements 1.3, 2.4**

### Property 4: Decomposition determinism
The same ingredient at the same weight decomposes to identical component contributions across all recipes (a pure function of ingredient + weight, defined by the skill table).

**Validates: Requirements 2.1, 2.3, 3.1, 3.2**

### Property 5: Non-negativity
Every component gram amount and percentage is ≥ 0; no component is double-counted across categories.

**Validates: Requirements 2.1, 6.1**

### Property 6: Display precision
Percentages are displayed to exactly one decimal place, regardless of internal precision.

**Validates: Requirements 2.5, 4.3**

### Property 7: Benchmark honesty
If any key component falls outside its benchmark range for the recipe's baked-good type, the takeaway explicitly acknowledges it (no silently ignored out-of-range value).

**Validates: Requirements 1.5, 6.3**

### Property 8: Exclusion consistency
Non-incorporated items (beeswax, dusting sugar) are excluded from the denominator consistently, and any significant finishing component (e.g. sugar coating) is either counted or explicitly noted as excluded.

**Validates: Requirements 6.2**

### Property 9: Eligibility soundness
An Analysis section exists if and only if the recipe satisfies the qualifying-recipe rule (no analysis on drinks/sauces/no-bake; analysis present on every qualifying baked batter/dough).

**Validates: Requirements 1.1, 1.6, 5.1, 5.2**

### Property 10: Build safety
After any Analysis section is added or edited, the Jekyll build succeeds with the section rendering as valid HTML.

**Validates: Requirements 6.4**

## Testing Strategy

Since this is authored static content rendered by Jekyll, "testing" is verification rather than unit tests:

1. **Arithmetic check (per recipe)**: confirm component grams sum to the stated total (±~2g rounding) and percentages sum to ~100% (Req 6.1, 6.2). This is the primary correctness gate.
2. **Decomposition consistency check**: spot-check that a shared ingredient (e.g. whole egg = ~5g fat / 38g water / 6g protein) is decomposed identically across recipes (Req 2.3).
3. **Benchmark cross-check**: confirm the takeaway's texture claim matches where the numbers fall in the skill's benchmark table, including acknowledging out-of-range components (Req 1.5, 6.3).
4. **Build check**: run the Jekyll build after each batch; confirm no Liquid/markdown errors and tables render (Req 6.4).
5. **Visual check**: verify the `.analysis` block renders distinctly in light mode, dark mode, and print, and that the table is readable on a narrow viewport (Req 4.4, 4.5).
6. **Regression on edit**: when a recipe's ingredient weights change later, re-run the arithmetic check and update the section (Req 5.3).

A lightweight reusable aid: a small throwaway script MAY be used during rollout to sum a pasted component breakdown and verify the totals, but it is not a shipped artifact.

## Open Decisions / Sequencing

- Start the rollout with the canelé family (already analyzed in the ratio article, lowest risk, highest payoff for the teaching goal), validate the styling and format on those, then expand to cookies, then cakes/chiffon/brownies, then misc batters.
- **Decided — coatings/glazes do not count toward the batter total.** Sugar coatings, glazes, frostings, and dustings are finishing components excluded from `total_batter_weight`. They are noted (not folded into the batter %) so the denominator stays the actual batter/dough. Where a frosting is itself substantial (e.g. matcha latte cookies' ermine frosting), it MAY get its own small breakdown labeled separately, but it never enters the cookie/cake batter denominator.
- **Decided — borderline items are analyzed.** `purin` (set custard), `tarte-tatin`, and `french-silk-pie` qualify for an Analysis section. For composite desserts, analyze the primary batter/custard component and label which component is being analyzed (e.g. "Custard base" for purin, "Filling" for French silk). These are added to the rollout (Batch 4) rather than excluded.
