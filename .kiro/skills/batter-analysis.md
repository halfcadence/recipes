---
name: batter-analysis
description: Analyze a batter or dough recipe by breaking down ingredients into functional components (fat, sugar, structure, liquid, protein). Use when diagnosing texture problems, comparing recipes, or adapting a recipe with substitutions.
triggers:
  - "analyze batter"
  - "batter analysis"
  - "ratio analysis"
  - "why is it cakey"
  - "why is it too soft"
  - "compare recipes"
  - "diagnose recipe"
  - "percentage breakdown"
---

# Batter & Dough Component Analysis

The key words "MUST", "MUST NOT", "SHOULD", "SHOULD NOT", and "MAY" in this document are to be interpreted as described in RFC 2119.

## How It Works

When the user asks to analyze a recipe, compare recipes, or diagnose a texture problem:

1. Read the recipe file(s) from `r/<recipe-slug>.md` (or accept ingredients pasted in chat)
2. Break down each ingredient into its raw functional components
3. Calculate percentages of total batter weight
4. Compare against known benchmarks if available
5. Diagnose any problems or predict behavior

## Ingredient Decomposition Rules

Composite ingredients MUST be broken down into their raw functional components. Do not treat "chocolate" or "cream" as single units — they contain multiple functional components.

### Common decompositions:

| Ingredient | Fat | Sugar | Liquid | Structure/Solids | Protein |
|---|---|---|---|---|---|
| Whole milk | 3.5% | 5% (lactose) | 87% | — | 3.5% |
| Heavy cream (35%) | 35% | 3% | 58% | — | 2% |
| Butter | 82% | — | 16% (water) | — | 1% |
| Whole egg (50g) | 5g | — | 38g | — | 6g |
| Egg yolk (18g) | 6g | — | 9g | — | 3g |
| Dark chocolate 70% | 42% fat | 30% sugar | — | 26% cocoa solids | 2% |
| Dark chocolate 85% | 48% fat | 15% sugar | — | 35% cocoa solids | 2% |
| White chocolate | 35% fat | 45% sugar | — | 0% cocoa solids | 20% milk solids |
| AP flour | — | — | — | 100% (structure) | ~11% protein within |
| Cake flour | — | — | — | 100% (structure) | ~8% protein within |
| Cornstarch | — | — | — | 100% (structure, no protein) | 0% |
| Cocoa powder | 10% fat | — | — | 85% (structure) | 5% protein |
| Matcha/hojicha powder | — | — | — | ~90% (fiber/solids, minimal structure) | — |
| Sugar (granulated) | — | 100% | — | — | — |
| Honey | — | 80% sugar | 17% water | — | — |
| Rum/brandy/spirits (40% ABV) | — | — | 100% (acts as liquid) | — | — |
| Cointreau/liqueurs | — | 24% sugar | 76% liquid | — | — |

### Matcha/hojicha note:
Matcha adds bulk (solid) but does NOT act as structure like flour or cocoa solids. It doesn't gelatinize or form networks. Treat it as "inert solid" — it thickens slightly but doesn't set.

## Output Format

Present the analysis as a table showing:

1. **Per-ingredient breakdown** (what each ingredient contributes)
2. **Total functional components** as percentage of total batter weight
3. **Comparison** against a reference recipe or ideal range (if available)

Example output:

```
## Batter Analysis: [Recipe Name]
Total batter weight: 960g

| Component | Amount | % of total |
|---|---|---|
| Fat (all sources) | 81g | 8.4% |
| Sugar (all sources) | 237g | 24.7% |
| Structure solids (flour + starch + cocoa solids) | 102g | 10.6% |
| Liquid (milk + rum + water from butter/eggs) | 520g | 54.2% |
| Egg protein | 22g | 2.3% |

### Compared to sweet spot:
| | This recipe | Custardy range | Cakey range |
|---|---|---|---|
| Structure % | 10.6% | 8–14% | 15%+ |
| Fat % | 8.4% | 7–10% | — |
| Sugar % | 24.7% | 19–25% | — |

### Diagnosis:
- Structure at 10.6% → expect custardy interior
- Fat at 8.4% → rich mouthfeel
- [any issues or predictions]
```

## Rules

1. You MUST decompose composite ingredients (chocolate, cream, eggs) into functional components.
2. You MUST calculate percentages of total batter weight.
3. You SHOULD compare against known benchmarks for the specific baked good (e.g., canelé custardy sweet spot: structure 8-14%, fat 7-10%).
4. You MUST flag when a component is significantly outside the expected range.
5. When comparing two recipes, you MUST show the gap and explain what functional difference that gap causes.
6. When diagnosing a problem (too soft, too cakey, too liquidy), you MUST identify which component is likely the cause.
7. You SHOULD suggest specific fixes with gram amounts, not vague advice.

## Canelé-Specific Benchmarks

From tested recipes (see `/a/canele-ratio-analysis`):

| Component | Custardy range | Cakey range | Too-soft/collapse range |
|---|---|---|---|
| Structure solids % | 8–14% | 15%+ | <7% |
| Fat % | 7–10% | — | — |
| Sugar % | 19–24% | — | — |
| Liquid % | 48–56% | <48% | >60% |
| Egg % | 8–16% | — | — |

## When to use this skill

- "Why is my canelé cakey?" → analyze flour/structure %
- "Why is this batter too liquidy?" → compare total solids vs liquid
- "Can I sub white chocolate for dark?" → decompose both, show the structure gap
- "Compare these two recipes" → side-by-side component analysis
- "Will this recipe work?" → check all components against benchmarks
