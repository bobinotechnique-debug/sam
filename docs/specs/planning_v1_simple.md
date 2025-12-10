# Planning visuel simple (Phase 4.3)

## Objectif
Première vue planning opérationnelle pour afficher et mettre à jour les missions par lieu, en modes jour et semaine, avec affectations visibles.

## Layout retenu
- Toolbar : sélection mode (Jour/Semaine), navigation par période, bouton rafraîchir.
- Grille : groupement par **lieu**, heures affichées de 06:00 à 02:00 (configurable dans `PLANNING_START_HOUR` / `PLANNING_END_HOUR`).
- Mode jour : une ligne par lieu, timeline horizontale avec missions empilées en cas de chevauchement.
- Mode semaine : section par lieu, sous-sections par jour (lundi-dimanche) réutilisant la timeline horaire.

## Interactions supportées
- Clic sur une mission → ouverture d'une modale détaillant horaire, lieu et collaborateurs.
- Modifications possibles :
  - Heure de début/fin (UTC)
  - Lieu de la mission
  - Affectations collaborateurs (création/suppression de shifts + alignement des heures sur la mission)
- Sauvegarde : PATCH mission puis créations/mises à jour/suppressions de shifts. Rafraîchissement du planning après succès.
- Erreurs backend : affichées dans la modale ou au-dessus de la grille.

## Mapping API
- Missions : `/api/v1/missions` (liste) et `PATCH /api/v1/missions/{id}` pour les mises à jour.
- Lieux : `/api/v1/sites` (liste) pour les libellés.
- Collaborateurs : `/api/v1/collaborators` (liste) pour les affectations.
- Affectations (shifts) :
  - GET `/api/v1/shifts` pour charger les collaborateurs par mission.
  - POST `/api/v1/shifts` pour ajouter un collaborateur à la mission (heures alignées sur la mission).
  - PATCH `/api/v1/shifts/{id}` pour synchroniser les heures en cas de changement d'horaire.
  - DELETE `/api/v1/shifts/{id}` pour retirer un collaborateur.

## Limites connues
- Pas de drag & drop ni redimensionnement : les déplacements se font via la modale uniquement.
- Gestion des chevauchements simplifiée : empilement vertical sans détection visuelle des conflits complexes.
- Fuseau horaire : affichage basique en UTC/local selon le navigateur, sans paramétrage par organisation pour l'instant.
- Pas encore de filtres avancés (rôle, statut, organisation) ni de vue mobile dédiée.
