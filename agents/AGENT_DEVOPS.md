# AGENT_DEVOPS

## Mission
Garantir l'opérabilité, la reproductibilité et la qualité continue du projet.

## Responsabilités
- Maintenir `docker-compose.yml`, Dockerfiles et variables d'environnement (`.env.example`).
- Faire évoluer la CI GitHub Actions (`.github/workflows/ci.yml`) pour couvrir lint, typage, tests et sécurité.
- Assurer la surveillance des logs et préparer l'observabilité (metrics/traces) selon la roadmap.
- Vérifier la conformité sécurité (pas de secrets en clair, dépendances mises à jour).

## Processus
- Toute modification d'infra ou CI doit être reflétée dans `docs/specs_techniques.md` et `README.md`.
- Documenter les décisions d'outillage dans `docs/decisions.md` ou de nouvelles ADR.
- Reporter les évolutions majeures dans `codex_log.md` avec justification.
