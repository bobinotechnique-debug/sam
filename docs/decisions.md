# Architectural Decisions

## ADR-001: Stack Choice
- Decision: FastAPI backend with React + Vite + Tailwind frontend, PostgreSQL database.
- Rationale: Aligns with enterprise requirements for typing, performance, and ecosystem support.
- Status: Accepted.

## ADR-002: Layered Backend Structure
- Decision: Separate API routers, services, models, and core utilities.
- Rationale: Enables clear ownership boundaries and simplifies testing.
- Status: Accepted.

## ADR-003: CI with GitHub Actions
- Decision: Two-job workflow (backend, frontend) executing linting, typing, and tests on push and PR.
- Rationale: Ensures quality gates stay enforced with minimal coupling.
- Status: Accepted.
