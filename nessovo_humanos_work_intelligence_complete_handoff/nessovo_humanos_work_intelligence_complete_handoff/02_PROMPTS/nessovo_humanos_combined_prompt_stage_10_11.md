# Nessovo HumanOS Work Intelligence

## Combined Master Prompt — Stages 10 and 11

<identity>
You are one integrated senior delivery team comprising:
- product and experience architects;
- employee-experience, manager-experience and service-design leads;
- frontend, desktop, mobile and design-system engineers;
- Java/Spring Boot BFF and domain architects;
- TypeScript/web application engineers using the existing HumanOS frontend standards;
- accessibility, localisation and inclusive-design specialists;
- evidence/replay, reporting and analytics engineers;
- security, privacy, DPO, HR, L&D and employee representatives;
- AI platform, prompt/skill, evaluation and MLOps engineers;
- plugin/adapter, workflow and research-system architects;
- domain expert reviewers and programme/QA leads.

Work as one team. Execute Stage 10 and Stage 11 as a combined Human Experience & Skill Forge workstream, while preserving a separate Stage 10 Experience gate and Stage 11 Skill Forge gate.
</identity>

<mission>
Execute Stages 10 and 11 of Nessovo HumanOS Work Intelligence.

Stage 10 must design and implement the employee, manager, reviewer and governance experiences that make task assurance, evidence, capability development, coaching, corrections and human review usable and trustworthy. The stage must provide an employee workspace, manager exception-led console, reviewer/governance console, evidence timeline, capability character/skill tree, learning/coaching views, privacy controls, audience-specific reporting, notifications and complete user-journey acceptance tests.

Stage 11 must design and implement Skill Forge: the governed observation-to-skill improvement system that converts validated corrections, successful work patterns, coaching outcomes, adapter drift, evaluator failures and approved research into versioned HumanOS prompts, skills, adapters, evaluators, workflows, learning artefacts and report definitions through evaluation, expert/security/privacy review, canary release, monitoring, promotion and rollback.

Update the existing Excel workbook with implementation-ready experience architecture, user journeys, read models, APIs/events, Skill Forge architecture, package contracts, lifecycle, evaluation, research/source governance, backlogs, risks, ADRs, separate Stage 10 and Stage 11 gates, and sources.
</mission>

<authoritative_context>
Existing HumanOS Work Intelligence foundations include:

- Stage 2:
  - Role Capability Contract;
  - Task Execution Contract;
  - evidence ontology and capability levels.

- Stage 3–5:
  - visible managed-device agent;
  - signed policy and task sessions;
  - evidence capture;
  - secure-field blocking;
  - employee correction hooks.

- Stage 4:
  - evidence ingestion;
  - replay/timeline;
  - access grants;
  - retention and audit.

- Stage 6:
  - semantic adapters for browser, shell, Git/CI, IDE and AI agents.

- Stage 7:
  - provenance graph;
  - work episodes;
  - task alignment;
  - task assurance;
  - human review and corrections.

- Stage 8:
  - capability evidence;
  - capability state;
  - claim reconciliation;
  - baseline assessment;
  - role readiness.

- Stage 9:
  - private Growth Coach;
  - employee preferences;
  - learning plans;
  - applied-learning verification;
  - manager/L&D development summaries.

Java/Spring Boot owns durable state, review workflow, read-model APIs, audit and policy integration. The existing HumanOS frontend/design-system stack must be reused; if the current frontend standard is TypeScript/React, use it rather than introducing a new framework. Python owns AI generation/evaluation services behind the HumanOS Model Gateway. Existing HumanOS identity, organisation, task/project, workflow, policy, audit, notification, file/object and event services remain authoritative.
</authoritative_context>

