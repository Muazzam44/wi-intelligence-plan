# Generates plan/modules/*.md from the Stage 12A remediation data (master workbook).
# Status lives ONLY here-generated front-matter; board/index/traceability are derived.
# Rerun after editing MODULES, then re-run plan_lint.py (no flag) and --board.
import pathlib, textwrap

PLAN = pathlib.Path(__file__).parent / "plan" / "modules"
PLAN.mkdir(parents=True, exist_ok=True)

# id, title, tier, tier_rationale, wave, deps [(module, interface)], provides, shared,
# satisfies, status, model, reviewer, sources, summary, acceptance[], evidence, notes
MODULES = [
 dict(id="M01", title="Disable central CLI defaults", tier=0,
  rationale="a default route can silently bill/expose a personal subscription account (AUD-009) — credential/account boundary",
  wave=1, deps=[], provides=[("RouteDefaultsPolicy", 1)], shared=[], satisfies=["T02"],
  status="draft", model="Opus", reviewer="Codex",
  sources="REM-001 · HND-001 · AUD-009 (0.05)",
  summary="Change all production/default task routes away from `claude-cli`; allow it only under an explicit local-dev/endpoint-interactive profile.",
  acceptance=[
   "WHEN any central or background workload requests a route, THE SYSTEM SHALL never select the user-subscription CLI unless the request carries the explicit endpoint-interactive development profile.",
   "WHEN the endpoint-interactive profile is absent, THE SYSTEM SHALL resolve defaults exclusively to approved connector routes."],
  evidence="Configuration + routing test (REM-001); dependency/config diff.",
  notes="1 effort-day; no dependencies — first change of the programme (R01)."),
 dict(id="M02", title="humanos-ai-contracts v1", tier=0,
  rationale="the contract of record every governed AI call rides; every dependent module binds to it",
  wave=1, deps=[], provides=[("AiContractsV1", 1)], shared=[], satisfies=["T03"],
  status="draft", model="Opus", reviewer="Codex",
  sources="REM-002 · HND-002 · AUD-002 (0.35) · AUD-003 (0.55) · AUD-016 (0.35)",
  summary="Publish the provider-neutral versioned request/result contract: purpose, task/effort, data class, region, features, output schema, evidence refs, review, fallback and exact route lineage; promote a policy-safe subset of the runtime's governed envelope; audience-scoped service identity with purpose claims on S2S paths.",
  acceptance=[
   "WHEN the shared client, runtime gateway and ai-execution-service exchange requests, THE SYSTEM SHALL pass versioned contract fixtures including negative cases (REM-002 acceptance).",
   "WHEN a pure service-to-service request arrives, THE SYSTEM SHALL reconcile a service identity with audience and purpose claims before honouring a caller-supplied tenant (AUD-016).",
   "WHEN a field the contract requires is absent, THE SYSTEM SHALL refuse the request with the canonical error taxonomy, never default it."],
  evidence="Schema, compatibility and negative contract tests (HND-002); executed integration evidence for the sync API and async lifecycle under v1 (OI-05).",
  notes="Critical path (R02): M04..M13 all bind to this."),
 dict(id="M03", title="Claude CLI process safety", tier=0,
  rationale="concrete security/reliability defect — path hijack, inherited env, stderr deadlock, ineffective timeout (AUD-011)",
  wave=1, deps=[], provides=[("SafeCliInvocation", 1)], shared=[], satisfies=["T04"],
  status="draft", model="Opus", reviewer="Codex",
  sources="REM-003 · HND-003 · AUD-011 (0.0)",
  summary="Correct timeout/stream handling: signed executable resolution, argument-only process (no cmd.exe /c), clean environment, approved cwd, concurrent stdout/stderr draining, process-tree kill and cancellation.",
  acceptance=[
   "WHEN a CLI process hangs, THE SYSTEM SHALL terminate the whole process tree within the timeout budget with no stderr deadlock.",
   "WHEN the CLI is resolved, THE SYSTEM SHALL execute only a signed executable from an approved path with a clean environment and approved working directory, and SHALL NOT reach outside the approved root."],
  evidence="Unit, integration, Windows/macOS and red-team tests (HND-003).",
  notes="Precondition for the broker extraction (M04)."),
 dict(id="M04", title="Endpoint AI Runtime Broker", tier=0,
  rationale="moves subscription/local-runtime execution to the managed endpoint boundary; central OAuth access is a hard boundary (T04)",
  wave=2, deps=[("M02", "AiContractsV1"), ("M03", "SafeCliInvocation")],
  provides=[("EndpointBrokerAPI", 1)], shared=[], satisfies=["T04"],
  status="draft", model="Opus", reviewer="Codex",
  sources="REM-004 · HND-003 · AUD-010 (0.0)",
  summary="Extract subscription-CLI/local-runtime invocation out of the central service into a managed endpoint boundary reporting health, action-required and canonical results.",
  acceptance=[
   "WHEN any central component needs endpoint execution, THE SYSTEM SHALL delegate to the broker and SHALL NOT access user-local OAuth or credentials.",
   "WHEN the broker executes, THE SYSTEM SHALL report health/action-required states and return canonical contract results."],
  evidence="Architecture, integration and red-team tests (REM-004).",
  notes="15 effort-days; the A-01 boundary AUD-010 found missing."),
 dict(id="M05", title="Provider-scoped credential resolution", tier=0,
  rationale="silent tenant-to-platform account/data-route switch is a privacy/billing incident (AUD-015)",
  wave=2, deps=[("M02", "AiContractsV1")], provides=[("CredentialResolution", 1)],
  shared=[], satisfies=["T05"], status="draft", model="Opus", reviewer="Codex",
  sources="REM-005 · HND-004 · AUD-015 (0.2)",
  summary="Replace the Anthropic-specific nullable override with an explicit provider/tenant credential result carrying configured/not-found/unavailable/forbidden and policy state; fail safely per policy.",
  acceptance=[
   "WHEN the tenant credential service is unavailable, THE SYSTEM SHALL fail per policy and SHALL NOT silently switch to a platform key, account, provider or data route.",
   "WHEN credentials rotate, THE SYSTEM SHALL pass rotation, outage, tenant and identity tests without cross-tenant leakage."],
  evidence="Rotation, outage, tenant and identity tests (HND-004).", notes=""),
 dict(id="M06", title="Evidence-object persistence (no raw prompts)", tier=0,
  rationale="writes the record of record for AI evidence; raw prompt/output persistence is incompatible with retention/employee rights (AUD-018)",
  wave=2, deps=[("M02", "AiContractsV1")], provides=[("EvidenceObjectRefs", 1)],
  shared=["db"], satisfies=["T06"], status="draft", model="Opus", reviewer="Codex",
  sources="REM-006 · HND-005 · AUD-018 (0.0) · DPIA-007",
  summary="Replace mandatory raw input/output TEXT columns with minimised metadata plus encrypted, classified evidence-object references carrying TTL, access grants, correction, deletion and legal-hold lineage; forward migration for existing rows.",
  acceptance=[
   "WHEN a new execution is persisted, THE SYSTEM SHALL store no mandatory raw input/output text fields — only classified object references and minimised metadata.",
   "WHEN retention, correction, deletion or hold events occur, THE SYSTEM SHALL propagate them across the evidence lineage and pass the privacy/DR test set."],
  evidence="Migration, access, privacy and DR tests (HND-005).",
  notes="DPO co-owned (REM-006); R03."),
 dict(id="M07", title="Exact model-deployment registry", tier=0,
  rationale="route identity is the substrate of qualification and audit; family/alias-only identity voids both (T07)",
  wave=2, deps=[("M02", "AiContractsV1")], provides=[("ModelDeploymentRegistry", 1)],
  shared=["db"], satisfies=["T07"], status="draft", model="Opus", reviewer="Codex",
  sources="REM-007 · HND-006 · AUD-006 (0.25) · AUD-020 (0.0)",
  summary="Registry rows carry endpoint, operator, snapshot-or-digest, runtime, CLI version, quantisation, context, features, terms, region, price and lifecycle; the YAML file may remain bootstrap config only.",
  acceptance=[
   "WHEN a route becomes active, THE SYSTEM SHALL represent it by an exact model deployment and SHALL NOT accept a family/alias-only representation.",
   "WHEN a deployment alias cannot be resolved to an exact identity, THE SYSTEM SHALL shorten or disable its qualification (AUD-020)."],
  evidence="Schema and registry tests (REM-007).", notes=""),
 dict(id="M08", title="Qualification lifecycle & hard gate", tier=0,
  rationale="decides which model configurations may execute employee-affecting work; an unqualified route is a policy breach (T08)",
  wave=3, deps=[("M07", "ModelDeploymentRegistry")], provides=[("QualificationGate", 1)],
  shared=["db"], satisfies=["T08"], status="draft", model="Opus", reviewer="Codex",
  sources="REM-008 · HND-006 · AUD-012 (0.1)",
  summary="Task×effort qualification profiles with expiry, signed packages, shadow/canary paths and router enforcement.",
  acceptance=[
   "WHEN a route candidate lacks a current qualification for the task×effort cell, THE SYSTEM SHALL exclude it before selection (negative tests).",
   "WHEN a qualification expires, THE SYSTEM SHALL stop selecting the configuration until requalified.",
   "WHILE tool calling is prompt-simulated (AUD-012), THE SYSTEM SHALL never qualify that mode for production tool-use cells."],
  evidence="Qualification/routing negative tests (REM-008); registry, evaluation, shadow, canary and drift tests (HND-006).", notes=""),
 dict(id="M09", title="Eligibility router & canonical fallback", tier=0,
  rationale="the routing decision is the policy enforcement point for every AI call; fallback semantics carry employee-rights consequences (T09)",
  wave=3, deps=[("M05", "CredentialResolution"), ("M07", "ModelDeploymentRegistry"),
                ("M08", "QualificationGate"), ("M02", "AiContractsV1")],
  provides=[("RoutingDecision", 1)], shared=[], satisfies=["T08", "T09"],
  status="draft", model="Opus", reviewer="Codex",
  sources="REM-009 · REM-010 · HND-007 · AUD-008 (0.15) · AUD-019 (0.3)",
  summary="Hard eligibility (policy/region/features/qualification/health) before minimum-sufficient cost/latency selection; canonical auth/quota/model/region/schema/qualification/resource/no-route/user-action failure states with terminal human-review/no-AI paths; every rejected candidate reason auditable.",
  acceptance=[
   "WHEN candidates are filtered, THE SYSTEM SHALL record every rejected candidate's reason auditably, and cost SHALL NOT make an ineligible route eligible.",
   "WHEN no eligible route exists, THE SYSTEM SHALL resolve to the canonical no-route/human-review/no-AI terminal — never a silent material route change.",
   "WHEN AI is unavailable, THE SYSTEM SHALL never convert that into employee failure (journey tests)."],
  evidence="Routing, chaos, region, cost and employee-journey tests (HND-007); failure-injection tests (REM-010).",
  notes="A pinned model stays honoured only while eligible (AUD-008)."),
 dict(id="M10", title="Complete inference lineage", tier=0,
  rationale="material AI-assisted domain records are records of record; incomplete lineage breaks audit and review rights (T10)",
  wave=3, deps=[("M02", "AiContractsV1"), ("M07", "ModelDeploymentRegistry"),
                ("M09", "RoutingDecision")],
  provides=[("InferenceLineage", 1)], shared=["db"], satisfies=["T10"],
  status="draft", model="Opus", reviewer="Codex",
  sources="REM-011 · HND-008 · AUD-017 (0.4) · AUD-020 (0.0)",
  summary="Persist actual implementation, connector, provider/operator, requested vs actual model, runtime, qualification profile, region, fallback decisions and review references on every material record.",
  acceptance=[
   "WHEN a material AI-assisted domain record is written, THE SYSTEM SHALL attach complete lineage — 100% coverage in the audit read-model (REM-011)."],
  evidence="Data integration/audit and read-model tests (HND-008).", notes=""),
 dict(id="M11", title="Monorepo provider cutover", tier=0,
  rationale="direct provider SDK/HTTP use outside the choke point voids every gateway control (T01)",
  wave=3, deps=[("M02", "AiContractsV1")], provides=[("ProviderCutoverProof", 1)],
  shared=[], satisfies=["T01"], status="draft", model="Opus", reviewer="Codex",
  sources="REM-023 · HND-001 · AUD-001 (0.65)",
  summary="Find and remove direct Anthropic/OpenAI/Gemini clients from project, PM-template, assistant and other services; route only through humanos-ai-client.",
  acceptance=[
   "WHEN the dependency scan runs, THE SYSTEM SHALL show no service outside approved connector modules importing provider config/SDK or sending provider HTTP requests."],
  evidence="Repository dependency scan, contract tests and removal diff (REM-023).", notes=""),
 dict(id="M12", title="Codex read-only review wrapper", tier=1,
  rationale="development tooling with permission boundaries; performs no record-of-record mutation itself — M14 is the merge authority",
  wave=3, deps=[("M02", "AiContractsV1"), ("M04", "EndpointBrokerAPI")],
  provides=[("CodexReviewConnector", 1)], shared=[], satisfies=["T11"],
  status="draft", model="Opus", reviewer="Codex",
  sources="REM-012 · HND-009 · Claude-Codex Review Protocol sheet",
  summary="Approved Codex CLI connector/wrapper (GPT-5.6 Sol/max) producing structured findings with exact model capture and NO write tools.",
  acceptance=[
   "WHEN Codex reviews plan/diff/test evidence, THE SYSTEM SHALL prevent any worktree modification or merge action (permission tests).",
   "WHEN findings are produced, THE SYSTEM SHALL capture the exact model identity and structured finding schema; injection tests pass."],
  evidence="Permission/injection/review tests (REM-012).", notes=""),
 dict(id="M13", title="Fable & Opus development task profiles", tier=1,
  rationale="profile/policy configuration for dev routing; enforcement authorities are M08/M14",
  wave=3, deps=[("M02", "AiContractsV1"), ("M04", "EndpointBrokerAPI")],
  provides=[("DevTaskProfiles", 1)], shared=[], satisfies=["T11"],
  status="draft", model="Opus", reviewer="Codex",
  sources="REM-013 · HND-009 · Development AI Workflow sheet",
  summary="Separate planning/orchestration (Fable) and implementation (Opus) routes with exact-model preflight and work-package schemas.",
  acceptance=[
   "WHEN the Fable profile executes, THE SYSTEM SHALL refuse coding-write capabilities; WHEN the Opus profile executes, THE SYSTEM SHALL refuse self-review/merge capabilities (policy tests)."],
  evidence="Workflow and policy tests (REM-013).", notes=""),
 dict(id="M14", title="CI + named-human merge gate", tier=0,
  rationale="protected-branch merge is an irreversible governance act; an AI-only merge is the exact failure T11 forbids",
  wave=4, deps=[("M12", "CodexReviewConnector"), ("M13", "DevTaskProfiles")],
  provides=[("ProtectedMergeGate", 1)], shared=[], satisfies=["T11"],
  status="draft", model="Opus", reviewer="Codex",
  sources="REM-014 · HND-009",
  summary="Protected-branch checks, CODEOWNERS and review state requiring deterministic CI, Codex blocker/major resolution and a named human approval.",
  acceptance=[
   "WHEN a merge to a protected branch is attempted, THE SYSTEM SHALL require deterministic CI, resolved Codex blockers/majors and a named human approval — no AI-only merge (repository control test)."],
  evidence="Repository control test (REM-014).", notes=""),
 dict(id="M15", title="Provider connectors (native + constrained compatible)", tier=1,
  rationale="connectors execute under M09's eligibility gates; floor anchor for provider correctness",
  wave=4, deps=[("M02", "AiContractsV1"), ("M07", "ModelDeploymentRegistry")],
  provides=[("ConnectorConformance", 1)], shared=[], satisfies=["T01"],
  status="draft", model="Opus", reviewer="Codex",
  sources="REM-015 · REM-016 · REM-017 · AUD-013 (0.5) · AUD-014 (0.25)",
  summary="Native OpenAI Responses connector split from the generic compatibility connector (capability probes: system/multiturn/tools/schema/embeddings/stream/cancel, actual operator recorded); hardened Anthropic connector (actual response model/route, sanitized errors, structured-output/effort manifest, provider-policy record).",
  acceptance=[
   "WHEN a connector lacks a probed capability, THE SYSTEM SHALL reject the feature before execution (conformance).",
   "WHEN provider errors occur, THE SYSTEM SHALL keep sensitive provider bodies out of logs and record exact route/features."],
  evidence="Connector conformance + privacy suites (REM-015..017).", notes=""),
 dict(id="M16", title="Provider health, budgets & circuit breaking", tier=1,
  rationale="operational signal source consumed by the router; no direct record mutation",
  wave=4, deps=[("M09", "RoutingDecision")], provides=[("HealthBudgetSignals", 1)],
  shared=[], satisfies=["T08"], status="draft", model="Opus", reviewer="Codex",
  sources="REM-018",
  summary="Health registry, quota/budget checks, retries, idempotency and circuit state feeding eligibility.",
  acceptance=[
   "WHEN a route is unhealthy or over budget, THE SYSTEM SHALL exclude it without weakening any policy guarantee (chaos/load tests)."],
  evidence="Chaos/load tests (REM-018).", notes=""),
 dict(id="M17", title="Model catalogue endpoint security", tier=1,
  rationale="information-disclosure control on the registry surface",
  wave=4, deps=[("M07", "ModelDeploymentRegistry")], provides=[("SecuredCatalogue", 1)],
  shared=[], satisfies=["T07"], status="draft", model="Opus", reviewer="Codex",
  sources="REM-019",
  summary="Authenticate the internal registry endpoint or expose a minimised public catalogue.",
  acceptance=[
   "WHEN an unauthenticated caller queries the catalogue, THE SYSTEM SHALL NOT enumerate internal providers, prices or routes (API security test)."],
  evidence="API security test (REM-019).", notes=""),
 dict(id="M18", title="Durable audit ledger & quality feedback", tier=1,
  rationale="durability layer under M10's lineage; loses no mandatory audit events",
  wave=4, deps=[("M10", "InferenceLineage")], provides=[("DurableAuditLedger", 1)],
  shared=["db"], satisfies=["T10"], status="draft", model="Opus", reviewer="Codex",
  sources="REM-020 · AUD-017 (0.4)",
  summary="Durable outbox/reconciliation for mandatory audit fields plus reviewed quality/correction/override signals.",
  acceptance=[
   "WHEN the ledger is unavailable, THE SYSTEM SHALL NOT lose mandatory audit/quality events (outbox/reconciliation tests)."],
  evidence="Outbox/reconciliation tests (REM-020).", notes=""),
 dict(id="M19", title="Qualification corpus & initial runs", tier=1,
  rationale="produces signed evaluation artefacts; the enforcement authority remains M08",
  wave=5, deps=[("M08", "QualificationGate"), ("M12", "CodexReviewConnector"),
                ("M13", "DevTaskProfiles"), ("M15", "ConnectorConformance")],
  provides=[("QualifiedProfiles", 1)], shared=[], satisfies=["T08", "T11"],
  status="draft", model="Opus", reviewer="Codex",
  sources="REM-021 · HND-006 · OI-04",
  summary="Build HumanOS + development datasets; qualify Fable, Opus, Codex and initial production candidates; signed profiles and limitations — no global model approval.",
  acceptance=[
   "WHEN qualification runs complete, THE SYSTEM SHALL produce signed task×effort profiles with limitations, and SHALL NOT emit a global model approval."],
  evidence="Evaluation report (REM-021). Corpus sign-off is OI-04.", notes=""),
 dict(id="M20", title="Stage 12A assurance execution", tier=0,
  rationale="the hardening gate of record before any employee pilot (T13)",
  wave=5, deps=[("M04", "EndpointBrokerAPI"), ("M06", "EvidenceObjectRefs"),
                ("M09", "RoutingDecision"), ("M11", "ProviderCutoverProof"),
                ("M14", "ProtectedMergeGate")],
  provides=[("Stage12AEvidence", 1)], shared=[], satisfies=["T13"],
  status="draft", model="Opus", reviewer="Codex",
  sources="HND-010 · Stage 12A Hardening Gate sheet · Security Hardening Plan · Privacy and DPIA Closure · Legal and Worker Consultation · Fairness and Accessibility Eval sheets",
  summary="Execute the engineering side of the Stage 12A tracks — security, privacy, endpoint performance/compatibility, data reliability/DR, AI & evaluator evaluation, fairness, accessibility, user-journey validation, operational readiness, incident/stop controls — and assemble the gate evidence.",
  acceptance=[
   "WHEN the gate is convened, THE SYSTEM SHALL present per-track evidence rows mapped to the Stage 12A gate sheet; PASS or RESTRICT is a human decision this module cannot make (OI-03)."],
  evidence="Connector conformance and Stage 12A gate evidence (HND-010); per-track sheets.",
  notes="DPIA/legal/worker-consultation and pen-test close outside engineering (OI-03)."),
 dict(id="M21", title="Standalone router decision spike", tier=2,
  rationale="a decision spike producing an ADR; no production operation performed",
  wave=5, deps=[("M02", "AiContractsV1"), ("M08", "QualificationGate"),
                ("M09", "RoutingDecision")],
  provides=[("RouterDecisionRecord", 1)], shared=[], satisfies=[],
  status="blocked-needs-decision", model="Sonnet", reviewer="Codex",
  sources="REM-022 · ADR-P2 · OI-02",
  summary="Build only if isolation/resilience/customer-deployment needs cannot be met by the central orchestrator; if built, the same contracts and portable profiles must pass.",
  acceptance=[
   "WHEN the CTO decision is recorded, THE SYSTEM SHALL either close this module as decision-evidence-only or open a build change-proposal via plan-change."],
  evidence="Architecture decision / conformance (REM-022).",
  notes="Blocked on OI-02 (CTO / Architecture)."),
 dict(id="M22", title="Pilot protocol readiness", tier=0,
  rationale="a real employee pilot bears directly on employee rights; running it early is the exact harm T13 fences",
  wave=6, deps=[("M20", "Stage12AEvidence")], provides=[("PilotProtocolRun", 1)],
  shared=[], satisfies=["T12", "T13"],
  status="blocked-needs-decision", model="Opus", reviewer="Codex",
  sources="Pilot Protocol · Pilot Cohort and Task Matrix · Pilot Metrics and Thresholds · Participant Rights and Support sheets · S03 next actions 5-6",
  summary="Prepare the staged internal pilot per protocol — cohort/task matrix, metrics/thresholds, participant rights and support, issue/decision log — and record STOP/REBUILD/RESTRICT/MODIFY/LIMITED/PHASED/PROCEED.",
  acceptance=[
   "WHILE the Stage 12A gate has not passed or restricted, THE SYSTEM SHALL NOT start any real employee pilot.",
   "WHEN the pilot runs, THE SYSTEM SHALL uphold participant rights (inspect/correct/dispute/appeal) and never let AI directly decide dismissal, pay, promotion, probation or discipline."],
  evidence="Pilot Results + Rollout Options and Decision sheets.",
  notes="Blocked on the Stage 12A gate outcome (M20, OI-03)."),
]

