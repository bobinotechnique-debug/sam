# Roadmap

## Phase 1: Bootstrap (current)
- Project structure with FastAPI + React + Tailwind
- Docker Compose for local stack
- CI pipeline with linting, typing, and tests
- Baseline documentation and ADRs

## Phase 2: Core Features
- Implement JWT authentication and session management
- Replace in-memory storage with PostgreSQL persistence
- CRUD endpoints with validation and service abstraction
- Seed scripts and migrations (Alembic)

## Phase 3: UX Enhancements
- Responsive CRUD screens with form validation
- Global state management (e.g., React Query)
- Error handling and notifications

## Phase 4: Observability & Ops
- Structured application metrics
- Request tracing and correlation IDs
- Hardened CI/CD with caching, coverage thresholds, and security scans
