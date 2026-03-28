# change-impact-mapper

Deterministic blast-radius mapper for synthetic change requests across a hybrid estate graph.

## MVP Features
- 24-node synthetic estate graph (services, jobs, databases, streams, external dependencies)
- Change request analysis for:
  - impacted nodes
  - critical paths
  - risky consumers
  - recommended tests
  - required approvals
- Sample scenarios:
  - `auth_schema_change`
  - `payments_queue_update`
  - `nightly_batch_shift`
- API and server-rendered UI
- SQLite report history

## Architecture
Graph loader -> impact traversal -> risk scoring -> recommendations -> report persistence/rendering.

## Local Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Routes
- `GET /`
- `POST /api/impact/sample/{sample_id}`
- `POST /api/impact/upload`
- `GET /api/impact/{report_id}`
- `GET /graph/{report_id}`

## Heroku
Includes `Procfile`, `runtime.txt`, `.env.example`, and CI workflow.

## Mock Mode
No OpenAI dependency in MVP.
