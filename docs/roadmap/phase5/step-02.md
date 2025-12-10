# Phase 5 – Step 02 – Planning PRO specification

- **Statut** : done
- **Date** : 2025-12-31
- **Responsable** : Codex (agents)

## Objectifs
- Formaliser la cible Planning PRO avant architecture/implémentation.
- Définir le modèle de données cible (entities/relations) couvrant missions, shifts, règles RH et disponibilités.
- Cadrer la V2 des interactions UI (timeline, drag/resize, filtrage, conflits) pour la future implémentation React.
- Lister les règles de détection de conflits et contraintes RH à supporter en backend + UI.
- Poser la version initiale de l'auto-assign (heuristique de base) et ses exigences d'API/observabilité.

## Livrables
- Spécification modèle de données cible : entités, relations et attributs clés.
- Catalogue des interactions UI V2 (desktop/tablette) incluant comportements, états et feedback utilisateurs.
- Règles de conflits et contraintes RH priorisées + attentes de restitution (warning/erreur, surfaces UI).
- Auto-assign v1 : périmètre fonctionnel, inputs/outputs et principes de calcul.

## Modèle de données cible (Planning PRO)
- **Organisation & référentiels** : `organisation`, `site`, `team` (équipes/couleurs), `role` + `skill` (compétences), `user`, `collaborator` (lien user/contrat/compétences).
- **Missions & modèles** : `mission` (description, site, rôles requis, budget/plafond heures) ; `shift_template` (récurrence, durée, rôle demandé, effectif attendu, site/team) ; `shift_instance` (créé depuis template ou ad-hoc, statut brouillon/publié, source).
- **Affectations** : `assignment` (shift_instance ↔ collaborateur, statut proposé/confirmé, source auto-assign/manuelle, horodatage, commentaires) ; `assignment_lock` (verrou d’édition/publication).
- **Disponibilités & absences** : `user_availability` (périodes disponibles/indisponibles, motifs), `leave` (congés/arrêts), `blackout` (périodes interdites par site/organisation), `capacity_override` (surbooking autorisé).
- **Contraintes & règles** : `hr_rule` (types : max heures jour/semaine/mois, repos min entre shifts, pause obligatoire, interdiction nocturne, limites rôle/site) ; `conflict_rule` (double booking, chevauchement même lieu, dépassement capacité site, non-respect compétences, chevauchement pause).
- **Audit & workflow** : `planning_change` (journal modifications), `publication` (versioning brouillon/publié, auteur, message), `notification_event` (alertes issues d’un conflit ou publication).
- Relations clés :
  - `mission` 1↔N `shift_template`; `shift_template` génère N `shift_instance` (via calendrier ou duplication unique).
  - `shift_instance` N↔N `role` via besoins (nombre de postes) ; `assignment` assure l'association d'un collaborateur sur un poste précis.
  - `assignment` dépend des disponibilités (`user_availability`, `leave`) et est contrôlé par `hr_rule`/`conflict_rule` avec statut de validation.
  - `publication` référence un ensemble de `shift_instance`/`assignment` versionnés ; `planning_change` journalise toutes transitions.

## Interactions UI V2 (desktop/tablette)
- **Timeline** : zoom jour/semaine, scroll horizontal avec virtualisation, groupement par site ou collaborateur, segments colorés par team/role ; affichage des labels (mission, rôle, statut, conflit) et handles de redimensionnement.
- **Création/édition** : double-clic ou drag sur plage vide pour créer un shift (default duration & role pré-remplis par template) ; édition inline (titre, rôle, team, site, notes) + modale avancée (répétition, contraintes, publipostage).
- **Drag & drop** :
  - Déplacer un shift sur une autre plage en conservant la durée ; snap aux pas configurables (15/30/60min) ; multi-jour autorisé (segment étendu sur plusieurs jours avec chevauchement visuel).
  - Copier-coller/duplication avec ALT + drag ; annulation (Ctrl/Cmd+Z) et redo.
  - Glisser un collaborateur depuis la liste latérale vers un slot libre ou un shift sélectionné pour créer/mettre à jour une assignment.
- **Redimensionnement** : handles sur bords pour ajuster début/fin avec snap ; respect des contraintes (repos min, pauses, capacité lieu) : avertissement en temps réel + blocage si règle dure.
- **Filtres & recherche** : par site, team, rôle, collaborateur, statut (brouillon/publié), conflits ; mode « highlights » pour afficher uniquement les éléments en erreur/avertissement.
- **Conflits UI** : badges et contours colorés (warning/erreur), panneau latéral listant les conflits triés (avec ancre vers shift) ; affichage des règles violées (type, règle, seuil, suggestion fix).
- **Accessibilité & clavier** : navigation clavier (tab/shift+tab entre shifts, enter pour éditer, espace pour sélectionner), raccourcis pour zoom, duplication, assignation rapide.
- **Collaboration** : indicateur de verrou (assignment_lock) lorsqu’un autre utilisateur édite/publie ; mode brouillon vs publié visible (bandeau, couleur de fond) ; bouton de publication avec résumé des deltas.

