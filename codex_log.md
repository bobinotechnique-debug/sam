2025-12-10 | Phase 0 | Système d'agents Genesis V2 | Refonte de `agent.md` et des contrats `agents/*.md` pour cadrer le SaaS de planning (phases, périmètres, traçabilité).
2025-12-10 | Etape 1 | agent.md cree | Initialisation du guide Codex et demarrage du journal.
2025-12-11 | Etape 1 | bootstrap complet | Ajout structure backend/frontend, docker-compose, CI stricte, documentation initiale.
2025-12-10 | Etape 2 | documentation renforcee | Ajout index/doc specs fonctionnelles et techniques, conventions, dossiers agents et mise à jour d'agent.md/README.
2025-12-10 | Environnement | tentative docker compose | Copie du template .env et essai de lancement docker compose (--build) bloque car Docker est absent sur l'environnement local.
2025-12-10 | Phase 1 | itération documentation fondatrice | Enrichissement des specs fonctionnelles/techniques, architecture, roadmap et ADR (versionnage API) pour préparer le bootstrap.
2025-12-11 | Phase 1 | documentation fondatrice | Consolidation des specs fonctionnelles/techniques, architecture, ADR et roadmap pour cadrer le SaaS de planning.
2025-12-11 | Phase 1 | documentation fondatrice approfondie | Itération sur la documentation (INDEX, specs fonctionnelles/techniques, architecture, roadmap, ADR erreurs) pour verrouiller le périmètre et la traçabilité.
2025-12-12 | Phase 1 | validation de phase | Périmètre et documents validés par les agents ; revue ADR effectuée (aucune décision structurante manquante) et journal synchronisé pour lancer le bootstrap.
2025-12-12 | Phase 2 | bootstrap technique | Mise en place des endpoints /api/v1 (référentiel planning, healthcheck), services en mémoire, front connecté et docs README synchronisés.
2025-12-13 | Phase 2 | alignement bootstrap et documentation | Clarification de l'état du bootstrap (healthcheck, CRUD référentiel en mémoire, docker-compose prêt), mise à jour des specs/architecture/roadmap/README et traçabilité.
2025-12-14 | Phase 3 | CI stricte backend/frontend | Ajout workflow GitHub Actions (lint/type/tests), règles CI bloquantes et documentation des commandes locales.
2025-12-15 | Phase 3 | CI/Qualité renforcée | Alignement des scripts (Vitest run), CI GitHub Actions backend/frontend stricte, documentation CI mise à jour et rappel des règles bloquantes dans les agents.
2025-12-16 | Phase 4.1 | démarrage MVP planning | Mise en place des CRUD backend avec validations/logs et tests API principaux pour le noyau planning.
2025-12-10 | Phase 4.1 | erreurs API structurées | Ajout d'handlers globaux avec trace_id et réponse normalisée pour harmoniser les erreurs et le suivi des requêtes.
2025-12-10 | Phase 4.1 | validation et passage 4.2 | Validation des livrables API core, mise à jour roadmap/specs et feu vert pour lancer l'UI CRUD basique (Phase 4.2).
2025-12-17 | Phase 4.2 | UI CRUD basique | Ajout du routeur frontend, écrans CRUD (listes/formulaires/suppression) pour organisations, collaborateurs, sites et missions, mise à jour README/roadmap/agent.
2025-12-18 | Phase 4.3 | Planning visuel simple | Ajout vue /planning (jour/semaine) groupée par lieu avec modale d'affectation (missions + shifts), documentation roadmap/agents/spec mise à jour.
2025-12-20 | Phase 4.4 | tests & docs finalisation | Renforcement des tests backend/frontend (planning, CRUD, validations), documentation phase 4 centralisée et liens CI/agents alignés.
2025-12-22 | Phase 4.U | ultimate stabilisation | Logs JSON, health/metrics enrichis, docs Phase 4 finalisées, CI frontend build ajoutée.
2025-12-23 | Phase 4.U | support CORS frontend | Ajout de la configuration CORS backend paramétrable pour permettre les appels API du frontend containerisé.