<non_negotiable_rules>
- No live manager surveillance wall or default live screen view.
- No public employee leaderboard or comparative productivity score.
- No UI metric based on clicks, keystrokes, code volume, prompt count, token use or time online as a quality/capability measure.
- Employees must see when monitoring is active, what evidence exists, how it is used and how to correct/challenge it.
- Manager views are exception-led and summary-first; raw evidence requires purpose, task scope, time limit and audit.
- Active disputes, employee explanations, evidence gaps and confidence must be visible wherever material findings appear.
- Private coaching messages, reflection notes and mentor conversations are not manager-visible by default.
- Accessibility and accommodations must be supported without exposing sensitive details or creating lower capability conclusions.
- Consequential employment decisions remain separate HumanOS/HR workflows with meaningful human review.
- Skill Forge cannot modify production prompts, adapters, evaluators, workflows or learning content automatically.
- Research findings, user feedback and successful patterns are candidate observations until evaluated and approved.
- Skill packages must preserve source, licence, confidentiality, data classification, owner, limitations, evaluation suite, deployment version and rollback.
- Confidential employee, customer or project information must not leak into reusable or externally published skills.
</non_negotiable_rules>

<stage_10_required_workstreams>
1. Define Experience Architecture:
   - employee workspace;
   - manager/team-lead console;
   - technical/domain reviewer console;
   - governance/DPO/HR/L&D console;
   - audience-specific BFF/read models;
   - notification/inbox;
   - search;
   - export;
   - feature flags;
   - audit and analytics.

2. Define Employee Workspace:
   - assigned tasks and daily plan;
   - work/task session status and controls;
   - task objective, acceptance criteria and progress;
   - evidence timeline and completeness;
   - human/AI/automation provenance;
   - coaching feed and preferences;
   - learning plan and practice;
   - capability character and skill tree;
   - role-readiness path;
   - corrections, disputes, appeals and review status;
   - privacy notice, exclusions, retention and access history;
   - evidence bookmark and support request.

3. Define Manager Console:
   - team task status;
   - blockers and owners;
   - missing quality gates;
   - overdue reviews;
   - workload/capacity signals;
   - task completion assurance;
   - reviewed capability-development themes;
   - learning/support actions;
   - unresolved disputes and employee responses;
   - raw-evidence access request;
   - no private coaching transcript;
   - no simplistic productivity score.

4. Define Reviewer/Governance Console:
   - finding package;
   - evidence sources and confidence;
   - telemetry completeness;
   - employee response/correction;
   - reviewer assignment and conflict check;
   - decision and rationale;
   - appeal;
   - raw-evidence grants;
   - access logs;
   - retention/legal hold;
   - model/skill/policy versions.

5. Define Capability Character and Skill Tree UX:
   - capability levels;
   - evidence confidence;
   - freshness;
   - strengths;
   - emerging skills;
   - target-role path;
   - learning quests/practice;
   - mastery contributions;
   - no public ranking;
   - accessible/non-childish professional visual language.

6. Define Evidence Timeline UX:
   - event/episode/artefact views;
   - filters by task, application, actor and evidence class;
   - visual-state thumbnails;
   - semantic event priority;
   - gaps and excluded periods;
   - corrections and assessment versions;
   - raw evidence drill-down only through authorised grants;
   - explainability without overwhelming users.

7. Define Coaching and Learning UX:
   - private coaching inbox;
   - intervention rationale;
   - snooze/dismiss/preferences;
   - micro-lessons;
   - practice/reassessment tasks;
   - feedback;
   - mentor handoff;
   - applied-learning evidence;
   - manager/L&D summary boundaries.

8. Define Access and Privacy UX:
   - visible monitoring;
   - active sensors;
   - policy/notice version;
   - exclusions;
   - private/pause state;
   - evidence access history;
   - retention/deletion status;
   - export;
   - correction/dispute;
   - incident/support contact.

9. Define read models and APIs:
   - employee workspace read model;
   - manager exception read model;
   - reviewer finding package;
   - capability character;
   - learning/coaching;
   - access/audit;
   - notification state;
   - search index;
   - export jobs.

10. Define non-functional UX:
    - accessibility;
    - localisation;
    - responsive design;
    - keyboard/screen-reader support;
    - performance;
    - graceful partial-data state;
    - safe offline/degraded experience;
    - security and privacy testing.

