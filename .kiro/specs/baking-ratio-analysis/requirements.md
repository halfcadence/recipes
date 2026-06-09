# Requirements Document

## Introduction

This feature adds an optional "Analysis" section to baking recipes on the site. The section breaks down a recipe's ingredients by their functional components (fat, sugar, structure, liquid, protein) as a percentage of total batter/dough weight, and explains what those percentages mean for the finished result. The goal is to turn each baking recipe into a teaching tool: by reading the analysis across many recipes, a reader learns how shifts in component ratios drive texture (custardy vs cakey, chewy vs crispy, fluffy vs dense).

This builds on two artifacts that already exist:
- The `batter-analysis` skill (`.kiro/skills/batter-analysis.md`), which defines ingredient decomposition rules, an output format, and texture benchmarks by baked-good type.
- The Canelé Ratio Analysis article (`a/canele-ratio-analysis.md`), which demonstrates cross-recipe comparison and the "custardy sweet spot" concept.

The new work is to bring that analysis *into individual recipe pages* in a consistent, styled, and accurate way, and to define the rules/process for producing and maintaining it.

## Glossary

- **Functional component**: A role an ingredient plays in a batter — fat, sugar, structure (gluten/starch/cocoa solids), liquid, or protein. A single ingredient may contribute to several (e.g. whole milk = liquid + fat + sugar + protein).
- **Structure solids**: Flour, starch, and cocoa solids — the components that set/firm the interior. Distinguished from inert solids like matcha which add bulk but do not set.
- **Total batter weight**: The summed weight of all ingredients that become the batter/dough. Excludes mold-coating items (beeswax) and non-incorporated finishing items (dusting sugar) unless they are part of the eaten product.
- **Analysis section**: The new styled block on a recipe page presenting the component breakdown table, comparison to benchmarks, and a short plain-language takeaway.
- **Baking recipe**: A recipe in the `sweets` category (and any future baked items) that is a batter or dough — canelés, cakes, cookies, brownies, chiffon, quick breads, clafoutis, mochi. Excludes drinks, sauces, no-bake items, and savory mains/soups/sides.
- **Benchmark**: A documented target range for a component for a given baked-good type (e.g. canelé structure 8–14% = custardy), as defined in the batter-analysis skill.

## Requirements

### Requirement 1: Analysis section on baking recipes

**User Story:** As a reader learning to bake, I want each baking recipe to show its ingredient breakdown by weight percentage, so that I can understand why the recipe produces its texture and how it compares to others.

#### Acceptance Criteria

1. WHERE a recipe is a baking recipe (batter or dough), the recipe page SHALL be eligible for an Analysis section.
2. WHEN an Analysis section is present, it SHALL display a table of functional components (fat, sugar, structure solids, liquid, egg/protein) with both gram amounts and percentage of total batter weight.
3. WHEN an Analysis section is present, it SHALL state the total batter weight used as the percentage denominator.
4. THE Analysis section SHALL include a short plain-language takeaway (1–3 sentences) describing what the ratios mean for the result.
5. WHERE a benchmark exists for the recipe's baked-good type, the Analysis section SHALL compare the recipe's key components against that benchmark range.
6. IF a recipe is not a baking batter/dough (drink, sauce, savory dish, no-bake), THEN it SHALL NOT have an Analysis section.
7. THE Analysis section SHALL be visually distinct from the Steps and Notes, using a styled wrapper consistent with the site's existing patterns.

### Requirement 2: Accurate, transparent decomposition

**User Story:** As a reader who trusts the numbers, I want the component breakdown to use consistent, correct decomposition of composite ingredients, so that the percentages are meaningful and comparable across recipes.

#### Acceptance Criteria

1. WHEN computing components, composite ingredients (milk, cream, butter, eggs, chocolate, liqueurs, honey) SHALL be decomposed into functional components using the decomposition table in the batter-analysis skill.
2. THE decomposition SHALL treat structure solids (flour, starch, cocoa solids) separately from inert solids (matcha, hojicha) which add bulk but do not set.
3. WHEN the same ingredient appears in multiple recipes, its decomposition SHALL be consistent across all of them.
4. THE percentage for each component SHALL be computed against the same total batter weight denominator within a recipe.
5. THE system SHALL allow higher precision for intermediate calculations but SHALL display percentages rounded to one decimal place.
6. IF an ingredient is not in the decomposition table, THEN it SHALL be added to the table (in the skill) before being used, so the source of truth stays complete.

### Requirement 3: Single source of truth for decomposition and benchmarks

**User Story:** As the site maintainer, I want the decomposition rules and benchmarks to live in one place, so that recipe analyses stay consistent and I don't duplicate or contradict numbers.

#### Acceptance Criteria

1. THE ingredient decomposition table and texture benchmarks SHALL remain defined in the `batter-analysis` skill as the single source of truth.
2. WHEN a recipe's Analysis section is produced, it SHALL use the decomposition and benchmarks from that skill.
3. IF a decomposition value or benchmark is updated in the skill, THEN affected recipe Analysis sections SHALL be updated to match.
4. THE steering file SHALL document the Analysis section as part of the baking-recipe convention, referencing the skill.

### Requirement 4: Consistent placement, format, and styling

**User Story:** As a reader, I want the Analysis section to appear in a predictable place and format on every baking recipe, so that I can scan and compare it easily.

#### Acceptance Criteria

1. THE Analysis section SHALL appear in a consistent position on the page relative to Steps and Notes across all baking recipes.
2. THE Analysis section SHALL follow a consistent internal structure: component table, optional benchmark comparison, plain-language takeaway.
3. THE Analysis section SHALL conform to the site's measurement rules (grams, one-decimal percentages) and voice rules (direct, no preamble).
4. WHERE the site theme defines colors and styled blocks, the Analysis section styling SHALL use existing theme tokens rather than introducing new arbitrary colors.
5. THE Analysis section SHALL render correctly in both light and dark mode and in print.

### Requirement 5: Rollout across existing baking recipes

**User Story:** As the site maintainer, I want a clear plan for adding the Analysis section to existing baking recipes, so that the feature is applied consistently rather than ad hoc.

#### Acceptance Criteria

1. THE feature SHALL define which existing recipes qualify as baking recipes requiring an Analysis section.
2. WHEN the feature is rolled out, each qualifying recipe SHALL receive an Analysis section computed from its current ingredient list. An Analysis section SHALL be required for every qualifying recipe regardless of rollout status, not only during active rollout periods.
3. WHERE a recipe is later edited in a way that changes ingredient weights, its Analysis section SHALL be recomputed to stay accurate.
4. THE new-recipe checklist SHALL be updated so that adding a baking recipe includes producing its Analysis section.
5. THE system SHALL always track which qualifying recipes still lack an Analysis section, regardless of whether the rollout is sequenced. IF the full rollout is large, THEN it SHALL be sequenced (e.g. canelés first, then cookies, then cakes) rather than required all at once.

### Requirement 6: Verification of analysis correctness

**User Story:** As the site maintainer, I want the analysis numbers to be verifiable, so that published percentages are not silently wrong.

#### Acceptance Criteria

1. WHEN an Analysis section is produced, the component gram amounts SHALL sum to within a small tolerance of the stated total batter weight.
2. WHEN an Analysis section is produced, the component percentages SHALL sum to approximately 100% (within rounding tolerance), accounting for any explicitly excluded items.
3. WHERE a recipe's analysis places a component outside its benchmark range, the takeaway SHALL acknowledge it rather than ignore it.
4. THE site SHALL continue to build successfully (Jekyll build passes) after Analysis sections are added.
