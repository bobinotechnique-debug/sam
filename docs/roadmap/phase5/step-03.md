# Phase 5 – Step 03 – Architecture Backend et API Planning PRO (V1 connectée)

- **Statut** : en cours
- **Date** : 2026-01-13
- **Responsable** : Codex (agents)

## Objectifs
- Brancher les modèles et services Planning PRO sur les endpoints `/api/v1/planning/*` (templates, instances, assignments, règles, audit, publication, auto-assign).
- Activer les premières validations métier (règles dures, collisions de disponibilité) pour sécuriser les écritures.
- Retourner au front des données réelles (shifts, assignments, conflits, statuts) afin de remplacer les mocks.
- Préparer l'auto-assign v1 comme job asynchrone (endpoint de lancement + statut) sans encore implémenter l'heuristique complète.

## Livrables attendus
### Backend : endpoints et règles
- Endpoints exposés via FastAPI et reliés aux services créés en Step 02 :
  - `GET|POST|PUT|DELETE /api/v1/planning/shift-templates` – CRUD des modèles de shifts.
  - `GET|POST|PUT|DELETE /api/v1/planning/shifts` – CRUD des instances (draft/published/cancelled).
  - `GET|POST|PUT|DELETE /api/v1/planning/assignments` – Gestion des affectations (proposed/confirmed/rejected, lock).
  - `GET|POST /api/v1/planning/availability` – Lecture/écriture des disponibilités et absences.
  - `GET /api/v1/planning/rules` – Catalogue des règles HR et conflits actives.
  - `POST /api/v1/planning/conflicts/preview` – Calcul des conflits (type hard/soft) sur un payload de planning.
  - `POST /api/v1/planning/publish` – Publication et journalisation d'une version de planning.
  - `POST /api/v1/planning/auto-assign/start` + `GET /api/v1/planning/auto-assign/status/{job_id}` – Démarrage et suivi du job d'auto-assign v1.
- Contrats de base alignés avec la migration Alembic de référence :
  ```json
  {
    "shift": { /* ou "assignment" */ },
    "conflicts": [
      { "type": "hard", "rule": "double_booking", "details": {} }
    ]
  }
  ```
- Validations minimales côté services/règles :
  - Fenêtre temporelle valide (`start < end`) et statuts autorisés (`draft`, `published`, `cancelled`).
  - Alignement mission/site/rôle pour les shifts ; rôle cohérent sur les assignments.
  - Conflits d'agenda : double booking collaborateur, repos minimal manquant, absence/leave, manque de compétence, capacité « hard » dépassée.
  - Warnings non bloquants : dépassement plafonds « soft », shift hors disponibilité déclarée, capacité « soft » dépassée, pause recommandée manquante.
- Audit et journalisation (`planning_change`) :
  - Création/mise à jour/annulation de shift, création/mise à jour/suppression d'assignment, publication.
  - Entrées contenant `user_id`, `action`, `before`, `after`, `timestamp` (UTC).
- Auto-assign v1 (squelette) : endpoints idempotents, stockage d'état en mémoire ou DB, métadonnées de job (`status`, couverture, conflits rencontrés).

### Frontend : intégration Timeline V2
- Page Planning PRO reliée aux endpoints réels via React Query (plus de mocks).
- Affichage des shifts et assignments réels, badges de conflits par shift, statuts brouillon/publié visibles, assignments proposés signalés.
- Actions UI connectées : création/édition/suppression de shifts et assignments, récupération des conflits, consultation du statut d'auto-assign.

### Documentation
- Fiche mise à jour (`docs/roadmap/phase5/step-03.md`) avec objectifs, livrables, critères d'acceptation et commandes de tests.
- `docs/roadmap/phase5/index.md` référencée/alignée, ainsi que `docs/architecture*.md` et `docs/blueprint/03_ux_ui_planning.md` pour le flux API ↔ UI.

### Tests
- Backend : `pytest -q app/tests/test_planning_pro_api.py` et suites associées une fois les endpoints branchés.
- Frontend : `npm run lint` puis `npm run test -- --runInBand` (ou équivalent CI) sur les composants Planning PRO.
- CI : conserver les jobs GitHub Actions au vert (ruff, mypy, pytest backend ; lint/test/build frontend ; Playwright quand activé).

### Critères d'acceptation
- Tous les endpoints listés sous `/api/v1/planning/*` répondent avec des schémas cohérents et appliquent les validations minimales.
- Les écritures planning génèrent des entrées d'audit consultables.
- La Timeline V2 consomme les données réelles (shifts, assignments, conflits, statuts, assignments proposés).
- Les suites de tests backend/frontend pertinentes passent en local et en CI.
