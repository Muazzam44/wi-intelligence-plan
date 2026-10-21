# Scenario: "give me an algorithm of bubble sort" → Opus writes it → Codex and Sonnet review it (2026-10-19)

Companion to `WI-Execution-Missing-Backend-2026-10-19.md` (the dispatcher/receipt gap, Prompts A and B now on branches).
Citations are `file:line` in the checkouts on this machine. Everything in section 1 was **verified today by running it**; section 2 is read from code.

## 0. The answer in one paragraph

The governed half already works end to end on this machine: Aide turns a request for code into a pending
`code.generate` capability request (proved today, request `4c5b0038…`), a second person countersigns, the Engine
dispatches, a worker executes and the signed receipt reaches the Console. What does **not** exist is everything
the scenario adds on top: (a) the lightweight worker does not generate code at all, and the full worker generates
it through an assistant service that cannot pin a model, so "Opus" is not a choice anyone makes or records;
(b) there is **no review step** in the governed path at all, by any model; (c) Orchestration owns an adversarial
review service and an LLM council that could do the reviewing, but they are API-only and have **no model adapters
wired**; (d) Codex exists on this machine as a CLI with a manifest in Orchestration but no execution profile, no
readiness/pinning and no approval record, while the constitution forbids a central service from using a user's
subscription CLI except through a broker that does not exist in the code. The Claude CLI profile is the one
CEO-approved exception. So the work is: a model-pinned generation path, a new `code.review` capability executed
by two distinct models, evidence for all three results, and a decision on how Codex is reached.

## 1. What exists today, verified by running it

| step | what happened | evidence |
|---|---|---|
| Aide → planner | `POST /v1/orchestration/propose` as wi.admin, `{"message": "give me an algorithm of bubble sort", "domain": "PROJECT_MANAGEMENT"}` → **HTTP 200 in 8.1 s, `proposed: false`, `action_state: CHAT`**: the planner answered the question directly, nothing governed was proposed | probe `aide_probe.py` (scratchpad) |
| Aide → proposal | same call with `"write a Python implementation of the bubble sort algorithm as a script"` → **`proposed: true`, `action_state: PROPOSED_FOR_COUNTERSIGN`**, capability `code.generate`, contract `1.0.0`, payload `{work_package, language: Python}`, `side_effect: true`, `approval_required: true`, state **PENDING**, request id `4c5b0038-ab87-45a0-9a0a-4a1bb80fcb07` (visible in the Console under Approvals now) | same probe, 5.6 s |
| which model planned | the `claude.cli` execution profile: a `MODEL_CALL` ledger row with `task_profile_id = claude.cli` and a route decision id | `orch-state.db` namespaces `budget.ledger`, `agent.plans`; profile registered at `container.py:161`; adapter `adapters/claude_cli.py` (pinned CLI `2.1.144`, the version installed) |
| approve → dispatch → Engine → worker → receipt → COMPLETED | proved on 2026-10-16/19 for `project.create` (requests `b091ae17…`, `7f867b43…`) | `WI-Execution-Pipeline-Status-2026-10-16.md`; branch `gate2-worker-receipt-relay` |
| models reachable right now | `business-hub-ai-execution` container on :8092 (image `business-hub/ai-execution-service:phase5`, `ANTHROPIC_API_KEY` present) lists **`claude-sonnet-4-6`, `claude-opus-4-7`, `claude-haiku-4-5`** (provider anthropic) and `moonshot-v1-128k` (provider openai); `POST /api/ai/executions` accepts `preferredModel` | `GET /api/ai/models`; `hbs-work/ai-execution-service/.../ExecutionController.java:67-70` |
| CLIs installed | `claude 2.1.144`, `codex-cli 0.162.1`; no `gemini` | `command -v` |
| services NOT running | ai-assistant-service (:8091, jar built at `hbs-work/ai-assistant-service/.../target/ai-assistant-service-1.0.0-SNAPSHOT.jar`), the hbs-work build of ai-execution-service (the running one is the business-hub image) | `netstat` |

## 2. How the scenario would flow through the code today, and where it stops

