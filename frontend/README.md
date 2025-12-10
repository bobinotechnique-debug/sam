# Frontend (React + Vite + Tailwind)

## Overview
This frontend uses React with Vite and Tailwind CSS. It now provides CRUD screens for organizations, collaborators, sites and missions (Phase 4.2) using the backend API, and a planning view (Phase 4.3) grouped par lieu avec affectations visibles.

## Getting Started

### Local (without Docker)
```bash
npm install
npm run dev
```
Open http://localhost:5173.

### Quality
```bash
npm run lint
npm run test
```
Les mêmes commandes sont utilisées dans la CI GitHub Actions.

### CI parity (local)
```bash
npm run lint && npm run test
```

## Project Layout
- `src/App.tsx` — router and CRUD pages entrypoint
- `src/main.tsx` — React entrypoint
- `src/index.css` — Tailwind entry
- `tests/` — Vitest setup for UI
- `src/pages/PlanningPage.tsx` — vue planning jour/semaine (groupée par lieu)
- `src/components/planning/*` — toolbar, grilles et modale de détail/affectation

## Tests UI ciblés (Phase 4.4)
- États de base : listes vides, erreurs et chargement couverts dans les écrans CRUD et la vue planning.
- Planning : rendu jour/semaine, ouverture de la modale de mission et rafraîchissement après sauvegarde mockée.
- Commande unique : `npm run test` (Vitest + Testing Library, environnement jsdom via `tests/setup.ts`).

## Phase 4.3 – Vue /planning
- Route : `/planning`, accessible depuis la navigation.
- Modes : jour et semaine, fenêtre horaire configurable en code (par défaut 06:00 → 02:00).
- Groupement : par lieu, missions positionnées horizontalement ; empilement simple en cas de chevauchement.
- Interaction : clic sur une mission → modale pour modifier heure début/fin, lieu, affectations (création/suppression de shifts).
- Chargement : missions, sites, collaborateurs et shifts sont rechargés via l'API après sauvegarde.

Layout ASCII simplifié (mode jour) :
```
[Jour|Semaine] [< 12 jan >] [Rafraîchir]

Lieu A | 06h | 08h | 10h | ... | 02h
        [==== Mission 42 ====]
Lieu B | 06h | 08h | 10h | ... | 02h
        [Mission 43][Mission 44     ]
```

## Phase 4.2 – UI CRUD basique
- Routes principales :
  - `/organizations`, `/organizations/new`, `/organizations/:id/edit`
  - `/collaborators`, `/collaborators/new`, `/collaborators/:id/edit`
  - `/sites`, `/sites/new`, `/sites/:id/edit`
  - `/missions`, `/missions/new`, `/missions/:id/edit`
- Chaque écran expose les états chargement/erreur/vides, des formulaires validés côté UI et une confirmation avant suppression.
- L'URL d'API est contrôlée par `VITE_API_BASE_URL` (par défaut `http://localhost:8000`).
