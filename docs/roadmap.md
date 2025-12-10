# Roadmap

## Phase 0 : Système d'agents (validée)
- Cadre des agents (`agent.md`, `agents/`), journal `codex_log.md`.
- Alignement sur la stack verrouillée et règles de qualité.

## Phase 1 : Documentation fondatrice (en cours)
- Consolider les specs fonctionnelles/techniques, l'architecture et les ADR.
- Définir le périmètre métier initial (organisations, sites, rôles, collaborateurs, missions, shifts).
- Formaliser critères d'acceptation et exigences de qualité (CI, sécurité, traçabilité).

## Phase 2 : Bootstrap technique
- Squelette FastAPI avec routers/domains, services et configuration `.env` ; healthcheck opérationnel.
- Squelette React/Vite/Tailwind avec layout, navigation et appels API mockés.
- Docker Compose complet (backend, frontend, PostgreSQL) + `.env.example` cohérent.
- CI GitHub Actions exécutant lint/type/tests sur backend et frontend.

## Phase 3 : Core produit
- CRUD organisations/sites/rôles/collaborateurs/missions/shifts avec validations métier.
- Authentification JWT + autorisations par rôle ; gestion des fuseaux horaires.
- Tests d'intégration (API + DB) et couverture front (Vitest) sur parcours critiques.
- Premières vues planning (Jour/Semaine) avec drag-and-drop côté front.

## Phase 4 : Fiabilisation & Observabilité
- Logs enrichis (trace-id), métriques et traces (OpenTelemetry envisagé).
- Optimisations perf (caching lecture, pagination généralisée) et durcissement CI (coverage thresholds, scan dépendances).
- Gestion des indisponibilités, notifications et exports partageables.
- Préproduction/production alignées (secret management, migrations automatisées).