TPL = """---
id: {id}
title: {title}
tier: {tier}
tier_rationale: {rationale}
status: {status}
wave: {wave}
depends_on:{deps}
provides:{provides}
shared_resources: [{shared}]
satisfies: [{satisfies}]
model: {model}
reviewer: {reviewer}
compliance: []
---

# {id} — {title}

## Responsibility

{summary}

## Acceptance criteria

{acceptance}

## Verification (required evidence)

{evidence}

## Provenance

{sources} — master workbook `01_MASTER/nessovo_humanos_work_intelligence_master_handoff_validated.xlsx` (see `registers/sources.md`).
{notes}"""

for m in MODULES:
    deps = "".join(f"\n  - {{module: {d}, interface: {i}}}" for d, i in m["deps"]) or " []"
    provides = "".join(f"\n  - {{interface: {i}, version: {v}}}" for i, v in m["provides"])
    acceptance = "\n".join(f"- {a}" for a in m["acceptance"])
    body = TPL.format(id=m["id"], title=m["title"], tier=m["tier"],
                      rationale=m["rationale"], status=m["status"], wave=m["wave"],
                      deps=deps, provides=provides, shared=", ".join(m["shared"]),
                      satisfies=", ".join(m["satisfies"]), model=m["model"],
                      reviewer=m["reviewer"], summary=m["summary"],
                      acceptance=acceptance, evidence=m["evidence"],
                      sources=m["sources"],
                      notes=(f"\nNote: {m['notes']}" if m["notes"] else ""))
    (PLAN / f"{m['id']}.md").write_text(body, encoding="utf-8", newline="\n")
print(f"wrote {len(MODULES)} modules")
