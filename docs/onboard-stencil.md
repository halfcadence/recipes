# Onboard Stencil → Stores Designer Design Registry (scratch plan)

**Status:** Phase 0 done. BLOCKED on a strategy decision (see "Open decision") before Phase 3.
**Driver:** shiauas + Claude, via `onboard-design-system` skill. Test run requested "full to prod (rungs 1–9)".
**Date:** 2026-07-14.

## Phase 0 discovery (verified against live packages)

- **CodeArtifact?** YES. `@amzn/stencil-react-components@4.13.3` (created 2026-06-22) ✓ CodeArtifact + NpmPrettyMuch, 3PAG PASSED. → CodeArtifact/"YES branch"; **skips Phase 4** (no Brazil→Peru `--setAsTarget` shared-VS mutation). This is why Stencil is a low-risk test.
- **Framework:** React (peer `react >=17 <18` on 3.x line; the `templates/stencil` seed uses `^4.0.0` + react 18). Uses `@emotion` for styling.
- **What the npm package ships (the load-bearing finding):**
  - `dist/` (CJS) + `esm/` (ESM) compiled JS, `static/`, `scripts/`.
  - **2,559 `.d.ts` type files**. **0 `.tsx`/`.ts` source files.** `files: ["dist","esm","static","scripts","*.ts","*.js"]`.
  - **Subpath-module layout**, NOT SDS's per-component dir: consumers import `@amzn/stencil-react-components/button`, `/card`, `/layout`, `/text`, `/link`, `/icons`, ... (~50+ top-level subpath entry files at `package/<name>.js`). Underlying components live deep under `esm/submodules/<group>/<Component>.{js,d.ts}` (many components per group).
- **Deps of interest:** `@amzn/stencil-react-desc@4.13.3` = a fork of `react-desc` (PropTypes-based schema). Ships `lib/*.js` runtime helpers (describe/descToJSON/descToTypescript) — a **library for authoring** descriptors, NOT a prebuilt component-metadata JSON catalog. So there is no ready-made registry.json-equivalent to ingest. Also `@amzn/stencil-design-tokens@4.13.3` (tokens) + `@amzn/stencil-react-theme-default` + `@amzn/stencil-react-icons`.
- **Repo:** source repo not conclusively identified (npmpm has no repo link; `Stencil` repo in code search is an unrelated schema DSL). Not needed for the CodeArtifact path — we consume the published package. (Owner per prioritization doc: PXF; requester was GREF/SpaceQ `sivajic`.)

## DRB ingestion capability (read from DesignRegistryBuilder/src/builder)

- `DSConfig.categories` = map of category → **component-source directory**. Generator (`generate-registry-minimal.ts`) walks each `categories` dir expecting **one subdirectory per component** named `<Name>/`, then per dir:
  - `<Name>.tsx|.js|.jsx` present → **react-docgen** (source path; SDS/Meridian).
  - else `interfaces.d.ts` present → **ts-morph parseDtsProps** ("Compiled package (e.g. Cloudscape)"). `type:'module'` still expects renderable bundles.
- So DRB DOES support compiled/`.d.ts` packages — but it assumes a **`<category>/<Name>/{Name.* | interfaces.d.ts}`** directory shape. **Stencil's `esm/submodules/<group>/<Component>.d.ts` layout does not match** — no per-component dir named after the component, no `interfaces.d.ts` file; types are `<Component>.d.ts` grouped by feature. → needs a reshaping/adapter step, not just config.

## CORRECTED (2026-07-14): NO adapter needed. Verified by running DRB over Stencil.

**Ground truth beats my earlier code-reading.** Ran installed DRB 1.0.100 `generateRegistry` (via the
`@amzn/design-registry-builder/builder` export) with `categories:{components: <pkg>/esm/submodules}`
over the real published `@amzn/stencil-react-components@4.13.3`:
- **69 items discovered, 45 with props, 13 contentSlot.** Clean props: button→{icon,iconPosition,isDestructive,size,…},
  progress-bar→{progress,status,threshold,…}, side-nav→contentSlot+aria-label. Only `utils` warned (correctly skipped).
- Stencil ships `esm/submodules/<group>/{index.js, interfaces.d.ts}` with `<Group>Props` in interfaces.d.ts
  (262 interfaces.d.ts files). Per-dir: `findMainFile('button')` looks for lowercase `button.js` → miss
  (file is `Button.js`), so mainFile=null; `index.js` present → dir enumerated; `interfaces.d.ts` exists →
  `hasDts=true` → `parseDtsProps` reads `ButtonProps`. Exactly the Cloudscape path from CR-289298897.
- **=> This is the compiled-dist React quadrant the Cloudscape dogfood (CR-289298897) already validated.
  No reshaping/adapter. `categories → esm/submodules` is enough.** My earlier "adapter needed" note (below)
  was wrong — I read the flat top-level `<Component>.d.ts` filenames, not the `submodules/<group>/` dirs.

### Superseded (kept for honesty): earlier WRONG conclusion "adapter needed as a build-script step"

