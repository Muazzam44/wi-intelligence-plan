# HumanOS Work Intelligence — status brief by functionality (21 Oct 2026)

One developer, AI-assisted (Claude Code implements, Codex reviews). Percentages are functional completeness of what a
user can do today, not plan-board progress. "Left" lists are the remaining tasks per functionality.

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
**Left:** (a) phrasing rule: "give me an algorithm" is answered as chat, only "write/generate…" proposes; (b) Aide refuses the same message three times in a row per user, needs a visible explanation in the UI.

### 2. Governed execution with signed evidence — 85%
**Works:** approved request → Engine (durable, exactly once) → worker → Engine-signed receipt → Orchestration verifies it → Console shows Completed with evidence. Fails closed when evidence cannot be stored. Engine capability descriptors register automatically on start-up.
**Left:** (a) Orchestration state to PostgreSQL (today a SQLite file); (b) Engine-side receipt read so a worker crash between completion and report self-heals; (c) permanent launcher folder and launch config; (d) three pre-existing failing tests to fix or quarantine.

### 3. Reviewed code generation (one model writes, another reviews) — 80%
**Works (proved 20 Oct):** "write a Python bubble sort … and have the draft reviewed" → draft by Opus (Claude CLI) with a signed receipt → review by the Codex CLI with a PASS verdict bound to the draft's digest → both shown in Evidence under one card.
**Left:** (a) Codex reviewer approval record (owner sign-off); (b) Sonnet as a second reviewer needs an Anthropic API key; (c) generated code is a reviewed draft only; nothing writes it into a repository yet (by design until the remediation plan's harness exists).

### 4. Console — 70%
**Works:** Home (needs-action / running / completed), Approvals with countersign, Evidence with drafts, reviews, receipts; WI screen merged to main; deploys on push.
**Left:** (a) 11 rows of the compatibility matrix (5 misaligned, 6 gaps: submitPlan 400, approval state/note, 400/404 classification, IAM via http(), chronology/receipts); (b) login required and mock mode off for non-local builds, CI running the e2e suite, ESLint; (c) "Estate not connected" banners until item 5 lands.

### 5. Real business side effects (projects, CRM) — 30%
**Works:** the pipeline writes a durable row in a local estate table; the full worker already knows how to call project-service-be and the CRM.
**Left:** (a) build and run project-service-be locally, prove `project.create` lands there; (b) connect estate reads (projects, CRM on Home) through the estate gateway; (c) CRM identity for the worker.

### 6. Work Intelligence service — 65% (15 of 23 modules verified)
**Works:** service platform and tenancy, task records, Engine worker, orchestration adapter, AI execution adapter, assurance runs and evaluation, employee rights and reviewer decisions, manager summary, public API, journey suite, capability evaluation, scope hardening.
**Left (8 modules, each needs its independent review):** reproducible build and attested image with green CI; Console read model; Console screen sign-off; reviewer completion and contradiction wiring; evaluation integrity; manager reporting-line scope; staging acceptance with three real users; real AI-assisted leg enablement. Plus one unreviewed local branch of nine commits to adopt or discard.

### 7. Workflow Engine production readiness — 60%
**Works:** durable journal, leases, worker protocol, signed receipts, descriptor certification, plan submission; proven under the pipeline above.
**Left:** push and merge the WI fix branch; gateway route and JWT wiring; live telemetry export; event-broker relay; WORM backups and non-superuser database role; hardening flags on in staging and the readiness review signed.

### 8. Identity (IAM) — 55%
**Works:** login, tenant membership, service-to-service secret, bridge into Orchestration.
**Left:** contract tests for the 46 endpoints' core flows; secret provisioning confirmed and a deployment README.

### 9. Orchestration production gates — 25%
**Works:** code is current with origin, deploys by CI, fail-closed configuration in development.
**Left:** gate-by-gate plan for the 16 live gates with owners; a dated full test-suite record; launch authorisation with two signed reviewers and a frozen release candidate.

### 10. AI provider governance (contracts, broker, model registry, qualification) — 0%
**Status:** specified as 22 modules in the plan repository, none approved or built. A separate programme that needs its own decision.

### 11. Launch governance (people, not code) — 0%
**Left:** DPIA, legal and worker consultation; independent penetration test; architecture amendment approval; standalone-router build/no-build decision; qualification corpus sign-off; a controlled pilot with named users. Owners are outside engineering; they gate everything after item 9.