```
"write ... bubble sort"            intent_planner.py:230-241  menu rule: WRITE/GENERATE CODE → code.generate
  → PENDING capability request      app.py:1329 (propose), critic.py (deterministic checks only, no LLM review)
  → countersign (2nd person)        unchanged
  → dispatch (one action per request)   app.py:2084; actions_from_capability_requests runtime_client.py:265-283
  → Engine: nodes start/a0/end      GovernedPlanExecutor.java:56 runs actions IN LIST ORDER; no output is passed
                                     from one action to the next
  → worker claims code.generate
       gate1-worker.py:270 execute() → INSERTs a gate1_estate row. NO CODE IS GENERATED.         ← stop 1
       real-worker.py:1353 do_code_generate → do_agent_execute (:1285) → ai-assistant-service
         POST /api/ai/conversations/{id}/agent-turn   body = {message, projectId}  (AgentController.java:120-125)
         → AiExecutionClient.java:91 taskType=CHAT / :127 PM_ORCHESTRATION, NO preferredModel     ← stop 2
         → ai-execution-service picks the task-type default model; the answering modelId is not
           carried back into the worker's output (do_agent_execute returns turn text only)        ← stop 3
  → receipt + ONE artifact {content ≤64k, sha256, draft_only}  app.py:3183-3216; Console shows it as
     "Draft artifact" (EvidenceView.tsx:133-139)
  → nothing reviews the artifact                                                                   ← stop 4
```

## 3. The gaps, exactly

### G1. Intent: "give me an algorithm" is answered as chat, not proposed
`orchestration/intent_planner.py:230-241` proposes `code.generate` only when the user asks to *write/generate code,
a script, or an implementation*. "Give me an algorithm of X" is treated as a question (verified). Decision: accept
that phrasing matters, or widen the menu rule (`when`) so algorithm/implementation requests propose.

### G2. The lightweight worker never generates code
`gate1-worker.py` lists `code.generate` among its capabilities (`:76`) but `execute()` (`:270`) writes a
`gate1_estate_record` row for every capability. Approving `4c5b0038…` today would mark it COMPLETED with a row and
no code. Only `real-worker.py:1353` generates, and only via ai-assistant-service, which is not running.

### G3. Nobody chooses, or records, the generating model
- `code.generate`'s contract has `work_package, repository, language` (`capabilities/platform_contracts.py:92`): no
  model field, no route.
- The assistant's turn request carries `message` and `projectId` only (`AgentController.java:120-125`); its client
  never sends `preferredModel` (`AiExecutionClient.java:86-135`).
- The worker's output has no `modelId` (`real-worker.py:1285-1350`), and the report endpoint's provenance whitelist
  (`app.py:3218-3230`) has no model field, so even a known model could not become evidence.
- Constitution T07 requires every active route to name an exact model deployment; the planner side already does
  this through `route_decisions` for `claude.cli`, the execution side does not.

### G4. No review stage in the governed path
- There is no `code.review` capability in `platform_contracts.py` (`review.submit` at `real-worker.py:1195` is a
  customer star-rating into review-service, unrelated).
- One capability request becomes one plan action; a plan with several actions runs them in order but passes no
  output between them (`GovernedPlanExecutor.java:56`), so a review action cannot receive the draft from the Engine.
  It must fetch the stored artifact from Orchestration (`GET /v1/domain/capability-requests/{id}/execution`
  returns it, `app.py:2255`) or be proposed as a follow-up request bound to the generation's receipt.
- The pre-approval critic (`agent_runtime/critic.py`) is deterministic (allowlist, autonomy, secrets, bounded
  plan); it reviews the *proposal*, never the *output*.

### G5. The review engines exist, but are unwired and API-only
- `sdlc/verification.py:173-274` `AdversarialReviewService` (SVC-051): runs a secondary-model critique of an
  artefact, refuses a reviewer equal to the author (`:225-228`), records `author_model`, `reviewer_model`,
  `verdict` durably.
- `sdlc/council.py` (WF-008 LLM council): seats resolved from the tenant menu, refuses a panel that resolves to one
  model (`:468-479`), executes answers/critiques/synthesis per seat through a `ModelAdapter`.
- Both are mounted (`app.py:4399-4408`) under `/v1/sdlc/...` but the adapter map is **empty by default**
  (`council.py:391`); no class implements `sdlc/modeladapters.py:71 ModelAdapter` anywhere in `src`, and the
  container wires adapters only for the orchestrator's profiles (`container.py:139`: mock, no-model,
  openai-compatible, claude.cli). The Console has no SDLC surface (`docs/sdlc-truth-audit.md` §0.2).

