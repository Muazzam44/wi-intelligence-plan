# HumanOS Work Intelligence — what is left, as small tasks for one developer (2026-10-21)

Re-baselines `EXECUTION-TIMELINE-1DEV.md` (16 Oct) after the work of 16–21 October. Every task below is
sized for **one developer** working serially, operating Claude Code for implementation and Codex for
review. Estimates are developer-days (`d`) or weeks (`w`) and include the review rounds the playbook
budgets (Tier-0: 3–5 rounds, 2–3 days each). Dates assume a start on Monday 26 October 2026.

Sources: `plan/` (22 REM modules, all `draft`, 2 `blocked-needs-decision`), the WI service repo's plan
(15 of 23 modules verified, 8 in flight), `EXECUTION-PLAYBOOK.md` v2, `EXECUTION-TIMELINE-1DEV.md`,
`WI-Execution-Missing-Backend-2026-10-19.md`, `WI-Reviewed-Codegen-Scenario-2026-10-19.md`.

## 0. Done since the timeline was written (so the plan does not double-count it)

| done 16–21 Oct | effect on the plan |
|---|---|
| Execution pipeline proved end to end: countersign → Engine → worker → signed receipt → COMPLETED tile | closes the "dispatcher / receipt" gap; part of Phase 4.1 Orchestration |
| Orchestration: fail-closed evidence store (B), automatic Engine descriptor registration (D), reviewed code generation (C1), Codex CLI reviewer profile + review-run + artifact read (C4), plan id per request | merged to `main` and deployed via `deploy.yml` |
| Worker: receipt relay (A), model-pinned `code.generate`, `code.review` (C2) | merged to humanos-console `main` |
| Console: WI integration branch, reviews shown under their draft, bindability warnings (C3) | merged to `main`, deployed to console.nessovo.com |
| Live proof: "write a Python bubble sort … and have the draft reviewed" → Opus (Claude CLI) draft, Codex PASS review, both Engine-signed | the scenario the owner asked for works locally |
| Orchestration `main` reconciled with `origin/main` (was 126 ahead / 8 behind) | Phase 4.1 "reconcile main" item done |
| Console `codex/wi-console-integration` merged (WI-M14 screen) | Phase 4.3 "merge" item done |

## 1. Track A — finish the WI MVP (Phase 0, repo `humanos-work-intelligence`)

15/23 modules are `implementation-verified`. The 8 below are in flight. Tier-0 items carry the dual-review
allowance; the "waiting on" column is outside the developer's control and must be raised on day 1.

| # | task | description | est. | waiting on |
|---|---|---|---|---|
| A1 | WI-M15 reproducible build, round 4 → first real CI run | verify packet hashes, Reviewer A, Codex, fix round; provision `HUMANOS_BACKEND_READ_TOKEN`; first green CI run with image digest; close P-8 / OI-01 | 6–8 d | OI-54 auth-lib publication, OI-22 registry environment |
| A2 | WI-M21 fresh independent verdict on the current SHA | fix the fix-check findings red-first, rebuild the packet, Reviewer A + Codex, fix round | 4–6 d | — |
| A3 | WI-M20 evaluation integrity, cross-family review | clear the OI-35 deviation with a second-family review and one fix round | 3–4 d | — |
| A4 | WI-M19 reviewer completion & contradiction wiring, full dual review | packet, Reviewer A, Codex, expect two fix rounds | 5–7 d | — |
| A5 | WI-M22 manager reporting-line scope, full dual review | packet, Reviewer A, Codex, fix round | 4–5 d | — |
| A6 | CP-01 approval; flip WI-M23 and WI-M14 | archive the change proposal, flip the two Tier-1 modules to verified with their review records | 1 d | WI owner signs CP-01 |
| A7 | Tier-1 review records for WI-M01, M03, M08, M11, M12, M13 | half a day each, recorded in front-matter | 3 d | — |
| A8 | WI-M16 Day-10 staging acceptance | run the runbook with P1–P3 and the owner, sanitised evidence bundle, independent bundle review (A8), Tier-0 dual review of runbook + bundle | 5–7 d | three real people + owner on the same days; staging secrets |
| A9 | WI-M17 real AI-assisted leg enablement | dual review, P-5 enablement readback (P-5 / P-7 / P-2a) | 5–6 d | — |
| A10 | Commit per module, push, open the PR, board 23/23 | one commit per module, PR for the named-human merge | 1 d | PR approval (WI owner) |
| A11 | Decide the stray `worktree-agent-a0c049a0…` branch (+9 "Wave 0 remediation" commits from the 21 Oct fan-out) | review against the 21 Oct backup, cherry-pick what is wanted onto a reviewed branch or delete; nothing of it is on a remote | 1–2 d | — |

**Track A total: 38–50 d ≈ 8–10 weeks** (timeline said W1–W8; A11 and the extra fix rounds already observed add one to two weeks).

