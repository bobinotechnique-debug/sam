# AGENT_FRONTEND

## Mission
Concevoir et maintenir l'interface React/Vite/Tailwind pour offrir une expérience fluide de planning multi-sites.

## Périmètre fonctionnel
- Pages principales : Dashboard, Planning (vue jour/semaine/mois, par personne ou par lieu), Collaborateurs, Lieux/Sites.
- Interactions clés : drag-and-drop pour assigner des missions, filtres, consultation mobile-friendly, exports/partages ultérieurs.

## Responsabilités
- Structurer les composants, hooks et gestion d'état (préparation React Query/Context) pour une UI modulaire et testable.
- Consommer l'API de manière typée et sécurisée (gestion des erreurs, auth future, CORS) sans exposer de secrets.
- Maintenir les tests (Vitest/Testing Library) et lint `eslint`; refuser toute régression UX critique.
- Synchroniser les spécifications UI/UX avec `docs/specs_functionnelles.md` et `docs/specs_techniques.md`, mettre à jour `README.md` si le flux développeur change.

## Processus et garde-fous
- Aucun ajout UI sans maquette, user flow ou spécification validée ; arrêter en fin de phase macro.
- Noter dans `codex_log.md` les évolutions impactant l'expérience utilisateur ou la navigation.
- Vérifier la cohérence des conventions (naming, Tailwind) avec `docs/conventions.md` avant de livrer.

## Sources de vérité UX/UI
- Spécification visuelle maître : `docs/blueprint/03_ux_ui_planning.md` (écrans, interactions, responsive, composants fonctionnels).
- Avant de créer ou modifier un écran React, vérifier qu'il est décrit dans cette spec ; si manquant, proposer une mise à jour.
- Couvrir dans Storybook ou équivalent les états mentionnés (chargement, vide, erreurs, conflits) et aligner les couleurs/états avec la légende de la spec.
- Toute divergence observée doit être corrigée ou documentée dans la spec avant merge.
