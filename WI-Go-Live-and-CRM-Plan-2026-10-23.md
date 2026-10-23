# Go-live plan: the governed pipeline on the live environment, and the live CRM (23 Oct 2026)

Two parts. Part 1 puts what was proved locally this month on the live environment. Part 2 connects it to the
CRM that is already live. Every step names the file or setting it touches; nothing here is invented.

## What already exists on the live environment (verified from the deploy workflows and compose files)

| piece | where | state |
|---|---|---|
| Backend host (`backend-vps` runner) | `/opt/humanos` with side-by-side checkouts of `humanos-console`, `humanos-ai-orchestration`, `workflow-engine`; one host PostgreSQL | runs compose project `humanos-workflow` from `humanos-console/deploy/docker-compose.humanos.yml` + `/opt/humanos/docker-compose.override.yml`, env in `/opt/humanos/.env` |
| Services in that compose | `runtime` (Engine, 127.0.0.1:8085), `orchestrator` (127.0.0.1:8099), `worker` (demo), `real-worker` (estate executor, readiness on :8410), and `work-intelligence` in the production variant | localhost-only; Plesk nginx fronts them |
| Deploy automation | push to `main` → `Rapidtackltd/ci-shared docker-service-deploy` rebuilds `orchestrator`, waits for `/health`, stamps `HUMANOS_BUILD_SHA`, runs the 25-case E2E matrix as the gate | triggered on 21 Oct by the merge to `main` (6b69ec8); result not yet checked |
| Console | Plesk static site `console.nessovo.com`, deployed from `main` by `static-site-deploy` | triggered on 21 Oct (193175e); result not yet checked |
| Estate (CRM, projects, IAM, gateway, AI execution) | the `humanos-backend-services` production compose on the same host, docker network `microservices-human-os_humanos`; public fronts `crm.nessovo.com`, `pm.nessovo.com`, `dev.nessovo.com` (gateway / IAM), `human-os.nessovo.com` | live today; the `real-worker` service joins that network by name |
| Model access on the host | runbook `deploy/CLAUDE-CLI-PROVISIONING.md`: a dedicated Claude identity logged in by an operator, token in `.env`, or `ANTHROPIC_API_KEY` ("production footing") | Codex is not provisioned anywhere outside this laptop |

## Part 1 — Put the pipeline live

### 1.1 Check what the 21 October push did (first, before anything else)
- Open the two GitHub Actions runs (orchestration `deploy.yml`, console `deploy.yml`). The orchestration gate is the line `E2E MATRIX: 25/25 PASS`.
- Expected risk: the new code **refuses to boot with the seam on and no durable `HUMANOS_DATABASE_URL`** (the fail-closed rule shipped on 19 Oct). The deploy README lists the `humanos_orchestration` database as optional; it is now mandatory. If the run is red on `/health`, that is why.
- Fix on the host: create the database (README §0 line 16), set `HUMANOS_DATABASE_URL=postgresql+psycopg://…/humanos_orchestration` in `/opt/humanos/.env`, run the Alembic chain, redeploy. Keep the Console deploy as is; it only serves files.

### 1.2 Complete the host configuration for the new features (`/opt/humanos/.env` and the override compose)
| setting | value | why |
|---|---|---|
| `HUMANOS_RECEIPT_SECRET` | distinct from `RUNTIME_SERVICE_SECRET`, equal to the Engine's `RUNTIME_RECEIPT_SECRET` | receipts verify; the pair must differ |
| `HUMANOS_WORKFLOW_RUNTIME_REGISTER_TENANTS` | the live tenant ids | capability descriptors register at start-up, no operator script |
| `HUMANOS_CODEGEN_AUTHOR_MODEL`, `HUMANOS_CODE_REVIEWERS` | `claude-opus-4-7` and `claude-sonnet-4-6` through the estate's `ai-execution-service` with `ANTHROPIC_API_KEY`; add `codex.cli` only after 1.4 | API models are the right footing inside containers; the CLI providers are a laptop convenience |
| `HUMANOS_ESTATE_GATEWAY_URL`, `HUMANOS_ESTATE_SERVICE_SECRET` | the estate gateway (`dev.nessovo.com` or the internal gateway container) and its service secret | estate reads for Home and the CRM screens |
| `RUNTIME_ALLOW_OPERATOR_CERTIFY=false`, `RUNTIME_ENFORCE_RLS_ROLE=true`, `RUNTIME_REQUIRE_ENVELOPE`, `RUNTIME_REQUIRE_ATTEMPT` | on | the Engine's production posture (already the staging defaults in `.env.example`) |
| `HUMANOS_ENV=production` | after 1.5 | production refuses in-memory stores, self-approval, operator certification and missing telemetry |

