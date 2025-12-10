# Architecture Overview

## High-Level Design
- **Backend (FastAPI)**: Exposes REST endpoints, validates requests with Pydantic, and hosts business logic in services. Ready to connect to PostgreSQL via `DATABASE_URL`.
- **Frontend (React + Vite + Tailwind)**: Consumes the API, renders health status, and will expand to CRUD flows.
- **Database (PostgreSQL)**: Provisioned via Docker Compose for local development; persistence layer to be implemented in services.
- **CI/CD (GitHub Actions)**: Runs linting, typing, and tests for both backend and frontend on push/PR.
- **Containerization**: Dockerfiles for backend and frontend with a single `docker compose up` entrypoint.

## Request Flow
1. HTTP request hits FastAPI router (e.g., `/items`).
2. Router delegates to service layer for business logic.
3. Service interacts with persistence (currently in-memory, future PostgreSQL).
4. Response serialized via Pydantic schemas and returned to the client.

## Observability & Logging
- Centralized console logging configured on startup.
- Healthcheck endpoint provides basic liveness signal.

## Security & Configuration
- Environment variables via `.env` (see `.env.example`).
- Secrets (e.g., `SECRET_KEY`) must not be committed and should be injected at runtime.
