Cette spécification décrit la vue planning minimale livrée en Phase 4.3 et consolidée en Phase 4 Ultimate.

## Objectifs
- Permettre aux responsables de visualiser les missions et shifts sur une grille jour/semaine.
- Ouvrir une modale de détail pour ajuster mission ou shift sans naviguer.
- Garantir des états clairs : chargement, vide, erreur.
- Colorer les missions par lieu et afficher les collaborateurs affectés comme badges.

## Scénarios couverts
1. **Affichage jour/semaine** : liste des missions par site avec leur fenêtre horaire et statut.
2. **Modale de mission** : clic sur une mission ouvre un panneau permettant d'éditer statut, note, horaires et d'ajuster un shift lié.
3. **Mise à jour rapide** : PATCH mission/shift depuis la modale, avec rechargement des listes.
4. **États UI** :
   - Chargement : skeleton/texte indiquant la récupération des missions.
   - Vide : message guidant la création de missions.
   - Erreur : bannière avec le message d'API.

## Schéma ASCII (frontend)
```
[Toolbar période] [Filtre site]
-------------------------------
| Site A | Mission #1 (09:00-12:00) [click -> modal]
|        | Shift: Jane (09:00-10:00)
| Site B | (vide)
-------------------------------
```

## Schéma ASCII (backend in-memory)
```
Organizations -> Sites -> Missions -> Shifts
      |             |          |         \
      |             |          |          -> Collaborators
      |             |          -> Roles
      -> Roles
```

## API utilisées
- `GET /api/v1/missions` (planning initial)
- `GET /api/v1/sites`
- `GET /api/v1/collaborators`
- `GET /api/v1/shifts`
- `PATCH /api/v1/missions/{id}` (ajustement horaires/statut/note)
- `PATCH /api/v1/shifts/{id}` (ajustement collaborateur/horaires/statut)

## Limitations reconnues (v1)
- Pas de drag & drop ; les ajustements se font via la modale.
- Pas de gestion avancée des chevauchements visuels (liste simple).
- Pas de filtres multiples ou de recherche par collaborateur.

## Tests attendus
- Ouverture de la modale depuis le planning.
- Gestion des états vide/erreur/chargement.
- Validation backend : cohérence site/rôle/organisation, fenêtres temporelles, chevauchements de shifts rejetés.
