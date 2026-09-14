# Nessovo HumanOS Work Intelligence — Complete Handoff

## Read this first

This package contains the complete **project plan, architecture, implementation roadmap, governance controls, validation framework, pilot plan, repository assessment and historical stage artifacts** for Nessovo HumanOS Work Intelligence.

The single authoritative spreadsheet is:

`01_MASTER/nessovo_humanos_work_intelligence_master_handoff_validated.xlsx`

Open its **START HERE** sheet first, then **AI Coding Handoff**, **Stage 12A Repo Assessment**, **Stage 12A Remediation Sequence** and **AI Execution Service Audit**.

## What the project does — simple explanation

HumanOS Work Intelligence is a transparent, company-managed task and work-evidence platform.

1. A role and task are defined with an objective, acceptance criteria, quality gates and evidence requirements.
2. The employee starts a visible work session and selects the active task.
3. A managed endpoint agent records only policy-approved evidence connected to the task: applications, processes, IDE/browser/shell/Git/test/build events, event-driven visual states and AI-agent activity.
4. Passwords, secure fields, excluded applications/domains/displays and private periods are blocked by policy.
5. Signed evidence is stored and replayed as an explainable timeline with gaps and exclusions visible.
6. Provenance distinguishes human, AI-agent, automation, system, mixed and unknown contributions.
7. Task Assurance checks evidence against task criteria and quality gates, identifies blockers and recommends completion/review states.
8. Employees can inspect, correct, dispute and appeal material findings.
9. Managers see blockers, missing gates and reviewed development summaries—not a live surveillance wall or simplistic activity score.
10. Reviewed evidence can support capability development, private coaching and learning plans, but AI cannot directly decide dismissal, pay, promotion, probation or discipline.

## Current status

- Architecture and programme plan: **complete**.
- Stage 0–11 specifications and Architecture Amendment A-01: **complete**.
- Stage 12 hardening and pilot plan: **complete**.
- Current repository assessment: **complete for the audited commit**.
- Current code alignment with the A-01 target: **25.4%**.
- Critical audit findings: **17**.
- P0 remediation items: **15**.
- Fable–Opus–Codex development workflow readiness: **4%**.
- Current formal decision: **REMEDIATE BEFORE QUALIFICATION**.
- Software implementation, model qualification, penetration testing, legal/DPIA closure and pilot: **not complete**.

## First engineering work

1. Remove central Claude CLI defaults and direct provider calls outside the gateway.
2. Publish the provider-neutral A-01 AI request/result contracts.
3. Fix CLI process handling and extract the Endpoint AI Runtime Broker.
4. Correct provider-scoped credential resolution.
5. Replace inline raw AI prompt/output storage with classified evidence-object references.
6. Implement the exact model deployment registry, task-by-effort qualification and hard-eligibility routing.
7. Build and qualify the Fable planning, Opus implementation and GPT-5.6 Codex read-only review workflow.
8. Execute Stage 12A hardening before any employee pilot.

## Package folders

- `00_START_HERE` — plain-language documentation, coding guide, validation report and file manifest.
- `01_MASTER` — authoritative validated master workbook and START HERE preview.
- `02_PROMPTS` — historical applied and final stage prompts.
- `03_STAGE_WORKBOOKS` — historical stage-by-stage workbook snapshots.
- `04_PREVIEWS` — dashboard images.

## Source-of-truth rule

When documents conflict, use this order:

1. The latest validated master workbook.
2. Accepted ADRs and non-negotiable rules.
3. Current stage/domain contracts.
4. Repository assessment, audit and evidence sheets for current code reality.
5. Remediation/backlog and gate sheets for implementation order and completion.
6. Historical prompts and stage snapshots only for traceability.

A completed specification is **not** proof that the software or pilot has passed.
