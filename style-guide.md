---
title: Style Guide
category: styleguide
permalink: /style-guide/
---

The key words "MUST", "MUST NOT", "SHOULD", "SHOULD NOT", and "MAY" in this document are to be interpreted as described in RFC 2119.

## Voice & Tone

- Recipes MUST be minimal and direct. There MUST NOT be storytelling or preamble.
- Steps MUST use imperative mood: "Sift matcha into a bowl", not "You should sift the matcha".
- Notes are where personality, expertise, substitutions, and science SHOULD live.

## Front Matter

- `title` MUST be included.
- `category` MUST be included. Valid values: `drinks`, `sweets`, `mains`, `soups`, `sides`, `pantry`, `articles`. This drives the page color theme.
- `number` MUST be included for recipes. Use the next sequential number (chronological). Articles and style guide pages MUST NOT have a number.
- `source` SHOULD be included if the recipe is adapted from an external source.
- `chef` MAY be included if the source chef is notable.
- `yield` MAY be included to indicate servings or pieces.
- `layout` MUST NOT be included — it inherits from the default.

## Measurements

- All weights and volumes MUST use grams (g). Cups, tablespoons, teaspoons, and milliliters MUST NOT be used.
- **Exception — cocktails**: Cocktail recipes MUST use ounces (oz) for spirits, liqueurs, juices, and syrups. Cocktails are built with jiggers, not scales.
- Temperatures MUST be in Fahrenheit (°F).
- Whole items (eggs, vanilla beans, chili peppers) SHOULD use counts.
- Ranges SHOULD use an en dash: `115–140g`.
- Volumetric measurements from sources MUST be converted to grams before writing (except cocktails).

## Ingredients

- Ingredients MUST use the headerless table format: amount in the left column, ingredient and prep notes in the right.
- Ingredients SHOULD be listed in the order they are used.
- Prep instructions SHOULD be included inline: "unsalted butter, cubed".
- Sub-components MAY be grouped with labels like `(A)` and `(B)` if mixed at different stages.

## Steps

- Steps MUST be a numbered list.
- Each step SHOULD be one logical action or a tightly related sequence.
- Temperatures and times MUST be included inline: "Bake at 350°F for 15 minutes".
- Steps MUST NOT omit critical details for the sake of brevity.

## Notes

- Notes MUST use a styled wrapper div for de-emphasized styling.
- Notes MUST be in bullet list format.
- Notes SHOULD cover: substitutions, storage, scaling, science, technique tips.
- The Notes section MAY be omitted entirely if there is nothing useful to add.

## Naming

- Titles MUST be as short as possible. Use the simplest recognizable name for the dish.
- Cooking technique modifiers (e.g., "triple-fried", "reverse-seared", "chargrilled", "brown butter") MUST NOT appear in the title. Technique belongs in the steps and notes.
- Parenthetical descriptions (e.g., "Pork & Cabbage Dumplings", "Salmon Hot Pot") MUST NOT appear in the title. If the dish name is unfamiliar, explain it in the notes.
- Chef or brand names (e.g., "Robuchon") SHOULD NOT appear in the title unless the dish is universally known by that name. Credit the chef in the `chef` front matter field or notes instead.
- Article titles MUST NOT include subtitles after colons. Keep to the core topic.
- When a variant exists (e.g., lazy tortilla, OJ whiskey sour), use the shortest distinguishing modifier.

## File Naming & Linking

- Filenames MUST be kebab-case in the `r/` directory (e.g., `r/doenjang-jjigae.md`).
- A link to the recipe MUST be added to `index.md` under the appropriate category.
- Recipes not linked from `index.md` will not appear on the site.
