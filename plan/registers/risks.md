# Risks

- R01 — Central subscription-CLI defaults remain live while remediation proceeds:
  every shared workload can silently bill/expose a personal account (AUD-009).
  Mitigation: M01 is wave 1, effort 1 day, no dependencies — do it first.
- R02 — Contract v1 (M02) is on the critical path of nearly everything; a late schema
  break re-opens all dependents. Mitigation: versioned fixtures + compatibility tests
  (DoD-4) before dependents start.
- R03 — Raw prompt/output migration (M06) touches employee data and rights; a defective
  migration is itself a privacy incident. Mitigation: migration/privacy/DR tests +
  DPO ownership per REM-006.
- R04 — Qualification (M08/M19) can be gamed by alias drift if exact-deployment identity
  (M07/T07) is weakened. Mitigation: unresolved aliases shorten/disable qualification
  (AUD-020 remediation).
- R05 — The dev-AI workflow the programme USES (Fable/Opus/Codex) is also a deliverable
  (M12–M14) at 4% readiness; using unqualified cells for Tier-0 work contradicts T11.
  Mitigation: human review remains the gate on every merge until M14+M19 close.
- R06 — Plan/board built from the handoff only; repo reality may have moved since
  commit 79a38ade. Mitigation: OI-01 re-assessment diff at build start; treat AUD rows
  as of that commit only.
