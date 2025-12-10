# Codex Enterprise Starter

A FastAPI + React + Tailwind starter aligned with enterprise-grade quality gates (CI, linting, typing, tests) and ready for PostgreSQL-backed CRUD features.

## Vision
- One-command local launch via Docker Compose.
- Strict CI with backend/frontend linting, typing, and tests.
- Clear documentation to onboard contributors quickly.
- Extensible architecture with separated layers and observable runtime.

## Quickstart
1. Copy environment template and adjust values:
   ```bash
   cp .env.example .env
   ```
2. Launch the stack:
   ```bash
   docker compose up --build
   ```
3. Access services:
   - Backend API docs: http://localhost:8000/docs
   - Frontend: http://localhost:5173

## Project Structure
```
/ (root)
├─ backend/          # FastAPI app, services, schemas, tests
├─ frontend/         # React + Vite + Tailwind UI
├─ docs/             # Architecture, roadmap, ADRs
├─ .github/workflows # CI definitions
├─ docker-compose.yml
├─ .env.example
├─ agent.md          # Operating guide for Codex agents
├─ codex_log.md      # Journal of Codex steps
```

## Development
### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Quality Gates
- Backend: `ruff check app`, `mypy app`, `pytest`
- Frontend: `npm run lint`, `npm run test`

## CI
GitHub Actions workflow runs backend lint/type/tests and frontend lint/tests on every push and pull request (see `.github/workflows/ci.yml`).

## Documentation
- `docs/INDEX.md` — plan de la documentation
- `docs/architecture.md` — high-level design and flows
- `docs/specs_functionnelles.md` — exigences et parcours métier
- `docs/specs_techniques.md` — stack, contraintes techniques et sécurité
- `docs/conventions.md` — conventions de contribution et de code
- `docs/roadmap.md` — phases et backlog
- `docs/decisions.md` — architectural decisions (ADR-style)
