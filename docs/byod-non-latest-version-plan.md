# BYOD: Non-Latest DS Version Selection — Design Plan

**Author:** shiauas (with Claude)
**Date:** 2026-07-16
**Status:** PROPOSAL — needs decision on approach before implementation
**Context:** Follow-up from the BYOD template node-major fix. During browser testing on
personal stack `shiauas-jig`, we confirmed projects render on `/latest`, but a user
cannot pick a non-latest DS version. This doc proposes how to fix that.

---

## TL;DR

"Can't choose a non-latest version" has **two independent causes**, and the real
blocker is data, not code:

1. **The registry only publishes ONE version per DS.** `GET /api/packages/@amzn%2Fsds-components/versions`
   returns `{"versions":["0.2.363"],"latest":"0.2.363"}`. The picker faithfully shows
   the single version it's offered — so there's nothing to pick. **This is the primary blocker.**
2. **Even if multiple versions existed, the container path would reject them.**
   `assertRegisteredDS` (in `DesignerAgent/src/ds-cache.ts`) rejects any version whose
   template archive it can't read, and **only `/latest/` ships a template archive** — older
   versions have none. So a non-latest selection would fail the allowlist gate.

A complete fix therefore spans **three layers** (registry publish → container inject → allowlist),
owned by different teams. This doc scopes what *we* can fix vs. what needs the registry/DRB team.

---

## What we verified (ground truth, personal stack + prod registry)

| Check | Result |
|---|---|
| `GET /api/packages/@amzn%2Fsds-components/versions` | `["0.2.363"]` only (== latest) |
| `s3://…/@amzn/sds-components/0.2.362/template/…zip` (and .360/.350/.300) | **404 — no template archive for non-latest** |
| `…/0.2.362/manifest.json` (root) | 403 cross-account (grant is `*/template/*` only) |
| `inject-ds.ts` slow path | CodeArtifact `npm install` of the **exact selected version** — this is the intended non-latest mechanism |
| `assertRegisteredDS` (new since 7/15 image) | reads root manifest → 403 → rejects every DS; my staged fix probes `template/`, but non-latest has no archive there either |
| Container CodeArtifact grant | `codeartifact:GetAuthorizationToken/GetRepositoryEndpoint/ReadFromRepository` on domain `amazon` (149122183214) — so npm-install of any published npm version IS possible |

**Key insight:** the DS packages (`@amzn/sds-components@X`) exist in **CodeArtifact** at many
versions (that's npm), but the **Design Registry template archive** (the vite harness + baked
node_modules) is only built for `/latest/`. inject-ds's slow path already knows how to
`npm install` an arbitrary version from CodeArtifact — the gates in front of it are what break.

---

## Where non-latest breaks today (request flow)

```
Picker (web-ds-picker.tsx)
  → useRegistryVersions → GET /api/packages/{pkg}/versions
      ↳ registry returns ONLY [latest]  ← BLOCKER #1 (data): nothing to choose
  → create project with dsVersion=X
  → container boot → inject-ds.ts
      → assertRegisteredDS(pkg, X)
          ⚠ reads .../{X}/... → non-latest has no template archive → UnregisteredDSError  ← BLOCKER #2 (gate)
      → fastInjectDS (S3 template @ /latest/ only)   ← would give WRONG version for X anyway
      → slow path: npm install pkg@X from CodeArtifact  ← THIS is the correct non-latest path, but never reached
```

---

## Proposed fix — three options

### Option A — Full non-latest support (correct, cross-team)  ⭐ recommended IF product wants it

Make non-latest actually work end-to-end.

1. **Registry/DRB (not our package):** publish `/versions` with the real version list, and
   keep publishing template archives for at least the last N versions (or a documented window).
   *Owner: DRB/registry team. This is the load-bearing dependency — without it there is nothing
   to select and no template to fetch.*
2. **`assertRegisteredDS` (ours):** stop gating on the template archive. Gate on **CodeArtifact
   package existence** (the authoritative source for "is this a real published version") OR on the
   registry `/versions` list. Fail-open on infra error (unchanged).
