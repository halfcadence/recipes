# SDT "all my projects broken" — sds-core/tokens.css race (tekeste writeup)

**Reporter:** patanger (Rupesh Patange, Sr UX Designer) — "receiving this error in all my
projects/pages, hard reset + Summarize don't help." Screenshot showed the agent chat
auto-looping **"Runtime error detected. Please fix the issue."**
**Status as of 2026-07-16 16:40 UTC:** root cause proven; fix merged + validated red→green
locally; fix **rolling out in prod now** (not 100%); comms held until fully confirmed live.

## Symptom → real error
The chat string is the collapsed UI label from `Harmony-stores-designer`
(`runtime-error-autofix.ts` → `cleanUserPromptText`). The real error, pulled from the MDE
container log (`/mde/environments`, project `d00cd398-…`):

```
Frame "frame" crashed with a runtime error.
Error: Frame failed to compile — syntax/compile error in /app/project/src/app.css.
[postcss] ENOENT: no such file or directory, open '@amzn/sds-core/tokens.css'
```

`SDSRegistry/template/app.css` line 1 = `@import '@amzn/sds-core/tokens.css';`. That export
IS real (`@amzn/sds-core` package.json: `"./tokens.css" → "./src/tokens/css/rio/index.css"`,
`"files":["dist","src"]`), so a *complete* install has it. The crash = the file isn't on
disk yet when Vite/PostCSS compiles.

## Root cause (proven)
`DesignerAgent/src/ds-cache.ts::fastInjectDS` symlinks the primary DS archive, then installs
the **sub-packages (incl. `@amzn/sds-core`)**. That sub-package install was **fire-and-forget
(not awaited)** → `fastInjectDS` returned → Vite compiled the preview → `app.css`'s
`@import '@amzn/sds-core/tokens.css'` raced the still-running install → ENOENT → frame crash →
autofix loop. Hard reset/Summarize clear *project* state, not the install, so they don't help.

### Regression + fix (git history on ds-cache.ts)
- `1ff48c58` (tktran, 2026-05-06): sub-packages background-installed.
- **`91aabd05` (walawala, 2026-07-01): "make backgroundInstallSubPackages fully non-blocking
  (AutoSDE feedback)"** — armed the race. Prod crashes began **2026-07-14 17:44 UTC**.
- **`95e176e5` (shiauas, 2026-07-15, CR-289559752, SHIPPED, approved rozayc):** "Block on
  sds-core (+SDS siblings) install so app.css CSS import can't race" — `await
  ensureSubPackagesInstalled(...)`. Ships WITH a regression test.

## Blast radius (prod CloudWatch)
66 crash-prompt events / 16 projects / 11 users in 24h; first 2026-07-14 17:44 UTC. NOT
universal — only projects whose `app.css` imports sds-core/tokens.css AND lost the race.
(Distinct from the figma-export alarm V2288375299 — unrelated.)

## Proof the fix works — local red→green (verified 2026-07-16)
Test: `ds-cache.test.ts` → "does NOT resolve until the sub-package npm install completes
(blocking)" (holds npm `close` open, asserts `fastInjectDS` hasn't resolved, releases, asserts
resolution). Verified per tekeste recipe:
- Fix code → **16/16 pass** (green).
- Reverted cache path to buggy `void ensureSubPackagesInstalled(...)` → **blocking test FAILS**
  (`expected true to be false` at `expect(resolved).toBe(false)` — resolved before install done).
- Restored fix → **16/16 pass**, tree clean.

## Deploy tripwires (log-string flip — no new instrumentation needed)
Log group `/mde/environments`, prod acct 028255565206, profile `design-assistant`:
- BUGGY: `background-installing sub-packages`
- FIXED: `installing sub-packages (blocking)` and/or `all sub-packages already at`
- CRASH: `tokens.css` + `ENOENT`
Fix is LIVE-everywhere when: background-installing → 0 (sustained), a FIXED string > 0, ENOENT
→ 0 (sustained). Watch script: `./deploy-watch.sh [minutes]`.

### Rollout observed (hourly, UTC, 2026-07-16)
| hour | bg-install (buggy) | blocking (fixed) | tokens.css ENOENT |
|---|---|---|---|
| ≤13:00 | 1–5 | 0 | 0 |
| 14:00 | 4 | 2 | 0 |  ← first fixed container 14:44 UTC (rolling deploy)
| 15:00 | 1 | 5 | 1340 (old-session tail) |
| 16:00 | 1 | 7 | 0 |
Rolling, not complete: still ~1 buggy container/hr. Need bg→0 + ENOENT=0 sustained 2–3h.

Verified the blocking-install envs are PROD via `scan` on `design-assistant-prod-projects-v2`
(table key is pk/sk — `get-item` on projectId throws; use scan, the method that also confirmed
patanger's project).

## Remaining / next
- Watch until background-installing → 0 sustained and ENOENT stays 0 (a few hours).
- THEN: reply to patanger (held per request) — "confirmed platform race, fix now live, please
  hard-refresh / reopen; new projects unaffected."
- Nice-to-have follow-up: promote the ENOENT to a distinct frontend `errorName`/metric so this
  class is queryable as a metric, not a log grep.
