# Decisions

- D01 (2026-09-14, plan baseline) — Adopt the master workbook as the controlling source
  and decompose the Stage 12A remediation sequence 1:1 into risk-tiered modules; module
  ids carry REM/HND/AUD provenance. Rationale: the package's own source-of-truth rule.
- D02 (2026-09-14) — ADR-P1: retain and extend `ai-execution-service` +
  `humanos-ai-client`; no competing orchestrator (AUD-001/003).
- D03 (2026-09-14) — ADR-P2: standalone router is a gated decision spike (REM-022),
  not default scope (M21 blocked-needs-decision, CTO owner).
- D04 (2026-09-14) — Plan tree + cockpit live INSIDE `D:\intelligence` (user directive),
  mirroring the humanos-plan-cockpit pattern; board served on port 4181 (4173 is owned
  by the Business Hub board, 4179 by the engine/orchestration cockpit).
