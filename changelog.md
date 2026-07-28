---
title: Changelog
category: colophon
permalink: /changelog/
---

## 2026-07-28

- **GitHub Pages' Sass had been silently deleting a selector, and 70 recipes shipped broken for a day because of it.** The stylesheet is built on Pages by jekyll-sass-converter 1.5.2 → **Ruby Sass 3.7.4**, which predates `:has()`. Standalone it passes an unknown selector straight through, so `.a:not(:has(> .x))` at the top level is fine — but the moment it has to *rebuild* a selector, which is what nesting a rule inside a parent block (or using `&`) requires, it re-parses, chokes on `:has` inside `:not`, and emits the rule **with the whole `:not(…)` dropped**. No warning. Exit 0. Green build.
  - What that did: yesterday's no-Analysis notes rule went live as an unconditional `.post-content > #steps ~ .notes`, which ties on specificity with `> #analysis ~ .notes` and **wins on source order** — so all **70 recipes that have an Analysis** took the full-width 4-up band meant for the 47 that don't, and the notes text printed directly on top of the "analysis" head. Every geometric assertion in yesterday's sweep passed, because they all ran against a locally-compiled stylesheet. Only diffing the **live** CSS selector-by-selector against a local compile found it.
  - The fix is a form the compiler won't touch: both `:not(:has(…))` rules are now written out in full at the top level of their media block, and the step-split trigger is an interpolated string variable (interpolation is textual, never re-parsed). Confirmed by installing Ruby Sass 3.7.4 locally and compiling — the output is now **byte-identical to the previous live CSS apart from the intended changes**, and both `:not(:has(…))` survive.
  - **`bin/check-selectors.py`** flags any `:not(:has(…))` nested under a parent selector, and prints the exact Ruby Sass command to verify against the compiler Pages actually uses. It fails on yesterday's commit and passes on this one, so it isn't vacuous. Run it before pushing a stylesheet change.
  - Lesson worth the entry: "it compiled" and "it compiled *the same way the host will*" are different claims. Two different Sass implementations agreed with each other and both disagreed with production.
- **The ultrawide split is now decided by the recipe, not by the breakpoint.** An equal 12&nbsp;|&nbsp;12 spread assumed both halves are about the same height, and they aren't: ingredients are almost always shorter than steps, so the right column ran past the left by **256px on average and 783px at worst** (the chiffon cakes and gâteaux — 12 steps beside 10 ingredient lines) across all 124 recipes at 1881px. No single split fixes that, because the geometry that helps a 12-step cake hurts a 3-step cocktail. So the page picks: a recipe with **six or more steps** puts ingredients in an 8-track bay and runs the steps in **two columns** across the remaining 17; a shorter recipe renders exactly as before. Overhang drops to **114px mean / 336px worst**, and the recipes over 300px go from 38 to 1.
  - **CSS can count, so there's no script.** `:has(> #steps ~ ol > li:nth-child(6))` *is* "six or more steps" — I checked the selector against the real DOM step count on 124/124 recipes, and the group-count selector against the real table count on 124/124 too.
  - **The threshold is measured, not chosen.** Splitting at 4+ leaves the least empty paper (103px mean) but gives 27 recipes a column of only **two** steps, which doesn't read as a column — it reads as a widow. 6+ is the lowest threshold where that never happens: 0 thin columns at 1792/1881/2560/3440, 73 of 124 recipes split.
  - **Three or more ingredient groups opt out.** Groups stack, so each one adds height to the *left* half; past two groups the left half is the taller side and halving the steps opens a gap under the steps instead of closing one. Measured all three cutoffs: opting out at 2+ groups gives 126px mean / 420px worst, at 3+ gives **114 / 336**, and never opting out gives 121 / **521** (tonyu-nabe, three groups beside six steps, overshoots by 521px). 3+ wins on both mean and worst case. The census is 106 recipes with one group, 12 with two, 6 with three or more.
  - **`columns`, not a second grid.** A step list has to *balance* across the two columns (7 steps → 4 + 3) and only multicol does that without measuring in JS; multicol is also column-major, so visual order stays source order (asserted on every recipe at every width). The **reading measure does not move**: 26 tracks read as three 8-track bays (8 + 1 + 8 + 1 + 8), and one bay is 548px at 1881px — which is the 34rem every step was already capped at. The second column is free.
  - **The step number moves to the head of its step.** A right-hung number works in one column because nothing is to its right; in two, the next column's text sits 20px away and `01` reads as if it belongs to step 05. This was found by looking at a render, not by measuring — every geometric assertion passed on the version with the bug. Leading the step removes the ambiguity without spending measure on an alley (the alternative, one track of gutter between the columns, cost 34px of measure). Same convention the notes band already uses.
  - **Ingredients are not also split.** A single `<table>` won't fragment across a CSS column (measured: a 20-row table in a `column-count:2` box stayed one column), so the ingredient side could only divide at a group boundary — and doing that measured as a wash against today (167px vs 163px on the multi-group recipes) while cutting the step measure to 510px. Dropped rather than shipped for symmetry.
  - The `> *:has(~ #steps)` form is load-bearing for the same reason it is elsewhere in the file: a blanket `#ingredients ~ *` chain carries three IDs and outranks `> #steps ~ ol` at two, which dragged the step list into the left bay — 94 overlaps and the measure collapsed to 226px. The one-ID-beats-any-number-of-classes trap, third time.
  - Verified on the compiled stylesheet, not the source: all 124 recipes × 4 widths ≥ `$split` on five invariants (two columns, number leading its own step, source order = visual order, no overlap between any pair of blocks, no horizontal overflow) — 0 failures — plus a byte-comparison of every `.post-content` child's geometry old-vs-new at 390/768/1024/1440/1791, which is **identical on all 124** at every width, so nothing below the breakpoint moved. Dark mode checked on a split recipe.

## 2026-07-27

