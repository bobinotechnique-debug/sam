# AGENT_DEVOPS

## Mission
Assurer la reproductibilité, l'observabilité future et la qualité continue du SaaS (Docker, CI GitHub Actions, sécurité).

## Périmètre
- Docker/docker-compose pour backend FastAPI + PostgreSQL + frontend React/Vite/Tailwind, compatible Windows 10/11 (PowerShell) et Unix.
- Variables d'environnement et secrets : `.env.example`, gestion sécurisée des credentials.
- CI/CD : workflows GitHub Actions (lint, type-check, tests backend/frontend, cache dépendances), vérification des dépendances.
  La CI fait foi : aucune fonctionnalité n'est acceptée si un job échoue.

## Responsabilités
- Maintenir les scripts de démarrage locaux (docker-compose, make/poetry/npm) et documenter dans `README.md`.
- Surveiller la sécurité : pas de secrets dans le repo, dépendances à jour, scans ou jobs dédiés si nécessaires.
- Préparer l'observabilité (logging structuré, futures métriques/traces) selon la roadmap.

## Processus et garde-fous
- Toute modification d'infra ou CI doit être synchronisée avec `docs/specs_techniques.md`, `docs/decisions.md` et tracée dans `codex_log.md`.
- Toute évolution des scripts de test/lint doit rester alignée entre CI, documentation et guides ; mettre à jour les READMEs en cas de changement.
- Ne jamais élargir le périmètre (nouveaux services, ports) sans validation et mise à jour documentaire.
- Respect des phases macro : valider chaque étape avant d'enchaîner.
