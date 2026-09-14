# Constitution — non-negotiables (inherited verbatim by every handoff)

## Source-of-truth hierarchy (AI Coding Handoff, master workbook)

1. Accepted ADRs and non-negotiable rules override older prompts and placeholders.
2. Stage/domain contracts define terminology, interfaces and required behaviour.
3. Repository assessment/audit/evidence sheets describe current code reality.
4. The remediation sequence and Stage 12 backlog define implementation order.
5. Gate/test sheets define completion; an AI statement or build success alone is
   insufficient.
6. Earlier stage workbooks and prompts are historical snapshots; the latest master
   workbook wins every conflict.

## Definition of done (every work package)

1. Acceptance criteria implemented and mapped to deterministic tests.
2. Required unit, contract, integration, migration, security/privacy and failure tests pass.
3. No provider, credential, tenant, evidence, review or employee-rights boundary is weakened.
4. Schemas/events are versioned and compatibility is addressed.
5. Logs/traces contain only approved operational metadata.
6. Codex blockers/majors are resolved or human-adjudicated.
7. CI passes and a named human approves the merge.
8. Workbook status/evidence/source/commit rows are updated with actual results.

## Hard boundaries (violating any of these is a stop, not a trade-off)

- No central or background workload may ever select a user's subscription CLI; endpoint
  subscription/local runtimes execute only behind the Endpoint AI Runtime Broker, and the
  central service never touches user-local OAuth (T02, T04).
- No silent material route change: tenant→platform account, provider, region, model or
  qualification substitutions are explicit, policy-checked and audited (T05, T09).
- No raw AI prompt/output persistence in domain stores; classified, encrypted
  evidence-object references only, with retention/correction/deletion/hold lineage (T06).
- Every active route names an exact model deployment (never a family/alias alone) and only
  qualified, unexpired task×effort configurations may be selected (T07, T08).
- Development AI separation of duties: Fable plans (no code writes), Opus implements
  (no self-review/merge), Codex reviews read-only (no write tools), CI plus a named human
  gate every protected merge (T11).
- AI cannot directly decide dismissal, pay, promotion, probation or discipline; AI
  unavailability never becomes employee failure (T12, T09).
- The Stage 12A hardening gate passes before any real employee pilot (T13).

## Planning method (spec-driven-planning)

- Provenance before assertion; never invent a domain, provider or regulatory fact — no
  dated source means an open-item, not a guess.
- The trigger checklist beats the label; default to the higher tier.
- Modular by construction: single responsibility, interface-only interaction, acyclic
  dependencies, independently testable, agent-sized units.
- Status lives only in module front-matter; board/index/traceability are derived and
  regenerated, never hand-edited.
- Reconcile after every build wave; a Tier-0 module is not `implementation-verified`
  without a recorded independent dual-review verdict.
- A green lint is a structural check, never a compliance verdict.