- Ultrawide follow-ups — two layout bugs in the spread that shipped an hour earlier, both caught on real pages:
  - **Multiple ingredient groups rendered stacked on top of each other.** A single `#ingredients ~ table { grid-row: 3 }` matched *every* following table, so tonkatsu's three groups (main / quick sauce / to serve) painted in the same row, and `grid-auto-flow: dense` backfilled their `###` subheads into the empty row 1 *above* the "ingredients" head. This was the common case, not an edge one: 24 recipes carry more than one table before Steps and 13 carry subheads. The left half now gets one row per block in source order, assigned by counting preceding siblings (`#ingredients ~ * ~ *…`) — which walks source order without caring what the elements are, the same reason the halves are assigned by `#id ~ *` rather than `nth-child`. Emitted shallow-to-deep so the deepest match wins. The `:has(~ #steps)` qualifier is load-bearing: without it the chain also matches `#steps`, the steps list, `.analysis` and `.notes` (all siblings of `#ingredients` too) and at (1,1,0) outweighs `.post-content > .analysis` at (0,2,0), dragging the right half and the superrow out of place — the same one-ID-beats-any-number-of-classes trap as the stranded notes. The sweep then turned up the mirror bug on the one recipe with **two** step lists (kombu-dashi: cold brew / simmer): both took `grid-row: 3 / span 60` and overlapped, so a recipe with a second list now opts out of the deep span and auto-places in order.
  - **The superrow separator sat on top of the last step.** Its 80px of air was *below* the rule rather than above it (the `.notes` base rule's top margin landed under the separator), so the hairline read as an underline on the steps instead of the top edge of a new band — 0px above, 81px below. The margin moves onto the rule's own row and the notes bind to it with the same 24px the Analysis head uses: now 80px above, 25px below, on every recipe.
  - Verified across all 124 recipes × 6 widths on two independent invariant sets — added no-overlap (every pair of blocks, not just tables) and source-order-equals-visual-order checks for the left half, plus air-above/air-below bounds on the separator — 124 pass · 0 fail. All twelve sample recipes fail those same checks against the shipped stylesheet, so the assertions aren't vacuous. One assertion from the earlier pass (`GAP-ING`) was itself wrong — it measured the head to the first `<table>`, which flags the *correct* layout on the 13 subhead recipes — and now measures the head to the next block; the bug it guarded is still covered by two other checks.
- **Ultrawide layout (≥ 112rem / 1792px)** — one recipe on one screen, and a directory that uses the whole monitor. The threshold is a single Sass variable (`$split`, top of `main.scss`) that three media queries read, so the breakpoint can be retuned in one place. It has to be Sass, not a custom property: `@media` can't evaluate `var()`.
  - **Grid:** `--cols` goes 12 → **26** at `$split` — two 12-column halves with a 2-track alley — so each half is the width the whole page used to be (12 tracks ≈ 71.6rem at 2560px ≈ the old 72rem ribbon). Below `$split` nothing changes; the existing 12/8/4 tiers are untouched.
  - **Home directory:** each category is now a **name | list pair** — the name hangs in a left margin and both hang from one shared *top* rule (a band edge, not an underline belonging to the name) — and this is the layout at **every** width above the phone tier, not just ultrawide. The page is full-bleed (`max-width: none`); the width freed by dropping the ribbon is exactly what buys the list more flow columns, so long categories (sweets = 51) grow in *width*, not height. At `$split` the directory pairs up into two page-columns reading "name list / name list". That's CSS `columns: 2` on `.dir`, not a grid: the browser balances the two columns so they end level, whereas a grid row is as tall as its taller half and the categories are wildly unequal (sweets 51 vs colophon 5) — pairing those in a grid leaves a hole the height of the difference. `break-inside: avoid` keeps a name from ever splitting off its list. The pair survives down to the phone tier, where the name column drops and it stacks.
  - **Recipe spread ("mise en place"):** ingredients LEFT, steps RIGHT, then analysis and notes side by side in their own band below both — a "superrow" separated by **one** hairline spanning both halves and the alley (the notes block's own shorter hairline is switched off; two rules 24px apart, one of them shorter, read as a mistake). Placement is driven by `h2` **ids** (`#steps ~ *`, `#analysis ~ *`), never `nth-child`: `.post-content` is a flat kramdown sequence whose shape varies — 118 recipes open with a table, 10 with an `###` subhead, 1 with a paragraph, 6 carry a Grind block, 53 have no Analysis — and any positional selector breaks on those. Steps keep their 34rem measure; the extra width buys a second column of *content*, never a longer line. The 47 recipes with notes but no Analysis take the full band 4-up instead of stranding an empty half. The hero photo becomes a fixed 30rem cinematic band (uncapped, a 16:9 figure is 1440px tall at 2560px — you'd scroll past a photo to reach the recipe the spread exists to fit on one screen).
  - **Article rail:** articles get a sticky contents list in the outer-left margin, built from their own `<h2>`s, with the section in view highlighted. The prose does **not** get wider — it keeps its 36rem measure and marginalia subheads; a two-column article body was rejected outright (prose that snakes up and back down a 2560px page is worse to read, not better). The same single `<ol>` renders as a **collapsed disclosure** above the standfirst on phones (≤34rem, 44px taps) and is hidden in between, where the marginalia subheads already show the structure. It ships `open` and is closed by script on the phone tier, not the reverse: a closed `<details>` hides its own content via UA `content-visibility` — which CSS can't override — so a default-closed element would render the ultrawide rail as a bare "Contents" label, and it also degrades correctly with JS off. Articles with fewer than 2 sections drop it entirely. Recipes get no rail.
  - Three bugs found and fixed by the verification sweep rather than by eye, all worth recording because each has a reusable lesson: (1) **grid rows couple the two halves** — column placement alone isn't enough, since both halves auto-place into the *same* implicit rows, so a standfirst offset one head and a 9-step list stretched whipped-cream's short ingredient table's row and left "ingredients" floating 380px above it; fixed with explicit rows, a deep `span` for the steps list, and `align-self: start` (an explicit row is also needed on each half's first block, because the `row dense` the superrow requires backfills empty row 1 and jumped the table *above* its own head). (2) **One ID outweighs any number of classes** — the no-Analysis notes fallback at (0,3,0) silently lost to `> #steps ~ *` at (1,1,0), so 47 recipes kept their notes pinned in the right half; adding `#steps ~` to the fallback buys the ID weight. (3) **A flat dark-mode override can't reach a nested rule** — `.art-toc { … }` (0,1,0) loses to the same rule nested under `body.section-articles` (0,2,1), which left `#111` hairlines on `#0c0c0d` paper at ~1.04:1, i.e. invisible; both new components are now authored against `var(--ink)`/`--grey`/`--hair`, which already flip with the scheme, so there's no override to lose. The article highlight also had to stop using the doc-nav's `IntersectionObserver` (its `-75%` top band is unreachable on a page shorter than ~2 viewports — and the rail is what makes articles that short, so the highlight stuck on section 2 of 5 for the whole second half of a 2560×1400 screen); it's a midline test with a bottom clamp instead.
  - Verified in headless Chrome across **all 124 recipes × 6 widths** (2560/1792/1791/1512/800/390) on nine geometric invariants — heads aligned, no block above its own head, no stranded half, one separator not two, no horizontal overflow, measure capped — plus real WCAG contrast ratios for every new rule and label in **both** schemes, and the phone disclosure's collapsed height and tap targets. Each new assertion was first proven to *fail* on the pre-fix stylesheet (the stranded-notes check: 47 fail / 77 pass), so the green isn't vacuous; two failures that reproduced identically on the live deployed CSS were confirmed pre-existing and left alone.
