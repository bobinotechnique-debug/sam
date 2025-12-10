# Architecture Overview

## High-Level Design
- **Backend (FastAPI)** : API REST stateless, organisée par domaines, exposant des routers typés et documentés (OpenAPI/Swagger).
- **Frontend (React + Vite + Tailwind)** : SPA consommant l'API, proposant vues planning (Jour/Semaine/Mois) et formulaires CRUD.
- **Database (PostgreSQL)** : schéma unique multi-organisation ; migrations gérées via Alembic.
- **CI/CD (GitHub Actions)** : pipeline lint/type/test pour backend et frontend, condition de merge bloquante.
- **Containerization** : docker-compose orchestre API, frontend, base de données et réseau interne unique.

## Domain Boundaries & Components
- **Organizations/Sites** : référentiel hiérarchique, impose fuseau horaire et politiques locales.
- **Collaborators & Roles** : gestion des profils, compétences, états d'activité ; mapping vers rôles requis par les missions.
- **Missions & Shifts** : planification des besoins et affectations ; validations de chevauchement et compatibilité.
- **Core & Security** : configuration, logging, auth JWT, gestion des erreurs, middlewares (trace-id, CORS).
- **Frontend Modules** : pages référentiel, vues calendrier et composants partagés (design system minimal, toasts/erreurs futures).

## Request Flow
1. Requête HTTP reçue par le router FastAPI (`/health`, `/organizations`, `/missions/...`).
2. Validation Pydantic -> service métier (vérif rôle/compétence, horaires, site/org présents).
3. Service appelle repository SQLAlchemy async (PostgreSQL), gère transactions et cohérence des fuseaux horaires.
4. Réponse sérialisée retournée ; logs structurés (trace-id) et erreurs normalisées (422/400/404/500).

## Observabilité & Logging
- Logging JSON console par service, niveau configurable via `.env`.
- Healthcheck `/health` ; exposition `/docs`/`/redoc` pour l'API ; métriques/trace prévus Phase 4.

## Sécurité & Configuration
- Variables d'environnement centralisées (`.env`) pour base de données, secrets JWT, CORS, log level.
- Pas de secrets en dur ; séparation nette des dépendances (requirements backend, package.json frontend).
- Authentification JWT prévue dès Phase 2 ; autorisation par rôle (admin org/manager site/collaborateur).

## Développement & Outillage
- **Backend** : uvicorn reload pour dev local, tests `pytest`, lint/format `ruff`, typage `mypy`.
- **Frontend** : Vite dev server, lint `npm run lint`, tests `npm run test` (Vitest, jsdom).
- **Docker** : `docker compose up --build` pour lancer API + frontend + PostgreSQL ; ports 8000 et 5173 exposés.
