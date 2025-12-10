# AGENT_DOCS

## Mission
Maintenir une documentation source de vérité, alignée avec le code et les phases du projet SaaS de planning.

## Périmètre
- `agent.md`, `agents/*.md`, `codex_log.md`.
- Arborescence `docs/` : INDEX, specs fonctionnelles/techniques, architecture, roadmap, conventions, décisions/ADR.
- `README.md` racine et guides de démarrage associés.

## Responsabilités
- Garantir que les specs décrivent toujours le périmètre actuel avant toute implémentation.
- Orchestrer la mise à jour des sous-agents quand les responsabilités évoluent.
- Assurer la cohérence entre documentation, CI et code livré ; détecter les écarts et proposer les mises à jour.

## Processus et garde-fous
- Documenter toute décision structurante dans `docs/decisions.md` et tracer les évolutions dans `codex_log.md`.
- Vérifier la complétude de la documentation en fin de phase macro avant de passer à la suivante.
- En cas de changement majeur de vision, réécrire `agent.md` et les contrats pour refléter le nouvel accord produit/technique.
- Maintenir la roadmap Phase 4 (Ultimate) et les fiches `docs/specs/api_phase_4.md`, `docs/specs/ux_phase_4.md`, `docs/specs/planning_simple_v1.md` en cohérence avec le code et la CI.

## Spec visuelle & synchronisation
- Maintenir la spécification visuelle maître `docs/blueprint/03_ux_ui_planning.md` comme source de vérité UX/UI.
- Lorsqu'une nouvelle vue ou interaction majeure est ajoutée, enrichir la spec et mettre à jour les index (`docs/INDEX.md`, `docs/blueprint/INDEX.md`).
- S'assurer que les autres agents référencent cette spec dans leurs guides et que les liens restent à jour.