- Home index (touch tiers): the hairline under each recipe name no longer reads as underlining the row *below* it. Splitting the 44px tap target's padding evenly put the rule ~20px beneath its own word but only ~10px above the next one — at a 2:1 ratio it detaches from the name it belongs to and stops reading as an underline. The padding is now asymmetric and deliberately sums past 44px (`1.4rem 0 .3rem`; if the padding box is *shorter* than `min-height` the content box stretches and dumps the slack back under the text, so symmetric padding can't fix this): the rule sits 7.7px under its word, matching the desktop tier's 6.1px. All 149 index links stay ≥44px, and the phone tier's separate override is gone — it inherits the tablet rule. Cost: two-line entries grow 53→61px, so the phone page is ~2% taller.
- Fix recipe steps collapsing to a single ~80px column on five recipes (tea jelly, thyme streusel, cold brew tea, coffee jelly, bay leaf panna cotta). The step `li` was a 12-track `subgrid` and only `li > p` carried the `1 / -2` reading span — but kramdown emits `<p>` only for a **loose** markdown list (blank line between items). A **tight** list (`1.` / `2.` / `3.` on consecutive lines) emits bare `<li>text`, which becomes an *anonymous* grid item no selector can reach, so it auto-placed into column 1 and wrapped at ~46–88px instead of 538px. The `li` now owns two tracks (`minmax(0,34rem) auto`, `space-between`) so the measure is the track itself and the layout no longer depends on how kramdown wrapped the text; the step number moves from the `-2 / -1` span to track 2, and a ul nested inside a step spans track 1 rather than the parent grid's line 9. Verified in headless Chrome at 1512/800/390px: the five affected pages go from 3–5 wrapped lines to 1, four control pages (gyoza, canelé + two articles) are geometrically byte-identical, and the phone tier — which was never affected, its `ol` having always had two tracks — is unchanged.

## 2026-07-24

- Responsive / mobile pass (adversarial persona-panel review — mobile-first user, a11y/junior, design director, typographer, minimalist, Ive/Rams reductionist, perf engineer):
  - **Ship-blockers:** home masthead is now `flex-wrap`'d ≤34rem with the byline dropping to its own line (was a no-wrap flex row that forced a horizontal scrollbar on every portrait phone — WCAG 1.4.10); article-table `white-space:nowrap` is gated to ≥34rem so prose tables wrap on phones instead of blowing past the viewport; the dark-mode focus outline is recolored to dark ink (was `#111` on `#0c0c0d` ≈ 1.05:1, effectively invisible — WCAG 2.4.11); the hero photo is no longer `loading="lazy"` and carries `fetchpriority="high"` (it's the above-the-fold LCP element, so lazy-loading it delayed LCP).
  - **Mobile UX:** the recipe step-number column is narrowed from a full 1fr (~25% of a 4-col row) to a 2rem track ≤34rem, reclaiming ~54px of reading measure while keeping the far-right number; hero-title leading loosened to 1.02 + `text-wrap:balance` ≤56rem so long lowercase titles stop colliding descenders/accents into the next line at the clamp floor; home-index tap targets (44px) now extend through the tablet tier (were phone-only).
  - **Polish:** `.wrapper` side padding drops to 1rem ≤34rem (was a fixed 1.75rem = 17.5% of a 320px screen); `preconnect` to `images.unsplash.com` to shave ~300–600ms off hero LCP on 4G; the wide comparison table's row-label column is now `position:sticky` so metric labels stay visible when scrolling right; `.grind`/`.analysis` pinned full-width at 4-col (were spanning to grid lines 9–10 that don't exist there); `.grind` setting column wraps on phone; `.notes h2` moved from `display:none` to visually-hidden so screen readers still announce the section.
  - **Cleanup:** delete the dead `.pill-sample::before` rule (nothing set `data-num`); remove the empty `_includes/footer.html` and its per-page include; stop tracking the generated `cafe/site/*.html` build output (the `build-review.js` generator + `today-sheet-setup.md` source stay tracked).
  - **Follow-ups (verified in DevTools mobile emulation at a true 390px):** pack the home index 2-up ≤34rem — `columns:12rem` collapses to a single column at phone width, so the directory (sweets = 51) was an endless single-file scroll; two even columns roughly halve the page height. Make bare (non-`.wide-table`) article tables their own `overflow-x:auto` block ≤34rem — gating `nowrap` wasn't enough because a 4–5-column table's min-width still beat the screen (canele-bags overflowed the *page* to 563px, packing-caneles to 425px; both now 390px, no page scroll). Confirmed live: masthead no longer overflows, the longest title ("big-batch hong kong milk tea canelé") wraps to 3 lines with leading 42.4px > cap 41.6px (no glyph collision), the wide-table row-label column stays pinned when scrolled, and the dark-mode focus ring is now 17.4:1 (was ~1.05:1).

## 2026-07-22

- Homepage masthead: remove the heavy 3px rule under the wordmark — it was the only 3px divider on an otherwise-1px-hairline site. The giant wordmark + whitespace carry the separation now (Ive pass, chosen from a 6-option chooser).
- Homepage: remove ornamental category index numbers (01–08) — the category name carries the meaning; order is visible from position.
- Minimalist cleanup pass (delete unused / dead / outdated / leaked):
  - **Security:** remove `docs/` (9 internal Amazon engineering docs — BYOD/Stencil/Stores-Designer, a CSS-race postmortem, env-ID files) and `byod-cr-explainer/` — both were committed to this **public** repo AND publishing to `halfcadence.github.io/recipes/docs/…`. Gitignored + excluded so they can't return. Also excluded `bin/` (dev tooling) and `.playwright-mcp/` from the build.
  - **Junk:** remove `.playwright-mcp/` (83 browser-tool debug logs, 11MB) + gitignore it.
  - **Retired archive (~50MB, the bulk of the repo):** delete `assets/illustrations/` (249 SVG + AI-riso PNG files), `_data/illustrations.yml`, and the `/illustrations` + `/illustrations-riso` + `/colors` gallery pages — all delisted (reachable from nowhere in the nav), preserving a retired risograph/EJ system. The risograph *article* stays as the record. Fixed the now-dead references in type.html, steering.md, AGENTS.md, README.md and the dead swatch selectors in the print CSS.
  - **Vestigial config:** drop `instagram_username` and `header_pages: []` (zero consumers).
  - **Outdated docs:** README + colophon prose still described the retired Experimental-Jetset "one accent per section" system as current — corrected to monochrome Müller-Brockmann.
