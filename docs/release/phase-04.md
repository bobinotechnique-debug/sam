# Phase 4 — Release Notes

## Résumé exécutif
La Phase 4 verrouille le MVP Planning Core avec un socle backend FastAPI stable, des écrans CRUD basiques et une vue planning jour/semaine. Les tests et la documentation sont alignés avec la CI stricte backend/frontend et l'observabilité minimale (health + metrics, logs JSON).

## Livrables clés
- **Backend** : CRUD complet (organisations, sites, rôles, collaborateurs, missions, shifts) avec validations métier, logs structurés et endpoints `/api/v1/health` + `/api/v1/health/metrics`.
- **Frontend** : vues CRUD opérationnelles et vue `/planning` (jour/semaine) groupée par lieu avec modale d'édition mission/shift.
- **Qualité/CI** : commandes locales alignées sur GitHub Actions (ruff, mypy, pytest, eslint, vitest, build).
- **Documentation** : roadmap Phase 4, spécs planning/API/UX, guides README (racine + backend + frontend), prompts Codex de clôture et de cadrage Phase 5.

## État qualité
- Couverture backend : objectif ≥ 85 % conservé comme garde-fou de phase (à vérifier à chaque évolution).
- Parcours UI : tests Vitest couvrant états chargement/erreur/vide et interactions principales sur le planning.
- CI : pipelines backend et frontend stables ; le build frontend fait partie des vérifications bloquantes.

## Observabilité
- Endpoints `/health` et `/metrics` disponibles pour l'API ; prêts pour une collecte Prometheus/Grafana.
- Logs JSON avec `trace_id` pour faciliter le suivi des requêtes.

## Points de vigilance ouverts (pré-Phase 5)
- Ajouter des scénarios e2e Playwright (CRUD + planning simple) pour sécuriser les flux critiques.
- Brancher une stack de monitoring (Prometheus/Grafana) dès l'ouverture de la Phase 5.
- Maintenir la mise à jour synchronisée des agents et de la roadmap pour chaque jalon Phase 5.

## Prochaines étapes
- Valider le prompt Codex Phase 5 et générer la roadmap détaillée (steps 01 → 30).
- Prioriser les features Planning PRO (drag & drop avancé, détection de conflits, auto-assignation).
- Préparer les chantiers observabilité et notifications pour accompagner l'extension fonctionnelle.
