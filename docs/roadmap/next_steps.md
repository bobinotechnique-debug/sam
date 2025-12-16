# Next steps

Guidance for Phase 5 execution based on the current code state.

## Step 1 - Wire Planning PRO persistence
- Objective: run Planning PRO endpoints on PostgreSQL instead of the in-memory store.
- Impacted files: `backend/app/services/planning_pro.py`, `backend/app/db/base.py`, `backend/app/db/models/*`, `backend/app/api/planning.py`, `backend/alembic.ini`, `backend/migrations/`.
- Backend: add DB session management, repositories for templates/instances/assignments, and Alembic migration(s) for the new models; align dependency injection in `registry.py`.
- Frontend: no change expected for this step beyond adjusting base URLs if needed.
- Docs: update `backend/README.md`, `docs/architecture.md`, and `docs/specs_techniques.md` to describe the persisted flows and connection string requirements.
- Tests: extend pytest suite to cover DB-backed Planning PRO paths; keep existing in-memory tests or migrate them to fixtures using a test DB.
- Acceptance: `/api/v1/planning/*` works against PostgreSQL with migrations applied; CI runs DB-backed tests without flakiness.

## Step 2 - Harden rules and auto-assign
- Objective: enforce conflict and HR rules with real data and provide deterministic auto-assign.
- Impacted files: `backend/app/services/planning_pro.py`, `backend/app/models/planning_pro.py`, `backend/app/api/planning.py`, `backend/app/tests/test_planning_pro_api.py`.
- Backend: add rule evaluation for blackout windows, team-based capacity, and availability; implement auto-assign that selects collaborators based on availability, role, and rest gaps.
- Frontend: surface conflict reasons and auto-assign results in `/planning/pro` responses (no new UI controls yet).
- Docs: document rule catalog and auto-assign algorithm in `docs/specs/planning_simple_v1.md` or a new Planning PRO spec addendum.
- Tests: new pytest cases covering leave/availability conflicts, rule severity (hard vs soft), and auto-assign selection.
- Acceptance: conflict preview returns meaningful entries, auto-assign produces assignments that respect rules, tests cover new scenarios.

## Step 3 - Upgrade Planning PRO UI interactions
- Objective: make `/planning/pro` actionable for operators.
- Impacted files: `frontend/src/pages/PlanningProPage.tsx`, `frontend/src/components/planning-pro/*`, `frontend/src/api/entities.ts`, `frontend/tests/`.
- Frontend: add filters (site, role, status), connect action buttons to publish/auto-assign endpoints, and add modals to create/update shift templates and shift instances; display conflict badges inline.
- Backend: expose publish and auto-assign endpoints with idempotent responses if missing today.
- Docs: align `frontend/README.md` and `docs/blueprint/03_ux_ui_planning.md` with the new interactions and states.
- Tests: Vitest coverage for UI flows (filters, modal submit, conflict labels), plus mocked API calls for publish/auto-assign.
- Acceptance: operators can create/update shifts and trigger auto-assign/publish from the UI with visible success/error states; tests pass in CI.

## Step 4 - Observability and CI coverage
- Objective: secure non-regression for Planning PRO and surface health signals.
- Impacted files: `.github/workflows/ci.yml`, `backend/app/api/health.py`, `backend/app/core/logging.py`, `frontend/tests/`, `docs/roadmap/phase-05.md`.
- Backend: add metrics for planning endpoints (latency, conflict counts), log context for rule evaluations, and health detail about DB connectivity.
- Frontend: add smoke e2e scenario for Planning PRO (Playwright) once the UI is actionable.
- Docs: record CI matrix and monitoring endpoints in `docs/roadmap/phase-05.md` and `docs/architecture.md`.
- Tests: enable Playwright job in CI; keep unit/integration suites green.
- Acceptance: CI runs backend/frontend checks plus at least one Planning PRO e2e; metrics endpoints expose planning counters; documentation lists how to run and observe them.