- Second review pass (finish the remaining audit items):
  - **Per-page descriptions:** each page now gets a unique meta/share snippet instead of the shared tagline — explicit front-matter `description:` wins, else a synthesized line (recipes: "title — a {category} recipe … No. N"; articles: a note line), else the site default. Documented the `description` field in steering's Front Matter; added a real one to the canelé article.
  - **Tokens:** expose the Sass palette + type ramp as CSS custom properties (`--ink`, `--fs-cat`, …) on `:root` with a dark override, and convert the `type.html` / `photos.html` inline styles to `var(--…)` — so their chrome stays on the ramp and dark mode flips automatically (deleted both pages' per-page dark blocks). Swatch/ramp-demo values stay literal (they're content).
  - **A11y:** byline links (`halfcadence` / `gh`) now carry a persistent underline, not color/weight alone (WCAG 1.4.1). Add PNG + apple-touch favicon fallbacks alongside the SVG.
  - **Steering doc nav:** hide the sticky section nav when a `toc` page has no `<h2>`s (was an empty labeled landmark); prefix auto-ids `toc-h-`; fix the nav floating ~24px above the body — its first row now aligns to the lede.
- Adversarial review fixes (design-director / nitpicky / junior / CEO personas + technical audit):
  - **Sharing:** replace the broken `og:image` (a relative-URL SVG that no platform renders) with a real 1200×630 PNG served at an absolute URL; a recipe now shares its own hero photo, others share the site card. Add `twitter:card: summary_large_image` + `twitter:image`. Switch `jekyll-feed` → `jekyll-seo-tag` (recipes are pages, not posts, so the RSS feed was empty/dead) and rewrite the site description, which still read "two inks, eight colors" (the retired riso identity) on every page.
  - **Print:** scope the dark theme to `screen` so a recipe printed from a dark-mode OS is black-on-white, not near-white-on-white; hide the hero photo when printing; narrow `print-color-adjust: exact` to the archived riso swatch pages only.
  - **Copy/detail:** fix the breadcrumb rendering "Soups & hot pots" (a `capitalize` filter was lower-casing the tail) → "Soups & Hot Pots"; remove a stray "." (an unstyled `---`) on the canelé article and add a proper `hr` hairline rule; recolor the 404 spot-blue to monochrome grey.
  - **A11y:** make the home wordmark an `<h1>` (was none); add `aria-label`s to the "gh"/personal-site byline links; fix light-mode caption contrast on `/photos` (`#9a9a98` → `#6b6b6b`, ~2.8→5.3:1).
  - **Mobile/perf:** single-column ingredients on phones (was cramped 2-col at 390px); ~44px tap targets on the home index; responsive hero `srcset` + `width`/`height` so phones don't fetch the 1600px image.
  - **Housekeeping:** remove dead CSS (`.post-title--plain`, `.num`/`%num`, the `$serif` alias, the undefined `.cat--wide` class) and the orphaned `og-image.svg`.
- Add `bin/check-numbers.py` — validates the recipe `number:` sequence (every `r/` page numbered, contiguous 1..N, no gaps/duplicates) and prints the next number to assign. Wired into AGENTS.md; current sequence is clean (1..124).
- Homepage recipe count: compute the masthead "124" at build time from the number of pages in `r/` instead of hardcoding it, so it can't drift out of sync when recipes are added. Renders identically (124) today. Documented in steering.
- Homepage byline: give the flat, unlinked "by / halfcadence" more weight and make it useful — now `by halfcadence / gh` on one baseline, with **halfcadence** linking to andrewshiau.com (ink) and **gh** to github.com/halfcadence (grey). The two external links open in named tabs (`target="halfcadence-site"` / `halfcadence-gh"`, `rel="noopener"`) so repeat clicks reuse one tab. Masthead wordmark + count unchanged.
- Add `bin/check-links.py` — validates every internal link (index `./` anchors + `relative_url` body links) against real files and declared permalinks; documented in AGENTS.md as a pre-push check. Full audit run: all internal links resolve.
- Remove `type-comparison.html` — a dead, unlinked colophon page that still described the retired Bricolage Grotesque type system (site is Helvetica-only now). Nothing linked to it.
- Header: fix the nav/category "stutter" — the top-bar "← index" kicker and the category eyebrow ("MAINS") directly below it were the same grey uppercase 11px label stacked, reading as a duplicate. Fold the category into the nav as a breadcrumb (`← index / mains`, index grey + category ink) and drop the separate `.section-label` eyebrow. Applies to all inner pages (recipes, articles, colophon).
- Fix 38 broken internal links in Drafts — the drafts index and all 6 draft pages used bare `](/drafts/…)` / `](/r/…)` / `](/a/…)` paths, which drop the `/recipes` baseurl and 404 on prod (e.g. the P-Bass Mute and Ttukbaegi links, the "recipe index" link). Wrap them all in `relative_url`. (`r/` and `a/` were already clean; `drafts/` had been missed.)
- Type: rationalize the ~9 ad-hoc small font-sizes into one Swiss ramp — "Univers Stepped": 11 / 13 / 15 / 21 / 26 / hero, as `$fs-*` tokens. Every `font-size` now references a token (no hardcoded px/rem). `/type` and `/photos` pages updated to match.
- Steering + AGENTS: correct the house-style description — the site is **Swiss-modernist / Müller-Brockmann grid**, monochrome (no accent, no per-section color), not the "Experimental Jetset + per-section accent" the doc still claimed. The `$sections` color map and accent are gone; documented as retired.
- `/photos` page restyled to the monochrome system + type ramp (26px category heads, 13px/11px steps, hairline "no photo" box instead of the old striped gradient; drop the monospace `<code>`). Also fixed the root cause it exposed — the page had no `layout:` front matter, so it shipped as raw serif with no CSS; added `layout: page` and an AGENTS.md guard requiring every `.html` page to declare a layout.
- Steering page: give it a proper reference layout (`toc: true` → two-column in `_layouts/page.html`): a sticky left nav auto-built from the section `<h2>`s (scroll-spy highlights the current section) and the body in a ~40rem reading measure. De-boxed inline code in doc bodies (faint fill, no hard border — the recipe chip was too noisy across a code-dense doc) and tightened the section-head rhythm. Collapses to one column under 46rem.
- Header: inner pages now show a minimal left-aligned "← index" back link in column 1 instead of the right-aligned "RECIPES BY HALFCADENCE" wordmark (the home masthead is unchanged).