### 1.3 Engine: publish the fix branch and rebuild
- `workflow-engine` branch `codex/wi-mvp-integration` (worker-certification fix) exists only on this laptop. Push it, open its PR, merge to `main`.
- On the host, update the `workflow-engine` checkout and rebuild `runtime` (the compose builds it from `../../workflow-engine`). Confirm `/actuator/health` and that `code.generate` and `code.review` bind for the live tenants (`GET /api/runtime/capabilities/{id}?version=1.0.0`).

### 1.4 Worker: one production worker, not the laptop one
- The live executor is `tools/real-worker.py` (estate handlers, readiness, spools). The code-generation and review handlers landed this month in `tools/gate1-worker.py`, the lightweight worker.
- Port those two handlers into `real-worker.py` (same model-pin and digest rules, same two review transports), so the host keeps one worker per tenant queue with the full capability list. Until then the compose's `HOS_CAPABILITIES` must not list `code.review`.
- Worker settings on the host: `AI_EXECUTION_URL` to the estate's `ai-execution-service` container, `SERVICE_INTERNAL_SECRET`, `HOS_ORCH_URL=http://orchestrator:8080`, `HOS_ORCH_REPORT_SECRET=RUNTIME_SERVICE_SECRET`. Acceptance is `/readyz` on :8410 answering 200, which proves registration, heartbeat and every dependency of every claimed capability.

### 1.5 Model providers on the host
- Claude: follow `CLAUDE-CLI-PROVISIONING.md` for the planner (dedicated identity, authentication gate before the traffic switch), or `ANTHROPIC_API_KEY` for the API route. One of the two must exist or Aide answers nothing.
- Codex: the reviewer profile pins CLI 0.162.1, probes `codex login status`, and refuses when logged out. To use it live: install the CLI in the orchestrator image or host, log in a dedicated identity the same way as Claude, write the approval line in `docs/gate1-codex-cli-evidence.md`, then add `codex.cli` to `HUMANOS_CODE_REVIEWERS`. Without the approval record it stays off.

### 1.6 Console build for the live backend
- Set the build variables for the Plesk build: `VITE_ORCH_BASE` and `VITE_RT_BASE` to the nginx paths that proxy `orchestrator` and `runtime` (README-DEPLOY §6), `VITE_LIVE_GATEWAY` to the estate gateway, login required and mock mode off for every non-local build (the Phase 4.3 item).
- Add the nginx reverse-proxy entries on Plesk for the orchestrator and runtime paths with authentication in front; the compose binds both to localhost on purpose.

### 1.7 Acceptance on the host, in this order
1. Deploy gate: `E2E MATRIX: 25/25 PASS` from the workflow.
2. `real-worker` `/readyz` 200 with the full capability list.
3. The governed project flow from the Console: propose, countersign by a second live user, Evidence shows the signed receipt.
4. The reviewed-generation flow: draft by the configured author model, review by the configured reviewer, both receipts in Evidence.
5. Only then flip `HUMANOS_ENV=production` and re-run 1 to 4.

### 1.8 Before real users
- Secrets rotated once after the runs above; `.env` readable by the operator only.
- Backup and restore drill for the Engine and Orchestration databases (`deployment/postgres/backup-restore-drill.sh`).
- Telemetry export on (`OTEL_*`), the health board watched for `attention` items (evidence store, registration failures).
- The Engine readiness review (PRR §8 open items) and the Orchestration launch gates remain the formal sign-offs; this plan gets the system running, not signed off.

## Part 2 — Connect the actual CRM