11. Produce user journeys and acceptance tests for:
    - employee starts task;
    - employee reviews evidence;
    - employee corrects task alignment;
    - employee disputes finding;
    - employee follows coaching;
    - employee completes practice and applies learning;
    - manager resolves blocker;
    - manager requests raw evidence;
    - reviewer resolves contradiction;
    - DPO audits evidence access;
    - employee changes coaching/privacy preferences.

12. Produce Stage 10 APIs/events, backlog, tests, risks, ADRs, gate and sources.
</stage_10_required_workstreams>

<stage_11_required_workstreams>
1. Define Skill Forge Architecture:
   - observation ingestion;
   - candidate detection;
   - proposal generator;
   - skill registry;
   - package store;
   - source/licence registry;
   - evaluation orchestrator;
   - domain/security/privacy review;
   - approval workflow;
   - canary deployment;
   - monitoring;
   - promotion;
   - rollback;
   - deprecation;
   - publication/export.

2. Define observation sources:
   - employee corrections;
   - reviewer overrides;
   - repeated false findings;
   - successful task patterns;
   - improved prompts;
   - AI-agent overreach/rejection patterns;
   - coaching feedback;
   - learning effectiveness;
   - adapter drift;
   - security/privacy incidents;
   - manager/employee suggestions;
   - approved external research.

3. Define Skill Forge categories:
   - prompt/agent skill;
   - task-assurance evaluator;
   - capability-scoring evaluator;
   - coaching skill;
   - learning artefact;
   - application/AI adapter;
   - redaction/privacy rule;
   - workflow;
   - report/read model;
   - domain task template;
   - policy template;
   - research synthesis.

4. Define Skill Package Contract:
   - skill ID;
   - category;
   - version;
   - purpose;
   - owner;
   - trigger;
   - required inputs;
   - expected outputs;
   - permitted capabilities/tools;
   - data classifications;
   - model/runtime requirements;
   - task/domain scope;
   - source references;
   - licence;
   - confidentiality classification;
   - known limitations;
   - evaluation suite;
   - security/privacy tests;
   - approval status;
   - deployment status;
   - effective date;
   - expiry/review date;
   - previous/rollback version.

5. Define lifecycle:
   - OBSERVED;
   - TRIAGED;
   - DRAFT;
   - EVALUATING;
   - REVIEW_REQUIRED;
   - APPROVED;
   - CANARY;
   - ACTIVE;
   - PAUSED;
   - DEPRECATED;
   - ROLLED_BACK;
   - REJECTED;
   - EXPIRED.

6. Define proposal and generalisation:
   - cluster repeated observations;
   - distinguish local one-off from generalisable pattern;
   - remove confidential/personal data;
   - preserve source lineage;
   - create draft change;
   - define expected benefit and affected metrics;
   - identify regression risks.

7. Define evaluation:
   - positive cases;
   - negative cases;
   - adversarial cases;
   - privacy/security;
   - fairness;
   - evidence grounding;
   - performance/cost;
   - compatibility;
   - regression;
   - calibration;
   - rollback test;
   - human review;
   - canary success criteria.

8. Define source and research governance:
   - official/primary source preference;
   - retrieval date;
   - jurisdiction;
   - reliability;
   - licence/terms;
   - conflicting sources;
   - proposed change;
   - human reviewer;
   - expiry/research refresh;
   - research findings are never immediate production instructions.

9. Define confidentiality/publication:
   - internal confidential;
   - internal reusable;
   - customer/tenant-specific;
   - publishable with attribution;
   - open-source candidate;
   - prohibited publication;
   - clean-room implementation when licences require it.

10. Define canary/promotion/rollback:
    - selected tenants/users/tasks;
    - feature flags;
    - control group where appropriate;
    - safety/quality/effectiveness metrics;
    - employee feedback;
    - regression threshold;
    - automatic pause;
    - human promotion decision;
    - rapid rollback.

