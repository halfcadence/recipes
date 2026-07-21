# AGENTS.md

Conventions and gotchas for AI agents working in this repo. Read this and `steering.md` before editing. `steering.md` is the authoritative style rulebook (voice, measurements, format, the New Recipe Checklist); this file is the practical map + the traps that aren't obvious from the file tree.

## What this repo is

A Jekyll / GitHub Pages recipe site (`halfcadence.github.io/recipes`), **Experimental-Jetset–styled**: self-owned CSS (no theme gem), Helvetica only, pure black-on-white inverting to white-on-black, **sentence case** (no all-caps / letter-spacing), one **per-section accent color**, no illustrations. Recipe titles are a big lowercase type-as-image moment; the homepage is a full-width text-only archive. Full rules in `steering.md` ("Design system"). See the README for the layout table. (The site was previously a two-ink risograph look with Bricolage Grotesque — retired; the `colors.html`/`illustrations*` colophon pages keep it as a labeled archive.)

## The three tiers — know which one you're touching

1. **Published site** — `r/` (recipes), `a/` (articles), `drafts/`, `index.md`, `steering.md`, `changelog.md`, `assets/`. Changes here go live on push.
2. **`drafts/`** — unfinished/untested recipes and unlisted pages. On the site (reachable at `/drafts`, linked from the Colophon) but kept out of the main index. No `number`; use `permalink: /drafts/{slug}`.
3. **`cafe/` — EXCLUDED from the build (`_config.yml`).** A hypothetical café business plan, baking-science deep-dives, a brand kit, and a local review site (`cafe/site/`). Repo-only, never published. **Do not assume anything in `cafe/` renders on the site, and do not link to `cafe/` files from published pages — those links 404.** If a published recipe needs a fact that lives in `cafe/`, inline it or link a published article instead.

## Hard rules (easy to get wrong)

- **A recipe/article is invisible until linked from `index.md`.** Creating the file isn't enough.
- **Body-text cross-links MUST use `relative_url`, not a bare root path.** Write `[Purin]({{ '/r/purin' | relative_url }})`, never `[Purin](/r/purin)` — a bare `/r/slug` drops the `/recipes` baseurl and 404s on the live site. (`index.md` uses relative `./r/slug` and is exempt.) Grep for regressions: `grep -rn '](/[ra]/' r/ a/`.
- **Any change to a published page requires a `changelog.md` entry in the same commit** (steering rule). Draft/`cafe/` changes don't.
- **Recipe numbers are sequential and unique.** Check `grep -rh "^number:" r/*.md` for the max before assigning. Drafts get **no** number.
- **New published recipe = the New Recipe Checklist** (steering.md): `r/{slug}.md` with front matter (next `number`) + `index.md` link + `changelog.md` entry. That's it — **no illustration** (recipe pages are type-only now; don't create SVGs or Nova PNGs for new recipes).
- **Baking recipes (batters/doughs) need an `## Analysis` block** between Steps and Notes. Component grams must sum within ~2g of the stated total and percentages to ~100%. The decomposition rules + benchmarks are the single source of truth in `.kiro/skills/batter-analysis.md` — use them; don't hand-invent the numbers. Custardy canelé target: ~12% structure.
- **Voice:** minimal, imperative, numeric, no marketing adjectives, no exclamation points. Notes are bullets in a `<div class="notes" markdown="1">`. Weights in grams (cocktails in oz); temps in °F.

## Illustrations are retired (archive only)

Recipe pages have no illustrations. The old per-recipe SVGs + `gen-riso/*.png`
remain only to feed the `/illustrations/` and `/illustrations-riso/` colophon
galleries (auto-globbed from `assets/illustrations/`), which are now an archive
of the previous system. Don't add new ones or hand-edit those gallery pages.

## Styling lives in one place

`assets/main.scss` is the entire stylesheet — self-contained, no `minima`/theme
gem. Section colors are the `$sections` SCSS map (`(ground, ink)` per category;
`ground` = text on white, `ink` = lighter variant for dark mode; both must pass
AA). Color is a quiet accent only (kicker, number, step counters, rules) — never
a filled title. Homepage full-width via `body.home`.

## Publishing / deploy

- Push to `main`; GitHub Pages builds automatically (classic Jekyll build, no Actions workflow).
- **Build failures are sometimes transient** GitHub-Pages infrastructure flakiness, not content — the same commit can show both `errored` and `built` in the Pages build history. Confirm by checking whether the *live URL renders* and whether a retry builds green before hunting for a content bug.
- Ruby/Jekyll may not build locally in every environment (libyaml/psych issues); verify via the live site instead of assuming a local `jekyll build`.

## Git

- Commit/push only when asked. Co-author trailer:
  `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`
- The GitHub remote uses a stored credential at `~/.config/git/recipes-credentials`.
