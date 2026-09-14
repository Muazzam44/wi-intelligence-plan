# Overview — HumanOS Work Intelligence: Remediation & Qualification Programme

## Outcomes

Bring `Rapidtackltd/humanos-backend-services` from its assessed 25.4% alignment with
Architecture Amendment A-01 to a state where the Stage 12A hardening gate can be executed:
every P0 remediation item (REM-001..REM-014, REM-023) closed with its required evidence,
the P1 hardening set (REM-015..REM-021) delivered, the Fable–Opus–Codex development AI
workflow built and qualified, and the staged internal pilot unblocked — without weakening
any provider, credential, tenant, evidence, review or employee-rights boundary.

## Scope boundaries

- IN: the A-01 AI platform remediation inside the existing monorepo — contracts, gateway,
  endpoint broker, credential resolution, evidence persistence, model registry,
  qualification, routing/fallback, lineage, connectors, dev-AI workflow, CI merge gate,
  Stage 12A assurance tracks, pilot protocol readiness.
- OUT: rebuilding the retained foundations (`ai-execution-service`, `humanos-ai-client`
  are retained and extended — AUD-001); the wider Work Intelligence capture/assurance
  product stages (0–11 are specified in the master workbook and not re-planned here);
  any real employee pilot before the Stage 12A gate passes.

## Status

Planning baseline created 2026-09-14 from the complete handoff package
(`nessovo_humanos_work_intelligence_complete_handoff`). Formal programme decision at
baseline: **REMEDIATE BEFORE QUALIFICATION**. All remediation modules are `draft`
(every REM item is Open / every HND package is Not Started in the master workbook);
nothing is in progress or verified. Two modules are `blocked-needs-decision`
(standalone-router spike — CTO decision; pilot execution — gated on Stage 12A).

## Key principles

- The master workbook (`01_MASTER/nessovo_humanos_work_intelligence_master_handoff_validated.xlsx`)
  is the single authoritative source; this plan tree is its executable decomposition and
  carries sheet-level provenance on every module.
- Work one bounded package at a time; never claim a pass without the required evidence
  (AI Coding Handoff, definition-of-done conditions 1–8).
- Retain and extend the existing gateway foundation; do not build a competing orchestrator
  (AUD-001, AUD-003).
