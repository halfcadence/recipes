# Recipes

https://halfcadence.github.io/recipes/

A recipe collection styled after risograph printing. Two inks — Blue (`#0078bf`) and Fluorescent Pink (`#ff48b0`). All other colors are overprints, tints, or blends of those two.

## Stack

Jekyll · minima · GitHub Pages · Bricolage Grotesque · Amazon Nova Canvas (illustrations)

## Layout

Three tiers: the published site, unfinished drafts, and repo-only planning that never ships.

| Path | What | Published? |
|---|---|---|
| `r/` | Recipes (one `.md` each, numbered) | ✅ site |
| `a/` | Articles (technique / ingredient essays) | ✅ site |
| `drafts/` | Unfinished/untested recipes + unlisted odds & ends. Reachable at `/drafts` (linked from the Colophon), **not** in the main index. | ✅ site |
| `assets/` | `main.scss`, `illustrations/*.svg`, `illustrations/gen-riso/*.png` | ✅ site |
| `_layouts/` `_includes/` `_data/` | Jekyll templates + `illustrations.yml` | build |
| `index.md` | The homepage master list — a recipe/article is invisible until linked here | ✅ site |
| `steering.md` | **The rulebook** — voice, format, colors, the New Recipe Checklist. Read before editing. | ✅ (Colophon) |
| `changelog.md` | Dated log; updated in the same commit as any site change | ✅ (Colophon) |
| `cafe/` | A hypothetical canelé-café business plan + baking-science deep-dives + brand kit + a local review site. **Excluded from the build** (`_config.yml`) — repo-only, never published. | ❌ excluded |
| `.kiro/` | Kiro skills/specs, incl. the `batter-analysis` skill that is the source of truth for recipe Analysis blocks | ❌ (dotdir) |

## Adding a recipe

Follow the New Recipe Checklist in the [steering doc](https://halfcadence.github.io/recipes/steering/) — in short: `r/{slug}.md` with front matter (next `number`), an SVG illustration + `_data/illustrations.yml` entry + a Nova Canvas riso PNG, a link in `index.md`, and a `changelog.md` entry. Baking recipes also need an `## Analysis` block (via the `batter-analysis` skill).

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
