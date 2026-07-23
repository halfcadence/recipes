# AGENTS.md

Conventions and gotchas for AI agents working in this repo. Read this and `steering.md` before editing. `steering.md` is the authoritative style rulebook (voice, measurements, format, the New Recipe Checklist); this file is the practical map + the traps that aren't obvious from the file tree.

## What this repo is

A Jekyll / GitHub Pages recipe site (`halfcadence.github.io/recipes`), **Swiss-modernist / Müller-Brockmann grid-styled**: self-owned CSS (no theme gem), Helvetica only, a responsive modular grid (`--cols` 12→8→4) everything snaps to, **pure monochrome — no accent/section color**, hierarchy by a fixed type ramp (`$fs-*` tokens) + weight, no illustrations. Recipe titles are a big lowercase type-as-image moment (the one Experimental-Jetset nod); the homepage is a full-width text-only archive. Full rules in `steering.md` ("Design system — Swiss modernist"). (History: first a two-ink risograph look with Bricolage Grotesque, then a per-section-color EJ phase — **both retired**; the old `colors.html` + `illustrations*` archive pages and their 50MB of assets have since been **deleted** — the risograph *article* is the only remaining record.)

## The three tiers — know which one you're touching

1. **Published site** — `r/` (recipes), `a/` (articles), `drafts/`, `index.md`, `steering.md`, `changelog.md`, `assets/`. Changes here go live on push.
2. **`drafts/`** — unfinished/untested recipes and unlisted pages. On the site (reachable at `/drafts`, linked from the Colophon) but kept out of the main index. No `number`; use `permalink: /drafts/{slug}`.
3. **`cafe/` — EXCLUDED from the build (`_config.yml`).** A hypothetical café business plan, baking-science deep-dives, a brand kit, and a local review site (`cafe/site/`). Repo-only, never published. **Do not assume anything in `cafe/` renders on the site, and do not link to `cafe/` files from published pages — those links 404.** If a published recipe needs a fact that lives in `cafe/`, inline it or link a published article instead.

## Hard rules (easy to get wrong)

- **A recipe/article is invisible until linked from `index.md`.** Creating the file isn't enough.
- **Every `.html` page MUST declare `layout:` in its front matter** (`page` for content pages, `default` for bare ones). `_config.yml` has NO layout default, and HTML — unlike markdown, which inherits minima's default — renders with *no layout at all* when unset: no `<head>`, no `main.css`, no `.wrapper` → the page ships as raw Times serif with invisible text (this bit `/photos`). Grep before pushing: `for f in *.html; do grep -q '^layout:' "$f" || echo "NO layout: $f"; done` (must print nothing).
- **Body-text cross-links MUST use `relative_url`, not a bare root path.** Write `[Purin]({{ '/r/purin' | relative_url }})`, never `[Purin](/r/purin)` — a bare `/r/slug` drops the `/recipes` baseurl and 404s on the live site. (`index.md` uses relative `./r/slug` and is exempt.) Grep for regressions across ALL content dirs (incl. `drafts/` and bare `](/)`): `grep -rnE '\]\(/([ra]|drafts)/|\]\(/\)' r/ a/ drafts/ *.md | grep -v relative_url` (must be empty).
- **Verify links actually resolve** (not just that they use `relative_url`): `python3 bin/check-links.py` checks every `index.md` `./` anchor AND every `relative_url` body link against real files + declared `permalink:`s (drafts resolve by permalink, not filename). Must print `✓ All internal links resolve`. Run it after any link/rename/permalink change.
- **Any change to a published page requires a `changelog.md` entry in the same commit** (steering rule). Draft/`cafe/` changes don't.
- **Recipe numbers are sequential and unique.** Run `python3 bin/check-numbers.py` — it verifies every `r/` page has a `number:`, the set is a contiguous `1..N` with no gaps or duplicates, and prints the next number to assign. Run before AND after adding a recipe. Drafts get **no** number (not checked). (The homepage masthead count is separate — it's auto-computed from the number of `r/` pages, not the max `number:`; don't hardcode it.)
- **New published recipe = the New Recipe Checklist** (steering.md): `r/{slug}.md` with front matter (next `number`) + `index.md` link + `changelog.md` entry. That's it — **no illustration** (recipe pages are type-only now; don't create SVGs or Nova PNGs for new recipes).
- **Baking recipes (batters/doughs) need an `## Analysis` block** between Steps and Notes. Component grams must sum within ~2g of the stated total and percentages to ~100%. The decomposition rules + benchmarks are the single source of truth in `.kiro/skills/batter-analysis.md` — use them; don't hand-invent the numbers. Custardy canelé target: ~12% structure.
- **Voice:** minimal, imperative, numeric, no marketing adjectives, no exclamation points. Notes are bullets in a `<div class="notes" markdown="1">`. Weights in grams (cocktails in oz); temps in °F.

## Illustrations are gone (deleted, not archived)

Recipe pages have no illustrations. The old per-recipe SVGs, the AI-generated
`gen-riso/*.png` set, their `assets/illustrations/` dir (~50MB), the
`/illustrations` + `/illustrations-riso` gallery pages, and `_data/illustrations.yml`
have all been **removed** (delisted archive, reachable from nowhere). Don't recreate
them or reintroduce an illustration system — recipe pages are type + hero photo only.

## Recipe photos (separate from illustrations — these ARE live)

A recipe MAY show a full-width 16:9 hero photo, resolved in `_layouts/page.html`:
front-matter `image:` → `_data/photos.yml` `specific[slug]`. **NO fallback** — a
recipe not in the registry shows no photo (a generic/wrong image is worse than
none). Adding one = a line in `photos.yml` under `specific:`, keyed by slug, value
an Unsplash **free** stem (`photo-<id>`; NOT `premium_photo-`). The full rule + the
find/verify procedure (search landscape+free, scrape stems, **download and LOOK
before trusting** — alt text lies) is in `steering.md` "Recipe Photos". Don't paste
image URLs into recipe front matter; use the registry.

## Styling lives in one place

`assets/main.scss` is the entire stylesheet — self-contained, no `minima`/theme
gem. **Monochrome**: ink `#111` / paper `#fff` / grey `#6b6b6b` / hair `#e4e4e4`
(+ dark variants) are the whole palette — no accent, no per-section color (the old
`$sections` map is gone; don't reintroduce it). Type sizes come from `$fs-*` ramp
tokens (11/13/15/21/26/hero) — every `font-size` references a token, no ad-hoc
px/rem. Homepage full-width via `body.home`; the modular grid is `--cols` 12→8→4.

## Publishing / deploy

- Push to `main`; GitHub Pages builds automatically (classic Jekyll build, no Actions workflow).
- **Build failures are sometimes transient** GitHub-Pages infrastructure flakiness, not content — the same commit can show both `errored` and `built` in the Pages build history. Confirm by checking whether the *live URL renders* and whether a retry builds green before hunting for a content bug.
- Ruby/Jekyll may not build locally in every environment (libyaml/psych issues); verify via the live site instead of assuming a local `jekyll build`.

## Git

- Commit/push only when asked. Co-author trailer:
  `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`
- The GitHub remote uses a stored credential at `~/.config/git/recipes-credentials`.
