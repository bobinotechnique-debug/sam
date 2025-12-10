# Architectural Decisions

## ADR-001: Stack Choice
- **Decision**: FastAPI backend with React + Vite + Tailwind frontend, PostgreSQL database.
- **Rationale**: Aligns with enterprise requirements for typing, performance, and ecosystem support.
- **Status**: Accepted.

## ADR-002: Layered Backend Structure
- **Decision**: Separate API routers, services, models, and core utilities.
- **Rationale**: Enables clear ownership boundaries and simplifies testing.
- **Status**: Accepted.

## ADR-003: CI with GitHub Actions
- **Decision**: Two-job workflow (backend, frontend) executing linting, typing, and tests on push and PR.
- **Rationale**: Ensures quality gates stay enforced with minimal coupling.
- **Status**: Accepted.

## ADR-004: Multi-organisation single schema
- **Decision**: Utiliser un schéma PostgreSQL unique avec colonnes `organization_id`/`site_id` sur toutes les entités métier.
- **Rationale**: Simplifie l'orchestration (un seul pool/connexion) tout en permettant l'isolation logique par organisation.
- **Impacts**: Index requis sur `organization_id`; filtres obligatoires dans les services/routers pour éviter les fuites inter-org.
- **Status**: Accepted.

## ADR-005: Stockage des horaires en UTC
- **Decision**: Persister toutes les dates/horaires en UTC, et afficher côté front dans le fuseau horaire du site ou de l'utilisateur.
- **Rationale**: Supprime les ambiguïtés multi-sites et simplifie les calculs de chevauchement.
- **Impacts**: Les services doivent convertir vers UTC à l'entrée et exposer le fuseau utilisé dans les réponses.
- **Status**: Accepted.

## ADR-006: Versionnage et normalisation des endpoints API
- **Decision**: Exposer l'API sous `/api/v1/...` avec ressources au pluriel et routes cohérentes par domaine (`organizations`, `sites`, `roles`, `collaborators`, `missions`, `shifts`).
- **Rationale**: Stabilise l'interface contractuelle pour le front et les intégrations tierces, et facilite l'évolution ultérieure via `/api/v2` sans breaking changes immédiates.
- **Impacts**: Documentation OpenAPI alignée sur ce préfixe ; tests et clients front doivent inclure la version ; rewrite éventuelle via reverse proxy à prévoir pour futures versions.
- **Status**: Accepted.

## ADR-007: Format d'erreurs normalisé et traçabilité
- **Decision**: Utiliser une réponse d'erreur unique `{ code, message, detail, trace_id }` sur toutes les routes, avec `trace_id` injecté par middleware.
- **Rationale**: Facilite le support, l'observabilité et les tests contractuels front ; simplifie la corrélation logs/requêtes.
- **Impacts**: Middleware de corrélation obligatoire, tests API doivent vérifier la présence de `trace_id`, les services doivent renvoyer des codes HTTP cohérents (400/401/403/404/409/422/500).
- **Status**: Accepted.
