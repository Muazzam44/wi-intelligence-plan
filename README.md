# HumanOS Work Intelligence — Spec-Driven Plan & Cockpit

Spec-driven-planning decomposition of the **Work Intelligence remediation & qualification
programme**, built 2026-09-14 from the complete handoff package in this folder
(`nessovo_humanos_work_intelligence_complete_handoff/` — its master workbook is the single
authoritative source; this plan tree is its executable, provenance-carrying decomposition).

- `plan/` — the plan tree: constitution, truths (T01–T13), architecture, research,
  registers, 22 modules (M01–M22, REM/HND/AUD provenance), waves, derived board/index/
  traceability.
- `plan/board.html` — THE visual control board (generated; never hand-edited).
  Serve: `set PORT=4181&& node plan\server.js` → http://localhost:4181/board.html
  (4173 is the Business Hub board, 4179 the engine/orchestration cockpit).
- `gen_modules.py` — regenerates `plan/modules/*.md`; then re-run the plugin's
  `plan_lint.py` (no flag) and `plan_lint.py --board`.
- `graphify-out/` — generated knowledge graph (45 nodes / 65 edges).

Baseline status is honest: every remediation module is `draft` (all REM items Open, all
HND packages Not Started, alignment 25.4%, decision REMEDIATE BEFORE QUALIFICATION);
M21/M22 are `blocked-needs-decision` (CTO router decision; Stage 12A gate).
