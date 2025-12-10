# Roadmap

## Phase 0 : Système d'agents (validée)
- Cadre des agents (`agent.md`, `agents/`), journal `codex_log.md`.
- Alignement sur la stack verrouillée et règles de qualité.

## Phase 1 : Documentation fondatrice (validée)
- Consolider les specs fonctionnelles/techniques, l'architecture et les ADR.
- Définir le périmètre métier initial (organisations, sites, rôles, collaborateurs, missions, shifts).
- Formaliser critères d'acceptation et exigences de qualité (CI, sécurité, traçabilité).
- **Livrables** : backlog priorisé pour le bootstrap, API cibles listées, règles de validation et modèle de données stabilisés.
- **Sortie de phase** : documents `docs/*.md` synchronisés, journal `codex_log.md` mis à jour, validation du périmètre par les agents.
- **Gates** : périmètre approuvé, ADR complètes pour les choix structurants (versionnage API, UTC, multi-org, erreurs).
- **Validation** : périmètre et documents approuvés par les agents ; aucune décision structurante en attente hors ADR.

## Phase 2 : Bootstrap technique (validée)
- Squelette FastAPI avec routers/domains, services et configuration `.env` ; healthcheck opérationnel.
- Squelette React/Vite/Tailwind avec layout, navigation et appels API mockés.
- Docker Compose complet (backend, frontend, PostgreSQL) + `.env.example` cohérent.
- CI GitHub Actions exécutant lint/type/tests sur backend et frontend.
- **État** : endpoints `/api/v1/health` et CRUD référentiel implémentés sur un service en mémoire, front connecté au healthcheck, docker-compose fonctionnel pour lancer API/front/DB.
- **Gates** : commandes dev documentées dans `README.md`, pipeline CI verte, endpoints `/health` et CRUD référentiel opérationnels.

## Phase 3 : CI / Qualité (validée)
- Workflows GitHub Actions prêts (ruff, mypy, pytest, npm lint/test) avec exigences bloquantes.
- Alignement des scripts locaux/CI documentés ; rappel des règles de traçabilité et de non régression.
- **Gates** : pipeline verte obligatoire avant toute évolution, commandes de qualité synchronisées entre doc/CI.

## Phase 4 : MVP Planning Core (en cours)
- **Phase 4.1 – Modèle de données & API core** : CRUD complet sur organisations, collaborateurs, sites, missions/shifts avec validations de cohérence et logs d'audit ; tests API principaux (livré).
- **Phase 4.2 – UI CRUD basique** : vues React pour gérer organisations/collaborateurs/lieux/missions, formulaires simples et appels API cohérents.
- **Phase 4.3 – Planning visuel simple** : vue planning jour/semaine, affichage des missions par lieu et affectations, mises à jour backend correspondantes.
- **Phase 4.4 – Stabilisation MVP** : tests supplémentaires, nettoyage des logs/code, documentation consolidée (README, specs fonctionnelles/techniques, roadmap mise à jour) et CI verte.
