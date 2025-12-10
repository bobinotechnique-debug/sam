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

### Tests and Quality (CI parity)
Les mêmes commandes sont exécutées dans la CI GitHub Actions :
```bash
ruff check app
mypy app
pytest
```
Les attentes de phase 4 (tests à lancer, validations) sont rappelées dans `docs/roadmap/phase-04.md` et la vue planning est décrite dans `docs/specs/planning_simple_v1.md`.

### Endpoints clés (MVP Planning Core)
- `GET /api/v1/organizations` — liste paginée, CRUD complet sous `/api/v1/organizations/{id}`.
- `GET /api/v1/collaborators` — CRUD des collaborateurs avec validation du rôle principal.
- `GET /api/v1/sites` — sites liés aux organisations, nécessaires pour les missions.
- `GET /api/v1/missions` — CRUD missions avec validation site/rôle et fenêtres temporelles.
- `GET /api/v1/shifts` — CRUD shifts avec détection de chevauchement et alignement organisationnel.

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
