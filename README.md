# Codex Enterprise Starter

Plateforme SaaS de planning multi-sites construite sur FastAPI + React + Tailwind, alignée avec des garde-fous enterprise (CI, linting, typage, tests) et prête pour un stockage PostgreSQL.

## MVP Planning Core
- **Périmètre livré (Phase 4.1 → 4.U)** : CRUD complet sur organisations, sites, rôles, collaborateurs, missions et shifts avec validations de cohérence, UI CRUD basique et vue planning jour/semaine, observabilité minimale (health enrichi + metrics, logs JSON).
- **Phase 4 Ultimate** : tests backend et frontend renforcés, nettoyage du bruit de logs, documentation actualisée, CI GitHub Actions synchronisée avec les commandes locales et build frontend.
  - États couverts côté front : chargement, erreur, listes vides, ouverture de la modale de mission.
  - Validations côté API : fenêtres temporelles cohérentes, correspondance organisationnelle site/rôle/mission, détection de chevauchement de shifts.
  - Documentation Phase 4 : `docs/roadmap/phase-04.md`, spécification planning simple v1 (`docs/specs/planning_simple_v1.md`), API (`docs/specs/api_phase_4.md`), UX (`docs/specs/ux_phase_4.md`).

## Clôture Phase 4 & transition Phase 5
- La Phase 4 est clôturée : release notes disponibles (`docs/release/phase-04.md`) et prompts Codex de fermeture/cadrage consignés dans `docs/notes/phase-04-closure.md` (rappel des cibles de couverture ≥ 85 %, e2e Playwright CRUD + planning, garde-fous agents).
- La roadmap capture les jalons de clôture et prépare l'ouverture de la Phase 5 (`docs/roadmap.md`).

## Vision
- One-command local launch via Docker Compose.
- Documentation fondatrice (spécs fonctionnelles/techniques, architecture, ADR, roadmap) avant toute implémentation majeure.
- Strict CI with backend/frontend linting, typing, tests and frontend build.
- Extensible architecture avec couches séparées, observation et sécurité (JWT) prévues.
- Phase 2 bootstrap déjà livré : healthcheck `/api/v1/health`, CRUD référentiel en mémoire, frontend connecté et docker-compose prêt (PostgreSQL inclus pour les prochaines migrations).

## Quickstart
1. Copier le template d'environnement :
   ```bash
   cp .env.example .env
   ```
2. Lancer la stack :
   ```bash
   docker compose up --build
   ```
3. Accéder aux services :
   - Backend API docs: http://localhost:8000/docs (API versionnée sous `/api/v1` avec `/api/v1/health` et `/api/v1/health/metrics`)
   - Frontend: http://localhost:5173

## Project Structure
```
/ (root)
├─ backend/          # FastAPI app, services, schemas, tests
├─ frontend/         # React + Vite + Tailwind UI
├─ docs/             # Architecture, roadmap, ADRs, specs fondatrices
├─ .github/workflows # CI definitions
├─ docker-compose.yml
├─ .env.example
├─ agent.md          # Operating guide for Codex agents
├─ codex_log.md      # Journal of Codex steps
```

## Development
### Lancer backend et frontend
```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Tests & qualité (parité CI)
- **Backend** :
  ```bash
  cd backend
  ruff check app
  mypy app
  pytest
  ```
- **Frontend** :
  ```bash
  cd frontend
  npm run lint
  npm run test
  npm run build
  ```
- **Vérification locale CI** : exécuter les commandes ci-dessus avant push ; les mêmes jobs tournent dans GitHub Actions (`.github/workflows/ci.yml`). Les commandes sont détaillées dans `docs/roadmap/phase-04.md`.

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## CI / Qualité
- Déclencheurs : chaque `push` et `pull_request`.
- Jobs vérifiés :
  - **CI / Backend - lint, type, tests** — lint (`ruff`), typage (`mypy`), tests (`pytest`).
  - **CI / Frontend - lint, tests, build** — lint (`eslint`), tests (`vitest`), build (`npm run build`).
- Commandes locales équivalentes :
  - Backend : `cd backend && pip install -e .[dev] && ruff check app && mypy app && pytest`
  - Frontend : `cd frontend && npm install && npm run lint && npm run test && npm run build`
- La CI fait foi : aucun merge ou nouvelle fonctionnalité sans pipeline vert (voir `.github/workflows/ci.yml`).

## Documentation
- `docs/INDEX.md` — plan de la documentation
- `docs/architecture.md` — high-level design and flows
- `docs/specs_functionnelles.md` — vision produit, domaines, règles et parcours cibles
- `docs/specs_techniques.md` — stack, modèle de données prévisionnel et contraintes techniques
- `docs/conventions.md` — conventions de contribution et de code
- `docs/roadmap.md` — phases et backlog
- `docs/decisions.md` — architectural decisions (ADR-style)
- `docs/blueprint/03_ux_ui_planning.md` — spécification visuelle UX/UI (source de vérité des écrans et interactions)
- Phase 4 : `docs/roadmap/phase-04.md`, `docs/specs/api_phase_4.md`, `docs/specs/planning_simple_v1.md`, `docs/specs/ux_phase_4.md`

## UX / UI & Maquettes
La spécification visuelle maître est définie dans `docs/blueprint/03_ux_ui_planning.md`. Elle sert de référence pour toutes les vues (planning jour/semaine/mois, fiches, modals, responsive). Les développeurs frontend doivent vérifier la conformité des écrans et interactions avec cette spec et la mettre à jour en amont de toute évolution UX/UI.

## Phase 5 preview (Planning PRO)
- Backend expose `/api/v1/planning/*` pour les templates, shift instances, assignments, preview des conflits et un auto-assign v1 ; le stockage reste en mémoire et n'utilise pas encore PostgreSQL ou l'authentification.
- Frontend propose une page `/planning/pro` qui consomme ces endpoints et affiche Timeline V2 en lecture seule (boutons de publication/auto-assign non connectés pour l'instant).
- Les données Planning PRO ne sont pas persistées entre redémarrages ; lancer `docker compose` démarre PostgreSQL mais l'API ne l'emploie pas encore.
