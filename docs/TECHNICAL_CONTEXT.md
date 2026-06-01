# Enterprise Visual Intelligence API — Technical Context

**Document version:** June 2026  
**Scope:** Describes what is in the repository today. Recommendations appear only in sections 8–9 and are labeled explicitly.

---

## 1. Project purpose

### What this application does

**Currently implemented:** A small FastAPI service that accepts an operational image via `POST /analyze`, runs multimodal vision analysis through OpenAI, classifies the scene type, grounds the result against local markdown policy documents, assembles a structured operational report, persists it as JSON, and exposes retrieval via `GET /reports/{report_id}`.

### Business / enterprise problem it solves

It targets operational visual review where humans would otherwise inspect photos and compare them to policy:

- warehouse_scene — Walkway obstructions, stacking, spills
- retail_shelf — Empty facings, damaged product
- equipment_inspection — Visible equipment condition
- dashboard_screenshot — KPI anomalies in screenshots
- inventory_delivery — Delivery / inventory escalation
- unknown — Unclassified images (no policy file mapped)

The README frames this as simulating enterprise AI workflows: multimodal ingestion, structured extraction, policy context, escalation-aware reporting, and persistence.

### What type of AI system it is

**Currently implemented:** A vision-language model (VLM) pipeline with rule-based post-processing, not an agentic system.

| Layer | Mechanism |
|-------|-----------|
| Perception / extraction | OpenAI Responses API with input_image + JSON output (VisualFacts) |
| Retrieval | Deterministic file lookup by input_type (full markdown file read) — NOT embedding search or RAG |
| Reasoning / reporting | Heuristic escalation in Python (report_service.py) over VLM possible_risks + policy text keywords |
| Persistence | Local JSON files under reports/ |

Best described as: structured VLM extraction + policy-grounded report assembly.

---

## 2. Current architecture

### High-level flow

Client → FastAPI (main.py) → Routes (/analyze, /health, /reports, /) → Services (vision, report, context, storage) → OpenAI API / context_docs / reports JSON files

### Main application entry point

- Entry: app/main.py — creates FastAPI(), registers routers, defines GET /
- Run locally: uvicorn app.main:app --reload
- Run in Docker: uvicorn app.main:app --host 0.0.0.0 --port 8000

### API routes / endpoints

| Method | Path | Module | Behavior |
|--------|------|--------|----------|
| GET | / | app/main.py | Service identification JSON |
| GET | /health | app/routes/health.py | status: ok, fixed service name |
| POST | /analyze | app/routes/analyze.py | Upload image → VLM → report → save → return |
| GET | /reports/{report_id} | app/routes/reports.py | Load JSON report or 404 |

OpenAPI/Swagger at /docs when running.

### Service layer

- vision_service.py — OpenAI client, multimodal call, JSON parse, VisualFacts validation
- context_service.py — Map input_type → markdown file; return full file text
- report_service.py — Build VisualAnalysisReport: issues, escalation, actions, fixed confidence
- storage_service.py — Write/read reports/{report_id}.json

### Schema / model layer

app/schemas.py (Pydantic v2):

- VisualFacts — VLM output contract
- Issue — typed severity: low | medium | high | critical
- VisualAnalysisReport — API response + persisted document

### Storage / persistence layer

- Reports: reports/{uuid}.json
- Policy context: static files in context_docs/
- No database, object store, or vector store in use

### Configuration layer

app/config.py — pydantic_settings.BaseSettings:

- app_name, openai_api_key, openai_model (default gpt-4o-mini)
- Loads from .env

### Test structure

- tests/test_health.py — GET /health
- tests/test_analyze_mock.py — POST /analyze with patched VLM
- tests/test_schema.py — Pydantic valid/invalid input_type
- tests/test_image_utils.py — validate + base64
- tests/test_storage_service.py — save/load with temp dir

pytest.ini sets pythonpath = .

### Docker / deployment setup

- Dockerfile — Python 3.11-slim, pip install, expose 8000
- docker-compose.yml — Single app service, port 8000, .env
- .dockerignore — Excludes .venv, .env, reports, caches

Not present: Kubernetes, Terraform, cloud IaC, GitHub Actions.

---

## 3. Current implemented tech stack

| Category | Choice |
|----------|--------|
| Backend | Python 3.11, FastAPI, Uvicorn |
| AI / VLM | OpenAI Python SDK — client.responses.create() with input_image + json_object |
| Validation | Pydantic models + Pydantic Settings |
| Uploads | python-multipart, UploadFile |
| Storage | Filesystem JSON (pathlib) |
| Testing | pytest, httpx (TestClient) |
| Deployment | Docker + docker-compose |
| Declared but unused | chromadb in requirements.txt — no imports in app code |

---

## 4. End-to-end workflow: POST /analyze

### Sequence (implemented)