Read DRB **mainline** (local checkout was stale): `src/builder/discover-components.ts` (`enumerateComponents`, added with the Cloudscape work) + `generate-registry-minimal.ts` + `src/__tests__/discover-components.test.ts`.
- Compiled-`.d.ts` path fires ONLY for layout `categories/<Name>/{index.*, interfaces.d.ts}`: `enumerateComponents` yields a subdir only with `<Name>.{tsx,ts,js}` or `index.*`; then `hasDts = !mainFile && !isFlat && exists(<Name>/interfaces.d.ts)`.
- Stencil ships `esm/submodules/<group>/<Component>.d.ts` (grouped, no per-component dir, no `interfaces.d.ts`) → not discovered.
- Flat mode picks up PascalCase compiled `.js` (`AppLayout.js`) but then runs react-docgen on COMPILED js → empty/garbage props. Not viable.
- `.d.ts` explicitly excluded from flat discovery (test: "ignores support files … d.ts").
- **Conclusion:** need a `peru-build.sh` prebuild that reshapes Stencil's `submodules` `.d.ts` tree → `<Name>/interfaces.d.ts` + a stub `index.js` per component. Build-script only; DRB unchanged.
- **No CloudscapeRegistry shipped** (manifest = SDS/Meridian/AUI3 only), so no existing reshaping script to copy — net-new but small. The Cloudscape `.d.ts` capability in DRB is the enabling precedent.
- **Skill staleness confirmed:** DRB mainline (discover-components, flat layout, compiled-.d.ts) has outrun the skill's 3-pattern table. This is the "conflicts with the skill" the prior Cloudscape agent hit.

## Open decision (need before building — this is what the "test" surfaces)

Stencil is a **4th ingestion shape** the skill's 3 reference patterns (SDS source / Meridian source+tarball / AUI metadata) don't cover cleanly. Options:

- **(A) Adapter that maps Stencil's subpath/`submodules` `.d.ts` tree into what DRB expects** (synthesize per-component `interfaces.d.ts` dirs, or extend DRB's discovery to walk Stencil's layout + resolve props from its `.d.ts`). Most faithful ("full" module registry, live render). Most work — real DRB/config code + a component allowlist (Stencil is huge; pick a curated set).
- **(B) `type:'metadata'` registry** reading Stencil's `.d.ts` (props only, no DRB live preview), mirroring the AUI/Books precedent but for a CodeArtifact React DS. Lower effort; loses live render (though a React-shell template could still author it, like Books).
- **(C) Escalate to the DS owner (PXF):** does Stencil already emit a `react-desc` descriptor JSON anywhere (build artifact / storybook)? If yes, ingest that directly = cheapest + richest.

**Recommendation:** confirm (C) first (cheap check with PXF/Stencil build); if no descriptor artifact exists, do (A) scoped to a curated component allowlist. Either way this is a **DRB-capability extension**, which the skill's self-improvement section says to expect and to feed back via a CR.