## 2. Track B — execution-pipeline follow-ups opened this week (repos: orchestration, console, hbs-work)

Small, independent, and most of them unblock the demo for real projects. Do B1–B4 before Track A if the
owner wants the Console demo on a real estate.

| # | task | description | est. |
|---|---|---|---|
| B1 | Build and run project-service-be locally (status doc P1) | build from `D:\hbs-work`, `projects_db` on Postgres :55433, IAM :8181 wiring, launcher + env, S2S create proves a row | 2–4 d |
| B2 | Switch to the real worker for `project.create` (P2) | run `real-worker.py` against B1; prove COMPLETED with `estate_provenance.service=project-service-be` and a row in `projects_db` | 1–2 d |
| B3 | Estate reads behind the Console banners (G6) | run the estate api-gateway, set `HUMANOS_ESTATE_GATEWAY_URL`; clears "Estate not connected" on Home | 1–2 d (after B1) |
| B4 | Orchestration state to Postgres (P3) | `wi_orch` database, psycopg in the venv, `alembic stamp head`, restart; SQLite-era requests do not migrate | 0.5 d |
| B5 | Durable launcher folder (P4) | move `wi-stack` + `wi-local` out of the session scratchpads to a permanent folder, fix paths, commit only `launch.json` | 0.5 d |
| B6 | Codex approval record | fill the approval line in `docs/gate1-codex-cli-evidence.md` (owner decision) and record it in `plan/registers/decisions.md`; until then `codex.cli` is local-only | 0.5 d + owner |
| B7 | Anthropic API key route (optional) | put a key in the model service, flip `HUMANOS_CODEGEN_AUTHOR_MODEL=claude-opus-4-7` and `HUMANOS_CODE_REVIEWERS=codex.cli,claude-sonnet-4-6`; gives Opus by name plus a Sonnet review | 0.5 d + key |
| B8 | Engine pull of receipts (brief Prompt C) | Engine persists receipts per attempt and exposes them; Orchestration's reconcile loop reads them for `DISPATCHED` rows without a report; resilience when a worker dies between complete and report | 3–4 d |
| B9 | Three pre-existing failing Orchestration tests | `test_gate2b_p0_red_probes` (unknown contract `h30.send_message@1.0.0`) and two cancellation tests; fix or quarantine with reasons | 1 d |
| B10 | Verify the two deployments triggered on 21 Oct | read the Actions runs for orchestration `docker-service-deploy` and console `static-site-deploy`; confirm the health gate and console.nessovo.com serve the new build; fix if red | 0.5–1 d |
| B11 | Delete or archive merged branches | eight `wi/*` and `gate2-*` branches are now in `main` on both repos; the eight prefilled PRs are superseded | 0.25 d |
| B12 | Engine `aiGatewayModel` default `claude-cli-sonnet` is not a model the model service lists | change the default or register the id; only matters if the Engine's own AI-task path is used | 0.5 d |
| B13 | Prompt phrasing rule in the planner | "give me an algorithm of X" answers as chat; widen the `code.generate` menu rule or document the phrasing | 0.5–1 d |

**Track B total: 12–19 d ≈ 3–4 weeks**, of which B1–B5 (≈ 5–9 d) are what the real-estate demo needs.

## 3. Track C — decisions and external gates (Phase 1, no developer time, longest lead times)

Raise all of them in the first week; each blocks a later track.

| # | item | owner | blocks |
|---|---|---|---|
| C1 | OI-02 standalone router build / no-build | CTO / Architecture | REM-M21 (stays blocked; no-build removes it) |
| C2 | OI-04 qualification corpus sign-off | AI Evaluation Lead | REM-M19 |
| C3 | S12-BL-019 DPIA, legal and worker consultation | HR / Legal / DPO | pilot (Track G) |
| C4 | S12-BL-018 independent penetration test booked | Security | Stage 12A gate |
| C5 | OI-01 monorepo toolchain confirmation (Maven modules, JDK, CI entry points) | first implementer (the developer, 1 d) | Track E build start |
| C6 | A-01 architecture amendment approval | Architecture board | gate S12A-G-001 |
| C7 | Codex CLI approval (B6) and the Claude-CLI-in-ai-execution posture | owner | any non-local use of the CLI providers |

## 4. Track D — approve the remediation specs (Phase 2, repo `D:\intelligence`)

All 22 REM modules are still `draft`. Nothing in Track E can start until its wave is `spec-approved`.

