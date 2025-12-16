# Spécifications techniques

## Stack imposée
- **Backend** : Python 3.11, FastAPI, Pydantic, uvicorn ; migration/DB avec SQLAlchemy + Alembic.
- **Frontend** : React + Vite + Tailwind CSS, Node.js 20 ; tests avec Vitest + Testing Library.
- **Base de données** : PostgreSQL (docker-compose), schéma unique multi-organisation via clés `organization_id`/`site_id`.
- **CI/CD** : GitHub Actions (lint, typage, tests backend et frontend) sur push et PR ; cache futur pour dépendances.

### État du bootstrap (Phase 2)
- **Backend opérationnel** : FastAPI expose `/api/v1/health` et les CRUD de référentiel (organizations, sites, roles, collaborators, missions, shifts) via services en mémoire. La couche service est isolée pour faciliter le basculement vers PostgreSQL/Alembic en Phase 3.
- **Front connecté** : Vite + React affiche l'état du healthcheck et lit l'URL API depuis `VITE_API_BASE_URL` (variable transmise par Docker ou le `.env`).
- **Conteneurs prêts** : docker-compose orchestre PostgreSQL, backend (uvicorn) et frontend, avec ports 8000/5173 exposés et variables déclarées dans `.env.example`.
- **Qualité** : CI GitHub Actions exécute `ruff`, `mypy`, `pytest`, `npm run lint` et `npm run test` ; pas de secrets en dépôt.