## Chosen strategy — LOCKED
- **SDS-quadrant sibling of CloudscapeRegistry**: CodeArtifact React, compiled-dist `.d.ts` props via DRB ts-morph. `categories → esm/submodules`, `StencilShell.tsx` mounts `<StencilProvider>` (Stencil throws without a provider — unlike Cloudscape's CSS-only), `type:'module'`, all ~69 discovered minus infra dirs. NO adapter, NO DRB change for the registry/props.

## Phase 3 RESULT (2026-07-14): registry builds clean; found a real DRB bundler bug

Created `StoresDesigner3/src/StencilRegistry` (mirrors CloudscapeRegistry). Ran DRB 1.0.100 `buildPreview` (skipTemplateValidation/Archive/screenshots — local desktop can't run bundled Chromium: `GLIBC_2.34 not found`, and the skill says screenshots are pipeline-only anyway).

**Works (rungs 1–2 substance):**
- **59 components**, 45 with props, 12 contentSlot. `manifest.componentMap == "registry.json"`, registry↔manifest name-sets identical (59==59).
- Props extracted richly from `.d.ts` via ts-morph: e.g. button → colorScheme(enum default|darkBackground), disabled(boolean=false), iconPosition(enum leading|trailing). Import paths `@amzn/stencil-react-components/<kebab>`. Excluded infra (context/styles/hooks/utils/a11y/responsive) correctly absent. `<StencilProvider>` wired into assembled `template/src/app.tsx` and previews (`_wrapper_default`).

**BUG FOUND (the headline dogfood finding) — DRB bundler hardcodes default export:**
- Every `components/<name>.mjs` is 81 bytes: `import"./shared/…";var e=void 0;export{e as default}` → exports **undefined**. Live-render bundles are broken for a **named-export** DS.
- Root cause: `@amzn/design-registry-builder/dist/builder/build.js:194`
  `writeFile(entryPath, \`import { default as C } from '${importSource}';\nexport default C;\n\`)`
  hardcodes the **default** export. Cloudscape works because its subpaths are default exports; **Stencil uses named exports** (`export { default as Button } from './Button'` at index → the index has NO default; registry already records `exports:{"named":["Button"]}`). So `import { default as C }` = undefined.
- **Scope of impact:** props/metadata/pickability are fine (they come from `.d.ts`); only the ESM *bundles* (live render/preview) are empty. First named-export compiled DS → new gap beyond the Cloudscape `.d.ts` props work.
- **Fix (small, DRB-side):** `registry` (with per-item `exports.named`/`exports.default`) is built at build.js:68 BEFORE the bundle loop at :167 — so the loop can emit the correct entry per component: default → `import { default as C }`; named → `import { <Named> as C } from '…'; export default C`. Look up the export shape from `registry.items[name].exports` (or re-derive via `isDefaultExport` already computed in generate-registry-minimal). Then StencilRegistry needs no change.

**Next:** this is a DRB change (raise on DesignRegistryBuilder), not a StencilRegistry change. Options: (a) fix DRB bundler to honor named exports [correct, unblocks Stencil + any named-export DS]; (b) ship Stencil as `type:'metadata'` now (props/pickability, no live preview) and follow up with the DRB fix. PAUSED here for the user before any DRB CR / manifest CR / shared-state change.

## DRB FIX APPLIED (2026-07-14) — StoresDesigner2/src/DesignRegistryBuilder

Patched `src/builder/build.ts` (~line 249): build a `exportsByName` map from `registry.items[].exports` and choose the entry import clause per component — `default as C` for default exports (Cloudscape/SDS, unchanged), `<named[0]> as C` for named exports (Stencil), fallback to default when no export info. Compiled with local `tsc` (system node 22.18.0; `brazil-build` can't run here — Brazil's NodeJS-24.x + Chromium need newer glibc than this desktop). Fix confirmed in `dist/builder/build.js`.

**Result — rebuilt Stencil against the patched DRB:** **52 of 59** component bundles now contain real code (were ALL empty/`undefined` before). e.g. button.mjs 81→320 bytes (imports the real `Button` from a shared chunk), table.mjs 81→32,818 bytes. Regression-safe: default-export path still emits `default as C` (verified on synthetic {default:'Button'} → `default as C`).

**7 still empty — DIFFERENT root cause (not the export-kind bug), a follow-up:**
`tabs, skeleton, form(*), survey, rte, whats-new, customer-satisfaction, filtering, ai(*), page(*)` — these are **aggregator modules** that export MULTIPLE components (`tabs` → TabBar/TabSwitcher/TabPanel; `skeleton` → SkeletonBase/Button/Text/…; `form` → FormWrapper) or pure `export *` barrels (`ai`, `filtering`, `page` → not even in the registry, no `<Pascal>Props`). The registry derived `named:['Tabs']` from the DIR NAME, but no `Tabs` binding exists → import resolves undefined. This is DRB's "one dir = one component" model not fitting Stencil's multi-component groups — a deeper modeling issue than the entry-import fix. Options for later: per-group multi-item expansion, or a config `resolveExport(name)` hook to name the canonical binding (e.g. tabs→TabBar), or exclude/curate these. (*form/ai/page weren't in the 59 — counts above are of registry items.)

**Net for the test:** the export-kind bug (the headline finding) is FIXED and verified; live render now works for 52/59. The 7 aggregator modules are a known, documented follow-up, not a blocker for a metadata launch and not caused by my fix.

## Post-fix hardening (2026-07-14)

- **StencilRegistry: excluded the 7 aggregator modules** (tabs, skeleton, survey, rte, whats-new, customer-satisfaction, filtering) via `config.js` EXCLUDE so the launch ships only clean bundles. Rebuilt against patched DRB: **52 items, 0 empty bundles, excluded dirs absent.** Clean launch set.
- **DRB unit test added** (`src/__tests__/integration.test.ts` + `fixtures/fake-ds/TestChip`): a NAMED-export fixture component (no default). Asserts (a) both fixture components discovered, (b) export kind recorded per component (TestButton default / TestChip named), (c) the named-export bundle re-exports real code, NOT `export undefined`. Full DRB suite: **138 passed, 1 skipped** — no regressions.
- **Incidental real DRB bug found while testing** (separate, NOT fixed — logged for follow-up): `generate-registry-minimal.ts:317` detects default exports with `/export\s+default\b/.test(source)` — a naive regex over raw source, so the phrase "export default" in a COMMENT or string falsely flags a component as a default export (it bit the TestChip fixture whose comment said "no `export default`"). Low severity (comments rarely contain the phrase) but worth a proper AST/heuristic check. Noted for a DRB follow-up CR.

## Ingestion strategy (locked parts)
- CodeArtifact React → registry package `npm install`s `@amzn/stencil-react-components` directly. **Skip Phase 4.**
- Registry name / `--out`: `@amzn/stencil` (single registry; revisit if we split components/icons/tokens).
- CTI: `SDT_CTI` (registry operator = us, matches SDS/Meridian).
- Visibility: start `restricted` (DESIGN_REGISTRY_PREVIEW lock) while validating, like Meridian/Books. Requester `sivajic` + PXF added as testers.

## STATE AT PAUSE (2026-07-14) — before any remote publish / prod mutation

Three artifacts staged locally; nothing pushed to remote, nothing deployed:
1. **DRB fix** — `StoresDesigner2/src/DesignRegistryBuilder/src/builder/build.ts` (named-export bundler) + new test (`integration.test.ts` + `fixtures/fake-ds/TestChip`). Uncommitted in that workspace. Full suite 138 pass. Needs: commit + CR + merge, then publish DRB so registry builds pick it up.
2. **StencilRegistry package** — `StoresDesigner3/src/StencilRegistry/` — brand-new, **not a GitFarm package yet** (`pkg/StencilRegistry` 404). Needs: create the Brazil package/repo, commit, CR, merge. It builds locally (52 comps, 0 empty bundles) against the PATCHED DRB.
3. **Manifest CR** — committed on clean branch `shiauas/onboard-stencil-registry` in worktree `/tmp/stencil-cdk-wt` (off origin/mainline). Commit d26972b. Not pushed.

### Sequencing (hard dependency order) — all remaining steps need explicit user go
1. **DRB fix lands first** (CR → merge → DRB published to CodeArtifact/registries VS). Without it, StencilRegistry's pipeline build produces empty (`undefined`) bundles. Regression-safe for SDS/Meridian/Cloudscape (default-export path unchanged, 138 tests pass).
2. **Create + CR the StencilRegistry package** (new GitFarm repo + Brazil package). Since Stencil is CodeArtifact, **Phase 4 is SKIPPED** (no DesignRegistryPeru --setAsTarget).
3. **Manifest CR** (d26972b): set workspace VS to DesignRegistryPeru/development for the synth dry-run; drive green with cr-monitor. Add StencilRegistry as a build target of the DesignRegistryPeru-registries pipeline + grant actor 9557033 Autobuild on its bindle (rung 6).
4. **Bump** StencilRegistry registries→development (bump-design-registry) → DesignRegistry pipeline beta→prod. **PROD-BOUND — explicit go required.**
5. **Verify:** registry API shows @amzn/stencil-react-components (rung 8); fresh Stores Designer project as a DESIGN_REGISTRY_PREVIEW tester renders a Stencil component (rung 9).

### Environment blocker (why I can't fully self-serve the builds here)
`brazil-build` fails on this desktop — Brazil's NodeJS-24.x binary (and bundled Chromium) require newer glibc (`GLIBC_2.34 not found`). Local proof used system node 22 + tsx + `--skip-template-validation/-screenshots` (screenshots are pipeline-only anyway per the skill). The real registry/template builds happen in the cloud pipeline, so the CR dry-run + pipeline are the authoritative gates.

## Phase checklist (verification ladder)
- [x] Phase 0 discovery
- [ ] Decision on A/B/C
- [ ] Phase 3: StencilRegistry pkg (mirror SDSRegistry: DesignRegistryBuilder+NpmPrettyMuch+NodeJS build-tools, brazil.ion+peru-build.sh, DSConfig) → clean local build emits build/registry/@amzn/stencil/{registry.json,manifest.json}, nonzero component count (rungs 1–2)
- [ ] (Phase 4 SKIPPED — CodeArtifact)
- [ ] Phase 5: DesignRegistryCDK manifest entry + brazil.ion build_after; VS DesignRegistryPeru/development; cr-monitor to green. **PAUSE before merge.** Then registries-pipeline build target + actor 9557033 Autobuild grant (rung 6).
- [ ] Phase 6: **PAUSE before bump.** bump-design-registry registries→development, shepherd beta→prod; verify registry API (rung 8) + picker render (rung 9).

## Skill-improvement note (for the onboard-design-system CR at the end)
Add a **4th reference row**: "CodeArtifact React DS that ships compiled `.d.ts` + subpath modules, no `.tsx` source, no per-component dir" (Stencil). Document the `generate-registry-minimal` `.d.ts`/Cloudscape path AND its per-component-dir/`interfaces.d.ts` assumption, and the adapter needed when a DS uses a `submodules/<group>` layout. Note `@amzn/*-react-desc` (react-desc) is an authoring lib, not a prebuilt descriptor catalog — don't assume it gives you metadata for free.

## PROGRESS toward prod (2026-07-14, later)
- ✅ DRB fix CR raised + published: **CR-289322338** (reviewers mshortt, rozayc; dry-run building). Branch shiauas/drb-named-export-bundler @ 97ffc80.
- ✅ **StencilRegistry package CREATED**: https://code.amazon.com/packages/StencilRegistry — real content pushed to mainline (commit 20ca98b), under DesignRegistry Bindle (amzn1.bindle.resource.5hxuqrzkalmv2pekcopa). Phase 4 skipped (CodeArtifact).
- ✅ Manifest CR committed (branch shiauas/onboard-stencil-registry @ d26972b, worktree /tmp/stencil-cdk-wt) — needs push + green (blocks on StencilRegistry being VS-resolvable).
- NEXT: (a) get StencilRegistry building into DesignRegistryPeru/registries + add as DesignRegistryPeru-registries pipeline build target + grant actor 9557033 Autobuild (rung 6); (b) push manifest CR, drive green with cr-monitor; (c) after DRB fix + StencilRegistry merged/built, bump beta→prod; (d) verify API + picker.

## CHECKPOINT (2026-07-14, driving to prod) — waiting on human approval

### CRs open (all mine, all technically ready):
- **DRB fix** CR-289322338 rev2: build PASS, AutoSDE/Coverlay/Security/ChangeGuardian PASS. ITL shows Fail but per its OWN message it auto-passes on approval (known ITL-724 chicken-egg; .crux_dry_run_build accepted, effective post-merge). **ONLY gate: 1 Shopping DT approval (mshortt/rozayc).** Files: build.ts + integration.test.ts + fixtures/TestChip + .crux_dry_run_build. No conflict with shiauas' other DRB CR-289320545 (.vite archive fix — different files).
- **Manifest** CR-289323233: AutoSDE clean; dry-run red because cut from a bare worktree (wrong VS) AND StencilRegistry not yet in the VS. Will re-cut from a DesignRegistryPeru/development workspace AFTER StencilRegistry builds into the VS.
- **StencilRegistry package**: created + live on GitFarm mainline (20ca98b).

### GATED sequence (user chose: gate pipeline edit on DRB fix merge):
1. ⏳ **[NEEDS HUMAN]** approve+merge CR-289322338 (DRB fix).
2. then add StencilRegistry as build target on DesignRegistryPeru-registries pipeline + grant actor 9557033 Autobuild (Chrome DevTools) → builds StencilRegistry (with the fix) into /registries.
3. then re-cut + drive manifest CR-289323233 green (workspace VS = DesignRegistryPeru/development).
4. then bump registries→development → DesignRegistry pipeline beta→prod [PROD].
5. verify API + picker (restricted / DESIGN_REGISTRY_PREVIEW tester).

## PROGRESS (2026-07-15) — pipeline build validated the whole registry end-to-end
- ✅ **DRB named-export fix MERGED** (CR-289322338, SHIPPED, approved tktran).
- ✅ **Manifest CR APPROVED by rozayc** (CR-289323233) — auto-merge armed; dry-run red only because StencilRegistry not yet in the VS (expected).
- ✅ **`pb build --setAsTarget` DRY-RUN of StencilRegistry into DesignRegistryPeru/registries** (build 7932203429) VALIDATED the registry in the real cloud pipeline: **52 components, 33 screenshots (x86_64), template install→build→RUNTIME (Playwright /pages/test/frame) PASSED, 50.4MB archive.** Confirms the whole StencilRegistry works on real infra (the parts my desktop couldn't run).
  - Only failure: trivial brazil.ion bug — declared `private_dir:'private'` but Cloudscape-modeled peru-build.sh never creates it. FIXED (drop private_dir, mirror Cloudscape). Branch-protection blocks direct mainline push, so: **CR-289516377** raised + published.
- NEXT: (a) approve+merge CR-289516377 (private_dir fix); (b) live `pb build --setAsTarget` StencilRegistry into /registries [PROD-BOUND shared VS — needs go]; then pipeline autobuild promotion turns on; (c) manifest CR dry-run goes green → auto-merges; (d) bump registries→development beta→prod; (e) verify.

## PROD BUMP DONE (2026-07-15) — deploying, verifying
- ✅ Live `pb build --setAsTarget` (7932221773) added StencilRegistry-1.0 to DesignRegistryPeru/registries (rev 130). [Bonus: CloudscapeRegistry also now in the VS.]
- ✅ **BUMP (7932235862) SUCCEEDED** — StencilRegistry-1.0 now in DesignRegistryPeru/development (rev 343). Triggered the DesignRegistry deploy pipeline (9314152, gold, no prod manual gate — auto-promotes beta→prod).
- ✅ Manifest CR-289323233 rev2 re-cut from proper /development workspace: dry-run now WORKING (resolves StencilRegistry), AutoSDE+SAS pass. CDK synth locally SUCCEEDED and generates dr-beta/prod-deploy-stencilregistry stacks. Published. NOTE: amend reset rozayc's approval → needs 1 re-approval to merge.
- ⏳ Registry API not yet showing stencil (deploy in flight; beta validation Playwright E2E ~20-30min). 
- REMAINING: (a) watch DesignRegistry pipeline beta→prod green; (b) re-verify API shows @amzn/stencil-react-components latest=... type=module visibility=restricted (rung 8); (c) fresh Stores Designer project as DESIGN_REGISTRY_PREVIEW tester → Stencil pickable + renders (rung 9); (d) manifest CR needs re-approval + merge (controls picker visibility/CTI).

## DEPLOY THROUGH PROD STAGES (2026-07-15) — API index lagging
- Heat map (VS rev 6485041065 = my bump): VersionSet/PipelineUpdate/Packaging = my rev ✓; Beta (Distribution/DNS/Foundation/Hydra) = my rev ✓; **Infra (prod) Distribution/DNS/Foundation/Infra-Hydra = my rev ✓; CodeArtifactPublish = my rev ✓**. So the deploy reached the prod stages successfully.
- BUT registry.design.amazon.dev/api/packages still lists only aui/books/meridian/sds*×5 — StencilRegistry (and CloudscapeRegistry, also freshly in /development) NOT shown. Per-package + /latest/registry.json 404.
- Likely the registry INDEX (api/packages) Lambda/CDN cache lag the bump-design-registry skill documents ("API shows old version after prod — delete s3://registry-prod-{account}/index.json"). The artifact deployed; the index just hasn't refreshed. Give it time or clear the index cache.
- REMAINING: (a) confirm API shows @amzn/stencil-react-components (rung 8) once index refreshes; (b) picker render as DESIGN_REGISTRY_PREVIEW tester (rung 9); (c) manifest CR-289323233 rev2 re-approval + merge.

## STATUS ~30min post-bump: deployed to prod, API INDEX STALE (known issue)
- Heat map confirms StencilRegistry (my bump rev) cleared ALL stages incl. prod Infra + CodeArtifactPublish. Artifact IS deployed.
- api/packages STILL only shows 8 (aui/books/meridian/sds×5). CRITICAL SIGNAL: CloudscapeRegistry (in /development for hours) is ALSO missing → the index (api/packages) is genuinely stale for recently-added registries, NOT a Stencil-specific problem.
- This is the documented bump-design-registry known issue: "API shows old version after prod — Lambda/index cache — delete s3://registry-prod-{account}/index.json". registry-prod account = 137769144454 (per SDS archive path seen earlier) / index served from registry-prod-*.
- DECISION NEEDED: (a) wait for natural index refresh, or (b) clear s3://registry-prod-137769144454/index.json (prod S3 write — needs go). Cloudscape being stuck too suggests waiting may not resolve quickly.
- Manifest CR-289323233 rev2 still needs re-approval (amend reset rozayc) + merge.

## CORRECTION (2026-07-15): API-missing cause was NOT index cache — it's the unmerged manifest CR
- User caught it: Stencil/Cloudscape not shown as pipeline build targets, and I re-checked mainline manifest → it has SDS/Meridian/AUI3/Books/**Cloudscape** but NOT Stencil. Cloudscape's manifest CR merged (mainline e944249→38422aa); Cloudscape's API entry is just mid-deploy, NOT stale-cached. My "delete index.json" theory was WRONG.
- The API entry + deploy stack (dr-{beta,prod}-deploy-stencilregistry) come from registry.manifest.ts. Without the manifest CR merged, the bumped artifact sits in the VS but nothing publishes it to the registry API. So the gate is: MERGE THE MANIFEST CR.
- Also caught via rebase: my manifest branch was based on pre-Cloudscape mainline → would have reverted Cloudscape's entry. REBASED onto 38422aa, resolved conflicts keeping BOTH Cloudscape + Stencil. CR-289323233 rev3 diff is now a clean +1 (Stencil only). AutoSDE working, SAS pass, dry-run building.
- STILL SEPARATE / not done: StencilRegistry (and CloudscapeRegistry) are NOT pipeline build targets on DesignRegistryPeru-registries Packages stage → they won't auto-rebuild on future source commits (rung 6). Add via promotion UI once resolvable, or note as follow-up.
- REMAINING: (a) manifest CR rev3 green + 1 approval → merge → deploys stencil stack → API shows it (rung 8); (b) picker render as DESIGN_REGISTRY_PREVIEW tester (rung 9); (c) add StencilRegistry as pipeline build target (rung 6, autobuild).

## MANIFEST CR MERGED (2026-07-15) — Stencil onboarding effectively DONE
- CR-289323233 SHIPPED: approved by saranyau, all analyzers pass, CRUX auto-merged commit 4941c701 to DesignRegistryCDK mainline. Clean +1 diff (Cloudscape preserved, Stencil added).
- This triggers the DesignRegistry deploy pipeline → deploys dr-prod-deploy-stencilregistry stack → Stencil appears in registry API + picker (restricted/DESIGN_REGISTRY_PREVIEW).
- Pipeline autobuild for StencilRegistry: ON (user enabled).
- FINAL VERIFY pending: (rung 8) API shows @amzn/stencil-react-components; (rung 9) picker render as DESIGN_REGISTRY_PREVIEW tester. Give the manifest deploy ~20-30min.

## ✅ LIVE IN PROD (2026-07-15) — rung 8 CONFIRMED
registry.design.amazon.dev/api/packages now lists @amzn/stencil-react-components: latest=4.13.3, type=module, visibility=restricted, designSystem.id=stencil. Matches shipped config exactly. (Cloudscape also live: 3.0.1328.)
ONBOARDING COMPLETE (rungs 1-8). Only rung 9 (functional picker render as DESIGN_REGISTRY_PREVIEW tester) remains as an optional confirmation.
FOLLOW-UPS (non-blocking): 7 aggregator modules excluded pending DRB multi-component-group support; isDefaultExport regex hardening; add StencilRegistry as DesignRegistryPeru-registries build target (autobuild) — user set promotion On.

## STATE @ compact (2026-07-16)
- Stencil + Cloudscape both LIVE in prod registry API: type=module, visibility=restricted (DESIGN_REGISTRY_PREVIEW tester lock). Stencil 4.13.3, Cloudscape 3.0.1328.
- Shepherd VMR:QUALYS:373119 (insecure http.server 8791) — remediated (killed) + ticket V2289577780 auto-resolved + audit comment posted. Prevention: global rule ~/.claude/rules/no-insecure-http-server-do-not-delete.md + PreToolUse hook ~/bin/claude-block-insecure-httpserver.
- BLOCKED (user): BYOD is currently TURNED OFF due to an unrelated prod issue. User will notify when fixed. DO NOT promote Stencil/Cloudscape to visibility=public until then. Rung-9 picker-render verification also on hold (needs BYOD on).
- WHEN UNBLOCKED: (1) rung-9 verify Stencil (+Cloudscape) render as a DESIGN_REGISTRY_PREVIEW tester; (2) THEN promote to public at GA. Stencil follow-ups: 7 excluded aggregator modules (tabs/skeleton/survey/rte/whats-new/customer-satisfaction/filtering) pending DRB multi-component support; isDefaultExport regex hardening.

## RUNG-9 BLOCKED BY PLATFORM BUG — root-caused (2026-07-16, BYOD back on)
Fresh Stencil project (8c4d33ce-61fb-4150-86ae-a982be47e47e) shows "This project
failed to load after multiple attempts." NOT a Stencil defect. Root cause:

- Container boots + reaches RUNNING fine. Then `bootstrap-template` SigV4-fetches
  the DS template zip and gets **403 Forbidden**.
- `resolveTemplateArtifactUri()` (DesignAssistantShared/packages/projects/src/services/templateResolver.ts,
  last line) HARDCODES `archive.al2023-x64-node22.zip`. DSes ship different node majors:
  - SDS/Meridian → node22 ✅ (194/194 fetches OK, that's why sds always works)
  - Stencil → node20.zip (52.9MB, exists); node22 → missing → 403
  - Cloudscape → node20.zip (46.1MB, exists); node22 → missing → 403
  - Books → node20 too
- Proven: head-object node20=200, node22=403 for stencil+cloudscape; registry
  detail API declares template.archive.path=…node20.zip, nodeVersion:"20".
- S3 returns 403 (not 404) for missing object w/o s3:ListBucket (cross-acct bucket) —
  so 403 = object-not-there, not the 7/16 S3-scoping incident/temp-policy.
- Fix already exists in the CONTAINER (DesignerAgent/src/ds-cache.ts resolveArchiveName
  reads template.archive.path from manifest; comment: "SDS/Meridian node22, Cloudscape
  node20") — the ENV-CREATION resolver never got the same fix. Fix = read
  template.archive.path from DS manifest/registry API instead of hardcoding node22.
- A/B control: fresh Cloudscape project created same time → also 403 (on books/node22
  path). Confirms platform-wide, DS-agnostic, predates onboarding (earliest 403
  2026-07-15 20:54; zero successful stencil/cloudscape/books template fetches ever).

STATUS: onboarding rungs 1-8 remain DONE (both DSes live in registry API). Rung-9
render is blocked on this platform bug, not the onboarding. Still HOLDING on
promote-to-public per user. Memory: project_byod-template-node-major-bug.md.

## FIX WRITTEN + VALIDATED test-first on personal stack (2026-07-16)
Per "don't fix anything we haven't actually tested": ran full repro→fix→confirm on shiauas-jig.

**Root cause (confirmed):** resolveTemplateArtifactUri (DesignAssistantShared/packages/projects/
src/services/templateResolver.ts) hardcoded archive.al2023-x64-node22.zip. Stencil+Cloudscape
ship node20 → resolved to nonexistent object → container SigV4 fetch 403 → project fails to load.

**Confound found on personal stack:** MDE rejects CreateEnvironmentFromWarmPool when the inline
devfile >1024 bytes (ParamMaxLenError). Personal stack's long resource names (…-shiauas-jig-…)
put Stencil's devfile at 1031B (SDS fits at ~1021 — shorter pkg name). Prod is ~1010B, unaffected.
Temporarily shortened metadata.name in the SSM devfile template (+Lambda env var) to unblock the
repro — a HARNESS accommodation only, RESTORED after. NOT part of the shipped fix.

**Baseline repro (unfixed, devfile unblocked):** Stencil project → container boots → fetches
node22 → 403 Forbidden (Fault:1,Fatal:1). Matches prod exactly.

**Fix:** resolver now HEADs candidate archives [node22, node20] and returns the first that exists
(async; both call sites awaited). Throws TemplateArchiveNotFoundError if none (e.g. Books ships
NO archive at all — different problem, now a clear error not a silent 403). + IAM: cross-account
s3:GetObject on registry-prod-137769144454/*/template/* + kms:Decrypt on the DRB KMS key added to
the projects-api Lambda role (mirrors mde-environment role grant in mdeInfraStack). 12 unit tests
pass (SDS/Meridian node22, Stencil/Cloudscape node20 fallback, Books not-found, prefers node22).

**Deploy:** projects stack only (light path, no MDE image rebuild), 332s, npx cdk deploy
--exclusively to shiauas-jig. IAM grant verified on role, live alias → v60.

**Fix confirmed:** fresh Stencil project → container fetches node20 → templateFetch Success:1,
extract complete, bootstrap done. The exact failure is gone.

**Files changed (uncommitted, in SDDeploy workspace):**
- DesignAssistantShared/packages/projects/src/services/templateResolver.ts (+ .test.ts)
- DesignAssistantShared/packages/projects/src/manager/projectV2Manager.ts (await)
- DesignAssistantShared/packages/agents/src/designer-agent/agent.ts (await) + agent.test.ts (mockResolvedValue)
- DesignAssistantCDK/lib/lambda/projectsApiLambdaManager.ts (IAM grant)

**NOT yet done:** CR (SDDeploy CDK is on branch shiauas/byod-warmpool-60, Shared on mainline —
rebase/branch cleanly before CR); Cloudscape spot-check (same code path, node20, high confidence);
still HOLDING promote-to-public per user.

## SECOND node-major bug found + fixed in ds-cache.ts (2026-07-16, browser retest)
Browser test on personal stack: SDS projects failed to load, Cloudscape worked — OPPOSITE of the resolver bug. Root-caused via /mde/environments logs:
- ALL 3 template fetches SUCCEEDED (resolver fix works: SDS node22, Cloudscape node20).
- SDS hung ~470s (7.8min) on `[ds-cache] installing sub-packages (blocking)` npm install from CodeArtifact → UI timed out ("failed to load after multiple attempts"). SDS has 7 sub-packages; Cloudscape is single-package → no blocking install → fast. NOT the design system, NOT my resolver fix.
- Deployed personal-stack platform image was STALE (2026-07-15 15:06): logged `installing sub-packages (blocking)` — mainline already has non-blocking `backgroundInstallSubPackages`.
- SECOND node-major bug: deployed ds-cache hardcoded node22 (Cloudscape logged `ds-cache download failed ...node22.zip 403 → npm fallback`). Mainline had a partial fix (`resolveArchiveName` reads manifest.json) but it ALSO 403s: manifest.json is at the version ROOT, outside the mde-environment role's `*/template/*` grant → silently falls back to node22. So even a fresh mainline rebuild wouldn't fix Cloudscape ds-cache.

FIX (DesignerAgent/src/ds-cache.ts): replaced `resolveArchiveName` (root-manifest read) with `fetchFirstArchive` — probes template/ prefix trying [node22, node20], first that downloads wins; 403/404 = try next, other errors propagate to npm fallback. Same shape as the templateResolver fix. 21 ds-cache unit tests pass incl. new node20-fallback test.

DEPLOY IN PROGRESS: rebuild platform MDE image (deleted ECR platform-latest tag to force BATS rebuild) + deploy mde-infra to shiauas-jig. This ALSO picks up mainline's non-blocking sub-package install (fixes SDS hang). NOTE: mde-infra deploy resets the shortened devfile → must re-shorten + re-publish projects Lambda alias after (1024-byte confound). Then retest all 4 DSes.

## mde-infra REDEPLOYED + digest false-alarm resolved (2026-07-16)
Rebuilt platform MDE image (DesignerAgent release → DesignAssistantImageBuild → CDK), deleted ECR platform-latest tag to force rebuild, deployed mde-infra to shiauas-jig (492s, "Published DesignAssistantImageBuild...", warm pool refreshed). New image pushed 16:07.

SCARE (resolved): new envs reported imageDigest sha256:9baba3c1 while platform-latest = sha256:995132d3 → looked like warm pool stuck on old image. ROOT CAUSE of confusion: 995132d3 is the ECR *manifest* digest; 9baba3c1 is the container *config* digest — SAME image, two digest types. Proof: config digest of new platform-latest (16:07 build) = 9baba3c1; config digest of OLD 7/15 image = 423618c8 (different). So containers ARE on the new fixed image. The 0.04s "pull" was a legit cache-hit on the correct new image.

POST-DEPLOY reconciliation done: mde-infra reset SSM devfile to 918 (original) → re-shortened to 894 (SSM v26) + re-shortened projects-api $LATEST env (1024-byte confound harness accommodation). live alias still v60 (fixed resolver + short devfile).

Direct-invoke retest confirmed template fetches correct on new image (SDS node22, Stencil+Cloudscape node20, all extract complete; Books 500 TemplateArchiveNotFoundError). BUT inject-ds/ds-cache only runs on a real agent invocation (frontend), not direct GET — so the SDS-non-blocking-install + ds-cache-node20 fixes need the BROWSER test to exercise.

Browser-test projects created on new image (use New Project dialog to drive, or these persist): SDS aa22a8c8, Stencil 769496b0, Cloudscape b5a555f0.

## MERGED ds-cache fix (mine + Arunkumar's lit-scope) — 2026-07-17
Discovered a THIRD bug via browser test + a peer's parallel work:
- assertRegisteredDS (new since 7/15 image) reads root manifest.json → 403 cross-account → rejected EVERY DS (UnregisteredDSError). Verified in live logs: Cloudscape/Stencil/Meridian all rejected on the 16:07 image.
- Arunkumar AR (arunkar) independently found scope-filter drops unscoped `lit` → BDS/Rufus (Lit libs) never boot. His CR-289926274 rewrites downloadPlatformArchive/symlinkCachedPackages to hydrate the FULL archive node_modules closure (not just @amzn scope) + closure index.
- CONFLICT/RECONCILE: his CR KEEPS node22 manifest-read (claims "node20 red herring") — but I PROVED via live log that Cloudscape requests node22→403, and BDS now ships node20-ONLY (node22=404). So his CR alone would NOT boot BDS/Cloudscape. Both changesets edit the same functions.
- RESOLUTION: merged all 3 into ds-cache.ts on branch shiauas/byod-dscache-merged (based on origin/mainline):
  1. fetchFirstArchive probes template/ [node22,node20] (mine) — replaces his resolveArchiveName manifest-read.
  2. full-closure hydration (his listArchivedPackages/writeClosureIndex/closureFor/closure-aware symlink) — for lit.
  3. assertRegisteredDS probes template/ candidates (mine) — no more false-reject.
  24 ds-cache tests, full suite 494 pass/8 skip. brazil-build release green.

DEPLOY IN PROGRESS (test-first): rebuilt platform image w/ merged code, deleted ECR platform-latest, deploying mde-infra to shiauas-jig. Then browser-retest SDS+Stencil+Cloudscape+BDS all boot+render. THEN CR (ours supersedes CR-289926274; credit arunkar for lit-scope in the merge). NOT green until deployed+proven.