### G6. Codex is installed but not a governed route
- `cli_adapters/official.py:3` has a Codex manifest (`codex exec -`, stdin, **no JSON output**, 600 s), used by
  nothing. There is no `ExecutionProfile`/`ProfileKind` for Codex, no pinned version, no readiness probe, no
  allowlisted child environment, none of what `adapters/claude_cli.py` does for Claude.
- Constitution T02/T04: no central or background workload may select a user's subscription CLI; such CLIs run only
  behind the Endpoint AI Runtime Broker. No such broker exists in the code (grep: nothing). The Claude CLI profile
  is allowed because the CEO approved it for this release with an evidence file
  (`docs/gate1-claude-cli-production-evidence.md`). Codex via CLI needs the same approval and the same adapter
  discipline, or it must be reached through an API key in ai-execution-service's OpenAI-compatible provider
  (`hbs-work/ai-execution-service/.../application.yml:61-66`, currently pointed at Moonshot).

### G7. Evidence shape
A completion carries one artifact. Three results (draft, review 1, review 2) need either three receipts (three
capability tasks, the clean option) or an extended artifact schema. The Console renders only "Draft artifact".

### G8. Side facts
- The Engine's own AI path (`AiTaskExecutor`, `RuntimeProperties.java:104`) pins `claude-cli-sonnet`, a model id the
  running ai-execution does not list. Irrelevant to the worker path, but it would fail if used.
- The planner itself spends the user's Claude CLI subscription on every Aide message (`claude.cli` profile).

## 4. Options

| option | shape | verdict |
|---|---|---|
| **1. Three governed tasks, worker calls ai-execution directly** | planner proposes a `project.codegen_reviewed` run that yields three capability requests: `code.generate` (model `claude-opus-4-7`), `code.review` (reviewer 1), `code.review` (reviewer 2), reviews bound to the generation's request id; the worker's handlers call `POST /api/ai/executions` with `preferredModel` and put `modelId` + `executionId` in provenance; each result is its own signed receipt + artifact | **Recommended.** Reuses every proven piece (approval, dispatch, receipt, artifact, Evidence); every model is named per call; no new service; review results are independent evidence. |
| 2. Worker calls the SDLC adversarial review service | after generating, the worker posts the draft to `/v1/sdlc/reviews/adversarial` twice | Needs ModelAdapters wired and a bearer for an S2S caller; the review record lives outside the capability evidence; still API-only. Later, if the SDLC module becomes the product. |
| 3. One task does all three inside ai-execution-service | a "reviewed generation" task type chains Opus → reviewers | Hides the reviews behind one receipt, one route decision: breaks "no silent route change" and per-model evidence. Not recommended. |

Codex route (independent of the option): **CLI** = write a `codex.cli` profile with the same discipline as
`adapters/claude_cli.py` plus an approval record like the Claude one (constitution T02/T04); **API** = configure
ai-execution's OpenAI-compatible provider with an OpenAI key and a codex-class model id, then it is just another
`preferredModel`. The API route needs no constitutional exception; the CLI route needs a human approval first.

## 5. Decisions you need to make

1. Phrasing: keep "write/generate" as the trigger, or make "give me an algorithm" propose too (G1).
2. Codex via CLI (approval needed) or via OpenAI API in ai-execution-service (G6).
3. Whether a review verdict can **fail** the run (blocking) or is advisory evidence only. Advisory is the safe
   first step; blocking needs the Engine to see the verdict, which it cannot today.
4. Run the hbs-work ai-execution-service locally (has the `claude-cli` model, subscription) or keep using the
   business-hub container on :8092 (API models, key already present).

## 6. Ready-to-paste prompts (assumes Option 1, API route for Codex, advisory reviews)

### Prompt C1: contract + planner (humanos-ai-orchestration)

