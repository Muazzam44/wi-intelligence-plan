# Project Overview — Nessovo HumanOS Work Intelligence

## 1. Executive summary

HumanOS Work Intelligence is a modular HumanOS platform capability that connects assigned work to explainable evidence, task outcomes, employee development and human review.

The system is not designed as a traditional time tracker. It is designed around an approved **Task Execution Contract**. That contract says what the task is, what outcome is expected, which acceptance criteria and quality gates apply, what evidence is necessary, which tools and methods are allowed, and who reviews completion.

While a visible task session is active, a company-managed endpoint agent records policy-approved work evidence. Cloud services ingest and store the evidence, semantic adapters add high-quality tool events, a provenance engine links human and AI contributions, and Task Assurance checks whether the task criteria appear satisfied. The employee can inspect the material evidence and correct or dispute it. Managers receive exception-led summaries and support needs rather than a continuous surveillance feed.

The platform can also use reviewed evidence to support a multidimensional capability profile, role-readiness path, private coaching and learning interventions. These are developmental systems. High-impact employment decisions remain separate and require meaningful human review.

## 2. The problem

Conventional project tools often know that a task exists and that somebody changed its status. Conventional monitoring tools often know how long a device was active or can display screenshots. Neither one reliably answers all of these questions:

- What was the employee actually trying to achieve?
- Which task criterion did each artefact or test support?
- Which work came from the employee, an AI agent, automation or the system?
- Was the employee blocked by access, requirements, environment or knowledge?
- Did the work meet the quality and review requirements?
- Is the evidence complete enough to make a conclusion?
- What can help the employee complete the task or improve a capability?
- Can the employee inspect and challenge the evidence?

HumanOS Work Intelligence addresses these questions through task contracts, evidence lineage, explicit uncertainty and human review.

## 3. End-to-end workflow

### 3.1 Role and task definition

A role is versioned and mapped to responsibilities, outcomes and capabilities. An assigned task is represented by a Task Execution Contract containing:

- objective and scope;
- acceptance criteria;
- quality gates;
- evidence requirements;
- dependencies and blockers;
- deadlines and workflow states;
- approved methods and tools;
- review requirements;
- accessibility accommodations and valid alternate methods.

A job description or employee claim is not evidence. A single task cannot permanently establish capability or misconduct.

### 3.2 Visible work session

The employee starts, pauses, switches and stops work/task sessions through a visible endpoint interface. Signed policy controls:

- working hours;
- applications, domains, displays and controls that may be observed;
- exclusions and private states;
- capture capabilities;
- local versus cloud processing;
- redaction and secure-field protection;
- retention;
- jurisdiction and tenant scope;
- emergency disable.

There is no covert mode.

### 3.3 Evidence collection

The endpoint agent can collect approved signals such as:

- active application, process and window events;
- browser navigation and task context;
- shell commands and process results;
- IDE diagnostics and debug states;
- Git branch, diff, commit, pull-request and review events;
- build, test, CI, deployment, simulator and emulator results;
- file and document changes;
- AI-agent sessions, prompts, tools, permissions, generated changes and human acceptance/rejection;
- event-driven visual states rather than constant full-motion video;
- input metadata and approved text changes where policy allows;
- gaps, unsupported tools, offline periods and exclusions.

Passwords, authentication codes, private keys and secure fields must be suppressed before sensitive capture. Application, domain, display and private exclusions apply before upload.

### 3.4 Evidence ingestion and replay

Every event batch is signed, schema-versioned, idempotent, tenant-scoped, device-scoped and session-scoped. Evidence metadata is stored in PostgreSQL; large or sensitive objects use encrypted object storage. Kafka-compatible streams support downstream processing. Replay preserves event order, duplicates, late events, clock drift, gaps, corrections and versions.

### 3.5 Semantic adapters

Semantic adapters provide higher-quality evidence from tools such as:

- Chrome and Edge;
- PowerShell, bash and zsh;
- Git and GitHub;
- CI/build/test systems;
- VS Code and JetBrains IDEs;
- Xcode and Android/Flutter tooling;
- Docker/container workflows;
- Codex, Claude Code and future AI agents.

Official semantic events and authoritative artefacts outrank screenshots, OCR and AI inference.

### 3.6 Provenance and work episodes

The provenance graph links:

- human input;
- agent sessions and prompts;
- tool calls;
- process execution;
- file and text changes;
- visual states;
- artefacts;
- tests;
- review actions;
- task criteria and quality gates.

Actor types remain HUMAN, AI_AGENT, AUTOMATION, SYSTEM, MIXED or UNKNOWN. UNKNOWN is valid and cannot be forced into another class.

