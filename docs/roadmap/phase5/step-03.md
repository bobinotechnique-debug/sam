# Phase 5 - Step 03 - Planning PRO API wiring (connected v1)

- Status: done
- Date: 2026-01-13
- Owner: Codex (agents)

## Objectives
- Expose Planning PRO endpoints under `/api/v1/planning/*` with strict schemas and validation.
- Return normalized conflicts (hard vs soft) for shifts and assignments, and record audit events for each change.
- Replace the Planning PRO frontend mocks with live API calls (shifts, assignments, conflicts, auto-assign status).
- Ship a minimal auto-assign v1 job skeleton with start/status endpoints.

## Deliverables
### Backend
- CRUD endpoints for shift templates, shift instances, assignments, and availability, all backed by the Step 02 services.
- Rule catalog exposed via `GET /api/v1/planning/rules` plus conflict preview and publish endpoints.
- Auto-assign start/status endpoints with in-memory job tracking, deterministic job ids, and conflict aggregation.
- Minimal validations enforced (time window order, allowed statuses, mission/site/role alignment, role match on assignment, double booking, min rest, leave overlap, missing skill, capacity checks).
- Audit trail entries (`planning_change`) for shift and assignment mutations and publish actions, exposing before/after payloads and filters.

### Frontend
- Timeline V2 powered by React Query to list live shifts, assignments, conflicts, and statuses.
- Auto-assign action wired to the backend with status polling and refetch on completion.
- Conflict badges kept in the timeline; proposed assignments highlighted via source.

### Documentation
- Roadmap and architecture notes updated to reflect the connected Planning PRO flow and UI/API contract.

### Tests
- Backend: `pytest -q app/tests/test_planning_pro_api.py`.
- Frontend: `npm run lint` and `npm run test`.

## Acceptance criteria
- All `/api/v1/planning/*` endpoints are live, validated, and return normalized conflict payloads.
- Audit entries are produced for publish, shift, and assignment changes and can be filtered by entity and date.
- Timeline V2 consumes the live Planning PRO data and exposes auto-assign status.
- Backend and frontend test suites pass locally and in CI.
