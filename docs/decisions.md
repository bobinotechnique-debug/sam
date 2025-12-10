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
