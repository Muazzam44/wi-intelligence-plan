# HumanOS Work Intelligence — status brief by functionality (21 Oct 2026)

One developer, AI-assisted (Claude Code implements, Codex reviews). Percentages are functional completeness of what a
user can do today, not plan-board progress. "Left" lists are the tasks to put deadlines on.

## Repositories

| repository | what it holds | main today |
|---|---|---|
| https://github.com/Rapidtackltd/humanos-ai-orchestration | Orchestration: Aide, approvals, dispatch, evidence, reviewer profiles | `6b69ec8` (21 Oct, deployed by CI) |
| https://github.com/Rapidtackltd/humanos-console | Console UI + the capability worker (`tools/`) | `193175e` (21 Oct, deployed to console.nessovo.com) |
| https://github.com/Rapidtackltd/humanos-work-intelligence | Work Intelligence service (assurance, rights, summaries) | in sync; 15 of 23 modules verified |
| https://github.com/Rapidtackltd/workflow-engine | Workflow Engine (durable execution, receipts) | `c73b635`; the WI fix branch `codex/wi-mvp-integration` is local only |
| https://github.com/Rapidtackltd/humanos-backend-services | Estate services (projects, CRM, IAM, AI execution) | unchanged by this work |
| https://github.com/Muazzam44/wi-intelligence-plan | Plan, briefs, this document | `f9f2003` |

## Functionality status

### 1. Governed request intake — 90%
**Works:** a user asks Aide in plain language; the planner drafts a governed request; a *different* person must countersign (two-person rule enforced); Approvals shows whether the Engine can run it before anyone approves.
**Left:** (a) phrasing rule: "give me an algorithm" is answered as chat, only "write/generate…" proposes — 1 d; (b) Aide refuses the same message three times in a row per user, needs a visible explanation in the UI — 0.5 d.

### 2. Governed execution with signed evidence — 85%
**Works:** approved request → Engine (durable, exactly once) → worker → Engine-signed receipt → Orchestration verifies it → Console shows Completed with evidence. Fails closed when evidence cannot be stored. Engine capability descriptors register automatically on start-up.
**Left:** (a) Orchestration state to PostgreSQL (today a SQLite file) — 0.5 d; (b) Engine-side receipt read so a worker crash between completion and report self-heals — 3–4 d; (c) permanent launcher folder and launch config — 0.5 d; (d) three pre-existing failing tests to fix or quarantine — 1 d.

### 3. Reviewed code generation (one model writes, another reviews) — 80%
**Works (proved 20 Oct):** "write a Python bubble sort … and have the draft reviewed" → draft by Opus (Claude CLI) with a signed receipt → review by the Codex CLI with a PASS verdict bound to the draft's digest → both shown in Evidence under one card.
**Left:** (a) Codex reviewer approval record (owner sign-off) — 0.5 d; (b) Sonnet as a second reviewer needs an Anthropic API key — 0.5 d once the key exists; (c) generated code is a reviewed draft only; nothing writes it into a repository yet (by design until the remediation plan's harness exists).

### 4. Console — 70%
**Works:** Home (needs-action / running / completed), Approvals with countersign, Evidence with drafts, reviews, receipts; WI screen merged to main; deploys on push.
**Left:** (a) 11 rows of the compatibility matrix (5 misaligned, 6 gaps: submitPlan 400, approval state/note, 400/404 classification, IAM via http(), chronology/receipts) — 6–8 d; (b) login required and mock mode off for non-local builds, CI running the e2e suite, ESLint — 3–4 d; (c) "Estate not connected" banners until item 5 lands.

### 5. Real business side effects (projects, CRM) — 30%
**Works:** the pipeline writes a durable row in a local estate table; the full worker already knows how to call project-service-be and the CRM.
**Left:** (a) build and run project-service-be locally, prove `project.create` lands there — 3–6 d; (b) connect estate reads (projects, CRM on Home) through the estate gateway — 1–2 d; (c) CRM identity for the worker — 1 d.

### 6. Work Intelligence service — 65% (15 of 23 modules verified)
**Works:** service platform and tenancy, task records, Engine worker, orchestration adapter, AI execution adapter, assurance runs and evaluation, employee rights and reviewer decisions, manager summary, public API, journey suite, capability evaluation, scope hardening.
**Left (8 modules, each needs its independent review):** reproducible build and attested image with green CI (6–8 d); Console read model (2 d); Console screen sign-off (1 d); reviewer completion and contradiction wiring (5–7 d); evaluation integrity (3–4 d); manager reporting-line scope (4–5 d); staging acceptance with three real users (5–7 d, needs the people); real AI-assisted leg enablement (5–6 d). Plus one unreviewed local branch of nine commits to adopt or discard (1–2 d).

### 7. Workflow Engine production readiness — 60%
**Works:** durable journal, leases, worker protocol, signed receipts, descriptor certification, plan submission; proven under the pipeline above.
**Left:** push and merge the WI fix branch (1 d); gateway route and JWT wiring (4–5 d); live telemetry export (3 d); event-broker relay (5 d); WORM backups and non-superuser database role (3–4 d); hardening flags on in staging and the readiness review signed (3–4 d).

### 8. Identity (IAM) — 55%
**Works:** login, tenant membership, service-to-service secret, bridge into Orchestration.
**Left:** contract tests for the 46 endpoints' core flows (6–8 d); secret provisioning confirmed and a deployment README (2 d).

### 9. Orchestration production gates — 25%
**Works:** code is current with origin, deploys by CI, fail-closed configuration in development.
**Left:** gate-by-gate plan for the 16 live gates with owners (3 d); a dated full test-suite record (1 d, 25-minute run); launch authorisation with two signed reviewers and a frozen release candidate (3–5 d plus reviewers).

### 10. AI provider governance (contracts, broker, model registry, qualification) — 0%
**Status:** specified as 22 modules in the plan repository, none approved or built. This is the long programme (roughly 59–72 developer-weeks with reviews) and is deliberately outside this brief's deadlines; it needs its own decision.

### 11. Launch governance (people, not code) — 0%
**Left:** DPIA, legal and worker consultation; independent penetration test; architecture amendment approval; standalone-router build/no-build decision; qualification corpus sign-off; a controlled pilot with named users (6–8 weeks). Owners are outside engineering; they gate everything after item 9.

## Suggested order for deadlines

1. Items 2(a,c,d), 3(a), 1(a) — about one week; closes the loose ends of what already works.
2. Item 5 — about two weeks; makes the demo create real projects and clears the Console banners.
3. Item 6 — about eight to ten weeks of reviews; completes the Work Intelligence service.
4. Items 4, 7, 8, 9 — about ten to twelve weeks if the same developer does them; parallel if their teams do.
5. Item 11 raised now in parallel; item 10 as a separate programme decision.
