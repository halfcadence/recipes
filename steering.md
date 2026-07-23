---
layout: page
title: Steering
category: colophon
permalink: /steering/
toc: true
---

The key words "MUST", "MUST NOT", "SHOULD", "SHOULD NOT", and "MAY" in this document are to be interpreted as described in RFC 2119.

## Voice & Tone

- Recipes MUST be minimal and direct. There MUST NOT be storytelling or preamble.
- Steps MUST use imperative mood: "Sift matcha into a bowl", not "You should sift the matcha".
- Notes are where personality, expertise, substitutions, and science SHOULD live.

## Front Matter

- `title` MUST be included.
- `category` MUST be included. Valid values: `drinks`, `sweets`, `mains`, `soups`, `sides`, `pantry`, `articles`, `colophon`. This places the recipe in its section on the homepage and drives the breadcrumb label. A new category MAY be created if a recipe does not fit an existing one.
- `number` MUST be included for recipes. Use the next sequential number (chronological). Articles and style guide pages MUST NOT have a number.
- `source` SHOULD be included if the recipe is adapted from an external source.
- `chef` MAY be included if the source chef is notable.
- `yield` MAY be included to indicate servings or pieces.
- `description` MAY be included to set the page's meta/share description (the search-result + social-card snippet). If omitted, one is derived automatically (articles use their opening sentence; recipes get a synthesized "title — a {category} recipe … No. N" line) — so a hand-written `description` is only needed when the auto one reads poorly. It MUST be a single plain sentence, ~150 chars, no markdown.
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
- Cross-links in recipe/article **body text** MUST use Jekyll's `relative_url` filter, not a bare root path: write `[Purin]({{ '/r/purin' | relative_url }})`, NOT `[Purin](/r/purin)`. A bare `/r/slug` renders as a root-absolute link that drops the site's `/recipes` baseurl and 404s. (Links in `index.md` use relative `./r/slug` paths and are fine as-is.)

## Design system — Swiss modernist (Müller-Brockmann grid)

The site follows the **International Typographic Style (Swiss modernism)**, in the
**Müller-Brockmann grid-system** lineage: one typeface (Helvetica), a visible modular
grid every element snaps to, tabular/objective data, baseline rhythm, and **pure
monochrome — NO color at all.** Hierarchy comes from size, weight, and position on the
grid. The one expressive flourish is the oversized lowercase **type-as-image wordmark**
(the recipe title / home masthead) — a nod to Experimental Jetset, but the system is
otherwise strictly grid-Swiss, not EJ's poster expressiveness.

(History: the site was first a two-ink risograph look with Bricolage Grotesque, then a
per-section-color Experimental-Jetset phase; **both are retired.** The `colors.html` /
`illustrations*` colophon pages preserve the old riso palette as a labeled archive, and
the riso-color *article* keeps its swatches as content. There is no live accent color.)

- **Type:** `Helvetica Neue, Helvetica, Arial, sans-serif` — one family, no serif, no
  mono (code excepted). Base 15px / 1.5. Sentence/lower case for content; the **only**
  place `text-transform: uppercase` + letter-spacing is used is the small section
  **kicker** (and masthead/caption labels). Large type is tight-negative tracking; body
  ~0. Hierarchy is the type **ramp + weight** (400 body / 700 heads), never color.
- **Type ramp** (`$fs-*` tokens, anchored to 15px body): `11` kicker/caption · `13`
  secondary (notes, analysis, tables, lists, step numbers) · `15` body/ingredients/steps
  · `21` lede + section head · `26` category head · `clamp(2.6rem,9vw,5rem)` hero title.
  Every `font-size` MUST reference a `$fs-*` token (or the hero clamp / an em-relative
  counter) — no ad-hoc px/rem sizes. See the `/type` page and "Univers Stepped".
- **The grid:** a responsive modular grid underlies every page — `--cols` 12 (desktop)
  → 8 → 4, with `1.25rem` gutters. Blocks span whole column ranges; recipe bodies,
  ingredient tables, steps, notes, and analysis all place onto it. Nothing floats.
