# Roadmap

## Phase 0 : Système d'agents (validée)
- Cadre des agents (`agent.md`, `agents/`), journal `codex_log.md`.
- Alignement sur la stack verrouillée et règles de qualité.

## Phase 1 : Documentation fondatrice (validée)
- Consolider les specs fonctionnelles/techniques, l'architecture et les ADR.
- Définir le périmètre métier initial (organisations, sites, rôles, collaborateurs, missions, shifts).
- Formaliser critères d'acceptation et exigences de qualité (CI, sécurité, traçabilité).
- **Livrables** : backlog priorisé pour le bootstrap, API cibles listées, règles de validation et modèle de données stabilisés.
- **Sortie de phase** : documents `docs/*.md` synchronisés, journal `codex_log.md` mis à jour, validation du périmètre par les agents.
- **Gates** : périmètre approuvé, ADR complètes pour les choix structurants (versionnage API, UTC, multi-org, erreurs).
- **Validation** : périmètre et documents approuvés par les agents ; aucune décision structurante en attente hors ADR.

## Phase 2 : Bootstrap technique
- Squelette FastAPI avec routers/domains, services et configuration `.env` ; healthcheck opérationnel.
- Squelette React/Vite/Tailwind avec layout, navigation et appels API mockés.
- Docker Compose complet (backend, frontend, PostgreSQL) + `.env.example` cohérent.
- CI GitHub Actions exécutant lint/type/tests sur backend et frontend.
- **État** : endpoints `/api/v1/health` et CRUD référentiel implémentés sur un service en mémoire, front connecté au healthcheck, docker-compose fonctionnel pour lancer API/front/DB.
- **Gates** : commandes dev documentées dans `README.md`, pipeline CI verte, endpoints `/health` et CRUD référentiel opérationnels.

## Phase 3 : Core produit
- CRUD organisations/sites/rôles/collaborateurs/missions/shifts avec validations métier.
- Authentification JWT + autorisations par rôle ; gestion des fuseaux horaires.
- Tests d'intégration (API + DB) et couverture front (Vitest) sur parcours critiques.
- Premières vues planning (Jour/Semaine) avec drag-and-drop côté front.
- **Gates** : CI verte avec lint/typage/tests, démos manuelles sur parcours référentiel + planning.
- **Observabilité minimale** : logs JSON corrélés, traces d'erreur avec `trace_id`, métriques healthcheck surveillées.

## Phase 4 : Fiabilisation & Observabilité
- Logs enrichis (trace-id), métriques et traces (OpenTelemetry envisagé).
- Optimisations perf (caching lecture, pagination généralisée) et durcissement CI (coverage thresholds, scan dépendances).
- Gestion des indisponibilités, notifications et exports partageables.
- Préproduction/production alignées (secret management, migrations automatisées).
