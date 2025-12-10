Step 03 – Architecture Backend et API Planning PRO (V1 connectée)
Objectifs

Brancher réellement les modèles et services Planning PRO aux endpoints API.

Activer les premières validations métier (règles dures, collisions, disponibilité).

Retourner au front de vrais shifts, assignments, conflits et statuts.

Préparer auto assign v1 comme job asynchrone (endpoint et squelette), sans encore implémenter l heuristique complète.

1. Architecture backend (V1 opérationnelle)
1.1 Endpoints à exposer (/api/v1/planning/*)

Les endpoints suivants doivent être exposés côté backend FastAPI, en s appuyant sur les modèles et services créés en Step 02 (missions, templates, instances, assignments, disponibilités, règles HR, audit, etc.) :

Domaine	Endpoint	Méthode	Fonction principale
Templates	/shift-templates	GET, POST, PUT, DELETE	CRUD des modèles de shifts
Instances	/shifts	GET, POST, PUT, DELETE	CRUD des instances de shifts (brouillon, publié, annulé)
Assignments	/assignments	POST, PUT, DELETE	Assignations manuelles ou proposées (proposed, confirmed, etc.)
Disponibilités	/availability	GET	Lecture des disponibilités d un collaborateur / d une équipe
Règles	/rules	GET	Renvoyer les règles HR et de conflits actives
Conflits	/conflicts/preview	POST	Calculer et renvoyer les conflits sur un payload de planning
Publication	/publish	POST	Publier un planning et enregistrer l audit associé
Auto assign	/auto-assign/start	POST	Lancer un job d auto assign (v1, squelette)
Auto assign	/auto-assign/status/{job_id}	GET	Consulter l état du job (couverture, conflits, logs)

Les contrôleurs FastAPI doivent déléguer la logique métier à des services Planning PRO dédiés (créés en Step 02) et non pas tout implémenter dans les routes.

1.2 Contrats de base (payloads et réponses)

Les schemas Pydantic Planning PRO doivent être alignés avec la migration Alembic de référence (Step 02). Les réponses d écriture (POST / PUT) sur les shifts et assignments doivent inclure:

{
  "shift": { /* ou "assignment": {...} */ },
  "conflicts": [
    {
      "type": "hard",
      "rule": "double_booking",
      "details": {}
    }
  ]
}


Le type de conflit (type) doit au minimum distinguer hard vs soft.

2. Logique de validation (V1)
2.1 Validation générale

Pour chaque shift et assignment, appliquer au minimum:

start < end

Le shift est lié à un site, un rôle et une équipe cohérents (références valides)

Statut du shift dans {draft, published, cancelled}

2.2 Règles dures (erreurs)

Les règles suivantes doivent remonter des erreurs (hard) :

Double booking d un collaborateur (overlap horaire sur des shifts différents)

Repos minimal non respecté entre deux shifts d un même collaborateur

Collaborateur sans compétence requise pour le rôle

Collaborateur en absence / leave

Capacité site / team dépassée pour une contrainte indiquée comme « hard »

2.3 Règles souples (warnings)

Les règles suivantes doivent remonter des avertissements (soft) :

Dépassement des plafonds d heures (jour / semaine / mois) considérés comme « soft »

Shift hors plage de disponibilité déclarée

Manque de pause recommandée selon la durée du shift

Capacité site / team dépassée mais marquée comme « soft »

Les warnings ne doivent pas bloquer l enregistrement, mais doivent être présents dans la liste conflicts.

3. Audit et journalisation (planning_change)
3.1 Actions auditées

Chaque action écriture sur le planning doit créer une entrée d audit planning_change (ou équivalent déjà présent en Step 02) pour:

Création / mise à jour / annulation de shift

Création / mise à jour / suppression d assignment

Publication d un planning (appel à /publish)

3.2 Format minimal d audit

L entrée d audit doit au minimum contenir:

user_id

action (par exemple: create_shift, update_shift, cancel_shift, assign_collaborator, publish_planning)

before (état avant, éventuellement null sur création)

after (état après)

timestamp (UTC)

4. Frontend : intégration API dans la Timeline V2
4.1 Connexion aux endpoints via React Query

La page Planning PRO (par exemple PlanningProPage) ne doit plus reposer sur des mocks : elle doit consommer les API suivantes:

GET /api/v1/planning/shifts

GET /api/v1/planning/assignments

GET /api/v1/planning/rules

POST /api/v1/planning/conflicts/preview (pour prévisualiser les conflits lors d une modification locale)

Les hooks / services front existants doivent être réutilisés ou étendus, en respectant les patterns du projet (fichiers de clients API existants).

4.2 Affichage des conflits et des statuts

Sur la timeline V2:

Afficher les shifts réels provenant du backend.

Pour chaque shift, afficher:

les assignments (collaborateurs affectés),

les badges / surlignages de conflits (hard vs soft),

le statut du shift (draft, published, cancelled).

