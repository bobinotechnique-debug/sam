# Système d'agents – SaaS Planning & Equipe

## 1. Rôle global
Codex pilote le dépôt de bout en bout pour construire une application SaaS de planning et de gestion d'équipes (intermittents du spectacle, exploitation multi-sites, retail, etc.). Il garantit la cohérence produit/technique, la sécurité et la qualité continue en respectant la stack verrouillée (FastAPI + PostgreSQL, React/Vite/Tailwind, Docker-compose, CI GitHub Actions).

## 2. Vision produit (rappel)
- Planifier des missions/shifts pour des collaborateurs avec vues jour/semaine/mois, par site ou par personne.
- Gérer organisations, sites/lieux, collaborateurs, rôles/compétences, missions et affectations.
- Couvrir les besoins des responsables planning, managers de site et collaborateurs (consultation, notifications ultérieures, export partageable).

## 3. Cycle de travail
- **Phases macro** :
  - Phase 0 – Système d'agents (fichiers agent + journal).
  - Phase 1 – Documentation fondatrice (INDEX, specs fonctionnelles/techniques, architecture, roadmap, conventions, décisions).
  - Phase 2 – Bootstrap technique (backend, frontend, docker-compose, .env.example).
  - Phase 3 – CI/qualité (workflows, lint, tests backend/frontend).
  - Phase 4 – MVP (organisations, utilisateurs, collaborateurs, lieux, missions, planning de base).
  - Phase 5 – Advanced Planning & Team Intelligence (steps 01 → 30) pilotée via `docs/roadmap/phase-05.md` + `docs/roadmap/phase5/step-XX.md`.
- **Workflow de chaque évolution** : Analyse ➜ Mise à jour documentaire/agents si périmètre touché ➜ Validation explicite ➜ Implémentation (code + tests) ➜ Synchronisation (README, journal) ➜ Vérification CI.
- Arrêt obligatoire en fin de chaque phase majeure avant de poursuivre.

## 4. Règles de qualité & sécurité
- Pas de données sensibles en dur ; configuration via `.env`/`.env.example` et secrets externes uniquement.
- Tests et linters obligatoires pour tout code critique ; CI rouge bloquante.
- La CI fait foi : aucune fonctionnalité ou merge si le pipeline n'est pas vert.
- Respect strict des conventions décrites dans `docs/conventions.md` (naming, commits, structure).
- Logs clairs pour démarrage, accès DB et erreurs ; validation systématique des entrées API.
- Aucune fonctionnalité ne peut être ajoutée si la CI n’est pas verte.

## 5. Synchronisation documentaire
- Toute évolution fonctionnelle ou technique doit être reflétée dans `docs/specs_functionnelles.md` et/ou `docs/specs_techniques.md` avant code.
- Les décisions structurantes sont consignées dans `docs/decisions.md` et les architectures dans `docs/architecture.md`.
- `agent.md` et les contrats `agents/*.md` peuvent et doivent être réécrits si le périmètre change ; chaque mise à jour est tracée dans `codex_log.md`.

## 6. Sous-agents et périmètres
- **AGENT_BACKEND** : API FastAPI, domaines (auth/organisations, collaborateurs, lieux, missions, planning, temps & coûts), persistance PostgreSQL, tests pytest/mypy/ruff.
- **AGENT_FRONTEND** : UI React/Vite/Tailwind, vues Dashboard/Planning/Collaborateurs/Lieux, interactions drag-and-drop, tests Vitest/ESLint. Doit s'aligner sur la spécification visuelle maître (`docs/blueprint/03_ux_ui_planning.md`) et la mettre à jour avant toute évolution UX/UI.
- **AGENT_DEVOPS** : Docker/docker-compose, variables d'environnement, CI GitHub Actions (lint, type-check, tests), sécurité dépendances.
- **AGENT_DOCS** : Cohérence documentaire (`docs/`, `README.md`, `agent.md`, `codex_log.md`), coordination des mises à jour d'agents. Garant de la mise à jour et de la diffusion de la spécification visuelle maître.

## 7. Traçabilité
- Chaque étape importante ajoute une ligne dans `codex_log.md` (date, phase, sujet, justification).
- Messages de commit au format conventionnel, PR incluant résumé et tests exécutés.
- Toute modification des scripts de test ou de lint doit être synchronisée entre CI, documentation et guides agents, et tracée
  dans `codex_log.md`.
- Aucune avancée silencieuse : si une décision dévie du cadre, l'ADR correspondante doit être ajoutée avant implémentation.
