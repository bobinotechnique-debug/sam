# UX Phase 4 — CRUD + Planning simple

Cette note synthétise les écrans Phase 4 (CRUD + planning) avec un design system minimal.

## Design system v4
- Couleurs : fond `slate-950/900`, accents `indigo-400`, badges `emerald/amber/red` selon statut.
- Typo : titres `font-semibold`, petites capitales pour labels secondaires.
- Spacing : grille 4/8/12/16 px, cartes arrondies `rounded-xl`, bordures `border-slate-800`.
- Composants :
  - **Button** (primaire + ghost) avec états désactivé/chargement.
  - **Card** pour sections (planning semaine, fiches CRUD).
  - **Modal** pour création/édition mission/shift avec actions dans le footer.
  - **Table** responsive (overflow-x) avec colonnes compactes.
  - **Tag/Badge** pour statuts (draft/published/cancelled, confirmed/pending).
  - **Form controls** : inputs, select, textarea, validation inline.

## Vues CRUD renforcées
- Listes : header avec titre + bouton "Créer", états vide/erreur/chargement explicites.
- Formulaires : validations frontend (champs obligatoires, formats date/heure) et message d'erreur API.
- Suppression : confirmation modale avant `DELETE`.

## Planning simple (Jour/Semaine)
- Toolbar : sélection mode, navigation date, refresh.
- Timeline horaire configurable (`PLANNING_START_HOUR`/`PLANNING_END_HOUR`).
- Affichage : missions groupées par **lieu** avec badges d'affectation (collaborateurs associés).
- Interactions : clic ouvre la modale mission (édition mission + shifts), refresh après sauvegarde.
- Couleurs : survol mission → halo indigo, missions par lieu séparées par cartes.
- Limitations connues : pas de drag & drop natif, chevauchement affiché en pile simple.

## Schéma ASCII (Planning semaine)
```
[Toolbar]
Site A
  Lun | [Mission A 08-12] [Mission B 14-18]
  Mar | [Mission C 10-16]
Site B
  Lun | (vide)
```

## Tests UI attendus
- Vitest : états loading/empty/error sur listes CRUD, ouverture modale planning.
- Interaction : mise à jour mission + shift via modale, rafraîchissement du planning.
