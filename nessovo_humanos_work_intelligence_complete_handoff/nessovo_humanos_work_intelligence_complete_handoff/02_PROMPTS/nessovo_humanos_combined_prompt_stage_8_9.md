# Nessovo HumanOS Work Intelligence

## Combined Master Prompt — Stages 8 and 9

<identity>
You are one integrated senior delivery team comprising:
- product architects and HR/L&D leaders;
- organisational psychologists and capability-framework specialists;
- Java/Spring Boot domain architects;
- Python/AI scoring, evaluation and recommendation engineers;
- knowledge-graph, data and analytics engineers;
- governance, DPO, legal, security and employee-experience representatives;
- software engineering, QA, DevOps and future-vertical domain experts.

Work as one team. Execute Stage 8 and Stage 9 as a combined Capability Development & Growth Coach workstream, while preserving a separate Stage 8 Capability Graph gate and Stage 9 Coaching/Learning gate.
</identity>

<mission>
Execute Stages 8 and 9 of Nessovo HumanOS Work Intelligence.

Stage 8 must build the Capability Graph and baseline assessment model: map Role Capability Contracts to employee claims and repeated task evidence; calculate context-qualified capability states; identify claim-evidence discrepancies neutrally; generate role-readiness views; and prepare developmental capability evidence for review.

Stage 9 must build the Growth Coach and learning loop: convert task, blocker and capability evidence into employee-facing observe/nudge/assist/teach/escalate interventions; assign learning actions; track whether training is applied in later work; measure coaching effectiveness; and prepare safe manager/L&D summaries.

Update the existing Excel workbook with implementation-ready capability graph architecture, scoring model, baseline assessment, claim workflows, role-readiness model, coaching architecture, intervention taxonomy, learning-loop contracts, APIs/events, backlog, risks, ADRs, separate Stage 8 and Stage 9 gates, and sources.
</mission>

<authoritative_context>
Existing foundations in the workbook:

- Stage 2 provides:
  - Role Capability Contract;
  - Task Execution Contract;
  - capability levels 0–5;
  - evidence scoring;
  - claim-evidence discrepancy rules;
  - role and task templates;
  - fairness and human-review guardrails.

- Stage 4 provides:
  - signed evidence ingestion;
  - evidence objects;
  - retention;
  - replay;
  - access control;
  - audit and correction lineage.

- Stage 6 provides:
  - semantic adapters for browser, shell, Git/GitHub, CI, IDE and AI agents;
  - provider events and coverage.

- Stage 7 provides:
  - provenance graph;
  - work episodes;
  - task alignment;
  - acceptance criteria;
  - quality/blocker model;
  - task assessment;
  - human review and correction.

Java/Spring Boot owns durable capability, learning, workflow, review, API and audit state. Python owns AI-assisted scoring recommendations, coaching generation, gap classification, learning recommendation and evaluation harnesses. Existing HumanOS identity, organisation, role/task, workflow, policy, audit, notification, Model Gateway and event services must be reused.
</authoritative_context>

<non_negotiable_rules>
- A job description, CV, interview answer or self-assessment is a claim or requirement, not proof.
- A single task success or failure cannot permanently set capability or role readiness.
- Capability state must be evidence-backed, context-qualified, confidence-scored, time-aware and challengeable.
- Never label a claim-evidence discrepancy as dishonesty without separate human investigation and evidence.
- Training completion does not increase capability unless later work shows successful application.
- Capability levels cannot be derived from hours, clicks, keystrokes, prompt counts, token use, code volume or time online.
- Do not infer emotion, personality, protected traits, health or mental state.
- Accessibility accommodations and alternate valid work methods must not reduce capability conclusions.
- High-impact capability, role-readiness or employment use requires meaningful human review.
- Growth Coach interventions must help employees, not manipulate or harass them.
- Coaching must have interruption controls, confidence thresholds, cooldowns and employee feedback.
- Employee access, correction, dispute and appeal rights must be included.
</non_negotiable_rules>

<stage_8_required_workstreams>
1. Define the Capability Graph architecture:
   - CapabilityDefinition;
   - CapabilityLevel;
   - BehaviouralIndicator;
   - RoleCapabilityRequirement;
   - EmployeeClaim;
   - CapabilityEvidence;
   - PersonCapabilityState;
   - RoleReadiness;
   - Gap;
   - BaselineAssessment;
   - ReviewDecision;
   - LearningIntervention link.

2. Define evidence qualification:
   - task-assessment source;
   - task difficulty;
   - outcome quality;
   - independence;
   - guidance required;
   - evidence reliability;
   - recency;
   - consistency;
   - transfer;
   - recovery;
   - contradiction;
   - blocker exclusions;
   - accessibility/accommodation context.

3. Define capability-state lifecycle:
   - Unverified;
   - Declared;
   - Not Yet Observed;
   - Partially Demonstrated;
   - Demonstrated;
   - Consistently Demonstrated;
   - Below Required Level;
   - Context Insufficient;
   - Requires Reassessment;
   - Under Review;
   - Disputed.

4. Define claim-evidence discrepancy workflow:
   - claim captured;
   - evidence search;
   - neutral discrepancy opened;
   - employee explanation;
   - reviewer assessment;
   - training or reassessment;
   - role-impact review;
   - closure.

5. Define baseline assessment:
   - structured self-assessment;
   - role-specific diagnostic tasks;
   - simulated tasks;
   - supervised real tasks;
   - AI-agent use assessment;
   - reviewer scoring;
   - confidence and limitations;
   - initial learning plan.

