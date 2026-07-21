# How Stores Designer Installs a BYOD Registry Project & Uploads to Protozoa

An explainer + self-quiz for the two flows we've been debugging. Everything here is
verified against prod/personal-stack logs + code, not hand-waved. Read the diagram,
then take the quiz at the bottom (answers included) to check your understanding.

> Why this exists: understanding the flow end-to-end is how we know **what to test and
> what to change**. Each numbered stage below is a place a bug can live — and the callouts
> mark the exact spots we found bugs in this project.

---

## Part 1 — Big picture (two separate flows)

```
  FLOW A: CREATE + INSTALL a BYOD project            FLOW B: SHARE to Protozoa
  (get a live, editable design-system project)       (publish a built frame as a URL)

  Picker → Projects API → MDE container              Share btn → build frame → S3 preview
         → fetch DS template → run DS → render                 → Protozoa API → CDN URL
```

They're chained: **you must have a rendered project (A) before you can share it (B).**
B reads the *built output* of A from an S3 preview bucket.

---

## Part 2 — FLOW A: Create + install a BYOD design-system project

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ FRONTEND (Harmony @ dev.console.harmony.a2z.com / stores-designer.harmony.a2z.com)│
│                                                                                   │
│  1. DS Picker (web-ds-picker.tsx)                                                 │
│       • useRegistryPackages → GET registry.design.amazon.dev/api/packages         │
│       • useRegistryVersions → GET .../api/packages/{pkg}/versions                 │
│         ⚠️ BUG-ZONE #4: registry returns only [latest] (old versions pruned) →    │
│            you can't pick non-latest. Registry-side policy, not our code.         │
│  2. User picks package + version → "Create Project"                               │
│  3. POST /projects-v2  { name, imageVariant:'platform', designSystems:[{pkg,ver}] }│
└─────────────────────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ PROJECTS API LAMBDA  (design-assistant-{env}-projects-api)                        │
│                                                                                   │
│  4. handleCreateProjectV2 → writes project row to DynamoDB (projects-v2)          │
│  5. Frontend then GET /projects-v2/{id}  → handleGetProjectV2                      │
│       → ensureMdeEnvironment(projectId):                                          │
│           imageVariant==='platform' → new TemplatedEnvironmentManager(            │
│               resolveTemplateArtifactUri({ projectId, designSystems }))           │
│                                                                                   │
│       resolveTemplateArtifactUri (templateResolver.ts):                           │
│           builds S3 URL for the DS template ZIP at .../{pkg}/latest/template/...  │
│         ✅ FIXED (BUG-ZONE #1): it HARDCODED node22; Stencil/Cloudscape ship       │
│            node20 → 403 → "failed to load". Now HEAD-probes [node22,node20],      │
│            returns the one that exists; TemplateArchiveNotFoundError if none      │
│            (e.g. Books ships no archive at all).                                  │
│         ⚠️ NOTE: it always uses /latest/ regardless of selected version.          │
│  6. CreateEnvironmentFromWarmPool(devfile with TEMPLATE_ARTIFACT_URI=<that URL>)  │
│         ⚠️ BUG-ZONE (personal stack only): inline devfile >1024B → ParamMaxLenError│
│            (long -shiauas-jig- names). Prod ~1010B, fine. Test harness shortens it.│
└─────────────────────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ MDE WARM-POOL CONTAINER  (logs: /mde/environments, stream = env-id)               │
│  Image: platform MDE image (DesignerAgent baked in). Warm pool pre-pulls it.      │
│                                                                                   │
│  7. bootstrap-template.ts: reads TEMPLATE_ARTIFACT_URI, SigV4-GETs the ZIP from   │
│     the DRB registry bucket (registry-prod-137769144454), unzips into /app/project│
│       • the ZIP contains a vite app + node_modules with the DS at /latest/        │
│       • cross-account read allowed only on the  */template/*  prefix (key detail!)│
│  8. agent proxy (OpenCode) starts on :8080; first request triggers bootstrap()    │
│  9. bootstrap(): restore from S3 (source-sync) → inject-ds → start vite (:5173)   │
│                                                                                   │
│     inject-ds.ts (installs the *selected version* of the DS on top of template):  │
│       a. assertRegisteredDS(pkg, ver)   ← allowlist gate                          │
│          ✅ FIXED (BUG-ZONE #3): read root manifest.json → 403 cross-account →     │
│             rejected EVERY DS ("UnregisteredDSError"). Now probes template/ prefix.│
│          ⚠️ still can't validate a pruned non-latest version (no archive exists). │
│       b. fastInjectDS (ds-cache.ts): download platform archive @ version → cache  │
│          → symlink into node_modules.                                             │
│          ✅ FIXED (BUG-ZONE #2a): hardcoded node22 here too → Cloudscape 403 →      │
│             npm fallback. Now probes [node22,node20].                             │
│          ✅ FIXED (BUG-ZONE #2b): sub-package install was BLOCKING → SDS hung 8min │
│             → UI "failed to load". Now background (non-blocking) → boots in ~7s.   │
│       c. slow path (if fast fails): CodeArtifact npm install of pkg@version.      │
│          ← THIS is how a true non-latest version would install (if retained).     │
│  10. vite serves the app; frontend shows it in an iframe (env-{id}.mde....dev)    │
└─────────────────────────────────────────────────────────────────────────────────┘

Result: a live, editable project rendering the design system. ✅
```

### The one theme behind almost every bug we found
**Cross-account reads against the DRB registry bucket are granted ONLY on the
`*/template/*` prefix.** Three separate functions tried to read the version-root
`manifest.json` (outside that grant) → 403 → each failed in its own way. All three now
probe the `template/` prefix instead. If you remember one thing: *the container can read
`{pkg}/{ver}/template/…` but NOT `{pkg}/{ver}/manifest.json`.*

---

## Part 3 — FLOW B: Share a frame to Protozoa

Source of truth: `Harmony-stores-designer/docs/protozoa-integration.md` + `useCreatePrototype.ts`.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ In the running project (Flow A must have succeeded — we need built assets)        │
│                                                                                   │
│  1. Click "Share with Protozoa" on a frame                                        │
│  2. useProtozoaAuth: hidden iframe loads protozoa.amazon.dev/authenticate/        │
│       → sets CloudFront Signed Cookies (Protozoa auth = CFS, not IAM)             │
│  3. Create-Prototype dialog: title, platforms, permissions                        │
│  4. POST /export to the MDE agent → vite BUILDS the frame → writes built assets   │
│     (index.html, assets/*.js/css) to the S3 PREVIEW bucket                        │
│       (design-assistant-{env}-preview). ← this is the build output of Flow A.     │
│  5. Frontend fetches those built files from the preview bucket                    │
│       (s3-preview-client.ts, using Harmony auth → IAM role → S3)                  │
│  6. POST protozoa.amazon.dev/api/createPrototype  (credentials:"include")         │
│       → returns { id, guid }                                                      │
│  7. POST /api/getPresignedURLs { guid, keys[] }  → S3 upload URLs                 │
│  8. PUT each built file to its presigned URL (parallel batches)                   │
│  9. Done → shareable URL: https://protozoa.amazon.dev/#/{id}/                     │
│           public URL:    https://.../prototypes/{guid}/                           │
└─────────────────────────────────────────────────────────────────────────────────┘
```

Key contrasts with Flow A:
- **Auth:** Flow A container uses SigV4/IAM (cross-account S3); Protozoa uses **CloudFront
  Signed Cookies** set via a hidden `/authenticate/` iframe.
- **Direction:** Flow A *reads* the registry template into the container. Flow B *writes*
  the container's built output out to Protozoa's S3 via presigned URLs.
- **Stage quirk:** dev/beta/gamma Protozoa host differs; currently some paths hardcode prod
  due to a CORS issue on dev.protozoa.

---

## Part 4 — What this tells us to test / change

| Area | Status | Test / change |
|---|---|---|
| Template resolver node major | ✅ fixed + verified | CR-289839650 (Shared) + CR-289839745 (CDK IAM) |
| ds-cache node major + blocking install | ✅ fixed, deployed to personal, SDS 8min→7s verified | fold into DesignerAgent CR |
| assertRegisteredDS root-manifest 403 | ✅ fixed (probe template/), 22 tests green | not yet committed/deployed |
| Non-latest version selection | ⚠️ registry-side blocker | registry must RETAIN old versions (dirs + template archives); then our slow-path npm install handles it |
| Protozoa export | ✅ appears healthy (E2E scenario 10 covers it) | no change identified; retest only if we touch build/preview |
| Personal-stack devfile >1024B | ⚠️ test-harness only | not a prod issue; don't ship a "fix" for it |

**Bottom line for "is there a blocker?":** The *code* path for non-latest exists (slow-path
npm install). The real blocker is the **registry prunes old versions** (SDS keeps only latest;
Meridian keeps 2 but its non-latest has no template archive). So shipping the code we've verified
(resolver + ds-cache + assertRegisteredDS) is safe and correct for the *latest* case — which is
every project today. Non-latest needs a registry retention policy change, owned by the DRB team.

---

# QUIZ (answers below — cover them first)

**Q1.** A user picks Cloudscape and the project shows "failed to load after multiple attempts."
The container reached RUNNING. Name the single most likely root cause and the one log line you'd grep for.

**Q2.** Why can the MDE container fetch `{pkg}/{version}/template/archive.…zip` but NOT
`{pkg}/{version}/manifest.json` — and why did that one fact cause *three* separate bugs?

**Q3.** SDS projects took ~8 minutes to boot (then timed out in the UI) while Cloudscape booted
in seconds. Neither is about the design system's *content*. What was different, and where's the fix?

**Q4.** True/False: `resolveTemplateArtifactUri` downloads the exact DS version the user selected.
Explain.

**Q5.** You select Meridian `8.13.1-experimental.2` (a non-latest version that IS in the
`/versions` list). Walk through what the container fetches at boot vs. what installs the pinned
version — and why the pinned version might still fail.

**Q6.** In Flow B (Protozoa), what must have happened in Flow A before a frame can be shared,
and which S3 bucket links the two flows?

**Q7.** Protozoa and the BYOD template fetch use two *different* auth mechanisms. Name both and
where each is used.

**Q8.** "We should just ship the code we know works now." For which set of projects is that
statement fully correct today, and what single external thing must change for non-latest to work?

---

## ANSWERS

**A1.** The template resolver asked for the wrong node major (`archive.al2023-x64-node22.zip`)
but Cloudscape ships node20 → S3 `403 Forbidden` on the fetch. Grep `/mde/environments` (stream =
env id) for `bootstrap-template.*403` or `Forbidden`. (Fixed: probe node22→node20.)

**A2.** The DRB registry bucket is cross-account; its bucket policy grants the MDE role
`s3:GetObject` only on the `*/template/*` prefix. `manifest.json` sits at the version *root*, so a
GET there 403s (and without `ListBucket`, 403 is indistinguishable from "no such key"). Three
functions read that root manifest — `resolveTemplateArtifactUri` (well, it constructed a root-ish
assumption), `ds-cache resolveArchiveName`, and `assertRegisteredDS` — so all three silently failed
(fell back to node22, or rejected the DS). Fix: all probe the readable `template/` prefix.

**A3.** SDS pulls 7 sub-packages; the old image installed them **blocking** via CodeArtifact npm
(~470s), so bootstrap didn't finish before the UI's retry limit → "failed to load." Cloudscape is a
single package → no blocking install. Fix is in `ds-cache.ts`: `backgroundInstallSubPackages`
(non-blocking) — mainline already had it; the personal stack was running a stale image.

**A4.** **False.** It always builds `.../{pkg}/latest/template/archive.…` — it ignores the selected
version (there's even a comment saying so). The *template* is always latest; the user's selected
version is layered on later by `inject-ds` (fast-path cache/symlink for latest, or slow-path
CodeArtifact npm install for a specific version).

**A5.** At boot, `bootstrap-template` fetches `@amzn/meridian/**latest**/template/...` (resolver
hardcodes latest) — so the container starts with 8.13.1's template. Then `inject-ds` would
`npm install @amzn/meridian@8.13.1-experimental.2` from CodeArtifact (slow path) to pin the
selected version. It can still fail because (a) `assertRegisteredDS` must pass, and (b) the exact
version must be installable from CodeArtifact; the registry template archive for that non-latest
version doesn't exist (only latest has one), so only the npm path can supply it.

**A6.** Flow A must have produced a **built, rendered frame** — the MDE container's vite build
wrote the compiled assets (index.html, JS/CSS) to the **`design-assistant-{env}-preview`** S3
bucket. Flow B reads those exact files from that preview bucket and re-uploads them to Protozoa.
No successful build → nothing to share.

**A7.** (1) **SigV4 / IAM** — the MDE container reading the DRB registry template cross-account,
and the frontend reading the preview bucket. (2) **CloudFront Signed Cookies** — Protozoa's own
auth, set by a hidden iframe hitting `protozoa.amazon.dev/authenticate/`; all Protozoa API calls
use `credentials:"include"`.

**A8.** Fully correct for **every project that uses the latest DS version** — which is all of them
today, because the registry only publishes latest. The one external change needed for non-latest:
the **DRB/registry team must retain old versions** (both the version directory and its
`template/` archive) instead of pruning to latest-only. Our code (resolver + ds-cache +
assertRegisteredDS + inject-ds slow path) is then ready to handle it with no further change.