- **Monochrome tones — no accent, no per-section color.** Ink `#111` on paper `#fff`
  (light), inverting to `#f2f2f0` on `#0c0c0d` (dark), plus grey `#6b6b6b` (secondary
  text) and hair `#e4e4e4` (rules); dark variants `#9a9a98` / `#2a2a2c`. These are the
  entire palette. Do NOT add a section/spot color or a filled color block. (The `$sections`
  color map and per-category accent are **gone**; don't reintroduce them.)
- **Rules & structure:** hard 1px/hairline rules, hard corners, flat fills — no shadows,
  gradients, or radii. Emphasis is weight or a hairline, never a hue.
- `print-color-adjust: exact` SHOULD be used only where the archived Colors/riso swatch
  pages need their colors to survive printing.

## Illustrations — none

- Recipe/article pages have **no illustrations.** The type + the numbered hero
  carry the page (the EJ archive uses no per-item art). Do NOT add illustration
  stamps to recipe pages, and do NOT generate riso PNGs for new recipes.
  (Photography is a separate system — recipes DO carry a hero photo; see
  "Recipe Photos". "No illustrations" means no drawn/riso art, not no photos.)
- The old per-recipe SVGs remain in `assets/illustrations/` (recolored to the
  single spot ink) only to feed the `/illustrations/` colophon gallery, which is
  now an archive of the earlier illustration system. New recipes do NOT need one.
- The `/illustrations-riso/` gallery and `gen-riso/*.png` set are likewise a
  retired archive; leave them, but don't extend them.

## AI Artifacts

- Articles and recipes MUST NOT contain meta-commentary about how content was produced, rephrased, or licensed. No "content rephrased for compliance" or similar.
- Source attribution belongs in a Sources section at the end of the article, as plain links. Inline parenthetical citations (e.g., "from [Source Name](url)") MAY be used sparingly when the source is directly relevant to a specific claim.
- AI tool instructions (compliance notices, verbatim reproduction limits, attribution boilerplate) MUST NOT leak into published content.

## Changelog

- All meaningful changes to recipes, styling, or site structure MUST be logged in `changelog.md` with the current date.
- Changelog MUST be updated in the same commit as the change, not retroactively.
- Entries SHOULD be grouped by date, newest first.
- Each entry SHOULD be a single bullet describing what changed. Keep it concise.
- Changelog MUST be the last item in the Colophon section of `index.md`.

## Analysis (baking recipes)

- Baking recipes (batters and doughs — canelés, cakes, cookies, brownies, chiffon, quick breads, clafoutis, mochi, and custard/pastry desserts) MUST include an `## Analysis` section.
- Non-baking recipes (drinks, sauces, no-bake sweets like jelly/panna cotta/affogato, savory mains/soups/sides) MUST NOT have an Analysis section.
- The Analysis section MUST appear between Steps and Notes.
- It MUST use a `<div class="analysis" markdown="1">` wrapper and contain, in order: a total batter weight line, a component table (fat, sugar, structure solids, liquid, egg/protein) with grams and percentages, an optional benchmark comparison, and a 1–3 sentence plain-language takeaway.
- Percentages MUST be of total batter weight and displayed to one decimal place.
- Coatings, glazes, frostings, and dustings MUST NOT count toward the batter weight; note them separately if significant.
- Inert solids (matcha, hojicha) MUST NOT be counted as structure solids.
- The decomposition values and texture benchmarks are defined in the `batter-analysis` skill (`.kiro/skills/batter-analysis.md`), which is the single source of truth. The on-page block format is documented there.
- Component grams MUST sum to within ~2g of the stated total, and percentages to ~100%. If a component is outside its benchmark range, the takeaway MUST acknowledge it.

## Recipe Photos

A recipe page MAY show a **full-width 16:9 hero photo** under the title. This is
distinct from the retired illustration system (see "Illustrations — none"): photos
are real food photography, not per-item art.

Resolution order (handled by `_layouts/page.html`), first match wins:

1. Front-matter `image:` on the recipe (a full URL) — an explicit override. Rare;
   prefer the registry.
2. `_data/photos.yml` → `specific:` keyed by the recipe **slug** (filename without
   `.md`). Value is an Unsplash CDN stem (`photo-<id>`); the layout appends sizing.

**There is NO fallback.** A recipe not in the registry (and with no front-matter
`image:`) shows no hero photo. This is deliberate: a generic or wrong photo
(e.g. a tortilla on the steak page) is worse than none. Only add a photo you have
verified depicts that specific dish.

Rules:

- A `specific:` entry MUST actually depict THAT dish and MUST crop cleanly to 16:9
  (subject centered, not cut off). When unsure, leave it out — no photo is fine.
- Variants SHOULD reuse one good photo where honest (e.g. all plain-canelé variants
  can share a canelé shot) but MUST NOT borrow an unrelated dish's photo.
- Photos MUST be **free-licensed** (Unsplash `images.unsplash.com/photo-…`), never
  Unsplash+ (`plus.unsplash.com/premium_photo-…`) or other paid/unlicensed sources.
- `image_credit` defaults to "Photo — Unsplash". If a photo is kept long-term, the
  real photographer SHOULD be credited (Unsplash guideline).
- Articles/colophon pages get a photo ONLY via explicit front-matter `image:`.

### How to find and verify a photo (the procedure)

1. On unsplash.com (logged in), search the dish with landscape+free filters:
   `https://unsplash.com/s/photos/<dish>?orientation=landscape&license=free`.
2. Scrape free CDN stems from the rendered grid (the `napi` search API returns 401;
   scrape `img[srcset]` instead), keeping only `images.unsplash.com/photo-…` (drop
   `premium_photo-`). Collect the `photo-<id>` stem + its alt text.
3. **Verify visually — do not trust alt text.** Download each candidate cropped to
   16:9 (`?w=640&h=360&fit=crop&q=70&auto=format`) and LOOK at it. A “flan” result
   is often panna cotta; a “tortilla” is often a wrap. Reject anything that isn’t the
   dish, isn’t appetizing, or loses its subject in the 16:9 crop.
4. Add the winning stem to `photos.yml` under `specific:` with a `# comment` naming
   what it shows. Rebuild and eyeball the recipe page before pushing.

A contact-sheet harness (download many candidates into a 16:9 grid, screenshot once)
is the efficient way to verify a batch — build it under `work/understand/…`, not in
this repo.

## New Recipe Checklist

When adding a new recipe, ALL of the following MUST be completed:

1. Create `r/{slug}.md` with front matter (`title`, `category`, `number` — next sequential).
2. Add a link to `index.md` under the appropriate category. Base recipes MUST be listed before variants. (A recipe is invisible until it's linked here — the homepage is the gate.)
3. Update `changelog.md` with the new recipe, in the same commit.
4. For baking recipes (batter/dough), add an `## Analysis` section between Steps and Notes, computed via the `batter-analysis` skill.
5. SHOULD add a verified `specific:` photo to `_data/photos.yml` if a good one exists (see Recipe Photos). If none is found, leave it out — there is no fallback and no photo is fine.

No illustration is needed — recipe pages are type-only (see Illustrations above); the hero photo is separate and comes from the photo registry.

The homepage recipe **count** (the "124" on the masthead) is computed at build time from the number of pages in `r/` (`_includes/header.html`), so it stays in sync automatically — do NOT hardcode or hand-update it.
