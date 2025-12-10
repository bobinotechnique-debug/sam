# Conventions

## Git & branches
- Nommage branches : `feat/<description>`, `fix/<description>`, `chore/<description>`.
- Un commit doit être atomique et testé ; messages impératifs courts.
- Toute PR référence les spécifications mises à jour et mentionne les tests exécutés.

## Qualité
- Respect strict des linters/typages : `ruff`, `mypy`, `eslint`, `vitest`.
- Pas de `print` en production ; utiliser le logger applicatif.
- Tests unitaires pour chaque fonctionnalité critique ajoutée.

## Documentation
- Tenir `agent.md`, `docs/` et les fichiers d'agent sous `agents/` synchronisés avec le code.
- Noter chaque évolution majeure dans `codex_log.md`.
- Mettre à jour `README.md` quand l'expérience développeur change (installation, commandes, prérequis).