Si un assignment est marqué comme proposed (issu d auto assign), l afficher avec un indicateur visuel « proposé » et, si disponible, un score.

Dans un premier temps, auto assign v1 peut être simulé / mocké côté backend, mais les endpoints doivent exister et renvoyer un payload cohérent avec la structure attendue.

5. Documentation à mettre à jour

Mettre à jour docs/architecture.md (ou équivalent) pour décrire:

Les nouveaux endpoints /api/v1/planning/*,

Le flux UI -> API -> DB pour Planning PRO (timeline V2 + audit).

Mettre à jour docs/blueprint/planning_pro*.md pour refléter que:

La timeline V2 consomme désormais de vrais endpoints,

Les conflits et statuts sont visibles en temps réel.

Mettre à jour docs/roadmap/phase5/index.md pour:

Marquer la Step 03 comme « en cours » puis « done »,

Lier step-03.md dans la liste des steps Planning PRO.

6. Critères de validation Step 03

Les endpoints /api/v1/planning/* existent et sont branchés aux services Planning PRO.

Au moins un test backend par endpoint critique (shifts, assignments, publish, conflicts/preview).

La timeline V2 n utilise plus de mocks mais la vraie API.

Les conflits sont renvoyés par l API et visibles dans l UI.

Les actions de modification planning créent bien des entrées d audit.

La CI GitHub Actions reste verte.

Backend – Implementation Planning PRO

Localiser les modules backend existants pour Planning PRO:

Modeles SQLAlchemy (missions, shift templates, shift instances, assignments, availability, rules, audit).

Schemas Pydantic correspondants.

Services skeleton crees en Step 02 (templates, instances, assignments, availability, rules, audit, auto assign job).

Creer / completer les routes FastAPI sous le prefixe /api/v1/planning avec:

Les endpoints de CRUD pour templates et shifts.

La gestion des assignments (proposed, confirmed, etc.).

Le calcul des conflits (règles dures et souples) dans un service dedie (pas en ligne dans les routes).

La publication et l ecriture dans la table d audit.

Ajouter ou completer les tests backend pour:

Creation / modification de shift avec detection d au moins un type de conflit (double booking).

Validation du statut (draft / published / cancelled).

Creation d une entree d audit planning_change lors d une modification.

Frontend – Integration Timeline V2

Localiser la page / composant principal Planning PRO (par ex. PlanningProPage).

Remplacer toute dependance aux mocks par des appels a l API via React Query.

Ajouter l affichage:

Des shifts et assignments reels,

Des conflits par shift (badges / surlignages),

Des statuts des shifts,

Des assignments proposes (si presents) avec un indicateur.

Ajouter des tests frontend (unitaires / component / integration) pour verifier:

Qu un jeu de donnees renvoye par l API s affiche correctement dans la timeline.

Que la presence de conflits se traduit par des badges / indicateurs visibles dans le DOM.

Documentation

Mettre a jour:

docs/roadmap/phase5/step-03.md (contenu ci-dessus, coherent avec Step 02).

docs/roadmap/phase5/index.md pour lier la step.

docs/architecture*.md pour exposer le flux Planning PRO.

Le blueprint Planning PRO pour noter que la timeline consomme maintenant la vraie API.

Nettoyage et coherence

Verifier les noms de fichiers, routes et schemas pour eviter les doublons ou anciennes versions Planning.

S assurer que la migration Alembic Planning PRO reste la reference et qu aucun changement de schema n est introduit dans Step 03 (Step 03 ne doit pas changer le schema DB, uniquement l architecture API et la logique).

ACCEPTANCE:

docs/roadmap/phase5/step-03.md existe et decrit clairement les objectifs, l architecture, la validation, l audit, le frontend et les criteres de validation.

Tous les endpoints /api/v1/planning/* listes dans la fiche sont exposes dans le backend FastAPI, avec des schemas Pydantic coherents.

Les validations de base (start < end, status, double booking) sont en place et testees.

Les ecritures sur le planning (shift, assignment, publish) creent des entrees d audit consultables en base ou via un service.

La page Timeline V2 (Planning PRO) consomme l API (plus de mocks) et affiche:

Shifts reels,

Assignments reels,

Conflits,

Statuts de shifts,

Assignments proposes si disponibles.

Les tests backend passent, incluant au moins une suite de tests pour les endpoints Planning PRO.

Les tests frontend pertinents pour la timeline passent.

Toute la CI GitHub Actions est verte.

La documentation architecture / roadmap / blueprint est a jour et liee a Step 03.

TESTS:

Backend:

pytest -q (ou la commande de tests backend specifique du projet, apres l avoir identifiee dans les scripts existants).

Frontend:

npm run lint

npm run test -- --watch=false

Global:

Lancer les scripts de test de repo si des scripts PowerShell / Bash globaux existent (par exemple scripts/dev/test_all.ps1 ou equivalent).
