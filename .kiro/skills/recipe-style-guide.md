---
name: recipe-style-guide
description: Style guide for writing and formatting recipes on the site. Covers voice, measurements, structure, and formatting conventions.
triggers:
  - "write a recipe"
  - "add a recipe"
  - "new recipe"
  - "recipe style"
  - "recipe format"
---

# Recipe Style Guide

## Voice & Tone

- Minimal and direct. No storytelling, no preamble. The recipe speaks for itself.
- Imperative mood in steps: "Sift matcha into a bowl", not "You should sift the matcha".
- Notes are where personality, expertise, substitutions, and science live.

## Front Matter

Required:
- `title`: Recipe name.

Optional:
- `source`: URL of the original recipe, if adapted from one.
- `chef`: Name and affiliation, if notable.
- `yield`: Number of servings or pieces.

Do not include `layout` — it inherits from the default.

```yaml
---
title: Recipe Name
source: https://original-source-url
chef: Chef Name
yield: 12
---
```

## Measurements

- **Weight and volume**: Always use grams (g) and milliliters (ml). Never use cups, tablespoons, teaspoons, or ounces.
- **Temperature**: Fahrenheit (°F).
- **Counts**: Use counts for whole items (eggs, vanilla beans, chili peppers).
- **Ranges**: Use an en dash for approximate quantities: `115–140g`.
- Convert volumetric measurements from sources to grams before writing the recipe.

## Ingredients

Always use the table format, no exceptions:

```markdown
## Ingredients

| | |
|---|---|
| 100g | dark chocolate, chopped |
| 3 | large eggs, separated |
```

- Amount in the left column, ingredient and prep notes in the right.
- No header row — the table is self-explanatory.
- List ingredients in the order they are used.
- Include prep instructions inline: "unsalted butter, cubed", "egg yolks and whites separated".
- Group with labels like `(A)` and `(B)` if a recipe has distinct sub-components mixed at different stages.

## Steps

- Numbered list.
- Each step is one logical action or a tightly related sequence.
- Include temperatures and times inline: "Bake at 350°F for 15 minutes".
- Blank line between steps for readability.
- Keep steps concise but complete — don't omit critical details for brevity.

## Notes

- Use a `<div class="notes" markdown="1">` wrapper for styling:

```markdown
<div class="notes" markdown="1">
## Notes

- Tip or substitution here.
</div>
```

- Bullet list format.
- Cover: substitutions, storage, scaling, science, technique tips.
- Optional — omit the section entirely if there's nothing useful to add.
- For very simple recipes with minimal notes, the `<div>` wrapper can be skipped.

## File Naming & Linking

- Filename: kebab-case in `r/` directory (e.g., `r/doenjang-jjigae.md`).
- After creating the recipe, add a link to `index.md` under the appropriate category.
- If no existing category fits, create a new one.
- Recipes not linked from `index.md` will not appear on the site.
