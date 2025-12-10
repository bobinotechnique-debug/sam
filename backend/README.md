# Backend (FastAPI)

## Overview
This FastAPI service exposes a versioned `/api/v1` surface with a healthcheck and in-memory CRUD for the initial planning domains (organizations, sites, roles, collaborators, missions, shifts). The application follows a layered approach (API -> services -> models -> core) and is ready to be extended with PostgreSQL persistence and authentication.

## Getting Started

### Local (without Docker)
1. Create a virtual environment and activate it.
2. Install dependencies:
   ```bash
   pip install -e .[dev]
   ```
3. Run the API:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Open http://localhost:8000/docs for interactive docs.

### Tests and Quality
```bash
ruff check app
mypy app
pytest
```

## Configuration
Configuration is loaded from environment variables (see `.env.example`). Key variables include:
- `DATABASE_URL` for PostgreSQL connection string.
- `SECRET_KEY` and `ACCESS_TOKEN_EXPIRE_MINUTES` for authentication.
- `PROJECT_NAME` for API metadata.

## Project Layout
- `app/main.py` — application factory and entrypoint
- `app/api/` — routers and request handling
- `app/services/` — business logic and data access layers
- `app/models/` — Pydantic schemas and domain models
- `app/core/` — configuration, logging, and shared utilities
- `app/tests/` — pytest-based test suite
