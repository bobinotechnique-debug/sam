# Backend (FastAPI)

## Overview
This FastAPI service exposes a versioned `/api/v1` surface with a healthcheck and CRUD for the planning domains (organizations, sites, roles, collaborators, missions, shifts). Planning PRO routes (`/api/v1/planning/*`) now persist to PostgreSQL via SQLAlchemy/Alembic (shift templates, instances, assignments, availability, audit/publications). Logs sont structurés en JSON et exposent `trace_id`, et les endpoints `/api/v1/health` + `/api/v1/health/metrics` fournissent l'état et les compteurs pour l'observabilité minimale. La Phase 4 est clôturée (voir `docs/release/phase-04.md`) avec un objectif de couverture backend ≥ 85 % conservé comme garde-fou.

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
4. Open http://localhost:8000/ to confirm the service is running (links to docs and health check).
5. Open http://localhost:8000/docs for interactive docs.
6. Run migrations against your `DATABASE_URL` (PostgreSQL expected in Docker):
   ```bash
   cd backend
   alembic upgrade head
   ```
   For local, file-based SQLite during development/tests, set `DATABASE_URL=sqlite:///./app.db` before running migrations.

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
