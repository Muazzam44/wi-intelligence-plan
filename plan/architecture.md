# Architecture

## Stack & versions

Brownfield target: `Rapidtackltd/humanos-backend-services` at assessed commit
`79a38ade1fc0163cadf39ae3cccd466b7f8d5d9d` — Java/Spring Boot monorepo with
Maven modules, PostgreSQL (Flyway migrations), and a YAML bootstrap model registry.
Assessed components: `ai-execution-service` (single model-call service; sync
`POST /api/ai/executions` + DB-backed async job dispatcher), `humanos-ai-client`
(provider-neutral shared client), `workflow-engine/runtime-ai/gateway` (governed AI
envelope: schema, evidence/citation, confidence, autonomy, budget — strong reuse,
AUD-003). Exact toolchain versions are read from the repo when work starts
(OI-01 — this plan was authored from the handoff package, not a local checkout).

## Repo layout (target A-01 shape inside the existing monorepo)

- `humanos-ai-contracts/` — NEW versioned contract module (M02): request/result,
  route lineage, canonical failure taxonomy.
- `ai-execution-service/` — RETAINED single choke point (AUD-001): router (M09),
  registry (M07), qualification enforcement (M08), credential resolution (M05),
  lineage persistence (M10), connectors (M15).
- `endpoint-ai-runtime-broker/` — NEW managed-endpoint component extracted from the
  in-process Claude CLI adapter (M04); owns subscription-CLI/local-runtime execution.
- `humanos-ai-client/` — RETAINED caller boundary; migrated to contracts v1 (M02, M11).
- Development AI workflow assets (M12–M14): Codex read-only reviewer wrapper, Fable/Opus
  task profiles, protected-branch CI + CODEOWNERS + named-human merge gate.

## Components & data flow

caller service → `humanos-ai-client` (contracts v1) → `ai-execution-service`:
credential resolution (provider-scoped, T05) → hard eligibility filter
(policy/region/features/qualification/health, T08) → minimum-sufficient selection →
connector (Anthropic native / OpenAI native / constrained compatible) OR delegation to
the Endpoint AI Runtime Broker (T04) → result with exact route lineage (T10) →
evidence-object persistence (T06) + durable audit ledger (M18). Failures resolve through
the canonical taxonomy to fallback / human-review / no-AI terminals (T09).

## API contracts

`humanos-ai-contracts` v1 is the one wire contract (T03); the runtime gateway's governed
envelope promotes a policy-safe subset into `AIJobRequest` while the workflow runtime
keeps final validation authority (AUD-003 "reuse, do not rebuild"). Registry/catalogue
endpoints are authenticated or minimised (M17). Schemas/events are versioned with
compatibility addressed (constitution DoD-4).

## Persistence & migrations

PostgreSQL + Flyway. The raw prompt/output columns (V1 migration, AUD-018) are replaced
by minimised metadata plus encrypted classified evidence-object references (M06) via a
forward migration with retention/correction/deletion/hold tests. Mandatory audit events
ride a durable outbox with reconciliation (M18); the model-deployment registry and
qualification tables are new schema (M07, M08).

## Conventions (errors, logging, validation)

Canonical A-01 error taxonomy separates provider diagnostics from user-safe messages
(AUD-019). Logs/traces carry only approved operational metadata — never prompts, outputs
or provider error bodies (DoD-5, AUD-013). Tenant isolation: audience-scoped service
identity with purpose claims and principal reconciliation on S2S paths (AUD-016).

## Build / test / lint commands (verification-loop)

Per assessed component, from the monorepo root (confirm against the checkout — OI-01):

- Build+test one module: `mvn -pl <module> -am test`
- Full verification: `mvn verify`
- Dependency/provider scan (M11 acceptance): repository dependency scan proving no
  provider SDK/config import outside approved connector modules, plus the removal diff.
- Each module's spec names its own required evidence class (contract fixtures, negative
  routing tests, failure-injection, migration/privacy/DR tests, permission/injection
  tests, repository control tests) per the Remediation Sequence's "Required evidence".

## Build tooling

Implementer/reviewer routing per module front-matter (`model:` / `reviewer:`), executed
through the plugin's orchestrate/review loop; the programme itself also BUILDS that
separation as product (M12–M14) — the dev workflow the plan uses and the one it ships
must end up being the same thing (T11).

## Decisions (ADRs)

- **ADR-P1 (baseline)**: Retain `ai-execution-service` + `humanos-ai-client` as the
  central gateway foundation; extend in place, never build a competing orchestrator.
  Context: AUD-001/AUD-003. Consequence: all P0 work lands inside the existing modules
  except the new contracts module and the extracted endpoint broker.
- **ADR-P2 (baseline)**: The standalone router is a decision spike (REM-022), built only
  if isolation/resilience/customer-deployment needs cannot be met centrally — CTO owns
  the decision (M21, blocked-needs-decision).
- Further ADRs are recorded in `registers/decisions.md` as they are accepted.
