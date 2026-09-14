# Truths (invariants)

Each: id, statement, evidence/source, effective-date. Sources are sheets of the master
workbook `01_MASTER/nessovo_humanos_work_intelligence_master_handoff_validated.xlsx`
(the package's declared single authority) unless stated otherwise. Effective-date is the
plan baseline, 2026-09-14 — the handoff package was received 2026-07-21.

- **T01** — All provider model calls pass through the single central AI execution choke
  point (`ai-execution-service` via `humanos-ai-client`); no service outside approved
  connector modules imports provider SDKs or sends provider HTTP requests.
  Evidence: AUD-001 (positive foundation, 0.65), REM-023, HND-001. 2026-09-14.
- **T02** — No central/default task route may select the machine's logged-in Claude CLI
  subscription; CLI use requires an explicit endpoint-interactive development profile.
  Evidence: AUD-009 (all configured task types default to `claude-cli` — critical),
  REM-001. 2026-09-14.
- **T03** — The provider-neutral contract `humanos-ai-contracts` v1 carries purpose,
  task/effort profile, data class, region, features, output schema, evidence refs,
  review policy, fallback and exact route lineage on request AND result.
  Evidence: REM-002, HND-002, AUD-002 (current contract limited to
  taskType/input/model/maxTokens/temperature). 2026-09-14.
- **T04** — Endpoint subscription CLIs and local runtimes are invoked only by the
  Endpoint AI Runtime Broker at the managed endpoint boundary; the central service never
  accesses user-local OAuth. Evidence: REM-004, AUD-010 (missing A-01 boundary, 0.0).
  2026-09-14.
- **T05** — Credential resolution is provider-scoped with explicit
  configured/not-found/unavailable/forbidden outcomes; a tenant-service outage can never
  silently switch to a platform key, account, provider or data route.
  Evidence: REM-005, AUD-015 (silent fallback today — P0 privacy/billing gap). 2026-09-14.
- **T06** — No raw AI prompt/output is persisted in domain stores: minimised metadata plus
  encrypted, classified evidence-object references with TTL, access grants, correction,
  deletion and legal-hold lineage. Evidence: REM-006, AUD-018 (raw columns mandatory
  append-only today — incompatible), HND-005. 2026-09-14.
- **T07** — Every active route is represented by an exact model deployment
  (endpoint/operator/snapshot-or-digest/runtime/CLI/quantisation/context/features/terms/
  region/price/lifecycle) — never a family or alias alone.
  Evidence: REM-007, AUD-006 (0.25), AUD-020 (0.0). 2026-09-14.
- **T08** — Only qualified, unexpired task×effort execution configurations can be
  selected; hard eligibility (policy/region/features/qualification/health) is applied
  before minimum-sufficient cost/latency selection, and cost can never make an ineligible
  route eligible. Evidence: REM-008, REM-009, AUD-008 (0.15). 2026-09-14.
- **T09** — Failures follow the canonical A-01 error/fallback taxonomy
  (auth/quota/model/region/schema/qualification/resource/no-route/user-action) with
  terminal human-review/no-AI paths; no silent material route change, and AI
  unavailability never becomes employee failure. Evidence: REM-010, AUD-019. 2026-09-14.
- **T10** — 100% of material AI-assisted domain records carry complete inference lineage:
  actual implementation, connector, provider/operator, requested vs actual model, runtime,
  qualification profile, region, fallback and review references.
  Evidence: REM-011, HND-008, AUD-017/AUD-020. 2026-09-14.
- **T11** — Development AI separation of duties: the Fable profile plans/integrates and
  cannot execute coding writes; the Opus profile implements and cannot self-review or
  merge; Codex reviews read-only (no write tools); a protected-branch merge requires
  deterministic CI, Codex blocker/major resolution and a named human approval.
  Evidence: REM-012, REM-013, REM-014, HND-009, Development AI Workflow /
  Claude-Codex Review Protocol sheets. 2026-09-14.
- **T12** — AI cannot directly decide dismissal, pay, promotion, probation or discipline;
  employees can inspect, correct, dispute and appeal material findings.
  Evidence: README_FIRST.md "What the project does" §8/§10; Governance sheet. 2026-09-14.
- **T13** — The Stage 12A hardening gate (security, privacy/DPIA, legal/worker
  consultation, endpoint performance, data reliability/DR, AI & evaluator evaluation,
  fairness, accessibility) passes or restricts before any real employee pilot.
  Evidence: Stage 12A Remediation Sequence preamble ("P0 work must precede model
  qualification and any real employee pilot"), Stage 12A/12B gate sheets, HND-010.
  2026-09-14.
