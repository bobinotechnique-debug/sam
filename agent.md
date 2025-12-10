# 1. Rôle global de Codex
Codex est le gardien enterprise-grade de ce dépôt. Il garantit l’architecture, la qualité, la sécurité, la documentation et la CI stricte conformément au prompt MASTER V3. Chaque intervention doit préserver la cohérence long terme et la maintenabilité.

# 2. Règles essentielles (résumé MASTER V3)
- Stack imposée : FastAPI + PostgreSQL (backend), React/Vite/Tailwind (frontend), Docker-compose, CI GitHub Actions.
- CI obligatoire : workflows push/pull_request avec tests backend/frontend, linters (ruff+mypy, eslint) et échec en cas d’erreur.
- Qualité : aucun code critique sans tests ; typage explicite ; séparation API / services / models / core ; logs lisibles (démarrage, DB, erreurs).
- Sécurité : aucune donnée sensible en dur ; configuration via `.env`/`.env.example` ; validation d’entrée côté backend.
- Transparence : chaque changement documenté (fichiers touchés, justification) et journal `codex_log.md` mis à jour.

# 2bis. Documentation et synchronisation
- `docs/INDEX.md` récapitule les ressources de référence (architecture, specs fonctionnelles/techniques, conventions, roadmap, ADR).
- Avant toute implémentation, vérifier et mettre à jour `docs/specs_functionnelles.md` et `docs/specs_techniques.md` si l’évolution modifie le périmètre.
- Les conventions d’équipe et de contribution sont décrites dans `docs/conventions.md` ; toute divergence doit être corrigée ou documentée.
- `README.md` doit rester fidèle à l’expérience développeur actuelle (installation, commandes, ports).

# 3. Comment utiliser Codex
- "Lance l’étape Backend Core : initialiser FastAPI avec endpoints CRUD et schémas".
- "Corrige les tests backend qui échouent et explique les erreurs".
- "Améliore la documentation de démarrage rapide dans le README racine".
- "Renforce la CI pour ajouter la vérification mypy et un cache de dépendances".
- "Prépare une étape frontend UI de base avec React/Vite/Tailwind et un composant principal".

# 4. Sous-agents / Responsabilités
- **AGENT_BACKEND** : API FastAPI, PostgreSQL, services, validation, authentification.
- **AGENT_FRONTEND** : UI/UX React, composants, tests frontend, intégration Tailwind/Vite.
- **AGENT_DEVOPS** : Docker, docker-compose, CI GitHub Actions, observabilité et logging.
- **AGENT_DOCS** : documentation README/docs, schémas d’architecture, ADR/decisions.

# 5. Historique
- [J0] Bootstrap initial : création de `agent.md` et démarrage du journal Codex.
- [J1] Étape 1 : structure complète backend/frontend/docs, docker-compose, CI stricte, documentation racine enrichie.
- [J2] Étape documentation : ajout de l’index doc, spécifications fonctionnelles/techniques, conventions, et création des sous-agents.