### Avancement Phase 4.1 – Modèle de données & API core (MVP – validée)
- CRUD REST complet pour organisations, sites, rôles, collaborateurs, missions et shifts avec validations Pydantic (fuseaux valides, fenêtres temporelles, cohérence organisation/site/rôle, prévention des chevauchements d'affectations).
- Services en mémoire enrichis de logs structurés lors des créations/mises à jour/suppressions pour faciliter le suivi.
- Tests API supplémentaires couvrant les flux critiques (CRUD organisation, validation rôle/collaborateur, cohérence mission, cycle de vie d'un shift avec annulation).
- Normalisation des erreurs API via une enveloppe `{code, message, detail, trace_id}` et propagation du trace_id dans le header `X-Request-ID` pour l'audit.
- Statut : livrables validés et prêts pour intégration front en Phase 4.2.

### Avancement Phase 4.2 – UI CRUD basique (validée)
- Connexion du frontend aux endpoints REST existants via hooks d'appel API (URL issue de `VITE_API_BASE_URL`), gestion explicite des états de requête (chargement, succès, erreur) et affichage des erreurs normalisées.
- Formulaires React/Tailwind pour organisations, sites, rôles/compétences, collaborateurs et missions/shifts, avec validations alignées sur les schémas API (horaires ordonnés, cohérence organisation/site/rôle, anti-chevauchement lors des confirmations de shift) et pré-remplissage des données lors des éditions.
- Structure de navigation réutilisable (liste ➜ détail/édition) avec confirmations pour les opérations destructives et messages de feedback utilisateur.
- Préparation à l'extraction de types front à partir d'OpenAPI ou de DTO communs pour réduire la divergence entre contrats front/back.

### Préparation Phase 5 – Planning PRO
- Architecture cible : services `shift_templates`, `shift_instances`, `assignments`, `availability`, `conflict_rules` et `auto_assign` exposés via API dédiées (`/planning/templates`, `/planning/instances`, `/planning/assignments`, `/planning/availability`, `/planning/conflicts`, `/planning/auto-assign`).
- Stockage PostgreSQL : tables versionnées (brouillon/publié) et journal `planning_change` ; `assignment_lock` pour protéger l'édition et la publication ; index sur fenêtres temporelles (`tsrange`) pour conflits et capacités par site/team. **Implémenté** : Alembic gère les tables Planning PRO, les services utilisent une session SQLAlchemy injectée (`get_session`) et un fallback SQLite est utilisé pour les tests.
- Validation multi-niveau : prévalidation front (snap, repos minimal, compétences) puis validation backend stricte (repos, capacité site/team, compétences obligatoires, collision blackout) avec sévérité (warning vs blocage) ; option "force" avec justification loggée.
- Observabilité : métriques Prometheus dédiées (durée auto-assign, taux de couverture, nb conflits détectés, temps de rendu planning), logs structurés par `job_id` pour les jobs asynchrones, traces pour drag/resize côté front (event tracking futur).
- Auto-assign v1 : tâche asynchrone idempotente (`job_id`) exécutant une heuristique gloutonne (tri par criticité, filtrage par compatibilité, scoring affinité/charge/continuité) et renvoyant des assignments en statut `proposé` avec score + justification ; API d'annulation du job prévue.
- API de conflits : endpoint listant les conflits calculés (type de règle, sévérité, entités concernées) et export JSON/CSV ; déclenchement côté publication pour blocages et en sauvegarde pour warnings.

### Principes de conception
- **Séparation stricte des couches** : API (routers) ➜ services ➜ repositories ; dépendances injectées.
- **Validation systématique** : schémas Pydantic `Create/Update/Read` dédiés, erreurs normalisées (422/400/404/409).
- **Versionnage** : API exposée sous `/api/v1/...` ; ressources nommées au pluriel ; réponses paginées.
- **Internationalisation temporelle** : stockage UTC, fuseau par site ; conversions gérées dans services/schemas.
- **Observabilité dès le bootstrap** : logs structurés JSON avec `request_id`, traces d'accès, healthcheck exposé.
- **Contract-first** : schémas OpenAPI sources de vérité pour générer types front (TS) et clients ultérieurs.

## Architecture applicative cible
- **Backend**
  - `app/api` : routers par domaine (`organizations`, `sites`, `roles`, `collaborators`, `missions`, `shifts`, `health`).
  - `app/schemas` : DTO Pydantic séparant `Create/Update/Read` ; validations (fuseaux horaires, chevauchements horaires).
  - `app/services` : logique métier (compatibilité rôle/compétence, disponibilité, statuts).
  - `app/repositories` : SQLAlchemy async ciblant PostgreSQL ; transactions explicites ; pagination et filtres standards.
  - `app/core` : configuration (`settings` via `.env`), logging structuré, sécurité (JWT, hashage mots de passe), gestion erreurs.
  - `app/tests` : API (FastAPI TestClient) + services isolés ; fixtures pour PostgreSQL (ou SQLite mémoire pour unitaires).
- **Services transverses** :
  - **Auth** : JWT courte durée + refresh futur, gestion des rôles (admin org, manager site, collaborateur).
  - **Validation fuseaux/horaires** : helpers centralisés pour éviter la duplication dans services/routers.
  - **Audit** : horodatage systématique `created_at`/`updated_at` et traces d'annulation sur les shifts.
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

#### Standards de réponse et d'erreur
- Succès : enveloppe JSON alignée sur les schémas Pydantic `Read`, pagination standard (`items`, `total`, `page`, `page_size`).
- Erreurs :
  - 400/422 pour validation, 404 pour ressource absente, 409 pour conflit (chevauchement, doublon), 401/403 pour auth.
  - Structure : `{ "code": "<slug>", "message": "...", "detail": {}, "trace_id": "..." }` (générée par les handlers globaux qui exposent aussi `X-Request-ID`).

## Modèle de données cible (Phase 5)
- `organizations`, `sites`, `roles`, `skills`, `teams` : référentiels multi-org avec couleurs et filtres pour la timeline.
- `missions` : contexte métier (site, rôles requis, budget/plafond), liées à des `shift_templates` récurrents.
- `shift_templates` : pattern récurrent (jour(s) de semaine, fenêtre horaire, durée, effectif attendu, team/site/role) générant des `shift_instances`.
- `shift_instances` : instances planifiables (brouillon/publié, source template ou ad-hoc), porteuse des besoins en rôles/équipes et de la fenêtre temporelle ; historisées dans `publication`.
- `assignments` : lien collaborateur ↔ shift_instance avec statut (`proposé`, `confirmé`, `annulé`), origine (auto-assign v1/manuelle), commentaire et timestamps ; `assignment_lock` pour réserver une plage lors d'une édition/publication.
- `user_availabilities` / `leaves` : disponibilités déclarées et absences bloquantes ; `blackouts` pour interdits de site/org ; `capacity_overrides` pour surbooking explicite.
- `hr_rules` : plafonds heures jour/semaine/mois, repos minimal, pauses obligatoires, interdits nocturnes/jours fériés, limites rôle/site.
- `conflict_rules` : détection double booking, chevauchement sur même site/role/team, dépassement de capacité, compétence manquante, collision pause ; stockage des violations dans `notification_events`.
- `planning_changes` : audit trail des modifications (avant/après, auteur, justification, forçage de règle soft) ; `publication` : versionnage brouillon/publié avec message de publication et liste des entités couvertes.

### Règles de cohérence technique
- Index sur `organization_id`/`site_id` pour toutes les tables ; contraintes de clé étrangère avec suppression restreinte.
- Colonne `status` normalisée (enum) pour missions et shifts ; timestamps `created_at/updated_at` généralisés.
- Validation SQL pour empêcher les chevauchements : vérification applicative obligatoire, contrainte DB optionnelle (exclusion).
- Normalisation des fuseaux : stockage du fuseau appliqué dans chaque enregistrement horaire pour traçabilité (colonne `timezone`).

### Gestion des migrations
- Alembic générant des migrations explicites ; aucune migration automatique en CI.
- Scripts seed limités aux environnements de dev ; interdits en production.

## Sécurité & conformité
- JWT stateless avec rafraîchissement prévu, hashage Argon2 ou bcrypt ; autorisation par rôle (admin org, manager site, collaborateur).
- Données en transit via HTTPS (hors périm local) ; aucun secret dans le dépôt ou la CI.
- Journalisation structurée (niveau info/debug, erreurs avec traceid) et masquage des données sensibles dans les logs.
- Politique de moindre privilège : chaque endpoint vérifie organisation/site et rôle avant de retourner les données ; le filtrage est côté service, jamais dans le front.

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
