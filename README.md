# Codex Enterprise Starter

Plateforme SaaS de planning multi-sites construite sur FastAPI + React + Tailwind, alignée avec des garde-fous enterprise (CI, linting, typage, tests) et prête pour un stockage PostgreSQL.

## Vision
- One-command local launch via Docker Compose.
- Documentation fondatrice (spécs fonctionnelles/techniques, architecture, ADR, roadmap) avant toute implémentation majeure.
- Strict CI with backend/frontend linting, typing, and tests.
- Extensible architecture avec couches séparées, observation et sécurité (JWT) prévues.
- Phase 2 bootstrap déjà livré : healthcheck `/api/v1/health`, CRUD référentiel en mémoire, frontend connecté et docker-compose prêt (PostgreSQL inclus pour les prochaines migrations).

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

## CI / Qualité
- Déclencheurs : chaque `push` et `pull_request`.
- Jobs vérifiés :
  - **CI / Backend - lint, type, tests** — lint (`ruff`), typage (`mypy`), tests (`pytest`).
  - **CI / Frontend - lint and tests** — lint (`eslint`), tests (`vitest`).
- Commandes locales équivalentes :
  - Backend : `cd backend && pip install -e .[dev] && ruff check app && mypy app && pytest`
  - Frontend : `cd frontend && npm install && npm run lint && npm run test`
- La CI fait foi : aucun merge ou nouvelle fonctionnalité sans pipeline vert (voir `.github/workflows/ci.yml`).

## Documentation
- `docs/INDEX.md` — plan de la documentation
- `docs/architecture.md` — high-level design and flows
- `docs/specs_functionnelles.md` — vision produit, domaines, règles et parcours cibles
- `docs/specs_techniques.md` — stack, modèle de données prévisionnel et contraintes techniques
- `docs/conventions.md` — conventions de contribution et de code
- `docs/roadmap.md` — phases et backlog
- `docs/decisions.md` — architectural decisions (ADR-style)
- `docs/blueprint/03_ux_ui_planning.md` — spécification visuelle UX/UI (source de vérité des écrans et interactions)

## UX / UI & Maquettes
La spécification visuelle maître est définie dans `docs/blueprint/03_ux_ui_planning.md`. Elle sert de référence pour toutes les vues (planning jour/semaine/mois, fiches, modals, responsive). Les développeurs frontend doivent vérifier la conformité des écrans et interactions avec cette spec et la mettre à jour en amont de toute évolution UX/UI.
