# AGENTS.md

Conventions and gotchas for AI agents working in this repo. Read this and `steering.md` before editing. `steering.md` is the authoritative style rulebook (voice, measurements, format, the New Recipe Checklist); this file is the practical map + the traps that aren't obvious from the file tree.

## What this repo is

A Jekyll / GitHub Pages recipe site (`halfcadence.github.io/recipes`), risograph-styled: two inks only — Blue `#0078bf`, Fluorescent Pink `#ff48b0`, on cream `#fbfaf8`; everything else is an overprint/tint. See the README for the full layout table.

## The three tiers — know which one you're touching

1. **Published site** — `r/` (recipes), `a/` (articles), `drafts/`, `index.md`, `steering.md`, `changelog.md`, `assets/`. Changes here go live on push.
2. **`drafts/`** — unfinished/untested recipes and unlisted pages. On the site (reachable at `/drafts`, linked from the Colophon) but kept out of the main index. No `number`; use `permalink: /drafts/{slug}`.
3. **`cafe/` — EXCLUDED from the build (`_config.yml`).** A hypothetical café business plan, baking-science deep-dives, a brand kit, and a local review site (`cafe/site/`). Repo-only, never published. **Do not assume anything in `cafe/` renders on the site, and do not link to `cafe/` files from published pages — those links 404.** If a published recipe needs a fact that lives in `cafe/`, inline it or link a published article instead.

## Hard rules (easy to get wrong)

- **A recipe/article is invisible until linked from `index.md`.** Creating the file isn't enough.
- **Body-text cross-links MUST use `relative_url`, not a bare root path.** Write `[Purin]({{ '/r/purin' | relative_url }})`, never `[Purin](/r/purin)` — a bare `/r/slug` drops the `/recipes` baseurl and 404s on the live site. (`index.md` uses relative `./r/slug` and is exempt.) Grep for regressions: `grep -rn '](/[ra]/' r/ a/`.
- **Any change to a published page requires a `changelog.md` entry in the same commit** (steering rule). Draft/`cafe/` changes don't.
- **Recipe numbers are sequential and unique.** Check `grep -rh "^number:" r/*.md` for the max before assigning. Drafts get **no** number.
- **New published recipe = the full New Recipe Checklist** (steering.md): `r/{slug}.md` + SVG in `assets/illustrations/` + `_data/illustrations.yml` entry + Nova Canvas riso PNG in `assets/illustrations/gen-riso/` + `index.md` link + `changelog.md`. Each illustration must be visually distinct (max 2 shapes, blue/pink only, `viewBox="0 0 200 200"`, multiply on overlaps).
- **Baking recipes (batters/doughs) need an `## Analysis` block** between Steps and Notes. Component grams must sum within ~2g of the stated total and percentages to ~100%. The decomposition rules + benchmarks are the single source of truth in `.kiro/skills/batter-analysis.md` — use them; don't hand-invent the numbers. Custardy canelé target: ~12% structure.
- **Voice:** minimal, imperative, numeric, no marketing adjectives, no exclamation points. Notes are bullets in a `<div class="notes" markdown="1">`. Weights in grams (cocktails in oz); temps in °F.

## Illustrations gallery is auto-generated

`illustrations.html` and `illustrations-riso.html` glob `assets/illustrations/` — you don't hand-edit them. Just drop the SVG/PNG in and add the `_data/illustrations.yml` shape entry.

## Nova Canvas (riso PNGs)

Generated via `amazon.nova-canvas-v1:0` on Bedrock using AWS profile **`shiauas-personal`** (an ada/conduit profile, `us-east-1`, auto-refreshing). The steering doc's prompt template applies. Nova is approximate — expect to generate a few and keep the best; it often ignores exact composition, which is acceptable for the abstract gallery.

## Publishing / deploy

- Push to `main`; GitHub Pages builds automatically (classic Jekyll build, no Actions workflow).
- **Build failures are sometimes transient** GitHub-Pages infrastructure flakiness, not content — the same commit can show both `errored` and `built` in the Pages build history. Confirm by checking whether the *live URL renders* and whether a retry builds green before hunting for a content bug.
- Ruby/Jekyll may not build locally in every environment (libyaml/psych issues); verify via the live site instead of assuming a local `jekyll build`.

## Git

- Commit/push only when asked. Co-author trailer:
  `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`
- The GitHub remote uses a stored credential at `~/.config/git/recipes-credentials`.
