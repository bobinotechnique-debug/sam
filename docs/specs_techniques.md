# Spécifications techniques

## Stack imposée
- **Backend** : FastAPI (Python 3.11), Pydantic, uvicorn.
- **Frontend** : React + Vite + Tailwind CSS, Node.js 20.
- **Base de données** : PostgreSQL (via Docker Compose), migrations prévues avec Alembic.
- **CI/CD** : GitHub Actions avec lint, typage, tests pour backend et frontend.

## Architecture applicative
- Backend structuré par couches : `api` (routes), `schemas` (Pydantic), `services` (métier), `core` (config/logs), `tests`.
- Frontend organisé autour de composants React, hooks, et styles Tailwind, prêt pour un gestionnaire d'état (React Query) ultérieur.

## Conformité et sécurité
- Configuration via variables d'environnement (`.env`), exemple dans `.env.example`.
- Journaux structurés (démarrage, erreurs) et healthcheck exposé.
- Validation systématique des entrées côté backend ; jamais de secrets en clair dans le code ou la CI.

## Performances & observabilité
- Démarrage local en moins de 2 minutes via `docker compose up --build`.
- Logging standardisé ; observabilité étendue (traces/metrics) planifiée en Phase 4.

## Qualité et tests
- Backend : `ruff check app`, `mypy app`, `pytest`.
- Frontend : `npm run lint`, `npm run test` (Vitest). Tests unitaires requis pour toute fonctionnalité critique.
