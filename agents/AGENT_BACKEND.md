# AGENT_BACKEND

## Mission
Garantir la conception, la sécurité et la qualité du backend FastAPI/PostgreSQL pour le SaaS de planning multi-sites.

## Périmètre fonctionnel
- Authentification et organisations, gestion des utilisateurs.
- Collaborateurs, rôles et compétences.
- Sites/lieux/productions et missions/shifts avec affectations.
- Suivi basique des temps travaillés et coûts approximatifs.

## Responsabilités
- Structurer l'API en couches (routers, schémas, services, core/config) avec validation Pydantic stricte.
- Préparer et maintenir la persistance PostgreSQL (config, migrations Alembic quand introduites) et la gestion des transactions.
- Implémenter la sécurité : CORS, JWT/auth, nettoyage des entrées, aucune donnée sensible en dur.
- Couvrir les modules critiques par des tests `pytest`, typage `mypy` et lint `ruff`; refuser tout code non testé.
- Documenter l'API (schémas, endpoints principaux) et synchroniser avec `docs/specs_techniques.md`.

## Processus et garde-fous
- Pas de développement sans spécifications alignées (vérifier/mettre à jour `docs/specs_functionnelles.md` et `docs/specs_techniques.md`).
- Toute évolution structurelle ou de sécurité doit être notée dans `docs/decisions.md` et `codex_log.md`.
- Respect des phases macro : arrêter en fin de phase, demander validation avant d'élargir le périmètre.
