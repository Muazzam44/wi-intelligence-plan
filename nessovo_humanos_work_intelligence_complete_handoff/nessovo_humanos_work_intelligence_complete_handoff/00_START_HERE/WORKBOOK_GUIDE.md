# Workbook Guide

## Authoritative workbook

`01_MASTER/nessovo_humanos_work_intelligence_master_handoff_validated.xlsx`

The workbook contains 248 sheets. Use the `Index` sheet as the complete navigation. The new `START HERE` and `AI Coding Handoff` sheets explain how to read and implement it.

## Sheet groups

### Foundation and programme control

Executive Charter, Product Charter, purpose/policy, RACI, market/OSS research, delivery stages, programme risks, KPI dashboard, source register and master prompts.

### Stage 0–1

Governance, purpose limitation, build/buy decisions, reference architecture, foundation threats, pilot definition and approval gates.

### Stage 2–3

Role/task/capability ontology and the native managed-device agent foundation.

### Stage 4–5

Signed evidence ingestion, storage, replay, retention/access and policy-controlled universal capture.

### Stage 6–7

Semantic adapters, AI-agent evidence, provenance, work episodes, task alignment and Task Assurance.

### Stage 8–9

Capability Graph, claims/baseline/readiness, Growth Coach, learning loop and reporting.

### Stage 10–11

Employee/manager/reviewer experiences and Skill Forge governed self-improvement.

### Architecture Amendment A-01

Separation of Work Intelligence from AI Orchestration, endpoint broker, provider/CLI connectors, exact model registry, task/effort qualification, routing, fallback, credentials, residency, cost and drift.

### Stage 12

Hardening, model qualification, security/privacy/legal/reliability/accessibility gates, controlled internal pilot and final rollout decision.

### Repository assessment

Current code evidence, AI execution audit, development workflow readiness and ordered remediation.

## Sheet types

- Dashboard: summary and formulas.
- Architecture/contract: required design and interfaces.
- Backlog/workplan/remediation: implementation tasks and status.
- Test/validation/results: expected tests and actual evidence fields.
- Risk/threat: risk, severity, mitigation and owner.
- ADR/decision: choices and trade-offs.
- Gate: formal entry/exit criteria.
- Source/evidence: URLs, repository paths, commits and provenance.
- Prompt: historical execution instruction; not the final architecture authority.

## Editing rules

- Backlogs: update owner, status, evidence, commit and actual result.
- Gates/results: never mark Pass/Met without implemented and tested evidence.
- Sources: append and preserve provenance; do not overwrite history silently.
- Contracts/ADRs: change through review and versioning.
- Historical stage snapshots and prompts: reference only.

## Status language

`Draft Complete` or `Complete plan` means the specification is ready. It does not mean the software has been built.

`Not Executed` means no implementation/pilot evidence exists.

`Passed` or `Approved` requires the authority and evidence defined in the sheet.

## Formula and validation usage

The workbook uses formulas for readiness, backlog completion, risk scoring, gate status, counts and dashboards. Editable categorical fields use dropdown validation where appropriate. The external validation report records the workbook-wide counts and checks.