## Règles de conflits & contraintes RH
- **Conflits d’agenda** : double booking collaborateur, chevauchement de shifts pour un même site/role, dépassement capacité site/team, non-respect des skills requis, collision avec blackout site.
- **Repos & limites horaires** : repos minimal entre shifts (paramétrable), max heures par jour/semaine/mois, limites de nuit/jours fériés, pauses obligatoires selon durée/role, durée max shift.
- **Statuts & sévérité** :
  - *Erreur bloquante* : double booking, dépassement repos minimal, absence/leave, absence de compétence obligatoire, dépassement capacité dure.
  - *Avertissement* : dépassement plafond soft (heures, capacité souple), shift hors plage de disponibilité déclarée, manquement pause recommandée.
- **Surfacing** : calcul en temps réel côté front (prévalidation) + validation backend lors de sauvegarde/publication ; panneau de conflits avec filtres ; surligne local sur la timeline ; exportable en CSV/JSON pour audit.
- **Résolution** : suggestions de fixes (changer collaborateur, décaler horaire, ajouter pause) ; option « forcer » pour règles soft avec justification (loggée dans `planning_change`).

## Auto-assign v1 (heuristique de base)
- **Entrées** : liste des shifts (brouillon), collaborateurs éligibles (skills/roles, sites, teams), disponibilités/absences, contraintes HR (repos, max heures), préférences simples (site favori, équipes assignables), poids de priorisation.
- **Principe** : heuristique gloutonne par priorité :
  1. Trier les shifts par criticité (statut publié imminent, début le plus proche, rôle rare) ;
  2. Pour chaque shift, sélectionner les collaborateurs disponibles correspondant aux compétences/sites ; filtrer par repos/absences ;
  3. Classer les candidats par score : affinité site/team, charge actuelle (heures semaine), continuité de mission, préférence déclarée ;
  4. Assigner le meilleur candidat en marquant l’origine « auto-assign v1 » ;
  5. Reporter les conflits éventuels (aucun candidat, dépassement plafond soft) avec statut warning.
- **Sorties** : assignments proposées (statut « proposé ») avec score, justification (règles appliquées), indicateur de confiance ; métriques d’exécution (nb shifts traités, taux de couverture, conflits rencontrés).
- **Exigences techniques** : endpoint backend dédié (asynchrone) avec idempotence via `job_id`, logs structurés, métriques Prometheus (durée, couverture, conflits) et possibilité d’annuler un job.
- **Limites connues** : pas de planification multi-objectif ni optimisation globale ; préférences avancées et contraintes contractuelles complexes repoussées à la v2.

## Actions réalisées (Step 02)
- **Backend** : ajout des modèles SQLAlchemy complets (missions, templates, instances, assignments, disponibilités, règles HR/conflits, audit/publications/notifications) avec migration Alembic « Planning PRO foundations » et schemas Pydantic alignés.
- **Services** : création des squelettes de services (templates, instances, assignments, disponibilités, règles, audit/publications) pour préparer la logique métier et l’auto-assign v1.
- **Frontend** : nouveaux types TypeScript et clients API placeholders (config planning, templates/instances/assignments) + page `PlanningProPage` avec timeline V2 mock, panneau filtres et zone conflits.
- **Documentation** : blueprint Planning PRO synthétisée, architecture enrichie (flux UI ↔ API ↔ DB) et cette fiche mise à jour.

## Points de contrôle qualité
- La migration Alembic doit rester la référence des tables Planning PRO ; tout changement ultérieur nécessite un nouvel incrément de version.
- Les validations temporelles (start < end) et statuts (draft/published/cancelled, proposed/confirmed) doivent être conservées dans les services et API.
- Les vues front doivent continuer à différencier brouillon/publié et surfaces de conflits (badges, panneau dédié) ; accessibilité clavier à maintenir dans les futures interactions.

## Préparation Step 03
- Exposer les endpoints `/api/v1/planning/*` en branchant les services squelettes (templates, instances, assignments, config règles, publications).
- Débuter la logique de validation (règles dures/soft, collisions de disponibilité, locks d’assignments) et l’enregistrement d’audit `planning_change`.
- Enrichir la timeline V2 avec de vrais fetch (React Query) et premiers retours de conflits/auto-assign (statut proposé + score).
