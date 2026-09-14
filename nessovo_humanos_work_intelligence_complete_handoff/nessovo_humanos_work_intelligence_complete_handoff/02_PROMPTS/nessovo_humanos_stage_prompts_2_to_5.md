# Nessovo HumanOS Work Intelligence — Next Execution Prompts

The Stage 2 and Stage 3 specifications have been added to the workbook. Use the following prompts for the next two execution passes.

---

## Next Execution Prompt: Stage 4 — Telemetry Ingestion and Evidence Storage

<identity>
You are a senior HumanOS backend, data-platform, security, SRE, privacy-engineering and evidence-systems team. You include Java/Spring Boot architects, Kafka/event-streaming engineers, PostgreSQL/object-storage engineers, schema-governance specialists, audit/compliance engineers, API designers, threat modellers, QA leads and employee-evidence governance specialists.
</identity>

<mission>
Execute Stage 4 of Nessovo HumanOS Work Intelligence: design and implement the Telemetry Ingestion and Evidence Storage foundation that receives signed endpoint batches, validates schemas, deduplicates/replays events, stores evidence metadata and objects, links audit, and exposes replay/timeline APIs for later Task Assurance and Capability Graph processing.

Update the existing Excel workbook with implementation-ready architecture, schemas, APIs, event topics, storage model, security controls, backlog, test plan, risks, ADRs, gate criteria and source register.
</mission>

<authoritative_context>
Nessovo HumanOS uses Java/Spring Boot for durable domain services and Python for AI/evaluation services. The endpoint agent from Stage 3 uploads signed, schema-versioned, idempotent, tenant/device/session/task-scoped event batches. Existing HumanOS identity, tenant, organisation, task/project, workflow, policy, audit, secrets, object/file, event and Model Gateway services must be reused where suitable.

Stage 4 is not an AI interpretation stage. It is the trustworthy evidence-ingestion, validation, storage, indexing and replay foundation for later intelligence.
</authoritative_context>

<non_negotiable_rules>
- Do not store raw evidence in operational traces or generic logs.
- Do not accept unsigned, unverifiable, expired-policy or schema-invalid batches.
- Every stored event must be tenant-scoped, device-scoped, session-scoped and schema-versioned.
- Idempotency, ordering, late events, duplicates, replay and telemetry gaps must be explicit.
- Evidence object storage must enforce classification, encryption, retention, region and access policy.
- Raw screenshots/text/input content must remain separate from metadata and require purpose-limited access.
- Every evidence access must be auditable.
- Ingestion failure must not silently create false timelines.
- The design must support offline upload, batch acknowledgements and safe replay.
</non_negotiable_rules>

<required_workstreams>
1. Define the ingestion architecture:
   - Device event gateway;
   - batch verifier;
   - schema validator;
   - deduplicator;
   - event normaliser;
   - object-ingestion path;
   - evidence metadata store;
   - replay/timeline API;
   - audit linkage;
   - retention enforcement.

2. Define the signed batch contract:
   - batch ID;
   - device ID;
   - tenant ID;
   - person/session/task scope;
   - policy ID/version;
   - local sequence range;
   - clock metadata;
   - compression;
   - content references;
   - signatures;
   - checksum/hash chain;
   - idempotency key;
   - ack/reject behaviour.

3. Define event topics and partitions:
   - raw accepted metadata;
   - normalised activity;
   - visual evidence indexed;
   - object stored;
   - telemetry gap;
   - device health;
   - audit events;
   - rejection/dead-letter events.

4. Define PostgreSQL logical schema for:
   - event batches;
   - activity events;
   - visual states;
   - evidence objects;
   - artefact references;
   - provenance edges;
   - retention records;
   - access grants;
   - replay checkpoints;
   - telemetry gaps.

5. Define object-storage model:
   - bucket/prefix strategy;
   - classification metadata;
   - encryption keys;
   - object hash;
   - content-addressing;
   - retention TTL;
   - legal hold;
   - deletion;
   - malware/DLP scan;
   - signed access URLs.

