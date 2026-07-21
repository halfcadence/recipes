# BYOD ds-cache Forward Fix — Deploy & Test Plan (personal stack first)

**Date:** 2026-07-17 · **Author:** shiauas (draft) · **Status:** plan for review before executing

## Context / where we are
- **Incident (Jul 16):** the blocking sds-core install (`95e176e5`) made every fresh MDE
  cold-boot hang ~470s → prod "projects won't load". **Resolved** by prod deployment
  rollback (`0e275460`) + mainline revert **CR-289768748** (`0fa7847`). Stale bad-image
  envs have since **all aged out** (verified 2026-07-17: 0/124 original mappings remain).
- **So mainline today = reverted/old behavior:** sub-package install is **non-blocking**
  again (`backgroundInstallSubPackages`). That means the *original* BYOD boot failures the
  blocking change was trying to fix are latent again — specifically the node-major 403 and
  the Lit/full-closure hydration gaps.

## What the forward fix IS (and is NOT)
The forward fix does **NOT** re-introduce the blocking install (that caused the outage).
It keeps non-blocking and fixes the actual BYOD boot failure modes a different way. It's a
**multi-package** change currently sitting on feature branches (NOT mainline):

| Package | Branch (local) | Change |
|---|---|---|
| `DesignerAgent` | `shiauas/byod-dscache-merged` @ `2f71978` | ds-cache: (1) probe `template/` for node major [node22, node20] instead of hardcoding node22; (2) hydrate FULL closure (not just @amzn+DS scope) so Lit/unscoped transitive deps (`lit`, `lit-html`, `@lit-labs/*`) resolve → BDS/Rufus boot; (3) DS-registration check on structured HTTP status not message regex. Sits on top of the revert `0fa7847`. |
| `DesignAssistantShared` | `shiauas/byod-template-node-major` | `resolveTemplateArtifactUri()` HEADs candidate archives [node22, node20], returns first that exists; throws `TemplateArchiveNotFoundError` if none. Both call sites (projectV2Manager, agent) awaited. +12 unit tests. |
| `DesignAssistantCDK` | `shiauas/byod-template-iam` | IAM: cross-account `s3:GetObject` on `registry-prod-137769144454/*/template/*` + `kms:Decrypt` on DRB KMS key added to projects-api Lambda role (mirrors mde-environment role grant). |
| `DesignAssistantImageBuild` | mainline | (no change / already mainline) |

**Root cause common to all three:** the MDE environment role can read the registry
bucket's per-DS `template/` prefix but NOT the version-root `manifest.json` (root GET 403s).
The old code read the root manifest → 403 → silent node22 fallback → node20 DSes
(Stencil/Cloudscape/BDS) 403 on fetch → "failed to load".

> Note: `DesignAssistantShared` node-major fix was already **test-first validated on
> personal stack shiauas-jig (2026-07-16)** per the byod-template-node-major memory —
> Stencil went node22→403 (baseline) → node20 Success after deploy, 12 unit tests pass.
> This plan re-validates the **merged** DesignerAgent ds-cache changes end-to-end, which
> that earlier test did NOT cover (it was Shared/CDK only).

## Guiding principle (per user)
**Do NOT assume it works — deploy to a personal stack and drive it end-to-end before any
pipeline push.** A green build / passing unit tests is necessary, not sufficient. The bug
we're fixing only manifests at container boot with a real registry fetch, so it must be
exercised on a live personal-stack MDE project per DS.

## Plan

### Phase 0 — Get ready (this session)
1. **Consolidate branches / pull to mainline base.** Rebase each package's feature branch
   onto latest `origin/mainline` so we're building on current mainline (revert is already
   there). Keep the 3 feature branches; do NOT merge to mainline yet.
   - DesignerAgent `shiauas/byod-dscache-merged` (already based on `0fa7847`=mainline HEAD)
   - DesignAssistantShared `shiauas/byod-template-node-major`
   - DesignAssistantCDK `shiauas/byod-template-iam`
2. **Local build + unit tests, each package** (`brazil-build` / `tsc` / vitest/jest). Green
   gate before deploy. (Shared already has 12 tests; DesignerAgent has ds-cache.test.ts.)
3. **Confirm personal stack target** — which stack (shiauas-jig from the memory, or a fresh
   one?) and that its account/profile + warm pool are usable.

### Phase 1 — Deploy to personal stack (NOT prod)
4. Use the **deploy-personal-stack** skill / `aps deploy` to push all 3 packages together to
   the personal stack (CDK for IAM, Shared + DesignerAgent for the image). The IAM change
   (CDK) and the code (image) must land together or the fetch still 403s.
5. Confirm deploy success + the personal-stack warm pool picks up the new image (watch
   `/mde/warmpools` on the personal account for image pull).

### Phase 2 — Drive it end-to-end on personal stack (the real test)
Per DS, create a fresh BYOD platform project and confirm boot + render. **Matrix must cover
the DSes that exercise each fix:**
| DS | node major | exercises | pass criteria |
|---|---|---|---|
| SDS (`@amzn/sds-components`) | node22 | baseline / non-regression | boots fast, `background-installing`, renders |
| Stencil | node20 | node-major probe | template fetch **Success** (was 403), boots, renders |
| Cloudscape | node20 | node-major probe | same |
| BDS (books) | node20 + Lit | node-major + full-closure hydration | `lit`/`lit-html` resolve, Vite boots, `<bds-*>` render |

For each: cold-boot (fresh project) → confirm **no 470s hang** (non-blocking install),
**no tokens.css ENOENT**, template fetch Success, frames render. Use Chrome MCP +
personal-stack MDE logs (`/mde/environments`) side by side.

### Phase 3 — Decide + ship (separate follow-up, NOT this session)
6. Only after Phase 2 passes for all 4 DSes: open CRs (already have the branches), get
   review, merge to mainline, let the pipeline carry through Beta→Gamma→Prod bakes.
7. Re-verify in prod post-deploy via the same log tripwires + one BYOD project per DS.

## Explicit non-goals / guardrails
- **No prod writes** in this plan (personal stack only through Phase 2).
- **Do NOT re-introduce blocking install** — the fix stays non-blocking.
- **Do NOT merge to mainline** until personal-stack e2e passes.
- Deploy all 3 packages together — the IAM (CDK) + code (image) are interdependent.

## Decisions (confirmed 2026-07-17)
1. **Personal stack: `shiauas-jig`.** ⚠️ It already had the DesignAssistantShared node-major
   fix deployed + tested (2026-07-16). Before Phase 1, confirm its baseline: which of the 3
   packages are already deployed there vs. need (re)deploy, so we test the *merged* set, not
   a stale mix. Re-deploy all 3 together to be sure the DesignerAgent ds-cache merge (`2f71978`)
   + Shared + CDK IAM are all present at the versions we're validating.
2. **`2f71978` (DesignerAgent merged ds-cache) is still in CR review** — not final-final, but
   it's the shape to test now. Personal-stack e2e is part of validating it *for* the CR;
   expect possible revisions. Don't merge to mainline until both CR approved AND Phase 2 green.
3. **Books `TemplateArchiveNotFoundError` = accepted behavior** (option b). Books ships no
   archive; a clear error (not a silent 403) is the desired outcome. No archive-publish
   dependency blocks this fix.
