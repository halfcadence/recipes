---
title: Steering
category: colophon
permalink: /steering/
---

The key words "MUST", "MUST NOT", "SHOULD", "SHOULD NOT", and "MAY" in this document are to be interpreted as described in RFC 2119.

## Voice & Tone

- Recipes MUST be minimal and direct. There MUST NOT be storytelling or preamble.
- Steps MUST use imperative mood: "Sift matcha into a bowl", not "You should sift the matcha".
- Notes are where personality, expertise, substitutions, and science SHOULD live.

## Front Matter

- `title` MUST be included.
- `category` MUST be included. Valid values: `drinks`, `sweets`, `mains`, `soups`, `sides`, `pantry`, `articles`, `colophon`. This drives the page color theme. A new category MAY be created if a recipe does not fit an existing one.
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
- Notes MUST be actionable — they should help someone make, modify, store, or scale the recipe. Commentary, trivia, and "watch the video" references MUST NOT be in notes.
- Notes SHOULD cover: substitutions, storage, scaling, science, technique tips.
- The Notes section MAY be omitted entirely if there is nothing useful to add.

## Naming

- Titles MUST be as short as possible. Use the simplest recognizable name for the dish.
- Cooking technique modifiers (e.g., "triple-fried", "reverse-seared", "chargrilled") MUST NOT appear in the title. Technique belongs in the steps and notes.
- Ingredient modifiers that materially change the flavor (e.g., "brown butter", "miso") MAY appear in the title when they distinguish the recipe from a base version.
- Parenthetical descriptions (e.g., "Pork & Cabbage Dumplings", "Salmon Hot Pot") MUST NOT appear in the title. If the dish name is unfamiliar, explain it in the notes.
- Chef or brand names (e.g., "Robuchon") SHOULD NOT appear in the title unless the dish is universally known by that name. Credit the chef in the `chef` front matter field or notes instead.
- Article titles MUST NOT include subtitles after colons. Keep to the core topic.
- When a variant exists (e.g., lazy tortilla, OJ whiskey sour), use the shortest distinguishing modifier.
- In `index.md`, the base recipe MUST be listed before its variants (e.g., Gateau au Chocolat before Matcha Gateau au Chocolat, Highball before Yuzu Highball).

## File Naming & Linking

- Filenames MUST be kebab-case in the `r/` directory (e.g., `r/doenjang-jjigae.md`).
- A link to the recipe MUST be added to `index.md` under the appropriate category.
- Recipes not linked from `index.md` will not appear on the site.

## Colors

- The site uses Risograph ink colors exclusively. All UI colors MUST be actual riso ink hex values from [stencil.wiki](https://stencil.wiki/colors).
- Each category has a riso ink color defined in `assets/main.scss`. New categories MUST be assigned a riso ink color and added to both the light and dark themed mixins.
- UI grays are derived from Riso Midnight (`#435060`) and Riso Light Gray (`#88898a`). Generic grays like `#666`, `#999`, `#ccc` MUST NOT be used.
- Dark mode colors MUST be derived from Midnight at varying lightness levels, not arbitrary neutral grays.
- The Articles section uses a lighter Midnight variant (`#8b96a3`) in dark mode because the standard Midnight is too dark against the dark background.
- Inline color swatches (e.g., in the riso article) SHOULD use the `.pill-sample` class for consistency with homepage pills.
- `print-color-adjust: exact` SHOULD be used when colors need to survive printing.

## Illustrations

- Illustrations MUST use only the two base inks: Blue (`#0078bf`) and Fluorescent Pink (`#ff48b0`).
- Each illustration MUST be an SVG file in `assets/illustrations/`, named to match the recipe slug (e.g., `clam-miso-soup.svg`).
- Each illustration MUST use at most 2 shapes. 1 shape is better than an ugly 2nd shape.
- Shapes MAY be pink only, blue only, or one pink + one blue. Single-shape illustrations are encouraged when they read clearly.
- When using both colors, the overlapping shape SHOULD use `mix-blend-mode: multiply` to create the overprint where they overlap.
- When using a single shape, it MAY be either pink or blue.
- Same-color pairs (two pink or two blue) are valid. To get a visible overprint at the intersection, add a paper-colored background rect (`#fbfaf8`) inside the SVG and apply `mix-blend-mode: multiply` to both shapes. The overlap will darken like a double ink pass.
- Shapes MUST be primary geometric forms only: circle, rectangle, square, triangle (polygon). No paths, no curves, no organic shapes.
- Illustrations SHOULD prioritize symmetry and minimalism. Clean, centered, balanced.
- Each illustration MUST be visually distinct from the others. Vary the shape combination: circle+circle, rectangle+rectangle, triangle+triangle, circle+rectangle, circle+square, etc. Reversing which color is pink vs blue is a valid way to differentiate similar compositions.
- The viewBox MUST be `0 0 200 200`.
- The illustration gallery page is at `/illustrations/` and MUST be linked from the Colophon section of `index.md`.
- When adding a new recipe, BOTH an SVG illustration and a riso PNG illustration MUST be created.
- The SVG goes in `assets/illustrations/{slug}.svg` and MUST be added to the SVG illustrations gallery page.
- The riso PNG is generated via Amazon Nova Canvas (`amazon.nova-canvas-v1:0`) on AWS Bedrock using `--profile personal`. The prompt template is: `Risograph print on lightly textured cream paper. {composition}. Completely flat solid color, no 3D, no shading, no gradients, no shadows, no perspective, no outlines. Visible halftone dot grain from stencil printing. Slight misregistration between color passes. Perfectly centered and symmetrical. Abstract geometric art print.` where `{composition}` describes the SVG shapes in words (no food references). The PNG goes in `assets/illustrations/gen-riso/{slug}.png`.
- The riso illustrations gallery page is at `/illustrations-riso/`.

## Changelog

- All meaningful changes to recipes, styling, or site structure MUST be logged in `changelog.md` with the current date.
- Entries SHOULD be grouped by date, newest first.
- Each entry SHOULD be a single bullet describing what changed. Keep it concise.
- Changelog MUST be the last item in the Colophon section of `index.md`.