| # | task | description | est. |
|---|---|---|---|
| D1 | Adversarial critique of the whole plan (`plan-critic`) | run, fold accepted findings into the specs | 2 d |
| D2 | Spec councils, wave 1: REM-M01, M02, M03 | five-lens council per Tier-0 module, verdict in front-matter | 3 d |
| D3 | Spec councils, wave 2: REM-M04, M05, M06, M07 | same | 4 d |
| D4 | Spec councils, wave 3–5 Tier-0: REM-M08, M09, M10, M11, M14, M20 | same | 6 d |
| D5 | Risk-tier sanity pass and lint clean (`plan_lint --analyze`) | fight tier inflation/deflation, fix drift, flip wave-1 to `spec-approved` | 1 d |
| D6 | Lighter councils for Tier-1 specs (REM-M12, M13, M15–M19) | run in the week before each wave | 3 d spread |

**Track D total: ≈ 19 d ≈ 4 weeks** (timeline W9–W12).

## 5. Track E — build the remediation (Phase 3, repo `D:\hbs-work`)

Implementation days are the workbook's; "review" is the Tier-0 dual-review allowance (1–2 weeks each).
One module at a time, Tier-0 first inside each wave, Tier-1 in the gaps while a packet is with Codex.

| wave | module | what it delivers (one line) | impl. | review | tier |
|---|---|---|---|---|---|
| 1 | REM-M01 Disable central CLI defaults | no central service may default to a user's subscription CLI | 1 d | 1–2 w | T0 |
| 1 | REM-M02 humanos-ai-contracts v1 | the versioned contract every provider call binds to | 8 d | 1–2 w | T0 |
| 1 | REM-M03 Claude CLI process safety | bounded, non-interactive, no-leak CLI execution everywhere | 5 d | 1–2 w | T0 |
| 2 | REM-M04 Endpoint AI Runtime Broker | the only path through which endpoint/subscription runtimes execute | 15 d | 1–2 w | T0 |
| 2 | REM-M05 Provider-scoped credential resolution | per-provider, per-tenant keys; no shared fallbacks | 8 d | 1–2 w | T0 |
| 2 | REM-M06 Evidence-object persistence | classified, encrypted evidence objects; no raw prompts in domain stores | 15 d | 1–2 w | T0 |
| 2 | REM-M07 Exact model-deployment registry | every route names an exact deployment, never an alias | 12 d | 1–2 w | T0 |
| 3 | REM-M08 Qualification lifecycle & hard gate | only qualified, unexpired task×effort configurations route | 20 d | 1–2 w | T0 |
| 3 | REM-M09 Eligibility router & canonical fallback | policy-checked, audited substitutions only | 22 d | 1–2 w | T0 |
| 3 | REM-M10 Complete inference lineage | every inference traceable end to end | 10 d | 1–2 w | T0 |
| 3 | REM-M11 Monorepo provider cutover | remove the 5 direct provider callers (ai-assistant, pm-templates, project-service-be, telephony, service-integrator) | 12 d | 1–2 w | T0 |
| 3 | REM-M12 Codex read-only review wrapper | automates Reviewer B (saves the manual Codex runs afterwards) | 8 d | 3 d | T1 |
| 3 | REM-M13 Fable & Opus development task profiles | the dev-AI separation of duties as profiles | 6 d | 3 d | T1 |
| 4 | REM-M14 CI + named-human merge gate | protected merges need CI green and a named human | 6 d | 1–2 w | T0 |
| 4 | REM-M15 Provider connectors | native + constrained compatible connectors | 26 d | 3 d | T1 |
| 4 | REM-M16 Provider health, budgets, circuit breaking | — | 10 d | 3 d | T1 |
| 4 | REM-M17 Model catalogue endpoint security | — | 3 d | 2 d | T1 |
| 4 | REM-M18 Durable audit ledger & quality feedback | — | 10 d | 3 d | T1 |
| 5 | REM-M19 Qualification corpus & initial runs | needs C2 | ≈10 d | 3 d | T1 |
| 5 | REM-M20 Stage 12A assurance execution | the engineering evidence for the gate | ≈10 d | 1–2 w | T0 |
| 5 | REM-M21 Standalone router decision spike | only if C1 says build | 5 d | — | T2 |
| — | Reconcile after every wave; whole-app `plan-test` pass at the end | — | 1 d/wave + 2 w | — | — |

**Track E total: 217–222 implementation days + 13 Tier-0 reviews ≈ 59–72 weeks** (timeline: W13–W71 best, W84 worst).
Build REM-M12 first inside wave 3: from then on reviews stop being manual, which is the single biggest saving (3–5 months per the timeline).

## 6. Track F — other systems to launch-ready (Phase 4; owning teams, or +11–15 weeks for the one developer)

Items marked ✔ were done this week and come off the Phase 4 lists.

