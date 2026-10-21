# WI Execution Pipeline: the missing backend functionality (2026-10-19)

Companion to `WI-Execution-Pipeline-Requirements.md` and `WI-Execution-Pipeline-Status-2026-10-16.md`.
Every citation is `file:line` in the checkouts on this machine as of today:

| short name | checkout | repo / branch |
|---|---|---|
| Orchestration | `D:\intelligence\orchestration-wi-mvp` | `Rapidtackltd/humanos-ai-orchestration`, worktree of `D:\codex-plan\humanos-ai-orchestration` (main) |
| Engine | `D:\intelligence\engine-wi-mvp` (the running jar's source, HEAD `efa3c5d`) | `Rapidtackltd/workflow-engine` |
| Workers | `D:\humanos-console\tools\` (`gate1-worker.py`, `real-worker.py`) | `Rapidtackltd/humanos-console`, branch `gate2-console-r1-r3` (same files exist in `D:\intelligence\console-wi-mvp\tools\`) |
| Console | `D:\intelligence\console-wi-mvp` | `humanos-console`, branch `codex/wi-console-integration` |

## 0. The answer in one paragraph

The Home page in the screenshot shows **1 Completed** only because a relay script written last session
(`gate1_relay_worker.py`, living in a session scratchpad, in no repo) forwards the Engine's signed receipt to
Orchestration. In the checked-in code, the Orchestration-to-Engine conversation is **one way**: Orchestration
pushes the approved plan to the Engine and can read instance state, but the **signed completion receipt**, which
is the only fact that moves a request to `COMPLETED`, is handed by the Engine **only to the worker** that
completes the task. Nothing in Orchestration pulls it, nothing in the Engine pushes it, and the lightweight
canonical worker (`gate1-worker.py`) never forwards it. The full worker (`real-worker.py`) does forward it, but
needs the whole estate (project-service-be and friends) running. A second, silent defect makes the problem
invisible: with the default in-memory store, Orchestration's report endpoint answers `recorded: true` and
persists nothing.

## 1. How completion is designed to flow, and where it breaks

```
Orchestration                               Engine                                   Worker
-------------                               ------                                   ------
decision APPROVED + side_effect
  -> outbox row APPROVED_PENDING_DISPATCH
  -> _attempt_dispatch: POST /api/runtime/plans  ──────►  instance WAITING
     (X-Correlation-Id = request_id,                      task AVAILABLE
      app.py:2084)                                            ◄──────────────────  POST /workers/register
  -> outbox row DISPATCHED (app.py:2085)                      ◄──────────────────  POST /workers/{id}/claim
                                                              (task carries correlationId
                                                               = the request_id)
                                                                                    does the estate side effect
                                                              ◄──────────────────  POST /tasks/complete
                                                          mints HMAC receipt
                                                          (WorkerController.java:121-141)
                                                          returns it ONLY in the
                                                          CompletionResponse ──────►  receipt in worker's hands

  ◄── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──   POST /v1/capabilities/report
  verifies HMAC with HUMANOS_RECEIPT_SECRET (app.py:3136-3171)                       (real-worker.py:843 does this;
  stores capability.reports row (app.py:3268-3289)                                    gate1-worker.py NEVER does)
  execution_state() -> COMPLETED (execution_state.py:74-75)
```

The dashed arrow is the missing link. Everything above it works in the checked-in code; everything below it
exists only in `real-worker.py` (estate required) and in last session's scratchpad relay.

## 2. The gaps, exactly

### G1. The lightweight worker never reports the receipt to Orchestration  (core gap)

- `D:\humanos-console\tools\gate1-worker.py:256-266` (`complete()`): posts `/api/runtime/tasks/complete`, writes the
  returned `receipt` into its local journal, returns. `run()` at `:268-299` calls `complete()` at `:289` and moves to
  the next claim. There are **0** references to `HOS_ORCH_URL` / `/v1/capabilities/report` in the file.
- `real-worker.py` has the complete implementation: env `HOS_ORCH_URL` / `HOS_ORCH_REPORT_SECRET` (`:128-129`),
  `_report_execution()` (`:843-910`), `_post_report()` (`:749`), disk spool and retry (`:727-778`), flushed each loop
  (`:3121-3122`). It only reports completions whose Engine status is `ACCEPTED` or `RECONCILED_DUPLICATE` and
  that carry a receipt.
- The canonical launcher confirms the design intent: `orchestration-wi-mvp/tools/estate-local/start-gate1-stack.sh:250-290`
  runs `real-worker.py` with `HOS_ORCH_URL`/`HOS_ORCH_REPORT_SECRET` exported, and keeps `gate1-worker.py` only behind
  `GATE1_WORKER_MODE=gate1` with no report wiring at all (`:292-294`).
- Proof that this is the whole missing piece: last session's `gate1_relay_worker.py` is `gate1-worker.py` plus
  `build_report()` / `relay()` / `spool()` / `flush_spool()` / the tail of `handle()` (relay script lines 123-240), and
  with it the request `b091ae17…` reached `COMPLETED` with receipt `58934a78…`.

### G2. Orchestration never pulls completion from the Engine  (by design, but worth knowing)

- The startup reconcile loop `orchestration-wi-mvp/src/humanos_ai/gateway/app.py:4280-4315` only re-submits
  `dispatch_outbox.pending()` rows (`:4304`). A `DISPATCHED` row is never visited again.
- The one server-side Engine read, `_engine_truth()` (`app.py:2156-2185`, via `WorkflowRuntimeClient.get_instance`,
  `integration/runtime_client.py:246-250`), runs only when `_engine_truth_needed()` (`app.py:2149-2154`) is true,
  which requires a **FAILED** report to already exist. It is a failure-disposition read, not a completion poll.
- Even if it polled, `engine_truth_from_instance()` (`outbox/engine_truth.py:46-84`) projects only
  `state / terminal / retry_owed / failure_*`; `execution_state()` reaches `COMPLETED` **only** from a `SUCCEEDED`
  report in `capability.reports` (`outbox/execution_state.py:68, 74-75`). Engine `COMPLETED` alone is treated as
  "acceptance is not completion" (`execution_state.py:114-116`). That is the receipt-bound evidence rule from the
  requirements doc, not a bug.

### G3. The Engine has no outbound completion channel

- The receipt is minted in `engine-wi-mvp/runtime-service/.../web/WorkerController.java:121-141` (`receiptFor`) and
  returned only inside `Api.CompletionResponse` (`Api.java:99-106`) to the caller of `POST /api/runtime/tasks/complete`
  (`WorkerController.java:98`).
- `GET /api/runtime/instances/{id}` (`InstanceController.java:58-62`) returns `Api.InstanceResponse` (`Api.java:22-25`):
  instance state, nodes, actor envelope. **No receipt, no signature.** No other read endpoint exposes receipts
  (full endpoint list: Capability, Definition, Event, Instance, Plan, Worker, Operations, Migration controllers).
- `RuntimeProperties.java:13-163` has no callback / report URL field. The transactional `EventOutbox`
  (`runtime-events/outbox/.../EventOutbox.java`) is instantiated (`config/RuntimeBeans.java:101`) but **no `Broker`
  implementation exists and nothing calls `publishBatch()`** outside tests; the only `@Scheduled` job is the lease
  sweeper (`operations/LeaseSweepDriver.java:94`). The outbox is inert.

### G4. The report endpoint silently succeeds without a durable store  (hides G1 completely)

- `app.py:3268-3296`: `st = container.module_store; if st is not None: <store + health atomically> ... ; _apply_health();
  return {"recorded": True, ...}`. When `module_store` is `None` the worker gets `recorded: true` and the receipt is
  dropped.
- `module_store` is `None` whenever `HUMANOS_DATABASE_URL` is unset or contains `:memory:`
  (`persistence/docstore.py:313-328`, default `sqlite+pysqlite:///:memory:` at `config.py:26`). `_reports_for()`
  (`app.py:2122-2129`) then returns `[]` for ever, and the tile stays `DISPATCHED`.
- `config.py:163-210` validates the seam (enabled, url, secret, receipt secret, R != S) but only in production, and
  never ties "seam enabled" to "durable store present". Last session this cost a full investigation; the fix last
  time was configuration (`HUMANOS_DATABASE_URL` pointed at a SQLite file).

### G5. Capability descriptors must be registered by hand  (operational gap)

- Before submitting, the dispatcher asks the Engine whether the capability is bindable for the tenant
  (`runtime_client.py:126-154`, `GET /api/runtime/capabilities/{id}?version=`). A fresh Engine DB has an empty
  `capability_descriptor` table, so every approval becomes `REJECTED` -> `MANUAL_REMEDIATION`
  (`execution_state.py:79-85`).
- Registration exists only as an operator script (`D:\humanos-console\tools\register-capabilities.py`, client method
  `runtime_client.py:112-124`). Nothing registers on startup or on package install, and nothing on the Console warns
  *before* approval that the capability is not bindable.

### G6. Estate reads are not connected  (the yellow banners in the screenshot; separate from dispatch)

- `HomeView.tsx:209` and `:310` render "estate is not connected" when `GET /v1/estate/status` answers
  `configured: false` (`gateway/estate_routes.py:77-81`), which is simply `estate_gateway_url` unset
  (`config.py:68`). The read client (`integration/estate_client.py`) expects the estate **api-gateway** in front of
  project-service-be / crm / person, called with the user's own IAM bearer. This needs the estate services built and
  running (prompt P1 in the status doc), then one env var. It does not affect Completed / Evidence.

## 3. The contract any implementation must honour

`POST {orchestration}/v1/capabilities/report` (`app.py:3096-3296`), header `X-Service-Secret` =
`HUMANOS_WORKFLOW_RUNTIME_SECRET` (the S secret; `:3109-3111`). Body:

```json
{
  "tenant_id":     "<tenant uuid>",
  "capability_id": "project.create",
  "request_id":    "<task.correlationId>",      // = the capability request id (app.py:2084); or omit and use
  "instance_id":   "<task.instanceId>",         //   instance_id, the endpoint binds on either (:3116-3124)
  "receipt":       { ...verbatim CompletionReceipt from /tasks/complete... },
  "ok":            true,                        // MUST equal receipt.success && receipt.status=="SUCCEEDED" (:3174-3178)
  "detail":        "<=300 chars",
  "provenance":    { "worker_id", "service_identity", "environment", "trace_id", "correlation_id",
                     "capability_version", "idempotency_key", "estate": { "service", "method", "route",
                     "id", "key", "applied", ... <=12 scalars } }      // optional, whitelisted (:3218-3262)
}
```

Gates the endpoint applies, in order: secret (403) -> known dispatch for the tenant (422) -> dispatch state is
`DISPATCHED` (409) -> capability is in the dispatched plan (422) -> `HUMANOS_RECEIPT_SECRET` configured (503) ->
receipt present (422) -> `receipt.status` in `SUCCEEDED|FAILED` (409) -> tenant/capability match (422) ->
HMAC-SHA256 over `tenant|taskId|capabilityId|attempt|status|success|idempotencyKey|completedAtEpochMs` with Java
`String.valueOf` semantics (`null` -> `"null"`, booleans lowercase) using the **receipt** secret (`:3153-3171`,
mirrors `WorkerController.java:133-137`) -> `ok` agrees with the receipt -> idempotent on `task_id#attempt`
(duplicate -> `recorded:false, duplicate:true`; contradiction -> 409) (`:3271-3289`).

Receipt shape (`Api.java:99-101`): `tenantId, taskId, capabilityId, attempt, status, success, idempotencyKey,
completedAtEpochMs, signature`. The Engine returns **no** receipt for `REJECTED_*` completions
(`WorkerController.java:124-130`); those are not evidence and must not be reported.

The worker never holds the receipt secret. It relays the receipt verbatim; Orchestration re-verifies.

## 4. Options and recommendation

| option | what changes | repos touched | verdict |
|---|---|---|---|
| **A. Worker relays the receipt** (port the relay into `gate1-worker.py`, optional via `HOS_ORCH_URL`) | ~120 lines in one Python file, mirrors what `real-worker.py` already does | humanos-console | **Do this.** It is the designed contract; the Orchestration endpoint calls itself the "worker/Engine completion callback" (`app.py:3098`). |
| **B. Fail closed in the report endpoint** when there is no durable store (503 "evidence store not configured") and refuse to start with the seam ON and an in-memory store | ~15 lines in `app.py:3268-3296` + a validator in `config.py:163-210` + tests | humanos-ai-orchestration | **Do this with A.** Without it a misconfigured stack reports success while dropping evidence. |
| C. Orchestration pulls completion from the Engine | reconcile loop visits `DISPATCHED` rows, calls `get_instance`; but no receipt is readable, so the Engine must also expose receipts (new `GET /api/runtime/instances/{id}/receipts` or a field on `InstanceResponse`) | workflow-engine + humanos-ai-orchestration | Later, as resilience against a worker dying between `complete` and `report`. Two repos, Engine API change. |
| D. Engine pushes via its EventOutbox | implement a `Broker` that posts to `/v1/capabilities/report`, a scheduled publisher, and `RUNTIME_ORCHESTRATION_URL` + secret config | workflow-engine | Most work, gives the Engine a new outbound dependency. Not needed for the pilot. |
| E. Register descriptors automatically | on Orchestration startup (or package install) call `register_capability` for the tenant's certified package capabilities, and surface "not bindable" on the Console before approval | humanos-ai-orchestration | Operational; schedule after A+B. |
| F. Connect estate reads | build/run estate services + api-gateway, set `HUMANOS_ESTATE_GATEWAY_URL` | none (config) + P1 from the status doc | Separate workstream; clears the yellow banners. |

## 5. Constraints that apply to every option

- The checkouts `D:\intelligence\orchestration-wi-mvp`, `D:\intelligence\engine-wi-mvp`,
  `D:\codex-plan\humanos-ai-orchestration` and `D:\humanos-native-runtime` are **read-only references**. Implementation
  goes on a fresh branch of the owning repo (table at the top), through its own tests and a human-gated merge
  (constitution T11: Opus implements, Codex reviews read-only, a named human merges).
- No simulated evidence: a receipt is only ever the one the Engine minted on `/tasks/complete`. Never hand-craft,
  re-sign or alter one.
- Secrets live in env files loaded by launchers, never on a command line, never printed. The worker holds S, never R.
- Two-person rule stays: proposer != approver. Do not set `HUMANOS_ALLOW_SELF_APPROVAL` to get past a test.
- Label what was executed: a `gate1_estate` row is not a project in project-service-be; provenance must say so.

## 6. Ready-to-paste prompts

### Prompt A: receipt relay in the lightweight worker (humanos-console)

> In `Rapidtackltd/humanos-console`, on a new branch from `gate2-console-r1-r3`, extend `tools/gate1-worker.py` so that
> after `complete()` returns an Engine `CompletionResponse` whose `status` is `ACCEPTED` or `RECONCILED_DUPLICATE`
> **and** which carries a `receipt`, the worker posts an execution report to Orchestration, exactly as
> `tools/real-worker.py` does in `_report_execution` / `_post_report` / `_spool_report` / `_flush_report_spool`
> (lines 727-910). Reporting is enabled only when `HOS_ORCH_URL` and `HOS_ORCH_REPORT_SECRET` are both set; with
> either unset the worker behaves exactly as today. Contract: `POST {HOS_ORCH_URL}/v1/capabilities/report`, header
> `X-Service-Secret: $HOS_ORCH_REPORT_SECRET`, body `{tenant_id, capability_id, request_id = task.correlationId
> (omit if empty), instance_id = task.instanceId, receipt = the Engine receipt verbatim, ok = receipt.success &&
> receipt.status == "SUCCEEDED", detail <= 300 chars, provenance = {worker_id, service_identity:"gate1-worker",
> environment: $HOS_ENV, trace_id, correlation_id, capability_version, idempotency_key, estate: {service:
> "gate1_estate", method:"INSERT", route:"gate1_estate_record", id: <row id>, key: <idempotency key>, applied:
> "INSERT"|"DUPLICATE"|"NONE", note:"local PostgreSQL table, not a HumanOS vertical service"}}}`. Delivery failures
> (5xx / connection) append the report to `HOS_REPORT_SPOOL` (default `gate1-report-spool.jsonl` beside the journal)
> and are retried at the top of every loop iteration; any 4xx is final (duplicate or refused) and leaves the spool.
> Never modify or re-sign the receipt. Journal `report-relayed`, `report-spooled`, `report-relayed-from-spool`,
> `no-receipt` events with `instanceId` and `requestId` (never the secret). Add unit tests next to
> `tools/tests/test_real_worker_*.py` with a fake Orchestration (`http.server` or `unittest.mock`) covering: no env ->
> no call; ACCEPTED+receipt -> one POST with the exact body; REJECTED_BAD_LEASE -> no POST and a `no-receipt` journal
> line; 503 from Orchestration -> spooled then delivered on the next loop; 409 -> dropped from the spool. Update the
> header docstring and `tools/estate-local` docs that describe gate1 mode. Do not touch `real-worker.py`.
> Reference implementation that already proved the path on this machine:
> `C:\Users\Admin\AppData\Local\Temp\claude\D--intelligence\72e30c0c-29d9-406d-950a-bb5ca2258f7b\scratchpad\wi-stack\gate1_relay_worker.py`
> (lines 123-240); port its logic, not its hard-coded strings. Acceptance: with the local stack from
> `WI-Execution-Pipeline-Status-2026-10-16.md` §5 (stop the relay worker first, run the new `gate1-worker.py` with
> `HOS_ORCH_URL=http://127.0.0.1:8099` and `HOS_ORCH_REPORT_SECRET` = S), `e2e_drive.py` reaches
> `state=COMPLETED` with `receipt_signature` set and `estate_provenance.service == "gate1_estate"`, and the Console
> Evidence row shows the signed report.

### Prompt B: fail closed when evidence cannot be stored (humanos-ai-orchestration)

> In `Rapidtackltd/humanos-ai-orchestration`, on a new branch from `main`: (1) in
> `src/humanos_ai/gateway/app.py` `capability_report` (the `/v1/capabilities/report` handler, around lines
> 3268-3296), when `container.module_store is None` raise `HTTPException(503, "execution evidence cannot be
> recorded: HUMANOS_DATABASE_URL is in-memory; configure a durable store")` **before** verifying anything, and
> remove the trailing non-durable `_apply_health(); return {"recorded": True}` path so the endpoint can never
> answer `recorded: true` without a stored row. (2) In `src/humanos_ai/config.py` `Settings` validation (the block
> at lines 163-210), add: when `workflow_runtime_enabled` is true and `database_url` is unset or contains
> `:memory:`, raise `ValueError("HUMANOS_WORKFLOW_RUNTIME_ENABLED=true requires a durable HUMANOS_DATABASE_URL
> (sqlite file or PostgreSQL): completion receipts cannot be recorded in memory")`, in every environment, not only
> production. (3) Surface the same fact on `/v1/dispatch/outbox` and the health board as an operator-attention
> item (`evidence_store: "in-memory"`), reusing the existing alert pattern. (4) Tests: a report posted to an app
> built with the in-memory store returns 503 and records nothing; `Settings(workflow_runtime_enabled=True,
> workflow_runtime_url=..., database_url="sqlite+pysqlite:///:memory:")` raises; a SQLite-file store still records
> and dedupes exactly as `tests/test_round5_probes.py` and `tests/test_codex_f10_evidence.py` expect. Keep the
> dedicated-receipt-secret and R != S rules untouched. Document the new rule in `docs/SEAM.md` next to the
> configuration table.

### Prompt C (later): Orchestration pulls completion as a resilience path

> Two changes, two repos, only after A and B are merged. Engine (`Rapidtackltd/workflow-engine`): persist the
> `CompletionReceipt` minted in `WorkerController.receiptFor` per `(tenant, taskId, attempt)` and expose it on
> `GET /api/runtime/instances/{id}/receipts` under the existing service-secret gate; receipts are immutable and
> byte-identical to what the worker received. Orchestration: in the startup reconcile loop
> (`app.py:4280-4315`) also visit `DISPATCHED` outbox rows with no `SUCCEEDED`/`FAILED` report older than N
> seconds, call the new endpoint through `WorkflowRuntimeClient`, and feed each receipt through the **same**
> verification and recording code as `/v1/capabilities/report` (factor the gate chain into one function so pull and
> push cannot diverge). Provenance for pulled receipts says `source: "engine-pull"`. Acceptance: kill the worker
> between `/tasks/complete` and the report and the request still reaches `COMPLETED` within one reconcile cycle.

### Prompt D: register descriptors automatically and warn before approval

> In `humanos-ai-orchestration`: on startup, and whenever a vertical package is installed or certified, call
> `WorkflowRuntimeClient.register_capability` for every certified capability of the package for that tenant
> (idempotent: the Engine version-locks rows). In the Console's Approvals view, read the existing bindability
> probe (`descriptor_status`) and show "this capability is not bindable at the Engine for this tenant" on the
> request before the approve button, so a countersigner never approves into `MANUAL_REMEDIATION`. Tests with the
> `httpx.MockTransport` pattern already used for the runtime client.

## 7. How to prove it afterwards

1. Start Engine -> (register descriptors once) -> Orchestration (durable store) -> the new `gate1-worker.py` with
   `HOS_ORCH_*` set. `check_stack.py` passes.
2. `e2e_drive.py`: propose as `wi.admin`, countersign as the reviewer, watch `/execution` go
   `QUEUED -> DISPATCHED -> COMPLETED` with `evidence.receipt_signature` 64 hex and
   `evidence.estate_provenance.service == "gate1_estate"`.
3. Negative: start Orchestration with the in-memory store and the seam ON; it must refuse to start (Prompt B).
   Start it with a durable store but post a report with a tampered signature; expect 403 and no row.
4. Console, signed in as `wi.admin`: Home shows the request under Completed; Evidence shows the dispatch, the
   estate record and the Engine-signed report, provenance worker `gate1-worker-1`.