Work episodes can represent task work, research, review, AI direction, AI execution, automation wait, collaboration, learning, blocked work, possibly unrelated activity, private/excluded time and insufficient evidence.

### 3.7 Task Assurance

Task Assurance compiles the approved task contract and evaluates each criterion using:

- deterministic facts where available;
- AI-assisted recommendations where appropriate;
- human review for material or disputed conclusions.

It distinguishes:

- verified completion from an employee claim;
- external blockers from employee capability gaps;
- legitimate alternate work methods from non-compliance;
- automated execution wait from inactivity;
- missing telemetry from no work;
- rework, scope expansion and contradictory evidence.

No task finding automatically becomes an employment decision.

### 3.8 Employee and manager experiences

The employee workspace provides:

- assigned tasks and daily plan;
- monitoring and active-sensor state;
- task contract and criterion progress;
- evidence timeline and provenance;
- AI route/model lineage;
- corrections, disputes and appeals;
- private coaching and preferences;
- learning and practice;
- capability character/skill tree and role path;
- privacy, access history, retention and support.

The manager console is exception-led. It shows blockers, quality-gate gaps, overdue reviews, workload/task status and reviewed development summaries. It does not show a default live screen wall, private coaching transcript or simplistic productivity score.

### 3.9 Capability and learning

Capability is multidimensional: knowledge, execution, autonomy, complexity, quality, transfer, error recovery and mentoring. It has separate confidence and freshness. Capability changes require multiple context-qualified evidence items and review.

Training completion does not increase capability. Learning moves through content, practice, later real-work application and capability review.

### 3.10 Growth Coach

The Growth Coach can observe, nudge, assist, teach, escalate, reflect, assign practice or hand off to a mentor. It uses the least intrusive effective intervention, respects focus and accessibility preferences, explains its evidence and uncertainty, and is private to the employee by default.

## 4. AI architecture

Work Intelligence and AI Orchestration are separate systems.

Work Intelligence owns:

- task purpose and contract;
- evidence references;
- data classification and allowed regions;
- required model features;
- task and effort profile;
- output schema;
- quality thresholds;
- human-review and fallback policy;
- interpretation of the result.

AI Orchestration owns:

- provider/API/CLI connectors;
- credentials and workload identities;
- exact model deployment registry;
- model discovery and capability probes;
- model qualification;
- route selection, quotas, cost, health and circuit breaking;
- fallback and canonical errors;
- model/provider/runtime/CLI drift.

Execution modes can include vendor API, enterprise cloud, Nessovo self-hosted, endpoint-local, endpoint subscription CLI and no-AI/manual mode.

A valid API key, installed CLI or strong public benchmark does not qualify a model. Qualification is specific to the provider endpoint, exact model/snapshot or weight digest, runtime/CLI, quantisation, context, prompt/skill, tool policy, task profile and effort profile.

Routing first applies hard policy and qualification filters, then selects the lowest-cost and lowest-effort route that meets quality, privacy, security, region and review requirements. Fallback cannot silently change local/cloud, provider, region or data terms.

## 5. Development workflow

The approved development model profile is:

- Claude Fable 5: architecture, planning, decomposition and integration review.
- Claude Opus 4.8: bounded implementation, refactoring, migrations and tests.
- GPT-5.6 Sol through Codex: independent read-only plan, diff, security and test-gap review.
- CI/CD: deterministic compile, test, schema, migration, security and policy gates.
- Human technical lead: final merge and release authority.

The cross-model review loop is capped at two cycles before human adjudication.

## 6. Privacy, fairness and prohibited uses

The plan prohibits:

- covert monitoring;
- emotion, personality, mental-state or protected-trait inference;
- automatic dismissal, pay, promotion, probation or discipline decisions;
- productivity/capability scores from clicks, keystrokes, time online, code volume, prompts, tokens or AI cost;
- treating missing sensors or telemetry gaps as inactivity;
- treating training completion as capability;
- penalising accessibility accommodations or valid alternate methods;
- hidden personal-subscription workloads;
- silent local-to-cloud/provider/region fallback;
- raw evidence access without purpose, scope, time limit and audit.

## 7. Current status

The master plan is complete. The current backend repository has reusable AI execution foundations but only 25.4% alignment with the A-01 target in the latest static assessment. There are 17 critical findings, 15 P0 remediation items and 7 P1 items. The Fable–Opus–Codex workflow is 4% ready. Current decision: REMEDIATE BEFORE QUALIFICATION.

No model has been qualified, no Stage 12A control has fully passed, no employee pilot has started and no production rollout decision is available.
