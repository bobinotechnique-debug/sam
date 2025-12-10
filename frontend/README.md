# Frontend (React + Vite + Tailwind)

## Overview
This frontend uses React with Vite and Tailwind CSS. It displays the backend healthcheck status and highlights the stack components.

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

## Project Layout
- `src/App.tsx` — main UI with healthcheck call
- `src/main.tsx` — React entrypoint
- `src/index.css` — Tailwind entry
- `tests/` — Vitest setup for UI