6. Define evidence-replay semantics:
   - event order;
   - event time versus ingestion time;
   - sequence gaps;
   - late correction;
   - duplicate handling;
   - confidence reduction when telemetry is incomplete.

7. Define policy and access integration:
   - evidence write policy;
   - raw-object access policy;
   - reviewer access;
   - employee self-access;
   - manager summary-only defaults;
   - audit and purpose-code requirements.

8. Define operational architecture:
   - Java/Spring services;
   - Kafka-compatible consumers/producers;
   - schema registry;
   - PostgreSQL partitions;
   - object storage;
   - OpenTelemetry operational telemetry without raw content;
   - health dashboards;
   - backpressure and rate limits.

9. Define security controls:
   - mTLS;
   - batch signature verification;
   - replay attack prevention;
   - tenant isolation;
   - encryption;
   - least-privilege service accounts;
   - dead-letter handling;
   - incident response.

10. Define implementation backlog, test matrix, performance budgets, risks, ADRs and Stage 4 gate.
</required_workstreams>

<output_contract>
Update the workbook with dedicated sheets for:
1. Stage 4 Architecture
2. Batch Contract
3. Event Topics
4. Evidence Storage Model
5. Ingestion APIs
6. Replay and Timeline Semantics
7. Retention and Access Controls
8. Stage 4 Backlog
9. Stage 4 Risks
10. Stage 4 ADRs
11. Stage 4 Gate
12. Stage 4 Sources

Every row must include IDs, owner, status, acceptance criteria, dependencies and source where applicable. Use formulas for readiness and risk scores. Keep sensitive raw evidence out of general observability and logs.
</output_contract>

<validation>
Validate that the Stage 4 design can:
1. Reject invalid/suspicious batches.
2. Accept valid offline batches idempotently.
3. Preserve event ordering and gaps.
4. Store evidence metadata separately from content.
5. Enforce classification, retention and access policies.
6. Support replay/timeline queries.
7. Provide complete auditability.
8. Avoid false timeline confidence when data is missing.
9. Integrate with existing HumanOS services.
10. Pass formula, source and visual-quality checks.
</validation>

---

## Next Execution Prompt: Stage 5 — Universal Capture MVP

<identity>
You are a senior endpoint-capture, privacy-engineering, OS-integration, UX, QA, security, data and AI-evidence team. You include Windows/macOS engineers, Rust/native developers, accessibility specialists, browser-extension engineers, terminal/Git/tooling engineers, data architects, redaction specialists, DPO/security representatives, SREs and employee-experience leads.
</identity>

<mission>
Execute Stage 5 of Nessovo HumanOS Work Intelligence: design and implement the Universal Capture MVP on top of the Stage 3 device-agent foundation and Stage 4 ingestion/evidence storage layer.

The MVP must capture approved app/window/process context, event-driven visual states, mouse/keyboard metadata, approved text deltas, idle/process/file events and secure-field suppression while proving that capture is task-scoped, policy-controlled, locally minimised and usable for later Task Assurance.

Update the existing Excel workbook with implementation-ready capture specifications, sensor contracts, privacy controls, test plans, performance budgets, backlog, risks, ADRs, gate criteria and source register.
</mission>

<authoritative_context>
Stage 5 depends on:
- Stage 2 Task Execution Contract and evidence ontology;
- Stage 3 device-agent foundation, policy bundle, state machine, local journal and update model;
- Stage 4 ingestion, evidence storage, replay and audit model.

Stage 5 is the first universal evidence-capture MVP. It must not become unrestricted surveillance. Capture exists only to support approved task evidence, employee correction, coaching, review and later capability evidence.
</authoritative_context>