3. **`fastInjectDS` (ours):** when `selectedVersion !== latest`, skip the `/latest/` S3 template
   fast-path (it's the wrong version) and go straight to the CodeArtifact `npm install` slow path
   for the pinned version. (Fast path stays for the common latest case.)

- **Pros:** actually delivers the feature; each layer becomes correct.
- **Cons:** needs the registry team; slow path is ~30-60s npm install vs ~5s template symlink;
  larger change.

### Option B — Gate-only fix: unblock the mechanism we own, leave data to registry (small, safe)  ⭐ recommended to ship NOW

Do only the parts in our packages so the moment the registry publishes more versions, it works —
and today's behavior is strictly more correct.

1. **`assertRegisteredDS`:** rewrite to verify against **CodeArtifact** (or the registry
   `/versions` list) instead of the template archive. This removes the false rejection and makes
   the check meaningful for any published version.
2. **`fastInjectDS`:** route non-latest to the npm slow path (as A.3).
3. **No registry dependency, no IAM change.** Picker still shows only `[latest]` until the
   registry publishes more — but nothing is falsely blocked, and non-latest works via npm the day
   a version list appears.

- **Pros:** entirely in `DesignerAgent`; ships now; no cross-team wait; converts a latent
  correctness bug into correct behavior.
- **Cons:** user *still* can't pick non-latest until the registry publishes versions (BLOCKER #1
  is out of our hands) — so this is enabling, not delivering, the feature.

### Option C — Minimal: just fix the false rejection (tiny)

Only fix `assertRegisteredDS` so it stops rejecting valid DSes (the bug my rebuild surfaced).
Leave version routing alone. This is the **already-written, already-tested** change in my working
tree (probe `template/` prefix). Note: this does NOT enable non-latest — it only ensures inject-ds
runs for the latest case; non-latest would still 404 in the probe.

- **Pros:** smallest; already done (22 tests green); removes the `UnregisteredDSError` log noise.
- **Cons:** doesn't move the feature forward at all; arguably the archive-probe is the wrong
  allowlist source (CodeArtifact is authoritative for versions).

---

## Recommendation

**Ship Option B now**, and file a registry-team ask for Option A.1 (publish real version lists +
retain template archives for a version window). Rationale:

- BLOCKER #1 (registry publishes only latest) is the true reason you can't pick non-latest, and
  it's not in our code. Nothing we ship makes the dropdown multi-version until the registry does.
- But B makes our half correct and *ready*: the allowlist becomes meaningful (CodeArtifact-based),
  and non-latest injection works the instant a version list exists — no second deploy needed.
- B supersedes my current staged Option-C change (archive-probe), which gates on the wrong thing.

**Open question for you:** does product actually want non-latest selection, or is
"always latest" the intended BYOD model? If the latter, we only need **Option C** (stop the false
rejection) and should make the picker's single-version state explicit rather than pursue A/B.

---

## Concrete changes if we pick B

- `DesignerAgent/src/ds-cache.ts`
  - `assertRegisteredDS(pkg, version)`: replace template-archive/root-manifest read with a
    CodeArtifact existence check (`codeartifact describe-package-version` or list-package-versions),
    or call the registry `/api/packages/{pkg}/versions` and assert `version ∈ versions`. Keep
    fail-open on infra error, keep structured-status branching.
- `DesignerAgent/src/inject-ds.ts`
  - Branch: `if (dsVersion === latestOf(pkg)) fastInjectDS(...) else npmInstallSlowPath(...)`.
    Requires knowing "latest" (from the registry `/versions` call reused above).
- Tests: version ∈ list → pass; version ∉ list → UnregisteredDSError; infra error → fail-open;
  non-latest → slow path chosen.
- **No CDK/IAM change** (CodeArtifact grant already present; registry API reachable via existing
  execute-api grant — verify the container's `execute-api` resource covers `/api/packages/*`).

## Registry-team ask (for A, file separately)

- `/api/packages/{pkg}/versions` should return the full published version list, not just latest.
- DRB should publish (and retain) `template/archive.*` for the last N versions, or document that
  BYOD platform projects are latest-only by design.

---

## Status of related work (already done)

- Template resolver node-major fix: **CR-289839650** (Shared) + **CR-289839745** (CDK IAM). Verified.
- ds-cache node-major probe + non-blocking sub-package install: on new platform image, deployed to
  `shiauas-jig`, SDS boot 470s→6.7s confirmed in browser.
- `assertRegisteredDS` archive-probe (Option C): written + 22 tests green in working tree, NOT
  committed/deployed — supersede with B if we go that route.