## 2026-07-21

- Photos review page (`/photos/`, in Colophon): every recipe grouped by category with its hero photo or a striped "no photo" marker + per-category coverage count. Mirrors the registry resolution so it's an accurate at-a-glance audit.
- Recipe photos: drop the per-category fallback (no photo is better than a wrong/generic one — a tortilla on the steak page). A recipe not in `_data/photos.yml` (and with no front-matter `image:`) shows no hero. Add verified per-dish photos as they're found (16 so far: purin, gyoza, cherry pie, matcha latte, tortilla, prime rib, canelé, old-fashioned, margarita, tonkatsu, chocolate gateau, iced pour over/aeropress, mojito, banana bread ×2). Steering + AGENTS updated to the no-fallback rule.
- Recipe photos: add a full-width 16:9 hero photo to every recipe via a two-layer registry (`_data/photos.yml`) — `specific:` per-slug verified photos win, else a per-category fallback so no page is imageless. `_layouts/page.html` resolves front-matter `image:` → specific → category. Verified per-dish photos for purin, gyoza, cherry pie, matcha latte, tortilla; verified soups/sides/pantry fallbacks. Document the system + the find/verify procedure in steering.md ("Recipe Photos") and AGENTS.md; clarify the "no illustrations" rule means no drawn/riso art, not no photos.
- New article: "Photographing Food at Home" — one-window/diffuse/fill/angle/settings/styling/edit, in the marginalia-subhead article layout. Listed under Articles.
- Analysis block restyled to the rule-free L2 (steps-pattern) layout: label · grams (small grey) · % far-right, no borders/header — was a bordered table that read as bolted-on; the ingredient-table transform was also over-matching it (and article data tables) and causing overlap. Scope fixed. Analysis now precedes Notes site-wide (reordered 14 recipes).
- Drinks: add by-weight analysis to all 26 (cocktails: ABV/sugar/dilution; coffee/tea brews: brew ratio + grounds retention; milk drinks: composition).
- Redesign (monochrome Müller-Brockmann grid): single typeface (Helvetica; dropped the serif accent), responsive 12/8/4 grid, home wordmark + count + cQ category heads as full-width bands, hero recipe number on the baseline, notes as 3 equal footnote columns (flush-left, no jut), black 3×3 grid favicon, colophon delisted (Colors/Type-Comparison/SVG+Riso illustrations).

- Banana Bread: rescale the base to a full, tall 9×5 loaf (×1.3, now 3 whole eggs). Ingredients up proportionally (banana 340→442g, flours 96→125g each, etc.); recompute analysis (1232g batter — ratios unchanged: fat 13.1%, sugar 20.0%, structure 21.8%, banana ~36%). Bake time now ~55–70 min for the single tall loaf; the deep-6×3 and 6×2 rounds move to a "scaling down" note.
- Fix broken internal cross-links site-wide. Recipe/article body links written as `[text](/r/slug)` rendered as root-absolute `/r/slug`, dropping the `/recipes` baseurl and 404'ing (e.g. the flan's "Related custards" links). Wrap all 72 such links across 26 files in Jekyll's `relative_url` filter (`[text]({{ '/r/slug' | relative_url }})`), which prepends the baseurl → `/recipes/r/slug`. Index links already used relative `./` paths and were unaffected. Verified live via a real browser click (flan → Purin resolves).
- Add a rule to steering (and AGENTS.md) requiring body-text cross-links to use `relative_url` rather than a bare `/r/slug`, so the baseurl bug doesn't recur.
- Flan Pâtissier: sharpen the cream note — all-milk is the classic and is rich enough (yolk fat + ~5% starch); quantify the optional cream upgrade (~100–170g / up to ~20% of the dairy, since cream fat inhibits the set past that) and keep the mascarpone variant.

## 2026-07-12

