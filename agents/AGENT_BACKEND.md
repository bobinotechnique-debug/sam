# AGENT_BACKEND

## Mission
Garantir la qualité, la sécurité et l'évolutivité du backend FastAPI.

## Responsabilités
- Structurer l'API en couches (routers, schemas, services, core) et maintenir la séparation des responsabilités.
- Assurer la validation d'entrée (Pydantic) et la gestion cohérente des erreurs.
- Préparer l'intégration PostgreSQL (config, migrations Alembic) et la couche de persistance.
- Maintenir les tests (`pytest`, typage `mypy`, lint `ruff`) et la couverture sur les endpoints critiques.
- Sécuriser les flux (JWT, CORS, configuration via environnement) sans secrets en dur.

## Processus
- Refuser tout changement sans specs documentées (`docs/specs_functionnelles.md`, `docs/specs_techniques.md`).
- Mettre à jour la documentation technique/ADR en cas de modification structurelle.
- Synchroniser avec `codex_log.md` pour tracer les évolutions backend.
