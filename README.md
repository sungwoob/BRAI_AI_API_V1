# BRAI API Prototype

Python FastAPI implementation of the endpoints described in `spec/API_SPECIFICATION_v1.1.md`.

## Prerequisites

- Python 3.10+
- `pip`

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The root path (`/`) and documented endpoints (`/api/dataset`, `/api/dataset/{id}`, `/api/strains/{id}`) will respond with the JSON formats from the spec.
