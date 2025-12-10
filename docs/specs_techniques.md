# Spécifications techniques

## Stack imposée
- **Backend** : Python 3.11, FastAPI, Pydantic, uvicorn ; migration/DB avec SQLAlchemy + Alembic.
- **Frontend** : React + Vite + Tailwind CSS, Node.js 20 ; tests avec Vitest + Testing Library.
- **Base de données** : PostgreSQL (docker-compose), schéma unique multi-organisation via clés `organization_id`/`site_id`.
- **CI/CD** : GitHub Actions (lint, typage, tests backend et frontend) sur push et PR ; cache futur pour dépendances.

### Principes de conception
- **Séparation stricte des couches** : API (routers) ➜ services ➜ repositories ; dépendances injectées.
- **Validation systématique** : schémas Pydantic `Create/Update/Read` dédiés, erreurs normalisées (422/400/404/409).
- **Versionnage** : API exposée sous `/api/v1/...` ; ressources nommées au pluriel ; réponses paginées.
- **Internationalisation temporelle** : stockage UTC, fuseau par site ; conversions gérées dans services/schemas.

## Architecture applicative cible
- **Backend**
  - `app/api` : routers par domaine (`organizations`, `sites`, `roles`, `collaborators`, `missions`, `shifts`, `health`).
  - `app/schemas` : DTO Pydantic séparant `Create/Update/Read` ; validations (fuseaux horaires, chevauchements horaires).
  - `app/services` : logique métier (compatibilité rôle/compétence, disponibilité, statuts).
  - `app/repositories` : SQLAlchemy async ciblant PostgreSQL ; transactions explicites ; pagination et filtres standards.
  - `app/core` : configuration (`settings` via `.env`), logging structuré, sécurité (JWT, hashage mots de passe), gestion erreurs.
  - `app/tests` : API (FastAPI TestClient) + services isolés ; fixtures pour PostgreSQL (ou SQLite mémoire pour unitaires).
- **Frontend**
  - Arborescence par domaine (`/modules/organizations`, `/modules/planning`, `/modules/collaborators`).
  - Pages de vues calendrier (Jour/Semaine/Mois), listes filtrées, formulaires CRUD ; hooks pour appels API (prévu React Query).
  - Design system minimal Tailwind (boutons, inputs, badges de statut) + layout réutilisable.

### Interfaces API initiales (Phase 2)
- `GET /api/v1/health` : vivacité.
- `GET/POST /api/v1/organizations`, `PATCH/DELETE /api/v1/organizations/{id}`.
- `GET/POST /api/v1/sites` (filtre `organization_id` obligatoire), `PATCH/DELETE /api/v1/sites/{id}`.
- `GET/POST /api/v1/roles`, `PATCH/DELETE /api/v1/roles/{id}`.
- `GET/POST /api/v1/collaborators`, `PATCH/DELETE /api/v1/collaborators/{id}`.
- `GET/POST /api/v1/missions`, `PATCH/DELETE /api/v1/missions/{id}`.
- `GET/POST /api/v1/shifts`, `PATCH/DELETE /api/v1/shifts/{id}` avec vérification de chevauchement.

## Modèle de données (prévisionnel)
- `organizations` (id, nom, fuseau par défaut, metadata de facturation)
- `sites` (id, organization_id, nom, fuseau, adresse, horaires d'ouverture)
- `roles` (id, organization_id, libellé, description, compétences requises JSONB)
- `collaborators` (id, organization_id, identité, coordonnées, statut, rôle principal)
- `collaborator_skills` (collaborator_id, skill, niveau)
- `missions` (id, site_id, rôle requis, date/heure début-fin, budget cible, statut)
- `shifts` (id, mission_id, collaborator_id, horaire début-fin, statut)
- `unavailabilities` (id, collaborator_id, début/fin, motif) — Phase 3+

### Règles de cohérence technique
- Index sur `organization_id`/`site_id` pour toutes les tables ; contraintes de clé étrangère avec suppression restreinte.
- Colonne `status` normalisée (enum) pour missions et shifts ; timestamps `created_at/updated_at` généralisés.
- Validation SQL pour empêcher les chevauchements : vérification applicative obligatoire, contrainte DB optionnelle (exclusion).

### Gestion des migrations
- Alembic générant des migrations explicites ; aucune migration automatique en CI.
- Scripts seed limités aux environnements de dev ; interdits en production.

## Sécurité & conformité
- JWT stateless avec rafraîchissement prévu, hashage Argon2 ou bcrypt ; autorisation par rôle (admin org, manager site, collaborateur).
- Données en transit via HTTPS (hors périm local) ; aucun secret dans le dépôt ou la CI.
- Journalisation structurée (niveau info/debug, erreurs avec traceid) et masquage des données sensibles dans les logs.

## Performances & observabilité
- Démarrage local < 2 minutes via `docker compose up --build` ; objectifs de p95 API < 300ms sur opérations CRUD simples.
- Healthchecks : `/health` backend (vivacité), `/metrics` envisagé (Phase 4) ; logs corrélés par requête.

### Pilotage et alertes (prévisionnel)
- Traces/métriques via OpenTelemetry envisagé ; exporter vers Prometheus/Grafana en Phase 4.
- Logs en JSON, enrichis par `request_id` injecté par middleware ; niveau configurable par env.

## Qualité et tests
- **Backend** : `ruff check app`, `mypy app`, `pytest` (coverage report futur), tests d'intégration contre PostgreSQL dockerisé.
- **Frontend** : `npm run lint`, `npm run test` (Vitest) ; tests de composants critiques et hooks d'appel API.
- **Contrôles de stabilité** : CI bloque en cas d'échec ; revue obligatoire ; pas de `print`, uniquement le logger.

### Critères d'acceptation techniques pour Phase 2
- API `/health` opérationnelle, documentation OpenAPI exposée ; réponses JSON cohérentes.
- Couverture de base : tests unitaires sur services + tests de routes principales (FastAPI TestClient) ; snapshot pour DTO front.
- Lint/typage obligatoires dans la CI ; absence de secrets dans le dépôt et les workflows.

## Exploitation & déploiement
- **Configuration** : variables via `.env` / secrets GitHub ; `.env.example` maintenu à jour.
- **Conteneurs** : Dockerfiles backend/frontend, orchestrés par `docker-compose.yml` (réseaux internes, dépendance DB).
- **Environnements** : dev local (docker compose), préproduction/production envisagés avec la même stack.