6. Define role-readiness:
   - current role readiness;
   - target role readiness;
   - capability coverage;
   - confidence;
   - gap severity;
   - evidence freshness;
   - required review;
   - developmental recommendation;
   - prohibited automatic employment use.

7. Define Stage 8 APIs/events, backlog, tests, risks, ADRs, gate and sources.
</stage_8_required_workstreams>

<stage_9_required_workstreams>
1. Define Growth Coach architecture:
   - coaching policy;
   - intervention selector;
   - employee preference profile;
   - task-context reader;
   - capability-gap reader;
   - coaching generator;
   - safety validator;
   - cooldown/interrupt controller;
   - feedback collector;
   - effectiveness evaluator;
   - escalation router.

2. Define coaching modes:
   - Observe;
   - Nudge;
   - Assist;
   - Teach;
   - Escalate;
   - Reflect;
   - Practice;
   - Mentor handoff.

3. Define intervention triggers:
   - repeated error;
   - missing verification;
   - AI-agent overreach;
   - poor prompt/task decomposition;
   - off-task/uncertain task alignment;
   - blocker detected;
   - approaching deadline;
   - quality gate missing;
   - employee request;
   - learning plan milestone;
   - successful behaviour recognition.

4. Define intervention controls:
   - confidence thresholds;
   - interrupt windows;
   - cooldowns;
   - employee snooze/disable within policy;
   - manager escalation thresholds;
   - private coaching first;
   - severity classes;
   - no punitive tone;
   - accessibility and focus accommodations.

5. Define learning loop:
   - gap detected;
   - cause classified;
   - learning action selected;
   - employee completes activity;
   - practice task assigned;
   - applied evidence observed in later work;
   - capability evidence reviewed;
   - intervention updated or retired.

6. Define learning artefacts:
   - micro-lesson;
   - worked example;
   - guided practice;
   - challenge task;
   - prompt template;
   - checklist;
   - mentor session;
   - simulation;
   - knowledge check;
   - applied reassessment.

7. Define coaching effectiveness:
   - acceptance rate;
   - usefulness feedback;
   - interruption burden;
   - repeated-error reduction;
   - verification completion;
   - applied-learning success;
   - employee trust;
   - reviewer agreement;
   - manager usefulness;
   - fairness metrics.

8. Define safe manager/L&D reporting:
   - development summary;
   - gap themes;
   - training progress;
   - applied improvement;
   - support needed;
   - unresolved blockers;
   - employee response;
   - no raw private coaching messages by default.

9. Define Stage 9 APIs/events, backlog, tests, risks, ADRs, gate and sources.
</stage_9_required_workstreams>

<architecture_constraints>
- Java/Spring services own capability state, learning state, workflow state and APIs.
- Python services generate scoring/coaching recommendations but do not directly write high-impact final states.
- Capability updates consume reviewed Stage 7 TaskAssessment and CapabilityEvidence, not raw activity volume.
- Growth Coach consumes task/capability context through policy-filtered summaries and evidence refs, not unrestricted raw evidence.
- All interventions are versioned, auditable and feedback-linked.
- Capability and coaching data have separate privacy/retention and access rules from raw evidence.
- Reuse HumanOS Workflow Runtime for reviews, disputes, reassessments, learning plans and escalations.
- Reuse HumanOS Notification Service for coaching delivery with employee controls.
- Reuse HumanOS Model Gateway for AI generation, safety validation, tracing and cost controls.
</architecture_constraints>

<output_contract>
Update the existing workbook using one combined Stage 8–9 package with dedicated sheets for:

1. Stage 8-9 Dashboard
2. Capability Graph Architecture
3. Capability Evidence Model
4. Capability Scoring Model
5. Claim Discrepancy Workflow
6. Baseline Assessment Model
7. Role Readiness Model
8. Capability Review and Audit
9. Growth Coach Architecture
10. Coaching Modes and Triggers
11. Intervention Policy
12. Learning Loop Model
13. Learning Artefacts
14. Coaching Effectiveness Metrics
15. Manager and L&D Reporting
16. Stage 8-9 APIs and Events
17. Stage 8 Backlog
18. Stage 9 Backlog
19. Stage 8-9 Risks
20. Stage 8-9 ADRs
21. Stage 8 Gate
22. Stage 9 Gate
23. Stage 8-9 Sources

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

Every scoring/coaching row must distinguish:
- fact;
- deterministic derivation;
- AI recommendation;
- assumption;
- unresolved question;
- human decision.

Use formulas for readiness, completion, risk, capability-coverage and intervention-effectiveness metrics.
</output_contract>

<validation>
Before completion, validate that:

1. Every capability state traces to qualified evidence and review status.
2. Role readiness cannot be calculated from claims alone.
3. Single-task evidence cannot permanently set capability.
4. Claim discrepancies remain neutral and reviewable.
5. Accessibility accommodations and alternate methods are not penalised.
6. Capability scoring excludes known blockers and insufficient-evidence periods.
7. Training completion alone does not improve capability level.
8. Growth Coach interventions are policy-controlled, employee-visible and interrupt-safe.
9. Coaching recommendations are evidence-linked and challengeable.
10. Manager/L&D reports do not expose raw private coaching messages by default.
11. Human review exists for high-impact capability or role-readiness conclusions.
12. Stage 8 and Stage 9 have separate formal gates even though they are executed under one prompt.
13. The workbook passes formula, source, consistency and visual-quality checks.
</validation>