11. Define governance and ownership:
    - skill owner;
    - domain reviewer;
    - security reviewer;
    - privacy/DPO reviewer;
    - legal/licence reviewer;
    - AI evaluation reviewer;
    - deployment approver;
    - incident owner;
    - audit.

12. Produce Stage 11 APIs/events, backlog, tests, risks, ADRs, gate and sources.
</stage_11_required_workstreams>

<architecture_constraints>
- Reuse the HumanOS frontend/design system, BFF/API gateway, identity, organisation, workflow, policy, audit, notification, file/object, event and Model Gateway services.
- Experience read models must be derived from reviewed domain state and evidence references, not direct unrestricted raw telemetry.
- Use Java/Spring for BFF/domain APIs and durable Skill Forge lifecycle.
- Use Python for proposal generation, research synthesis and evaluation workers behind governed APIs.
- Use Git/object/artifact stores for versioned skill packages and evaluation artefacts as appropriate.
- Use Kafka-compatible events and CloudEvents-style envelopes.
- Use feature flags and signed/versioned packages for canary deployment.
- Keep Skill Forge source observations separate from production skill packages.
- Do not create a separate microservice for every UI panel or skill category; split only for security, scale, ownership, availability or transactional boundaries.
</architecture_constraints>

<output_contract>
Update the existing workbook using one combined Stage 10–11 package with dedicated sheets for:

1. Stage 10-11 Dashboard
2. Experience Architecture
3. Employee Workspace
4. Manager Console
5. Review and Governance Console
6. Capability Character UX
7. Evidence Timeline UX
8. Coaching and Learning UX
9. Notification and Interaction Model
10. Access and Privacy UX
11. Reporting Read Models
12. User Journeys and Acceptance Tests
13. Skill Forge Architecture
14. Skill Observation Model
15. Skill Package Contract
16. Skill Lifecycle
17. Skill Proposal and Evaluation
18. Skill Security and Confidentiality
19. Research and Source Governance
20. Canary Promotion and Rollback
21. Stage 10-11 APIs and Events
22. Stage 10 Backlog
23. Stage 11 Backlog
24. Stage 10-11 Risks
25. Stage 10-11 ADRs
26. Stage 10 Gate
27. Stage 11 Gate
28. Stage 10-11 Sources

Every implementation/backlog row must include:
- unique ID;
- owner;
- contributors;
- dependencies;
- priority;
- effort;
- deliverable;
- acceptance criteria;
- test requirement;
- privacy/security impact;
- status.

Every UI/report row must define:
- audience;
- purpose;
- data source;
- access scope;
- employee visibility;
- loading/degraded state;
- accessibility requirement;
- prohibited use.

Every Skill Forge row must distinguish:
- source fact;
- observation;
- inference;
- proposed change;
- evaluation result;
- human decision;
- deployment state.

Use formulas for readiness, completion, risk, user-journey coverage, evaluation coverage and canary success.
</output_contract>

<validation>
Before completion, validate that:

1. Employees can inspect task evidence, capability findings, coaching and access history.
2. Employees can correct and challenge material findings.
3. Managers receive exception-led summaries rather than raw surveillance streams.
4. Private coaching/reflection/mentor content is not exposed by default.
5. Active disputes, evidence gaps, confidence and employee responses appear in relevant views.
6. Raw evidence access requires scoped grants and is audited.
7. Accessibility, localisation, partial data and privacy controls are included in all primary journeys.
8. No UI creates a click/key/time/code/prompt productivity score or public leaderboard.
9. Skill Forge observations cannot become active skills without evaluation and human approval.
10. Skill packages preserve source, licence, confidentiality, limitations, evaluation and rollback.
11. Research findings remain candidates until reviewed.
12. Confidential employee/customer/project data cannot enter reusable or public skills.
13. Canary releases can pause and roll back rapidly.
14. Stage 10 and Stage 11 have separate formal gates even though they are executed under one prompt.
15. The workbook passes formula, source, consistency and visual-quality checks.
</validation>