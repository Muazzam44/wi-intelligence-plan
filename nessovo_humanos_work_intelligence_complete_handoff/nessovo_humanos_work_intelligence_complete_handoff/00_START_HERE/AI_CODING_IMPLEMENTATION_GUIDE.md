# AI Coding Implementation Guide

## 1. Authoritative artifact

Use `01_MASTER/nessovo_humanos_work_intelligence_master_handoff_validated.xlsx` as the current source of truth.

Read in this order:

1. `START HERE`
2. `AI Coding Handoff`
3. `Stage 12A Repo Assessment`
4. `Stage 12A Remediation Sequence`
5. `AI Execution Service Audit`
6. accepted ADR sheets;
7. relevant domain contracts;
8. backlog, test and gate sheets.

Historical stage workbooks and prompt files are traceability artifacts, not the current authority.

## 2. Source-of-truth precedence

1. Non-negotiable rules and accepted ADRs.
2. Current stage/domain contracts and schema/event definitions.
3. Repository Evidence Register and static/dynamic assessment results for current code reality.
4. Stage 12A Remediation Sequence and Stage 12 Backlog for implementation order.
5. Gate and test sheets for completion.
6. Historical prompts and snapshots.

Never claim that a work package is complete because an AI produced code or a plan. Completion requires implemented acceptance criteria and evidence from the required tests.

## 3. Required development roles

### Claude Fable 5

- architecture and planning;
- dependency and migration analysis;
- risk and rollback planning;
- final cross-service integration assessment.

### Claude Opus 4.8

- bounded implementation;
- refactoring inside the approved scope;
- tests and migrations;
- implementation summary.

### GPT-5.6 Sol through Codex

- independent read-only plan review;
- diff review;
- test-gap and security review;
- structured blocker/major/minor/question findings.

Codex must not modify the worktree during reviewer mode.

### Deterministic CI and human authority

CI is authoritative for objective tests. A named human technical lead resolves model disagreement, approves scope and decides merge/release.

Maximum two AI review/fix cycles before human adjudication.

## 4. Standard work-package lifecycle

1. Select one backlog/remediation ID.
2. Read cited source sheets and ADRs.
3. Inspect the repository baseline and current evidence.
4. Write a bounded implementation plan with modules, contracts, migrations, security/privacy impact, tests and rollback.
5. Obtain plan challenge/review.
6. Implement only the approved scope in a branch/worktree.
7. Run unit, contract, integration, migration, security/privacy and failure tests required by the sheet.
8. Run independent Codex review.
9. Resolve or human-adjudicate findings.
10. Run final CI and human merge review.
11. Update the workbook/backlog/evidence rows with actual results, commit and sources.

## 5. P0 implementation order

1. Remove `claude-cli` from central/global defaults.
2. Complete the monorepo provider-call cutover through the central AI client.
3. Publish `humanos-ai-contracts` v1.
4. Fix the CLI process runner.
5. Extract the Endpoint AI Runtime Broker.
6. Replace fail-open credential/account fallback.
7. Migrate raw prompt/output storage to classified evidence-object references.
8. Implement exact Model Deployment Registry.
9. Implement task-by-effort qualification lifecycle.
10. Replace the simple router with hard eligibility plus minimum-sufficient routing.
11. Implement canonical errors and no-silent-fallback.
12. Persist complete inference lineage.
13. Build the Codex read-only review wrapper.
14. Add Fable planning and Opus implementation profiles.
15. Enforce deterministic CI and human protected-branch merge controls.

Do not qualify models or start an employee pilot before the prerequisite P0 controls are closed.

## 6. Architecture rules

