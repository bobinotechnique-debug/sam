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
- Garantir la vue `/planning` (jour/semaine) : toolbar de période, grille temporelle par lieu, affichage des affectations (shifts), modale d'édition synchronisée avec l'API missions+shifts.

## MVP Planning Core – Phase 4.x
- **Tests** : assurer des scénarios Vitest couvrant navigation CRUD et vue planning (états vide/erreur/chargement, ouverture modale, mises à jour mockées).
- **Qualité** : `npm run lint` et `npm run test` obligatoires avant merge (parité avec GitHub Actions).
- **UX** : supprimer les logs de debug, conserver la cohérence avec le blueprint `docs/blueprint/03_ux_ui_planning.md` et documenter les limitations restantes.
  - Références phase 4 : `docs/roadmap/phase-04.md` (sous-phases, objectifs) et `docs/specs/planning_simple_v1.md` (planning v1, états UI).

## Processus et garde-fous
- Aucun ajout UI sans maquette, user flow ou spécification validée ; arrêter en fin de phase macro.
- Noter dans `codex_log.md` les évolutions impactant l'expérience utilisateur ou la navigation.
- Vérifier la cohérence des conventions (naming, Tailwind) avec `docs/conventions.md` avant de livrer.
- Pour la phase 4.2, livrer des écrans CRUD basiques (liste/formulaire/suppression avec confirmation) pour organisations, collaborateurs, sites et missions avant d'attaquer le planning visuel (phase 4.3).

## Sources de vérité UX/UI
- Spécification visuelle maître : `docs/blueprint/03_ux_ui_planning.md` (écrans, interactions, responsive, composants fonctionnels).
- Avant de créer ou modifier un écran React, vérifier qu'il est décrit dans cette spec ; si manquant, proposer une mise à jour.
- Couvrir dans Storybook ou équivalent les états mentionnés (chargement, vide, erreurs, conflits) et aligner les couleurs/états avec la légende de la spec.
- Toute divergence observée doit être corrigée ou documentée dans la spec avant merge.
- Pour la vue planning simple (Phase 4.3), documenter les limites (pas de drag & drop avancé, chevauchements empilés) et lier toute évolution au fichier `docs/specs/planning_v1_simple.md`.
