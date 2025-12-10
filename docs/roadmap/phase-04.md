# Phase 4 — MVP Planning Core (Ultimate)

Cette phase consolide le MVP planning avec API et UI simples. La version « Ultimate » inclut observabilité minimale, design system v4, documentation centralisée et CI stricte.

## Sous-phases
- **4.1 – Fondations backend** : CRUD en mémoire pour organisations, rôles, collaborateurs, sites, missions, shifts. Validation de cohérence (fuseaux horaires, plages horaires, appartenance organisationnelle). Healthcheck et erreurs normalisées.
- **4.2 – Écrans CRUD frontend** : vues de liste/filtre, formulaires de création/édition, suppression avec confirmation. États de chargement, vide et erreur pour chaque écran principal.
- **4.3 – Planning visuel simple** : vue planning jour/semaine minimaliste listant les missions et shifts, ouverture d'une modale de détail, mise à jour mission/shift depuis cette modale (API PATCH).
- **4.4 – Stabilisation & qualité** : renforcement des tests backend/frontend, nettoyage des logs de debug, documentation centralisée, parité stricte avec la CI.
- **4.U – Ultimate** : logs JSON structurés, health enrichi (`/api/v1/health` + `/api/v1/health/metrics`), design system Phase 4, docs complètes (API/UX/roadmap), CI incluant build frontend.

## Livrables clés
- Couverture de tests renforcée (backend : validations métier, health/metrics ; frontend : vues CRUD + planning avec états de chargement/erreur/vide).
- Documentation centralisée : ce fichier, `docs/specs/planning_simple_v1.md`, `docs/specs/api_phase_4.md`, `docs/specs/ux_phase_4.md`.
- CI GitHub Actions verte exécutant ruff + mypy + pytest côté backend, eslint + vitest + build côté frontend.
- Observabilité : logs JSON, header `X-Request-ID`, metrics texte exposant compteurs d'entités + uptime.

## Commandes de référence (doivent rester alignées avec la CI)
- Backend : `cd backend && ruff check app && mypy app && pytest`
- Frontend : `cd frontend && npm run lint && npm run test && npm run build`

## Diagrammes ASCII
### Architecture backend
```
[FastAPI Router] -> [Services] -> [InMemory DB]
       |                 |-> logging (JSON)
       |-> /health /metrics
```

### Architecture frontend
```
[Router] -> [Pages CRUD/Planning]
  |            |
  |            -> components (tables, modales, badges)
  -> utils/api -> fetch /api/v1
```

### Flux authentification (placeholder v4)
```
Client -> (future) /auth/login -> token -> appels API avec headers Authorization (à implémenter Phase 5)
```

### Flux CRUD missions
```
UI Form -> POST /missions -> reload list -> select mission -> PATCH /missions/{id}
```

### Flux planning jour/semaine
```
PlanningPage -> load missions/sites/collabs/shifts
             -> render lanes grouped by site
             -> click mission -> modal -> PATCH mission/shift -> refresh
```

### Flux CI/CD
```
push/PR -> GitHub Actions
  -> backend-ci (ruff, mypy, pytest)
  -> frontend-ci (npm ci, lint, test, build)
```

## État actuel (Ultimate)
- Tests supplémentaires couvrant health/metrics, suppressions bloquées, héritage de fuseau horaire, mise à jour de mission depuis la vue planning.
- Tests frontend pour les écrans CRUD (chargement, vide, erreurs, formulaires) et le planning (modale, états).
- Documentation indexée et liens ajoutés dans les READMEs et les agents.
- Observabilité minimale prête pour Prometheus et dashboards.
