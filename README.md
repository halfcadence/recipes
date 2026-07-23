# Recipes

https://halfcadence.github.io/recipes/

A recipe collection in a **Swiss-modernist / Müller-Brockmann** style: Helvetica only, **pure monochrome** (ink on paper, inverting to white-on-black — no accent or per-section color), a responsive modular grid, hierarchy from a fixed type ramp + weight, no illustrations. Recipe titles are a big lowercase type-as-image moment (the one Experimental-Jetset nod); the homepage is a full-width text-only archive. (History: a two-ink risograph look, then a per-section-color Experimental-Jetset phase — both retired.)

## Stack

Jekyll · GitHub Pages · self-owned CSS (no theme) · system Helvetica

## Layout

Three tiers: the published site, unfinished drafts, and repo-only planning that never ships.

| Path | What | Published? |
|---|---|---|
| `r/` | Recipes (one `.md` each, numbered) | ✅ site |
| `a/` | Articles (technique / ingredient essays) | ✅ site |
| `drafts/` | Unfinished/untested recipes + unlisted odds & ends. Reachable at `/drafts` (linked from the Colophon), **not** in the main index. | ✅ site |
| `assets/` | `main.scss` (the entire stylesheet) | ✅ site |
| `_layouts/` `_includes/` `_data/` | Jekyll templates + `photos.yml` (hero-photo registry) | build |
| `bin/` | dev checkers (`check-links.py`, `check-numbers.py`) — run before pushing | ❌ excluded |
| `index.md` | The homepage master list — a recipe/article is invisible until linked here | ✅ site |
| `steering.md` | **The rulebook** — voice, format, colors, the New Recipe Checklist. Read before editing. | ✅ (Colophon) |
| `changelog.md` | Dated log; updated in the same commit as any site change | ✅ (Colophon) |
| `cafe/` | A hypothetical canelé-café business plan + baking-science deep-dives + brand kit + a local review site. **Excluded from the build** (`_config.yml`) — repo-only, never published. | ❌ excluded |
| `.kiro/` | Kiro skills/specs, incl. the `batter-analysis` skill that is the source of truth for recipe Analysis blocks | ❌ (dotdir) |

## Adding a recipe

Follow the New Recipe Checklist in the [steering doc](https://halfcadence.github.io/recipes/steering/) — in short: `r/{slug}.md` with front matter (next `number`), a link in `index.md`, and a `changelog.md` entry. No illustration needed (recipe pages are type-only). Baking recipes also need an `## Analysis` block (via the `batter-analysis` skill).

Untested recipes live in `drafts/` (no `number`, `permalink: /drafts/{slug}`) until baked and proven, then graduate to `r/`.

## Local development

```
bundle exec jekyll serve
```

[GitHub's local-testing guide](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/testing-your-github-pages-site-locally-with-jekyll)

## Publishing

Push to `main` — GitHub Pages builds automatically.

```
git push
```

Conventions and gotchas for AI agents working in this repo: [`AGENTS.md`](./AGENTS.md).
