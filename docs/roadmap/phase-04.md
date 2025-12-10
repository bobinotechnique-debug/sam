# Phase 4 — MVP Planning Core

Cette phase consolide le MVP planning avec API et UI simples, en quatre sous-phases :

- **4.1 – Fondations backend** : CRUD en mémoire pour organisations, rôles, collaborateurs, sites, missions, shifts. Validation de cohérence (fuseaux horaires, plages horaires, appartenance organisationnelle). Healthcheck et erreurs normalisées.
- **4.2 – Écrans CRUD frontend** : vues de liste/filtre, formulaires de création/édition, suppression avec confirmation. États de chargement, vide et erreur pour chaque écran principal.
- **4.3 – Planning visuel simple** : vue planning jour/semaine minimaliste listant les missions et shifts, ouverture d'une modale de détail, mise à jour mission/shift depuis cette modale (API PATCH).
- **4.4 – Stabilisation & qualité** : renforcement des tests backend/frontend, nettoyage des logs de debug, documentation centralisée, parité stricte avec la CI.

## Livrables clés
- Couverture de tests renforcée (backend : validations métier et flux CRUD ; frontend : vues CRUD + planning avec états de chargement/erreur/vide).
- Documentation centralisée : `docs/roadmap/phase-04.md`, `docs/specs/planning_simple_v1.md`, liens croisés dans tous les README et agents.
- CI GitHub Actions verte exécutant ruff + mypy + pytest côté backend, eslint + vitest côté frontend.

## Commandes de référence
- Backend : `cd backend && ruff check app && mypy app && pytest`
- Frontend : `cd frontend && npm run lint && npm run test`

## État actuel (4.4)
- Tests supplémentaires couvrant suppressions bloquées, héritage de fuseau horaire site, mise à jour de mission depuis la vue planning.
- Tests frontend pour les écrans CRUD (chargement, vide, erreurs, formulaires) et le planning (modale, états). 
- Documentation indexée et liens ajoutés dans les READMEs et les agents.
