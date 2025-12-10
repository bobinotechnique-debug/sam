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

## Phase 4 : MVP Planning Core (validée)
- **Phase 4.1 – Modèle de données & API core (validée)** : CRUD complet sur organisations, collaborateurs, sites, missions/shifts avec validations de cohérence et logs d'audit ; tests API principaux livrés.
- **Phase 4.2 – UI CRUD basique (validée)** : vues React pour gérer organisations/collaborateurs/lieux/missions, formulaires simples et appels API cohérents.
  - Vues livrées : listes avec états de chargement/erreur/vide, actions créer/éditer/supprimer avec confirmation.
  - Périmètre limité : aucun planning visuel ni drag & drop, uniquement la gestion des référentiels et formulaires basiques.
- **Phase 4.3 – Planning visuel simple (validée)** : vue planning jour/semaine, affichage des missions par lieu et affectations, mises à jour backend correspondantes.
  - Nouvelle page `/planning` avec modes Jour/Semaine et fenêtre horaire configurable (06:00 → 02:00) documentée dans le code.
  - Groupement par lieu ; les missions sont positionnées dans la grille temporelle avec les collaborateurs issus des shifts.
  - Interaction principale : clic sur une mission pour ouvrir une modale, modifier heure début/fin, lieu et affectations ; synchronisation via API missions + shifts (création/suppression mise à jour des affectations).
  - Gestion des erreurs basique en surimpression et rafraîchissement du planning après sauvegarde ; drag & drop restera optionnel pour une phase ultérieure.
- **Phase 4.4 – Stabilisation MVP (validée)** : tests supplémentaires, nettoyage et documentation consolidée (README, roadmap) avec CI verte.
  - Backend : couverture des validations critiques (fenêtres temporelles mission/shift, cohérence site/role/mission, conflits de planning) via pytest.
  - Frontend : tests Vitest sur la vue planning (états vide/erreur, ouverture modale) en plus des parcours de navigation existants.
  - CI : workflows GitHub Actions alignés sur les commandes locales (`ruff`, `mypy`, `pytest`, `npm run lint`, `npm run test`).

### Clôture de phase & transition
- Consolidation documentaire finale : READMEs racine/backend/frontend, doc planning (vues, interactions, modèles), schémas ASCII API ↔ frontend et release notes Phase 4 (`docs/release/phase-04.md`).
- Qualité et observabilité : objectif de couverture backend ≥ 85 %, scénarios e2e Playwright CRUD + planning simple, validation `/health` et `/metrics`, pré-configuration Prometheus/Grafana minimale.
- Garde-fous agents & workflow : mise à jour des agents et prompts Codex consignés dans `docs/notes/phase-04-closure.md` ; scripts de garde à appliquer pour la Phase 5.
- Phase 5 : lancer la roadmap avancée (steps 01 → 30) centrée sur le Planning PRO et la collaboration (voir section suivante).