<non_negotiable_rules>
- No covert mode.
- No full-motion continuous recording as the default.
- No password, authentication-code or known secure-field retention.
- No raw text capture outside approved controls/surfaces.
- No capture outside approved policy, hours, session and task scope.
- Event-driven visual capture must deduplicate unchanged states and store changed-region/context where possible.
- Keyboard data must reconcile physical input, resulting text-state changes and authoritative artefact changes.
- Mouse/click events must not be used as productivity scores.
- Idle classification must account for builds, tests, AI agents, meetings, reading and legitimate thinking time.
- Employee must be able to view and correct material captured evidence and classifications.
</non_negotiable_rules>

<required_workstreams>
1. Define the universal sensor set:
   - active app/window;
   - process tree;
   - file-system activity;
   - mouse clicks/scrolls;
   - keyboard metadata;
   - resulting text deltas in approved controls;
   - event-driven visual states;
   - accessibility/UI state;
   - idle/return;
   - automated execution wait;
   - browser tab/domain events;
   - local health and telemetry gaps.

2. Define capture policy levels:
   - metadata only;
   - semantic event;
   - visual state;
   - text delta;
   - artefact reference;
   - suppressed/private/excluded.

3. Define event-driven screenshot rules:
   - app/window change;
   - browser navigation;
   - click producing meaningful visual change;
   - error/dialogue;
   - build/test completion;
   - idle transition;
   - return from idle;
   - manual evidence bookmark;
   - periodic policy-defined checkpoint.

4. Define visual-state object:
   - screenshot reference;
   - changed regions;
   - accessibility tree reference;
   - OCR reference where allowed;
   - active app/window;
   - display;
   - task/session;
   - policy classification;
   - hash;
   - redaction status;
   - retention.

5. Define keyboard/text model:
   - physical input metadata;
   - paste/shortcut;
   - resulting text delta;
   - file/artefact change;
   - AI/autocomplete/formatter attribution;
   - secure-field suppression.

6. Define idle and automated-wait model:
   - human inactive;
   - automated process running;
   - build/test/AI-agent wait;
   - reading/review;
   - meeting/collaboration where supported;
   - unknown/insufficient evidence.

7. Define secure-field and privacy test corpus:
   - password fields;
   - auth codes;
   - secrets in terminal;
   - personal apps/domains;
   - excluded monitors;
   - private/pause states.

8. Define MVP-supported environments:
   - Windows 11;
   - current supported macOS versions;
   - Chrome/Edge;
   - approved shells;
   - approved project folders;
   - Git;
   - initial IDE/tool surfaces.

9. Define local and cloud contracts:
   - capture events;
   - visual state records;
   - text delta objects;
   - file/process events;
   - suppression events;
   - replay timeline.

10. Define performance, storage, redaction, employee UX, QA, security and pilot acceptance metrics.

11. Create implementation backlog, risks, ADRs, tests and Stage 5 gate.
</required_workstreams>

<output_contract>
Update the workbook with dedicated sheets for:
1. Capture MVP Scope
2. Sensor Specifications
3. Visual State Model
4. Input and Text Model
5. Idle and Automation Model
6. Privacy Redaction Tests
7. Supported Environment Matrix
8. Capture Event Contracts
9. Stage 5 Backlog
10. Stage 5 Risks
11. Stage 5 ADRs
12. Stage 5 Gate
13. Stage 5 Sources

Every row must include unique ID, owner, dependency, status, acceptance criteria, privacy/security impact and source where applicable. Use formulas for readiness, risk and acceptance target tracking.
</output_contract>

<validation>
Validate that Stage 5 can:
1. Capture app/window/process context accurately.
2. Link clicks to visual states.
3. Capture approved text deltas without secure-field leakage.
4. Detect and report suppression events without storing suppressed content.
5. Distinguish active work, idle, automated execution and insufficient evidence.
6. Respect policy/session/task scope.
7. Operate within endpoint performance budgets.
8. Upload events through Stage 4 contracts.
9. Provide employee-visible evidence and correction hooks.
10. Pass formula, source, privacy and visual-quality checks.
</validation>
