# Stencil onboarding — submission runbook

Everything below is staged and verified locally. These are the steps that need
your credentials / a working Brazil build host (this desktop's glibc is too old
to run `brazil-build` — the cloud pipeline does the real builds). Do them in
order; steps 1–2 can go in parallel, step 3 depends on both, step 4 is the
prod-bound bump.

Verified locally against the committed DRB fix: **52 components, 0 empty bundles.**

---

## 1. DRB named-export bundler fix  (do first — StencilRegistry live-render depends on it)

- **Branch (committed):** `shiauas/drb-named-export-bundler` → commit `dbcfb67`
- **Worktree:** `/tmp/stencil-drb-wt`  (of `StoresDesigner2/src/DesignRegistryBuilder`)
- **Change:** `src/builder/build.ts` — bundler now emits `import { <Named> as C }` for
  named-export components (was hardcoded `default`). + regression test
  (`integration.test.ts` + `fixtures/fake-ds/TestChip`). Full suite 138 pass.

```bash
cd /tmp/stencil-drb-wt
# sanity: brazil-build release (on a build host); then:
cr --new-review \
   --summary "fix(DRB bundler): honor named component exports, not just default" \
   --description "Unblocks named-export design systems (Stencil). Cloudscape/SDS/Meridian (default exports) unaffected. Adds a named-export regression test. See docs/onboard-stencil.md."
# drive to green with cr-monitor; merge; then ensure DRB republishes
# (DesignRegistryPeru-registries auto-builds DesignRegistryBuilder) so
# StencilRegistry's build picks up the fix.
```
Regression note for reviewers: the only behavior change is for components whose
registry `exports` is `{named:[…]}` (no default). Default-export DSes take the
unchanged `import { default as C }` path.

Also worth a **separate follow-up ticket** (found during this work, NOT fixed):
`generate-registry-minimal.ts:317` uses `/export\s+default\b/.test(source)` — a
naive regex that a "export default" occurring in a comment/string can fool.
Low severity; wants an AST check.

---

## 2. Create + CR the StencilRegistry package  (new GitFarm package — does not exist yet)

- **Files (ready, verified):** `/local/home/shiauas/workplace/StoresDesigner3/src/StencilRegistry/`
- Mirrors CloudscapeRegistry (compiled-dist `.d.ts` quadrant). CodeArtifact →
  **Phase 4 (DesignRegistryPeru --setAsTarget) is SKIPPED.**

```bash
# Create the Brazil package/repo (BuilderHub "create package" or):
brazil ws create --name StencilRegistry ...            # per your normal package-create flow
# Copy the staged files into the new package root, then in a workspace on a build host:
brazil ws use --package StencilRegistry
brazil-build release      # expect: build/registry/@amzn/stencil-react-components/{registry.json,manifest.json}
                          # 52 components, componentMap==registry.json, non-empty *.mjs bundles
cr --new-review --summary "New package: StencilRegistry (PXT Stencil design registry)"
# cr-monitor to green; merge.
```
Config highlights (already set): `categories → esm/submodules`, `StencilShell.tsx`
mounts `<StencilProvider>` (Stencil throws without it), `type:'module'`, EXCLUDE
drops infra + the 7 aggregator modules.

---

## 3. Manifest CR  (committed, needs push + green)

- **Branch (committed):** `shiauas/onboard-stencil-registry` → commit `d26972b`
- **Worktree:** `/tmp/stencil-cdk-wt`  (of `StoresDesigner3/src/DesignRegistryCDK`, off origin/mainline — your in-flight CDK edits were left untouched)
- Adds the StencilRegistry entry (registries=`['@amzn/stencil-react-components']`,
  cti=SDT_CTI, visibility=`restricted`) + `StencilRegistry` to CDK `brazil.ion` build_after.

```bash
cd /tmp/stencil-cdk-wt
brazil ws use --versionset DesignRegistryPeru/development   # so the synth dry-run resolves deps
cr --new-review --summary "Onboard StencilRegistry to the Design Registry manifest"
# The CDK synth dry-run stays red until StencilRegistry (step 2) is in the VS —
# sequence step 2 before expecting green. Drive to green with cr-monitor; merge.
```
Then (rung 6, Pipelines UI — no API): add `StencilRegistry` as a build target of
the **DesignRegistryPeru-registries** pipeline, and grant actor **9557033**
"Autobuild Brazil Package" on the StencilRegistry bindle. Confirm the pipeline
shows `BUILD_PACKAGE StencilRegistry needsSync:false` — don't assume the grant took.

---

## 4. Bump beta→prod  (PROD-BOUND — get explicit go, then shepherd)

```bash
# bump-design-registry: promote StencilRegistry registries → development,
# then watch pipelines.amazon.com/pipelines/DesignRegistry beta→prod
# (Beta Validation Hydra: Integ Auth, Integ API, Registry Assets, Playwright E2E).
```

## 5. Verify (rungs 8–9)
- API: `https://registry.design.amazon.dev/api/packages` → `@amzn/stencil-react-components`
  present, `latest` == shipped version, `type: module`, `visibility: restricted`.
- Picker: fresh Stores Designer project, as a **DESIGN_REGISTRY_PREVIEW** tester
  (`amzn1.bindle.resource.b7phsij2u5dxqt6aq6kq`), select Stencil, confirm a placed
  component renders. Add PXT/`sivajic` as testers, or drive it yourself.

## Known follow-ups (documented, not blockers)
- 7 aggregator modules (tabs, skeleton, survey, rte, whats-new,
  customer-satisfaction, filtering) excluded — need DRB multi-component-group
  support (or a `resolveExport` hook) before they can ship. See docs/onboard-stencil.md.
- The `isDefaultExport` regex hardening (step 1 note).