- Add Bakery-Style Banana Bread recipe (Eric King / easygayoven) — the American bakery-loaf counterpart to the Yoshida base: butter *and* oil, granulated + brown sugar, Greek yogurt, both baking soda and powder, mixed by the muffin method (melted butter, no creaming) for a light, tender, open crumb. Analysis (1237g batter): fat 13.0%, sugar 26.7%, structure 24.7%. Notes cover measuring the banana, temp-based doneness (200–205°F), yogurt/cream/milk swaps, and why melt-and-whisk keeps it loose. SVG + riso PNG (two offset squares, blue/pink overprint).
- Banana Bread: loosen the base toward a moister, more open crumb. Fold in 30g neutral oil, 40g heavy cream (or milk), and 4g baking powder alongside the soda; bump both flours to 96g each (192g total) for structure. Recompute analysis (936g batter: fat 9.1→12.9%, banana ~40→~36%, structure held ~22%). Rewrite the intro, the soda-only note (now soda + powder), and the keeps-poorly note to match; drop the earlier standalone "looser variation" note now that it's the default.
- Add Flan Pâtissier recipe — the Parisian custard tart: a cornstarch-and-egg-set vanilla custard cooked like a pastry cream (boiled to kill the yolks' amylase), poured hot into a raw (not par-baked) pâte brisée shell, baked hot for the dark blistered top, then chilled overnight. No par-bake needed — the set custard carries little free water and the long hot bake cooks the base; keep it crisp by freezing the shell hard, pouring the custard hot, and using a metal ring (par-bake given as optional insurance). Sized for an 8×2-inch tart ring; the custard uses the one-pot cold-start method (everything whisked cold and boiled, no tempering — Stella Parks-endorsed, and even safer since the flan bakes again); a real vanilla bean can go straight into the cold pot (seeds + pod, no separate steep) since it comes to a boil anyway. Notes cover the boil-the-custard rule, chasing the dark top, and a mascarpone-enriched variant. Analysis on the custard only (crust excluded). SVG + riso PNG (pink slice, blue dark top).

## 2026-07-10

- Add "Ripening Bananas" article — the ethylene/starch→sugar science, and the honest ranking of ripening methods: counter-ripen (best) and frozen-already-ripe, paper bag (~1–2 days), and the oven/microwave shortcuts that soften but barely sweeten. Busts the apple-in-the-bag myth. Linked from the Banana Bread recipe's ripeness note.

## 2026-07-09

- Add Banana Bread recipe (Morihide Yoshida) — baking-soda-leavened, pound-cake-style, ~40% ripe banana. Translated from the original (cassonade → light brown sugar; 中強力粉 medium-strong flour → all-purpose, blended 1:1 with cake flour for a tender-but-sturdy crumb), with scaling for a 6-inch round or 9×5 loaf and a serving-as-cake note. Notes cite Yoshida's original 180°C/35min in two small shallow pans and explain the single-deep-pan adaptation (drop ~25°F, ~1.5–2× the time), plus oven-without-340°F options (325°F straight, or 350°F→325°F). SVG + riso PNG (blue loaf, pink dome).
- Add Cherry Pie recipe — easy fresh-cherry pie in a store-bought crust. Cornstarch thickener sized for juicy fresh fruit (32g sweet / 40g sour), sweet-vs-sour sugar and acid adjustments, hot-start-on-a-preheated-sheet-pan for the bottom crust (no blind bake), the bubbling-center doneness cue, and full cool-down to set. Reduce the macerated juice on the stove before filling (a reliable anti-runny step). Corrected the whole-cherry buy weight to ~2.25 lb (10–12% pitting loss). Adds a cast-iron skillet method (Field No. 8: ~1150g cherries scaled up, assemble cold, move up a rack at 375°F; bake directly in a seasoned pan, clean and re-oil after). Analysis on the filling only (crust excluded, per French Silk Pie / Tarte Tatin precedent). SVG + riso PNG (pink pie circle, blue slice wedge).

## 2026-07-08

- Add Whipped Cream recipe — the three-stage lift-and-look test (soft/medium/stiff), cold-everything rationale, over-whip rescue (fold in cold cream), and stabilizer options. Leads with the hand mixer (deep chilled bowl, start low then medium-high) as the everyday tool; immersion blender, stand mixer, whisk, food processor, and jar-shake given as alternatives. SVG + riso PNG (blue circle base, pink triangle peak).
- Gateau au Chocolat: tune the dark version moister (it ran drier/firmer than the matcha sibling). Milk 90→100g, Dutch cocoa 18→12g (fewer liquid-absorbing solids), and add 1 extra egg yolk for fat + emulsification; flour held at 20g on purpose (it's the binder, not a moisture lever). Recompute analysis (519g batter: structure 13.5→11.8%, liquid 40.2→42.4%). Notes: why cocoa/dark chocolate dry the crumb, the more-chocolate-punch alternative (raise cocoa + milk, or higher-fat cocoa), and why butter is a weaker moisture fat than yolk/oil.

## 2026-07-06

- Purin: bump the caramel to 100g sugar (from 70g), water scaled to 20g + 20g. Gives a thicker, saucier amber layer — enough to pool nicely when unmolded, and better suited to a wide single pan (e.g. a 6-inch round) where the caramel spreads thin.

## 2026-07-02

- Chocolate Mochi Canelé: fix the layer-yield mismatch — the chocolate layer is the full Ferrandi batch (~1007g, ~24 molds) but the mochi was sized for ~12, leaving a big chocolate surplus. Double the mochi (whole egg now, no weighing half an egg) so both layers finish together across 24 molds (~20g mochi + ~42g chocolate each). Yield 12 → 24; note the fuller ~21-mold option.

## 2026-06-30

- Add Big-Batch Hong Kong Milk Tea Canelé and Big-Batch Thai Tea Canelé (24-mold scale-ups of the tea canelés, ×2.2 with eggs snapped to whole counts; the Thai version pushes evaporated milk to ~36% of the dairy for a fuller cooked-milk body). Both note full-tray oven handling and a condensed-milk experiment arm.
- Add a Drafts page (/drafts, linked from Colophon) — untested recipes (the three Thai tea canelés + the Thai iced tea drink) now readable on the site, kept out of the main index until baked and proven.
- Move the two unlisted pages (P Bass Foam Mute, Ttukbaegi Comparison) into /drafts and list them there; the ttukbaegi permalink moves from /ttukbaegi to /drafts/ttukbaegi.
- Add README architecture map + an AGENTS.md documenting repo conventions (both build-excluded).
- Add "Cream in Custards" article — what replacing milk with cream does to a custard/canelé: richer then greasy past a point, browns faster (bake the second stage ~15–25°F cooler), sweet spot is swapping ¼–⅓ of the milk.
- Add "Condensed Milk" article — what it is vs evaporated milk, the DIY evaporated-milk-plus-sugar substitute, and the sugar-subtraction rule for baking with it (cut ~0.55g sugar per g condensed milk). Companion to the Evaporated Milk article.
- Evaporated Milk article: add a "why cook milk twice?" section — the custard cook (structure) vs the can's retort cook (caramel flavor) are different jobs; the double cook is the backbone of flan/leche-flan/tres-leches, worth it only when you want the cooked-milk note.

## 2026-06-29

- Big-Batch Canelé: add non-convection-oven troubleshooting for a full 24-mold tray — preheated baking steel (the key fix), 550°F start, stop opening the oven to fight mushrooms, rotate-once-late, and the bake-12-at-a-time fallback.
- Big-Batch Canelé: clarify start-temp logic — 550°F is a no-steel compensation; with a steel set ~475–500°F instead (don't stack 550 + steel = scorched bottoms). And you can't bake low-only (350–375°F) — caramelization needs a ~320–340°F surface, which a low oven can't drive past the wet-surface 212°F plateau.

## 2026-06-26

- Earl Grey and Thai tea canelés: made alcohol-free. The spirit was aromatic, not structural, so Cointreau → orange zest + bergamot extract, and rum → added vanilla + a little more tea, each replaced gram-for-gram with milk to hold the batter balance. Original boozy versions noted inline.
- Canelé: add an all-flour (traditional, no-cornstarch) option note — the cornstarch is a deliberate tweak toward a softer crumb, not a requirement.
- Add "Buying Bags for Canelés" article — waxed/glassine/kraft single-and-pair bags ranked by fit, cost (~$0.03–0.16/bag), and stamp-friendliness; companion to Packing Canelés.
- Bags article: add a "Stand-up & flat-bottom bags" section — flat-bottom/SOS box bags and roll-top triangle bags that stand on a stall table, with the base-dimension sizing rule and closures.
- Bags article: add a "Boxes & the elevated tier" section — giftable stock boxes (ballotin, rigid, drawer, window), the honest custom-print MOQ/cost reality, and the recommended middle path (stock box + riso sticker/belly-band).

## 2026-06-25

- Add galbi recipe (traditional Asian-pear marinade for LA-cut short ribs, grilled over high direct heat on a gas grill).
- Steering: correct the Nova Canvas riso-PNG profile to `shiauas-personal` (the old `personal` profile's creds were stale).

## 2026-06-22

- Add steeping tea into milk article (infusing without throwing off ratios; steep-and-measure-back; scales to any batch; what tea to buy with links).
- Tea canelés: steep tea in milk only, then weigh and measure the strained milk back to a clean 340g base; corrected absorption estimate to an honest 2–4× range.

## 2026-06-07

- Add savory canelé recipe (canelés salés — bacon, Comté, caramelized onion; sugar slashed).
- Add evaporated milk article (what it is, baking uses, ratio-neutral substitution).
- Add Earl Grey, Hong Kong milk tea, and Thai tea canelé recipes (tea-infused variants of the custardy canelé).
- Add big-batch canelé recipe (custardy canelé scaled to fill 24 molds).
- Add packing canelés article (gift-box sizing from 1 to a full batch, with sourcing links).
- Add chocolate soufflé recipe (Robuchon's 3-ingredient version via Chris Young, Swiss meringue, no flour).
- Add black tea pudding recipe (water-bath baked tea custard with Calvados).
- Rename canelés: the custardy recipe is now "Canelé" (the default), the full-flour one is "Cakey Canelé".
- Add cream far breton recipe (cream-rich, canelé-like, deeply caramelized; sized for the Field No. 8).
- Add cherry buckle recipe (leavened coffee-cake batter, cherries, streusel top — the cakey counterpoint to the clafoutis family).
- Add The Field No. 8 skillet article (cast iron care, seasoning, the acid problem, recipes sized for it).
- Add sour cream cherry clafoutis recipe (Ishikawa — custard-end of the clafoutis family, ~3% flour).
- Add chocolate mochi canelé recipe (hybrid: butter-mochi base + chocolate canelé top).
- Add cherry far breton recipe (dense, sliceable cousin of clafoutis).
- Update cherry clafoutis: swap 10% of milk for cream (tested), add analysis section.
- Update custardy canelé: tested bake (525°F shock → 375°F 50–55min), nonstick spray works.
- Update crispy butter mochi: hot-shock method to control ballooning, lighter-version note (baking powder, tapioca).
- Add ingredient ratio analysis sections to all 26 baking recipes (% by weight of fat, sugar, structure, liquid, protein) with texture benchmarks — a teaching feature for learning how ratios drive texture.
- Add `.analysis` styled block, batter-analysis on-page format, and steering convention for the analysis sections.
- Add tteokbokki recipe (spicy rice cakes with anchovy-kelp stock).
- Add kimbap recipe (seaweed rice rolls).
- Add Eric Kim matcha latte cookies recipe (matcha cookie with ermine frosting).
- Add Vietnamese coffee marble cookies recipe (creamed drop cookie, espresso + condensed milk swirl).
- Add matcha shortbread recipe (slice-and-bake, low-temp to keep the color bright).
- Add custardy canelé recipe (half batch ~12, lower flour + cornstarch for a silkier set).
- Add crispy butter mochi recipe (Shanghai-style, baked in canelé molds).
- Add cherry clafoutis recipe (sized for the Field No. 8 skillet).
- Add eggnog canelé recipe (nutmeg, cinnamon, clove, bourbon).
- Add white chocolate matcha canelé Ferrandi recipe (higher flour to compensate for white chocolate's lack of cocoa solids).
- Add spirits in baking article (pairing matrix, spirit decomposition, test results).
- Add batter analysis skill (fat/sugar/structure/liquid/protein decomposition with benchmarks).
- Update chocolate canelé Ferrandi: increased flour, tested bake schedule (450°F/10min + 375°F/50min), cover technique, Dutch cocoa substitution note.
- Update chocolate canelés: default to brandy/cognac (tested better than rum).
- Add salt to all canelé recipes (Marchal ratio).

## 2026-06-01

- Add miyeokguk (Korean seaweed soup) recipe.
- Add Japanese beef curry (lazy frozen veg version) recipe.
- Add cucumber tea sandwiches, watercress tea sandwiches, ham & cheese tea sandwiches recipes.
- Add tamago sando (Japanese egg salad sandwich) recipe.
- Add ankake don (thick dashi sauce rice bowl) recipe.
- Add ume highball recipe.
- Add chocolate canelé recipe (Marchal-adapted).
- Add chocolate canelé Ferrandi recipe (low-flour, intense chocolate).
- Add white chocolate matcha canelé recipe (experimental).
- Add canelé ratio analysis article.
- Add ttukbaegi comparison page (unlisted).
- Add shopping list generator skill.
- Update canelé recipe: simplified method, AP flour, tested bake schedule (475°F/11min + 350°F/50min), flavor notes (matcha, hojicha, coffee).
- Update nicoise salad: fresh seared tuna, jammy eggs, remove tomatoes.
- Update gamjatang: siraegi/yeolmu prep instructions, watercress note.
- Update samgyetang: donabe serving note.
- Update potato salad: sando filling note.

## 2026-04-29

- Add AeroPress filters article (paper vs metal vs cloth, flavor profiles, stacking technique).
- Add coffee syrup pantry recipe.
- Add gamjatang (pork neck bone soup) recipe.
- Add samgyetang (ginseng chicken soup) and yukgaejang (spicy beef soup) recipes.
- Add reheating frozen bread article.

## 2026-04-23

- Add segmented color bar header on unthemed pages (all 8 section colors), solid on themed.
- SVG illustrations gallery now auto-discovers files with shape descriptions from `_data/illustrations.yml`.
- Add new recipe checklist to steering.
- Remove non-actionable notes across 7 recipes. Add actionability rule to steering.
- Add iced AeroPress, strawberry milk, French silk pie, simmered potato and chicken recipes.
- Add 76 AI-generated riso illustrations via Amazon Nova Canvas. New `/illustrations-riso/` gallery page.
- Add illustration generation rules to steering (SVG + riso PNG pipeline).
- Riso illustrations used as centered footer stamp on recipe pages (PNG preferred, SVG fallback).
- Minimal 2-shape SVG illustrations for all recipes with self-documenting gallery.
- Same-color overprint technique via paper background rect.
- Per-section colored favicons. Custom `<title>` with `·` separator.
- Favicon, OG image, 404 page, pill hover, RSS cleanup, sitemap.
- Selection color per section theme.
- Paper background `#fbfaf8`. Bump base font to 1.0625rem. A11y contrast fixes. Focus-visible outlines.
- Thicker 1rem top border. Print stylesheet.
- Misregistered overprint instagram pill on about page.
- Switch active palette to Blue + Fluorescent Pink overprint. Previous spot-color palette to first alt.
- Move overprint palettes from riso article to colors page. Consolidate color catalog into single table.
- Rename Port Tonic, Suze Tonic. Restore Acid-Adjusted OJ title.
- Add section breaks to homepage index with toggleable block layout.

## 2026-04-21

- Add 11 overprint palette explorations to riso article (1–3 base inks, overprints, tints, split-color treatments).
- Make riso article swatch pills full-width in their table cells.
- Expand riso color catalog from 12 to 77 colors in the risograph article, organized by hue family.
- Add Riso Overprint palette (Blue + Fluorescent Pink two-ink constraint) to colors page.
- Add shaken black tea (Taiwanese 泡沫紅茶).
- Add 3 coffee recipes: pour over (Tetsu Kasuya 4:6 method), iced pour over (Japanese flash brew), Hario Switch, AeroPress — with grind settings for Remi and Lagom Mini 2.
- Add grind settings to coffee manhattan.
- Correct grinder settings to official units: Lagom Mini 2 uses dots from zero, Remi uses revolutions.
- Add 2 articles: Dialing In the Remi, Dialing In the Lagom Mini 2.
- Rename "Style Guide" section to "Colophon".
- Add changelog page with full reverse-engineered history. Add changelog rule to steering.
- List base recipes before variants in index.
- Distinguish technique modifiers from flavor modifiers in naming rules. Add 7 recipes: steak au poivre, corn soup, kinpira gobo, ohitashi, potato salad, highball, yuzu highball.
- Add riso color rules to steering.
- Distinguish technique modifiers from flavor modifiers in naming rules.
- List base recipes before variants in index (highball → yuzu highball, gateau au chocolat → matcha/orange/hojicha/vanilla, brownies → matcha brownies).
- Rename Chocolate Gateau au Chocolat → Gateau au Chocolat.
- Rename Porto Tonico → Port Tonic, Suze & Tonic → Suze Tonic.
- Simplify 27 recipe and article titles: drop technique modifiers, parenthetical descriptions, chef names, article subtitles.
- Add naming rules to steering.
- Riso-derived dark mode: all grays derived from Midnight and Light Gray inks. Themed pages keep section colors in dark mode. Articles section uses lighter Midnight variant.
- Fix notes heading/body color mismatch in dark mode.
- Note dividers use neutral grey instead of theme color.
- Riso article color table uses pill-style hex swatches with colored backgrounds.
- Fix hardcoded grays in type-comparison and colors pages for dark mode.
- Body text uses Midnight (#435060) in light mode instead of minima default.
- Add steering page (published style guide). Kiro steering doc references it as source of truth.
- Drop numbers from style guide and article pages.
- Allow new categories in steering doc.

## 2026-04-20

- Switch to authentic Risograph ink colors from stencil.wiki.
- Add article: Risograph Printing and Color.
- Add Style Guide section to homepage (colors, typography, type comparison).
- Make section labels clickable — navigate to homepage anchor.
- Add recipe numbers (#001–#063) to all recipes.
- Hang step counters in left margin as monospace notes.
- Switch notes to tight vertical stack with thin separators.
- Apply inverted pill style to index section titles with auto-numbered counters.
- Convert all px values to relative units (rem/em).

## 2026-04-19

- Add gyoza, matcha brownies, chocolate brownies, Robuchon mashed potatoes, mentsuyu, ponzu.
- Add coffee manhattan, porto tonico, suze & tonic, lillet spritz.
- Add gimlet, manhattan, old fashioned.
- Add tonjiru, sukiyaki, ishikari nabe, tonyu nabe.
- Add awase dashi, ushiojiru, kombu dashi, clam miso soup.
- Add salade niçoise, nitsuke, chawanmushi.
- Add tarte tatin, purin.
- Add acid-adjusting juice article.
- Add whiskey sour, acid-adjusted OJ variant, tonkatsu.
- Add tortilla española and lazy version.
- Add karaage, prime rib, thin burgers.
- Reorganize index from 11 categories to 7.

## 2026-04-18

- Add 6 recipes: pickled cabbage, pickled daikon, margarita, mojito, corpse reviver no. 2, tinto de verano.
- Standardize all recipes to table format and grams.
- Use oz for cocktail measurements.
- Use Bricolage Grotesque font.
- Brutalist typography: uniform text size, bold headings, inverted pill titles.
- Brutalist header: border-top, no nav, "recipes by andrew".
- Remove footer. Combine title and attribution in header.
- Add dark mode support.
- Convert all temperatures to Fahrenheit.
- Unify formatting across all recipes.

## 2026-04-17

- Add brown butter hojicha white chocolate cookies.
- Add orange chocolate and hojicha gateau au chocolat.
- Add vanilla bean gateau au chocolat with brown butter.
- Add matcha americano and matcha latte.
- Add article: salt percentages in baking.
- Bump salt across gateau and cookie recipes.

## 2026-04-16

- Add chocolate gateau au chocolat.
- Add earl grey chiffon cake, matcha chiffon cake, matcha gateau au chocolat.
- Convert all recipes to metric measurements.
- Add article: hydration and baking ratios.

## 2026-04-15

- Add canelé recipe (Gilles Marchal).
- Add miso grilled chicken and miso marinated steak.
- Add matcha white chocolate cookies.
- Add double chocolate chip cookies.

## Earlier

- Initial site setup with Jekyll and minima theme.
- Add matcha affogato, coffee jelly, tea jelly, bay leaf panna cotta.
- Add cold brew tea, thyme streusel, salted caramel sauce.
- Add about page.
