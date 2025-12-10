# Codex Enterprise Starter

Plateforme SaaS de planning multi-sites construite sur FastAPI + React + Tailwind, alignée avec des garde-fous enterprise (CI, linting, typage, tests) et prête pour un stockage PostgreSQL.

## Vision
- One-command local launch via Docker Compose.
- Documentation fondatrice (spécs fonctionnelles/techniques, architecture, ADR, roadmap) avant toute implémentation majeure.
- Strict CI with backend/frontend linting, typing, and tests.
- Extensible architecture avec couches séparées, observation et sécurité (JWT) prévues.

## Quickstart
1. Copier le template d'environnement :
   ```bash
   cp .env.example .env
   ```
2. Lancer la stack :
   ```bash
   docker compose up --build
   ```
3. Accéder aux services :
   - Backend API docs: http://localhost:8000/docs (API versionnée sous `/api/v1` avec `/api/v1/health`)
   - Frontend: http://localhost:5173

## Project Structure
```
/ (root)
├─ backend/          # FastAPI app, services, schemas, tests
├─ frontend/         # React + Vite + Tailwind UI
├─ docs/             # Architecture, roadmap, ADRs, specs fondatrices
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
- `docs/specs_functionnelles.md` — vision produit, domaines, règles et parcours cibles
- `docs/specs_techniques.md` — stack, modèle de données prévisionnel et contraintes techniques
- `docs/conventions.md` — conventions de contribution et de code
- `docs/roadmap.md` — phases et backlog
- `docs/decisions.md` — architectural decisions (ADR-style)
