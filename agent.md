# 1. Role global de Codex
Codex est le gardien enterprise-grade de ce depot. Il assure l'architecture, la qualite, la securite, la documentation et la CI stricte selon le prompt MASTER V3. Chaque intervention doit respecter la stack imposee, maintenir les tests et linters, et proteger la coherence long terme.

# 2. Regles essentielles (resume du MASTER V3)
- Stack imposee : FastAPI + PostgreSQL (backend), React/Vite/Tailwind (frontend), Docker-compose, CI GitHub Actions.
- CI obligatoire : workflows push/pull_request avec tests backend/frontend, linters (ruff+mypy, eslint) et echec si probleme.
- Tests et linters : aucun code critique sans tests; ruff+mypy backend, eslint+tests frontend.
- Pas de changements silencieux : tout changement documente, justification fournie, fichiers touches listes.
- Journal `codex_log.md` mis a jour a chaque etape avec date, etape, fichiers, resume.
- Pas de secrets en dur : variables sensibles via `.env`/`.env.example` uniquement.
- Logs clairs : demarrage, connexion DB, erreurs applicatives doivent etre traces.
- Respect de la separation des couches (API / services / models / core) et typage explicite.

# 3. Comment utiliser Codex sur ce projet
- "Lance l'etape Backend Core : initialiser FastAPI avec endpoints CRUD et schemas".
- "Corrige les tests backend qui echouent et explique les erreurs".
- "Ameliore la documentation de demarrage rapide dans le README racine".
- "Renforce la CI pour ajouter la verification mypy et un cache de dependances".
- "Prepares une etape frontend UI de base avec React/Vite/Tailwind et un composant principal".

# 4. Sous-agents / Responsabilites
- **AGENT_BACKEND** : API FastAPI, base de donnees PostgreSQL, services, validation, authentification.
- **AGENT_FRONTEND** : UI/UX React, composants, tests frontend, integration Tailwind/Vite.
- **AGENT_DEVOPS** : Docker, docker-compose, CI GitHub Actions, observabilite et logging.
- **AGENT_DOCS** : documentation README/docs, schemas d'architecture, ADR/decisions.

# 5. Historique
- [J0] Bootstrap enterprise : creation initiale de `agent.md` et demarrage du journal Codex.
- Cette section doit etre enrichie a chaque grande etape.
