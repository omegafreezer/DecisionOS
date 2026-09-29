# DecisionOS

**Agentic Enterprise Decision Intelligence Platform**

DecisionOS is a production-style portfolio project that turns enterprise-style retail data into traceable business decisions. It combines data quality checks, feature engineering, forecasting, anomaly detection, root-cause analysis, what-if simulation, and a multi-agent decision workflow behind a FastAPI service and React dashboard.

> This repository is a self-contained student project using synthetic data. It does **not** claim real Fortune-500 deployment or real-world business impact.

## What it demonstrates

- Python data engineering and validation
- Pandas + scikit-learn ML pipelines
- Revenue forecasting and anomaly detection
- Feature importance / evidence-based root-cause analysis
- Multi-agent orchestration with specialized tool-calling agents
- What-if business simulation
- FastAPI model serving
- React/Vite executive dashboard
- Docker Compose
- GitHub Actions CI
- Automated tests

## Architecture

```text
Synthetic Enterprise Data
        |
        v
+---------------------+
| Data Quality Engine |
+---------------------+
        |
        v
+---------------------+       +----------------------+
| Feature Engineering |------>| ML Models            |
+---------------------+       | Forecast + Anomaly   |
        |                     +----------------------+
        |                              |
        +---------------+--------------+
                        v
              +-------------------+
              | Agent Orchestrator|
              +-------------------+
                |   |   |   |   |
                v   v   v   v   v
              Data Analyst       Forecast
              Anomaly            Root Cause
              Scenario           Decision
                        |
                        v
              +-------------------+
              | Decision Evidence |
              | + Audit Trail     |
              +-------------------+
                        |
                        v
                 FastAPI + React
```

## Quick start

### 1. Backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_data.py
python scripts/train_models.py
uvicorn app.main:app --reload
```

API: http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Dashboard: http://localhost:5173

### 3. Docker

```bash
docker compose up --build
```

Dashboard: http://localhost:5173
API: http://localhost:8000/docs

## Optional LLM mode

The core demo works without an API key. The decision layer is deterministic and evidence-first so that the project remains reproducible. If you later want an LLM explanation layer, add an adapter under `backend/app/services/llm.py` and pass only structured evidence to the model. Never let an LLM invent metrics.

## Main API endpoints

- `GET /health`
- `GET /api/summary`
- `GET /api/forecast`
- `GET /api/anomalies`
- `GET /api/root-cause`
- `POST /api/simulate`
- `POST /api/decision`
- `GET /api/audit/{decision_id}`

## Resume-ready project statement

**DecisionOS — Agentic Enterprise Decision Intelligence Platform** | Python, PySpark, Scikit-learn, LangGraph-style orchestration, FastAPI, React, PostgreSQL-ready, Docker

- Built an end-to-end decision intelligence platform combining data-quality validation, forecasting, anomaly detection, root-cause analysis and scenario simulation.
- Designed specialized Analyst, Forecast, Anomaly, Scenario and Decision agents with an evidence-first audit trail from source data to final business action.
- Developed a FastAPI model-serving layer and React executive dashboard for KPI monitoring, forecasts, anomalies and interactive what-if analysis.

## Important note for interviews

Be able to explain every module. The project intentionally avoids fake complexity: agents are ordinary Python components with explicit tools and contracts, making the system easy to defend in a technical interview.