> On a new branch from `main` in `D:\codex-plan\humanos-ai-orchestration`: (1) in `capabilities/platform_contracts.py`
> add a `code.review` capability (package `humanos.project`, class COMPUTE, reversible, autonomy A0/A1) with input
> `{subject_request_id, artifact_sha256, reviewer_model, rubric?}` and bump nothing else; add an optional `model`
> field to `code.generate`'s input. (2) In `orchestration/intent_planner.py` add a menu action
> `project.codegen_reviewed` ("the user asks for code and wants it reviewed, or asks for an algorithm/implementation
> to be produced") whose domain agent (`domain_agents/project.py`) creates THREE capability requests in one run:
> `code.generate` with `model: claude-opus-4-7`, then two `code.review` with `reviewer_model` taken from a new
> setting `HUMANOS_CODE_REVIEWERS` (default `claude-sonnet-4-6,<openai codex model id>`), each review carrying the
> generation's `request_id` as `subject_request_id`; refuse a reviewer equal to the author model (mirror
> `sdlc/verification.py:225-228`). (3) In `gateway/app.py` extend the report provenance whitelist (`:3218-3230`)
> with `author_model`, `reviewer_model`, `model_execution_id`, `verdict`, and let a `code.review` report be bound
> to its own dispatch while naming `subject_request_id`. (4) Register the new descriptor through the same
> registration path Prompt D added. Tests: planner proposes three PENDING requests with the right bindings; a
> review whose reviewer equals the author is refused at proposal; provenance fields survive to `/execution`.

### Prompt C2: worker handlers (humanos-console, tools)

> On a new branch from `gate2-worker-receipt-relay` in `D:\humanos-console`: in `tools/gate1-worker.py` (or a new
> `tools/codegen-worker.py` that reuses its register/claim/complete/relay code) add two handlers. `code.generate`:
> call `POST {AI_EXECUTION_URL}/api/ai/executions` with `taskType` from `AI_EXECUTION_TASK_TYPE` (default `CHAT`),
> `preferredModel` = the task input's `model` (refuse the task with POLICY_DENIED if absent: no silent default),
> the framed prompt from `real-worker.py:1360-1362`, trust headers as `real-worker.py` sends them; output =
> `{artifact: {content, chars, sha256, sha256_of: full_draft, draft_only: true, language}, model_id, execution_id}`;
> provenance `{author_model: <modelId from the response>, model_execution_id}`. `code.review`: fetch the subject's
> stored artifact via `GET {HOS_ORCH_URL}/v1/domain/capability-requests/{subject_request_id}/execution` (service
> secret), verify its sha256 equals the task's `artifact_sha256` (refuse otherwise), call ai-execution with
> `preferredModel = reviewer_model` and a fixed review rubric that asks for `{verdict: PASS|FAIL|NEEDS_CHANGES,
> findings: [...]}` as JSON; output the review as an artifact plus provenance `{reviewer_model, verdict,
> model_execution_id, subject_request_id}`. Never execute generated code. Tests with a fake ai-execution and a fake
> Orchestration: model pin sent verbatim, missing model refused, sha mismatch refused, review JSON parsed, both
> provenance blocks relayed. Env names documented in the header; `AI_EXECUTION_URL` defaults to
> `http://127.0.0.1:8092`.

### Prompt C3: Console evidence (humanos-console, branch `codex/wi-console-integration`)

> In `src/views/EvidenceView.tsx` and the Approvals view: render `code.review` completions as "Review by
> <reviewer_model>: <verdict>" with the findings artifact collapsible, grouped under the generation they reviewed
> (`provenance.subject_request_id`); show `author_model` on the draft; show the three-request run as one card with
> three states. No new API: everything comes from `/v1/domain/capability-requests/{id}/execution` and the outbox.

### Prompt C4: Codex route (one of the two)

> API: in the ai-execution-service deployment used locally, set the OpenAI-compatible provider to an OpenAI key and
> register a codex-class model id in the model registry; prove `POST /api/ai/executions` with `preferredModel` set
> to it answers and reports `modelId`. Secrets in env files only.
> CLI (needs a human approval first): add `ProfileKind.CODEX_CLI` and `adapters/codex_cli.py` modelled line by line
> on `adapters/claude_cli.py` (pinned version `0.162.1`, readiness probe, allowlisted child env, non-interactive
> `codex exec -`, distinct outcome exceptions), register profile `codex.cli` with capability `review`, and write
> `docs/gate1-codex-cli-evidence.md` in the format of the Claude one. Do not route any task to it until the
> approval record exists.

## 7. Proof when it is built

Signed in as wi.admin: Aide "write a Python implementation of bubble sort and have it reviewed" → Approvals shows
three pending requests → reviewer countersigns all three → Evidence shows: draft by `claude-opus-4-7` (receipt,
artifact), review by `claude-sonnet-4-6` (receipt, verdict, findings), review by the Codex route (receipt,
verdict, findings), each with its own Engine-signed receipt and model execution id. The request `4c5b0038…` raised
today can be the first subject once the generate handler exists.
