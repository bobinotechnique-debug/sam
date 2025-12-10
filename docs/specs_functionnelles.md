# Spécifications fonctionnelles

## Vision produit
Plateforme SaaS de planning multi-sites pour organiser des missions et shifts d'équipes (intermittents, retail, exploitation multi-sites).
Elle doit fluidifier la collaboration entre responsables planning, managers de site et collaborateurs, avec une traçabilité claire et des notifications futures.

## Personas et responsabilités
- **Responsable planning** : structure les organisations et sites, définit les rôles/compétences, planifie à l'échelle multi-sites.
- **Manager de site** : gère le staffing local (affectations, indisponibilités), valide les changements et suit les coûts/temps.
- **Collaborateur** : consulte son planning, confirme la disponibilité (futur), signale des indisponibilités.

## Domaines métier
- **Organisations & sites** : entités hiérarchiques, horaires d'ouverture, fuseaux horaires, paramètres de coût.
- **Collaborateurs** : identité, coordonnées, rôles/compétences, statut et contrat (temps de travail, rémunération future).
- **Rôles & compétences** : référentiel commun pour planifier et filtrer les affectations.
- **Missions** : besoins planifiés (date, site, rôle requis, volume horaire, budget cible).
- **Shifts / affectations** : créneaux attribués à un collaborateur sur une mission, avec état (brouillon, confirmé, annulé).
- **Disponibilités/indisponibilités** : calendrier des contraintes collaborateur (prévu Phase 3+).

## Parcours utilisateur courts terme (Phase 2-3)
- **Gestion du référentiel** : créer/éditer/supprimer organisations, sites, rôles/compétences, collaborateurs.
- **Gestion des missions** : créer une mission avec rôle requis, date/heure et site associé ; lister/filtrer par site/période/statut.
- **Planification des shifts** : affecter un collaborateur à une mission, ajuster horaires, changer le statut, annuler une affectation.
- **Consultation planning** : vues Jour/Semaine/Mois par site et par personne ; recherche par rôle ou compétence.
- **Qualité de données** : validation des champs (horaires cohérents, rôles obligatoires, site requis, doublons évités).

## Exigences fonctionnelles immédiates (Phase 1)
- Documentation fondatrice alignée sur le périmètre (présent fichier + `specs_techniques.md`, `architecture.md`, `roadmap.md`).
- Description des domaines métier prioritaires et des parcours cibles pour préparer le bootstrap technique.
- Critères d'acceptation formalisés pour les futures livraisons (CI, sécurité, doc synchronisée).

## Règles métier clés (préparatoires)
- Un shift appartient à une mission et à un site ; un collaborateur ne peut avoir deux shifts qui se chevauchent sur le même créneau.
- Les horaires sont stockés en UTC et présentés dans le fuseau du site.
- Les missions définissent un rôle/compétence requis ; seules les personnes compatibles peuvent être affectées (vérification côté service).
- Statuts prévus : `draft`, `confirmed`, `cancelled`. Une annulation conserve l'historique (audit ultérieur).

## Critères d'acceptation transverses
- **Documentation** : chaque évolution de périmètre met à jour `docs/` et `agent.md` avant code.
- **Qualité** : tests automatisés pour chaque parcours ajouté (API + front) et CI verte obligatoire pour merger.
- **Sécurité** : aucun secret en clair ; validation d'entrée stricte et logs structurés d'erreur/acquisition.