| # | system | task | est. |
|---|---|---|---|
| F1 | Orchestration | gate-by-gate execution plan for the 16 live gates (OIDC-LIVE … OPERATIONS-STAFFING): infrastructure, receipt, owner | 3 d |
| F2 | Orchestration | ✔ main reconciled with origin; ✔ WI integration merged; still: dated full-suite junit under `evidence/` (last recorded run is July; a full run takes 25+ minutes) | 1 d |
| F3 | Orchestration | `evaluate_launch_authorization` → AUTHORIZED with two signed reviewers and a frozen release candidate | 3–5 d + reviewers |
| F4 | Workflow Engine | merge `codex/wi-mvp-integration` to main after review | 2 d |
| F5 | Workflow Engine | api-gateway route + JWT wiring | 4–5 d |
| F6 | Workflow Engine | live OTel export | 3 d |
| F7 | Workflow Engine | event-broker relay (the `EventOutbox` has no broker today) | 5 d |
| F8 | Workflow Engine | WORM backups + non-superuser `RlsRoleStartupGuard`; flip `RUNTIME_REQUIRE_MIGRATION_JWT`, `_ENVELOPE`, `_ATTEMPT`, `RUNTIME_ENFORCE_RLS_ROLE` on in staging, `RUNTIME_ALLOW_OPERATOR_CERTIFY=false`; full surefire run; PRR for sign-off | 6–8 d |
| F9 | Console | fix the 5 MISALIGNED + 6 GAP rows of `docs/gate1-compatibility-matrix.md` (submitPlan 400, pythonApprove state/note, 400/404 classification, IAM via http(), chronology/receipts) | 6–8 d |
| F10 | Console | `mockMode=false` and `VITE_REQUIRE_LOGIN=1` for non-local builds; CI job running `scripts/run-e2e-all.mjs` + tsc; ESLint; README | 3–4 d |
| F11 | Console | ✔ merge `codex/wi-console-integration` (done 21 Oct) | — |
| F12 | IAM | contract tests for login/refresh/token-exchange/logout, internal tenant-created / member-joined, role assignment, X-Service-Secret gate; run in monorepo CI; surefire totals | 6–8 d |
| F13 | IAM | confirm `JWT_SECRET` / `SERVICE_INTERNAL_SECRET` provisioning; write the deployment README | 2 d |
| F14 | Backend services | list the 5 direct provider callers in REM-M11's acceptance criteria now | 0.5 d |

**Track F total: 45–55 d ≈ 10–12 weeks** if the one developer does it (timeline said 11–15; F2 and F11 are done).

## 7. Track G — Stage 12A gate and the pilot (Phase 5)

| # | task | est. | needs |
|---|---|---|---|
| G1 | Stage 12A gate evidence pack and signed decision (S12-BL-024) | 2–4 w | C3, C4 reports; C6 approved; Track E done; Track F closed |
| G2 | REM-M22 council and pilot protocol build | inside G3 | G1 decision as input |
| G3 | Technical dry run | 2–4 w | — |
| G4 | Controlled work pilot with the named cohort | 6–8 w | three real people, the WI owner |
| G5 | Stage 12B gate sheet and rollout decision | 2 w | — |

## 8. Totals and the critical path

| track | developer time | calendar (serial, one developer) |
|---|---|---|
| A WI MVP | 38–50 d | 26 Oct – mid Jan 2027 (holiday weeks at half capacity) |
| B pipeline follow-ups | 12–19 d (5–9 d for the real-estate demo) | interleaved with A, or first if the demo matters more |
| C decisions | 1 d developer, weeks of lead time | raise 26 Oct; decisions by late Nov |
| D spec approval | ≈ 19 d | ≈ 4 weeks after A |
| E remediation build | 217–222 d + reviews | 59–72 weeks |
| F other systems | 45–55 d | parallel if owned by other teams; else +10–12 weeks |
| G gate + pilot | 12–18 w elapsed, mostly waiting | after E (and F) |

Serial total for the developer: **≈ 330–365 developer-days plus 12–18 weeks of gate and pilot elapsed
time**, which is 18–22 months from 26 October 2026 if other teams do Track F, 21–25 months if not.
That is consistent with the 16 Oct timeline (rollout decision between May and September 2028) once
this week's progress is subtracted.

**What moves the date most** (unchanged from the timeline): a second person as reviewer-operator
(3–5 months), Track F done by the owning teams (10–12 weeks), C1 recorded as no-build (REM-M21 never
enters the plan), and the Track C decisions landing in the first four weeks.

## 9. The first two weeks, concretely (26 Oct – 6 Nov 2026)

1. Day 1: raise C1–C7 with their owners; B10 (check the two deployments); B11 (branch cleanup).
2. Days 1–3: B4, B5, B6, B9, B12 (the half-day items), then B1 if the real-project demo is wanted.
3. Days 3–10: A1 (WI-M15 round 4) and A2 (WI-M21) as the timeline's W1–W2, using Codex wait time for B2–B3.
4. End of week 2: Friday rhythm — re-baseline this file from the observed review-round counts, record the reasons in `plan/progress.commentary.md`.