1. Client sends multipart file upload to POST /analyze
2. validate_image_file checks content_type (jpeg/jpg/png only)
3. file.file.read() → bytes; encode_image_to_base64
4. analyze_image_with_vlm sends OpenAI Responses API request (system prompt + base64 image, JSON mode)
5. json.loads(output_text) → VisualFacts validated with Pydantic
6. generate_report_from_visual_facts calls get_context_for_input_type (full markdown file)
7. Rule-based escalation from policy keywords + possible_risks text
8. save_report writes reports/{report_id}.json
9. VisualAnalysisReport returned as JSON

### Escalation rules (report_service.py)

- critical: risks exist AND "critical" in policy text AND risk contains blocked/exit/walkway/fire/obstruction
- high: risks exist AND "high" in policy text
- else medium if risks else low
- confidence: hardcoded 0.85

### Image handling notes

- Data URL always uses image/png label even for JPEG uploads
- No file size limit or binary image validation

---

## 5. Important files

### Application core

- app/main.py — FastAPI app, router wiring, root message
- app/config.py — Environment-backed settings
- app/schemas.py — API and VLM contracts

### Routes

- app/routes/analyze.py — Orchestrates validate → encode → VLM → report → save
- app/routes/health.py — Health JSON
- app/routes/reports.py — Report retrieval; 404 on missing file

### Services

- app/services/vision_service.py — OpenAI integration
- app/services/context_service.py — input_type → policy markdown mapping
- app/services/report_service.py — Report assembly + escalation
- app/services/storage_service.py — JSON filesystem CRUD

### Utilities

- app/utils/image_utils.py — Content-type gate + base64

### Policy context

- context_docs/warehouse_safety_rules.md → warehouse_scene
- context_docs/retail_shelf_rules.md → retail_shelf
- context_docs/equipment_inspection_rules.md → equipment_inspection
- context_docs/dashboard_anomaly_policy.md → dashboard_screenshot
- context_docs/inventory_escalation_policy.md → inventory_delivery

### Tests, ops, docs

- tests/* — pytest suite
- requirements.txt, Dockerfile, docker-compose.yml
- README.md — Product narrative and API examples

---

## 6. Current strengths

1. Clear layered architecture (routes → services → schemas)
2. Typed contracts (VisualFacts vs VisualAnalysisReport)
3. Structured VLM output (JSON mode + Pydantic)
4. Policy grounding concept (retrieved_context in response)
5. Operational fields (escalation, issues, limitations, actions)
6. Persistence + retrieval (audit trail pattern)
7. Testability (mocked VLM at route boundary)
8. Containerized run path (Docker + compose)
9. Domain breadth (five scenario types + policy docs)
10. Strong README with examples and pipeline narrative

---

## 7. Current limitations / gaps

| Gap | Current state |
|-----|----------------|
| Real database | JSON files only |
| Vector DB / real RAG | Full-file lookup; chromadb unused |
| Async jobs / queue | Sync blocking request |
| CI/CD | No GitHub Actions |
| Cloud deployment | Docker local only |
| Terraform | Absent |
| Observability | No structured logging/metrics/tracing |
| Authentication | Public endpoints |
| Microservices | Monolith |
| Evaluation framework | None |
| Agentic workflow | Single-shot VLM + rules |
| Image handling | MIME-only; forced PNG data URL |
| Confidence | Static 0.85 |
| Policy reasoning | Keyword heuristics, not LLM adjudication |

---

## 8. Recommended next steps

### Tier 1 — Highest ROI, lowest risk

1. GitHub Actions CI (pytest on push/PR)
2. Structured logging (request ID, latency, input_type, escalation)
3. Fix image pipeline (correct MIME in data URL; max size)
4. Remove or implement ChromaDB (chunked RAG or drop dependency)
5. Expand tests (escalation matrix, unknown context, VLM errors)

### Tier 2 — Strong portfolio signal

6. SQLite + SQLAlchemy for reports
7. Simple API key auth (header + env)
8. Deploy to one cloud (Fly.io, Railway, Cloud Run)
9. Eval harness (labeled images + thresholds)
10. Optional second-pass LLM report (VisualFacts + policy chunks)

### Tier 3 — Only if role-specific

- Async queue, Terraform, microservices split, agent frameworks — defer until baseline eval + deploy exist

---

## 9. Do not over-engineer

- Keep single FastAPI service until scale demands split
- Prefer SQLite + chunked RAG over Postgres + Pinecone + workers for portfolio scope
- CI + logging + one cloud deploy + eval set beats Kubernetes for most FDE interviews
- Remove chromadb from requirements until actually wired, or implement minimal chunk retrieval

---

## Summary

This is a well-structured multimodal API prototype: VLM structured extraction, policy grounding, escalation reporting, file persistence, Docker, and tests. It does not yet include auth, real DB, vector RAG, async processing, CI/CD, cloud deploy, observability, or evals. Section 8 prioritizes next steps without unnecessary enterprise complexity.
