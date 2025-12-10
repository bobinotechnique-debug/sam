# Frontend (React + Vite + Tailwind)

## Overview
This frontend uses React with Vite and Tailwind CSS. It now provides CRUD screens for organizations, collaborators, sites and missions (Phase 4.2) using the backend API.

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

## Phase 4.2 – UI CRUD basique
- Routes principales :
  - `/organizations`, `/organizations/new`, `/organizations/:id/edit`
  - `/collaborators`, `/collaborators/new`, `/collaborators/:id/edit`
  - `/sites`, `/sites/new`, `/sites/:id/edit`
  - `/missions`, `/missions/new`, `/missions/:id/edit`
- Chaque écran expose les états chargement/erreur/vides, des formulaires validés côté UI et une confirmation avant suppression.
- L'URL d'API est contrôlée par `VITE_API_BASE_URL` (par défaut `http://localhost:8000`).
