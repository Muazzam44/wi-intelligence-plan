# Research (Phase 0) — findings & open unknowns

Corpus: the complete handoff package in this folder
(`nessovo_humanos_work_intelligence_complete_handoff/`), ingested as source data
(untrusted until cross-checked against the master workbook, which the package itself
names as the single authority). Full sheet inventory: ~240 sheets across Stages 0–12,
the A-01 AI amendment, and the Stage 12A execution set.

## What exists and is reusable (brownfield)

- `ai-execution-service` is explicitly the single model-call service and
  `humanos-ai-client` centralises callers — retained as the core foundation
  (AUD-001, alignment 0.65, "Implemented — unverified").
- Sync execution API (`POST /api/ai/executions`, AUD-004, 0.65) and a DB-backed async
  job lifecycle (AUD-005, 0.55) exist in code but have no executed integration evidence.
- The workflow runtime's governed AI envelope (schema, evidence/citation, confidence,
  autonomy, budget) is a strong reuse seam (AUD-003, 0.55): promote a policy-safe subset
  into the gateway contract; do not rebuild.
- Anthropic native connector is a good Tier-1 foundation (AUD-013, 0.5).

## What is defective or missing (drives the module set)

- All configured task types default to the machine's `claude-cli` subscription
  (AUD-009, 0.05) — immediate configuration remediation (M01).
- Contract is materially below A-01 (AUD-002, 0.35) — new `humanos-ai-contracts` v1 (M02).
- CLI adapter: in-process, no endpoint boundary (AUD-010, 0.0) and concrete process
  defects — `cmd.exe /c`, inherited env, no project root, stderr/timeout defect
  (AUD-011, 0.0) — M03 then extraction M04.
- Credential resolver is Anthropic-specific with silent platform-key fallback
  (AUD-015, 0.2) — M05.
- Raw prompts/outputs are mandatory append-only DB columns (AUD-018, 0.0) — M06.
- Registry is family/alias-level YAML (AUD-006, 0.25; AUD-020, 0.0) — M07, M10.
- Router is pin-or-static-default with no eligibility model (AUD-008, 0.15) — M08/M09.
- No canonical failure taxonomy (AUD-019, 0.3) — M09.
- OpenAI-compatible connector is capability-limited; parity must not be assumed
  (AUD-014, 0.25) — M15. Tool calling via the CLI is prompt-simulated, dev/test only —
  never qualified for production (AUD-012, 0.1) — constraint on M08/M19.
- Tenant isolation on pure S2S paths lacks principal reconciliation (AUD-016, 0.35) —
  folded into M02/M11 acceptance plus Stage 12A security track (M20).
- Development AI workflow readiness is 4% — M12/M13/M14/M19.

## Programme numbers at baseline (Stage 12A Repo Assessment)

Alignment 25.4% overall (boundary/client 0.55, registry/routing 0.12,
providers/credentials 0.30, data/audit 0.20, endpoint CLI 0.05, development workflow
0.00); 26 controls assessed, 17 critical findings, 15 P0 + 7 P1 remediation items,
Stage 12A gate execution readiness 11.1%; decision **REMEDIATE BEFORE QUALIFICATION**.

## Open unknowns (tracked in registers/open-items.md)

- OI-01: exact repo toolchain/build commands — the repo is not checked out beside this
  plan; verify `mvn` module names and CI layout at build start.
- OI-02: REM-022 standalone-router decision is the CTO's; the spike is specified but
  gated (M21).
- OI-03: Stage 12A human gates (DPIA/legal/worker consultation, pen-test) have owners
  outside engineering; module M20 sequences engineering evidence but cannot close them.
- OI-04: qualification corpus content (HumanOS + development datasets, REM-021) needs
  the evaluation lead's sign-off before initial runs count (M19).
