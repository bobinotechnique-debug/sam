# Spécifications techniques

## Stack imposée
- **Backend** : Python 3.11, FastAPI, Pydantic, uvicorn ; migration/DB avec SQLAlchemy + Alembic.
- **Frontend** : React + Vite + Tailwind CSS, Node.js 20 ; tests avec Vitest + Testing Library.
- **Base de données** : PostgreSQL (docker-compose), schéma unique multi-organisation via clés `organization_id`/`site_id`.
- **CI/CD** : GitHub Actions (lint, typage, tests backend et frontend) sur push et PR ; cache futur pour dépendances.

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

## Modèle de données (prévisionnel)
- `organizations` (id, nom, fuseau par défaut, metadata de facturation)
- `sites` (id, organization_id, nom, fuseau, adresse, horaires d'ouverture)
- `roles` (id, organization_id, libellé, description, compétences requises JSONB)
- `collaborators` (id, organization_id, identité, coordonnées, statut, rôle principal)
- `collaborator_skills` (collaborator_id, skill, niveau)
- `missions` (id, site_id, rôle requis, date/heure début-fin, budget cible, statut)
- `shifts` (id, mission_id, collaborator_id, horaire début-fin, statut)
- `unavailabilities` (id, collaborator_id, début/fin, motif) — Phase 3+

## Sécurité & conformité
- JWT stateless avec rafraîchissement prévu, hashage Argon2 ou bcrypt ; autorisation par rôle (admin org, manager site, collaborateur).
- Données en transit via HTTPS (hors périm local) ; aucun secret dans le dépôt ou la CI.
- Journalisation structurée (niveau info/debug, erreurs avec traceid) et masquage des données sensibles dans les logs.

## Performances & observabilité
- Démarrage local < 2 minutes via `docker compose up --build` ; objectifs de p95 API < 300ms sur opérations CRUD simples.
- Healthchecks : `/health` backend (vivacité), `/metrics` envisagé (Phase 4) ; logs corrélés par requête.

## Qualité et tests
- **Backend** : `ruff check app`, `mypy app`, `pytest` (coverage report futur), tests d'intégration contre PostgreSQL dockerisé.
- **Frontend** : `npm run lint`, `npm run test` (Vitest) ; tests de composants critiques et hooks d'appel API.
- **Contrôles de stabilité** : CI bloque en cas d'échec ; revue obligatoire ; pas de `print`, uniquement le logger.

## Exploitation & déploiement
- **Configuration** : variables via `.env` / secrets GitHub ; `.env.example` maintenu à jour.
- **Conteneurs** : Dockerfiles backend/frontend, orchestrés par `docker-compose.yml` (réseaux internes, dépendance DB).
- **Environnements** : dev local (docker compose), préproduction/production envisagés avec la même stack.
