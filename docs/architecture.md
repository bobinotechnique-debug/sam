# Architecture Overview

## High-Level Design
- **Backend (FastAPI)** : API REST stateless, organisée par domaines, exposant des routers typés et documentés (OpenAPI/Swagger).
- **Frontend (React + Vite + Tailwind)** : SPA consommant l'API, proposant vues planning (Jour/Semaine/Mois) et formulaires CRUD.
- **Database (PostgreSQL)** : schéma unique multi-organisation ; migrations gérées via Alembic.
- **CI/CD (GitHub Actions)** : pipeline lint/type/test pour backend et frontend, condition de merge bloquante.
- **Containerization** : docker-compose orchestre API, frontend, base de données et réseau interne unique.

### Découpage par domaine
- **Référentiel** : organisations, sites, rôles/compétences ; partagé par toutes les autres entités.
- **Identité & accès** : base JWT + rôles (admin org, manager site, collaborateur) prévue dès Phase 2.
- **Planification** : missions (besoins) et shifts (affectations), validations de fuseau et de chevauchement.
- **Support** : santé/observabilité, configuration, gestion des erreurs.

## Domain Boundaries & Components
- **Organizations/Sites** : référentiel hiérarchique, impose fuseau horaire et politiques locales.
- **Collaborators & Roles** : gestion des profils, compétences, états d'activité ; mapping vers rôles requis par les missions.
- **Missions & Shifts** : planification des besoins et affectations ; validations de chevauchement et compatibilité.
- **Core & Security** : configuration, logging, auth JWT, gestion des erreurs, middlewares (trace-id, CORS).
- **Frontend Modules** : pages référentiel, vues calendrier et composants partagés (design system minimal, toasts/erreurs futures).

### Modules applicatifs (prévisionnels)
- **Backend**
  - `app/core` : settings `.env`, logger JSON, middlewares (CORS, trace-id, auth), gestion d'erreurs normalisées.
  - `app/api/<domaine>` : routers par ressource avec dépendances injectées (services/repos) et pagination standard.
  - `app/services/<domaine>` : règles métier (compatibilité rôle/compétence, validation fuseau, transitions de statut).
  - `app/repositories/<domaine>` : accès Postgres via SQLAlchemy async, gestion transactionnelle et filtres `organization_id`/`site_id` obligatoires.
  - `app/tests` : tests isolés service + tests API avec fixtures DB.
- **Frontend**
  - `modules/core` : layout, providers (React Query futur), gestion des notifications/erreurs.
  - `modules/<domaine>` : écrans CRUD référentiel, vues planning jour/semaine/mois, composants d'édition de shift.
  - `components/ui` : boutons, inputs, badges de statut, modales de confirmation.

## Request Flow
1. Requête HTTP reçue par le router FastAPI (`/health`, `/organizations`, `/missions/...`).
2. Validation Pydantic -> service métier (vérif rôle/compétence, horaires, site/org présents).
3. Service appelle repository SQLAlchemy async (PostgreSQL), gère transactions et cohérence des fuseaux horaires.
4. Réponse sérialisée retournée ; logs structurés (trace-id) et erreurs normalisées (422/400/404/500).

### Flux front ➜ API (Phase 2)
1. Front utilise hooks d'appel API (React Query envisagé) avec tokens JWT ; headers `X-Request-ID` générés côté front si manquants.
2. Les pages planning consomment des endpoints paginés/filtrés (`site_id`, `start`, `end`, `role_id`).
3. Les validations front (saisie horaires, fuseau, filtres) réutilisent les contraintes exposées par les schémas API (OpenAPI/TS types).

### Scénario de planification (séquence simplifiée)
1. **Créer mission** : POST `/missions` ➜ service vérifie site/rôle et fuseau, enregistre en `draft`.
2. **Affecter collaborateur** : POST `/shifts` ➜ service vérifie disponibilité (chevauchements) + compatibilité rôle/organisation, retourne shift `confirmed` ou `draft` selon règle.
3. **Afficher planning** : GET `/shifts` filtré par site/période ➜ front mappe fuseaux locaux et affiche statuts via composants calendrier.
4. **Annuler shift** : PATCH `/shifts/{id}` ➜ statut `cancelled` et motif stockés ; réponse propage `trace_id` pour audit.

## Observabilité & Logging
- Logging JSON console par service, niveau configurable via `.env`.
- Healthcheck `/health` ; exposition `/docs`/`/redoc` pour l'API ; métriques/trace prévus Phase 4.

### Traçabilité
- Middleware de corrélation (trace-id) appliqué sur toutes les routes ; ID propagé au logger.
- Erreurs normalisées (code, message, détail, trace-id) pour faciliter le support.

## Vue déploiement (local dev)
- **docker-compose** : réseau interne unique, services `backend` (uvicorn), `frontend` (Vite build/serve), `db` (PostgreSQL). Dépendances : backend attend DB healthy ; frontend consomme API via URL configurée.
- **Configuration** : `.env.example` référence les variables critiques (DB, JWT, CORS, log level) et sert de base au `.env` local.
- **Ports** : 8000 (API), 5173 (front), 5432 (PostgreSQL) exposés pour le dev ; aucune exposition additionnelle par défaut.

## Sécurité & Configuration
- Variables d'environnement centralisées (`.env`) pour base de données, secrets JWT, CORS, log level.
- Pas de secrets en dur ; séparation nette des dépendances (requirements backend, package.json frontend).
- Authentification JWT prévue dès Phase 2 ; autorisation par rôle (admin org/manager site/collaborateur).

## Développement & Outillage
- **Backend** : uvicorn reload pour dev local, tests `pytest`, lint/format `ruff`, typage `mypy`.
- **Frontend** : Vite dev server, lint `npm run lint`, tests `npm run test` (Vitest, jsdom).
- **Docker** : `docker compose up --build` pour lancer API + frontend + PostgreSQL ; ports 8000 et 5173 exposés.

### Livrables Phase 1
- Schémas d'API et modèle de données validés dans les specs techniques.
- Roadmap alignée sur l'enchaînement bootstrap backend/frontend + CI.
- ADR mises à jour si des choix structurants évoluent.