### What is already built for it
- Orchestration has nine governed CRM capabilities (`crm.enquiry.create/update/assign`, `crm.deal.create/update`, `crm.activity.create`, `crm.note.create`, `crm.contact.create`, `crm.enquiry.reply`) and a CRM domain agent that turns Aide requests into them. Each is a WRITE with the two-person rule.
- The estate read client already knows the CRM routes (`/api/crm/v1/me`, customers, enquiries, deals, activities, timelines) and the Console's Home and CRM pages read through `/v1/estate/crm/*`.
- The real worker has handlers for all nine, with before-and-after reads of the record as evidence, and a readiness probe that proves the CRM login.

### How the CRM authenticates (the one real constraint)
The CRM accepts only an IAM bearer with audience `crm` and CRM-owned permission grants; it has no service-to-service path. So the worker must act as a **real IAM user of its own**, pinned to one tenant: `CRM_WORKER_EMAIL`, `CRM_WORKER_PASSWORD`, `CRM_WORKER_TENANT`. It refuses any CRM task for another tenant, and the human proposer and approver are carried in the record and in the signed receipt, while the CRM's actor field shows the worker. That limitation is stated in the evidence, not hidden.

### Steps
1. **Provision the worker identity in the live IAM**: one user per tenant, member of that tenant, CRM role with the grants the nine capabilities need (enquiries, deals, activities, notes, contacts). Store the credentials in the host's private identities file (the `GATE1_LVP_PRIVATE_IDENTITIES` pattern), never in a repository.
2. **Worker settings on the host**: `CRM_URL=http://humanos-service-integrator:8000` on the estate network (or the gateway's `/api/crm`), `IAM_URL` to the IAM container, `PERSON_URL` for contacts, the three `CRM_WORKER_*` values, and the nine `crm.*` ids in `HOS_CAPABILITIES`. Acceptance: `/readyz` shows CRM as served, which means the login succeeded in the pinned tenant.
3. **Orchestration settings**: `HUMANOS_ESTATE_GATEWAY_URL` and `HUMANOS_ESTATE_SERVICE_SECRET` set (clears "Estate not connected" on Home); the `humanos.crm` package installed and certified for the live tenant; the nine descriptors registered at the Engine (automatic at start-up with `HUMANOS_WORKFLOW_RUNTIME_REGISTER_TENANTS`).
4. **Gateway hygiene**: the api-gateway has a duplicate `/api/crm/**` route (`crm-service` vs `service-integrator`, first wins) and the CRM's default port differs between its config and compose. Point the worker at the container directly and leave the gateway for reads until the duplicate is removed.
5. **First live scenario, on a test tenant**: in the Console, "Log a CRM enquiry" → Aide proposes `crm.enquiry.create` → a second user countersigns → the worker creates it → the enquiry appears in crm.nessovo.com with the worker as actor and the humans in the record → Evidence shows the CRM id, the before-and-after state and the signed receipt. Then `crm.deal.create` and `crm.activity.create` the same way.
6. **Hold `crm.enquiry.reply` behind a separate approval**: it sends real messages through the omnichannel service. Enable it only on the test tenant first, and keep it at the higher autonomy class.
7. **Duplicates**: the CRM honours no idempotency key, so a retried write could create a second record. The worker's before-and-after verification is the current guard; adding idempotency-key support to the CRM's create routes is the proper fix and belongs with the estate team.
8. **Go to the production tenant** once steps 5 and 6 pass on the test tenant and the audit entries read correctly.

### What you need from other people
- An IAM administrator to create the worker identities and grant the CRM role (step 1).
- The estate team for the gateway duplicate route and, later, idempotency keys (steps 4 and 7).
- The owner's approval record for the Codex reviewer if it is to run live (1.5).
- A second live user per tenant for every countersign in the acceptance runs.

## Order
1. Part 1, 1.1 to 1.4: make the deployed code run with the new rules (durable store, Engine rebuild, one worker).
2. Part 2, steps 1 to 3: identity, worker and Orchestration settings for the CRM.
3. Part 1, 1.6 and 1.7: Console against the live backend, acceptance runs.
4. Part 2, steps 5 and 6 on the test tenant, then step 8.
5. Part 1, 1.5 (Codex live) and 1.8 (hardening) when the owner records are in place.