- Work Intelligence cannot import provider SDKs, hold provider keys or directly invoke CLIs.
- Provider-specific logic belongs in approved connector modules behind the AI Execution Contract.
- The endpoint broker is separate from monitoring/capture.
- User CLI OAuth credentials remain under vendor/OS control and are never read or exported.
- Tenant, person, task, case, device and session scope must be explicit.
- No service may silently switch tenant credentials to a platform account.
- Actual model, provider/operator, endpoint, runtime/CLI, quantisation, qualification, region and fallback must be recorded.
- An alias or family name alone is not sufficient lineage.
- No model is globally approved; only exact task-by-effort qualification cells are routable.
- Cost/latency optimisation occurs only after policy, qualification, feature, health and review eligibility.
- No silent local-to-cloud/provider/region fallback.

## 7. Data and evidence rules

- Raw prompts, screenshots, source code and coaching text do not belong in generic logs or traces.
- Sensitive evidence uses encrypted object references, purpose-specific retention and access controls.
- Corrections, supersession, deletion/restriction and legal/dispute holds must propagate.
- Evidence gaps, exclusions and unsupported tools remain explicit.
- Authoritative semantic events outrank visual and AI inference.
- Every material finding includes evidence refs, confidence, versions, missing evidence and alternatives.

## 8. Employee and fairness rules

- No covert monitoring.
- No personality, emotion, protected-trait or mental-state inference.
- No productivity/capability score from clicks, keystrokes, time, code volume, prompts, tokens or cost.
- No single-task permanent capability conclusion.
- External blockers cannot become employee capability gaps.
- Accessibility accommodations and alternate valid methods cannot lower conclusions.
- AI unavailability, auth/quota and telemetry gaps cannot become employee failure.
- Material negative/high-impact conclusions require meaningful human review.
- Employees must be able to inspect, correct and challenge material evidence.

## 9. Engineering conventions

### Java/Spring Boot

- durable domain state, workflow and public APIs;
- records/immutable request DTOs where appropriate;
- explicit validation and versioned OpenAPI/JSON Schema;
- Flyway migrations with rollback/forward strategy;
- tenant and purpose checks at service boundaries;
- idempotency and outbox patterns for critical events.

### Python

- AI evaluation, extraction and model workers behind approved APIs;
- pinned environments and reproducible datasets;
- structured outputs and explicit abstention;
- no direct final high-impact state writes.

### Rust/native

- endpoint capture and broker core;
- signed policy and default-deny capability enforcement;
- bounded memory/CPU/disk/network;
- secure local journal and process-tree cleanup;
- platform-specific bridges only where necessary.

### TypeScript/frontend

- reuse HumanOS design system and BFFs;
- WCAG 2.2 AA target;
- audience-specific read models;
- no raw evidence in general analytics;
- degraded state and employee correction always visible.

## 10. Test requirements

Depending on the work package, add:

- unit tests;
- JSON Schema/OpenAPI/CloudEvents contract tests;
- integration and tenant-isolation tests;
- migration and data-retention tests;
- security/privacy and prompt-injection tests;
- failure, retry, timeout, cancellation and offline tests;
- model qualification and regression tests;
- accessibility and user-journey tests;
- performance and cost tests;
- canary and rollback tests.

## 11. Standard implementation prompt

> Implement only work package `<ID>` from the latest Nessovo HumanOS Work Intelligence master workbook. Read the cited source-of-truth sheets, accepted ADRs, repository evidence and acceptance tests first. State affected modules, dependencies, data/security/privacy impact, migration and rollback. Do not broaden scope. Do not introduce provider SDKs or keys outside approved connector modules. Add deterministic tests and evidence for every acceptance criterion. Use Claude Fable for planning/integration, Claude Opus for bounded implementation, GPT-5.6 Codex for independent read-only review, CI for objective verification and a named human for merge/release. Report unresolved risks honestly and leave the work package blocked rather than fabricating a pass.

## 12. Definition of done

A work package is done only when:

- acceptance criteria are implemented;
- required tests pass;
- no architecture/privacy/security boundary is weakened;
- schemas/events and migrations are versioned;
- failure/degraded behavior is implemented;
- employee visibility/correction/review remains intact;
- Codex blockers/majors are resolved or human-adjudicated;
- CI passes;
- a named human approves merge;
- workbook status and evidence are updated with actual source/commit.
