# Waves — sequence & dependency map

P0 work precedes model qualification and any real employee pilot (Stage 12A Remediation
Sequence preamble, T13). Order follows the sequence's declared dependencies.

## Wave 1 — stop the bleeding + the contract (no dependencies)

- M01 Disable central CLI defaults (Tier 0, 1d) — first change of the programme.
- M02 humanos-ai-contracts v1 (Tier 0, 8d) — critical path for everything below.
- M03 Claude CLI process safety (Tier 0, 5d).

## Wave 2 — boundaries on the contract

- M04 Endpoint AI Runtime Broker (Tier 0, 15d) ← M02, M03.
- M05 Provider-scoped credential resolution (Tier 0, 8d) ← M02.
- M06 Evidence-object persistence (Tier 0, 15d) ← M02.
- M07 Exact model-deployment registry (Tier 0, 12d) ← M02.

## Wave 3 — routing truth + monorepo cutover + dev-AI pieces

- M08 Qualification lifecycle & hard gate (Tier 0, 20d) ← M07.
- M09 Eligibility router & canonical fallback (Tier 0, 22d) ← M05, M07, M08, M02.
- M10 Complete inference lineage (Tier 0, 10d) ← M02, M07, M09.
- M11 Monorepo provider cutover (Tier 0, 12d) ← M02.
- M12 Codex read-only review wrapper (Tier 1, 8d) ← M02, M04.
- M13 Fable & Opus task profiles (Tier 1, 6d) ← M02, M04.

## Wave 4 — enforcement & hardening

- M14 CI + named-human merge gate (Tier 0, 6d) ← M12, M13.
- M15 Provider connectors (Tier 1, 26d across three REMs) ← M02, M07.
- M16 Health, budgets & circuit breaking (Tier 1, 10d) ← M09.
- M17 Catalogue endpoint security (Tier 1, 3d) ← M07.
- M18 Durable audit ledger (Tier 1, 10d) ← M10.

## Wave 5 — qualification & the gate

- M19 Qualification corpus & initial runs (Tier 1, 20d) ← M08, M12, M13, M15 (OI-04).
- M20 Stage 12A assurance execution (Tier 0) ← M04, M06, M09, M11, M14 (OI-03).
- M21 Standalone router decision spike (Tier 2, 10d if built) — blocked-needs-decision (OI-02).

## Wave 6 — pilot (gated)

- M22 Pilot protocol readiness (Tier 0) ← M20; blocked until the Stage 12A gate passes
  or restricts (T13).
