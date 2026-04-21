---
inclusion: fileMatch
fileMatchPattern: "r/*.md"
---

# Recipe Style Guide

The key words "MUST", "MUST NOT", "SHOULD", "SHOULD NOT", and "MAY" in this document are to be interpreted as described in RFC 2119.

## Voice & Tone

- Recipes MUST be minimal and direct. There MUST NOT be storytelling or preamble.
- Steps MUST use imperative mood: "Sift matcha into a bowl", not "You should sift the matcha".
- Notes are where personality, expertise, substitutions, and science SHOULD live.

## Front Matter

- `title` MUST be included.
- `category` MUST be included. Valid values: `drinks`, `sweets`, `mains`, `soups`, `sides`, `pantry`, `articles`. This drives the page color theme.
- `number` MUST be included. Use the next sequential number (chronological). Check the highest existing number in `r/` and `a/` files and add 1.
- `source` SHOULD be included if the recipe is adapted from an external source.
- `chef` MAY be included if the source chef is notable.
- `yield` MAY be included to indicate servings or pieces.
- `layout` MUST NOT be included — it inherits from the default.

```yaml
---
title: Recipe Name
category: drinks
number: 64
source: https://original-source-url
chef: Chef Name
yield: 12
---
```

## Measurements

- All weights and volumes MUST use grams (g). Cups, tablespoons, teaspoons, and milliliters MUST NOT be used.
- **Exception — cocktails**: Cocktail recipes MUST use ounces (oz) for spirits, liqueurs, juices, and syrups. Cocktails are built with jiggers, not scales.
- Temperatures MUST be in Fahrenheit (°F).
- Whole items (eggs, vanilla beans, chili peppers) SHOULD use counts.
- Ranges SHOULD use an en dash: `115–140g`.
- Volumetric measurements from sources MUST be converted to grams before writing (except cocktails).

## Ingredients

- Ingredients MUST use the table format:

```markdown
## Ingredients

| | |
|---|---|
| 100g | dark chocolate, chopped |
| 3 | large eggs, separated |
```

- Amount MUST be in the left column, ingredient and prep notes in the right.
- There MUST NOT be a header row.
- Ingredients SHOULD be listed in the order they are used.
- Prep instructions SHOULD be included inline: "unsalted butter, cubed".
- Sub-components MAY be grouped with labels like `(A)` and `(B)` if mixed at different stages.

## Steps

- Steps MUST be a numbered list.
- Each step SHOULD be one logical action or a tightly related sequence.
- Temperatures and times MUST be included inline: "Bake at 350°F for 15 minutes".
- There SHOULD be a blank line between steps for readability.
- Steps MUST NOT omit critical details for the sake of brevity.

## Notes

- Notes MUST use a `<div class="notes" markdown="1">` wrapper for styling:

```markdown
<div class="notes" markdown="1">
## Notes

- Tip or substitution here.
</div>
```

- Notes MUST be in bullet list format.
- Notes SHOULD cover: substitutions, storage, scaling, science, technique tips.
- The Notes section MAY be omitted entirely if there is nothing useful to add.

## File Naming & Linking

- Filenames MUST be kebab-case in the `r/` directory (e.g., `r/doenjang-jjigae.md`).
- A link to the recipe MUST be added to `index.md` under the appropriate category.
- If no existing category fits, a new one SHOULD be created.
- Recipes not linked from `index.md` will not appear on the site.
