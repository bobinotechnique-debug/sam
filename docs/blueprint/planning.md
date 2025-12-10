# Planning PRO – Foundations (Phase 5 Step 02)

## Modèle de données (résumé)
- **Référentiel** : organisations, sites, équipes (`team`), rôles et compétences avec liens `role_skills` et `collaborator_skills`.
- **Utilisateurs & collaborateurs** : `user` (identité) relié à `collaborator` (statut, rôle principal, compétences, disponibilités, absences).
- **Missions & planning** : `mission` (site, rôle, budget, fenêtre UTC) ➜ `shift_template` (récurrence, effectif, active) ➜ `shift_instance` (brouillon/publié, capacité, source) ➜ `assignment` (statut proposé/confirmé, verrou, origine).
- **Disponibilités & contraintes** : `user_availability`, `leave`, `blackout` (site/org), `hr_rule` (max heures, repos, pauses) et `conflict_rule` (double booking, capacité, skills).
- **Audit & publication** : `planning_change` (actions horodatées), `publication` (versioning brouillon/publié, message), `notification_event` (alertes suite à conflits ou publication).

## Relations clés
- 1↔N `organization` ➜ `site`/`team`/`role`/`skill`/`collaborator`.
- 1↔N `mission` ➜ `shift_template` ➜ `shift_instance` (avec source template ou ad-hoc) ➜ `assignment`.
- `assignment` contrôlé par `user_availability`/`leave`/`blackout` et évalué par `hr_rule` + `conflict_rule` (erreur vs warning).
- `publication` capture un scope de `shift_instance`/`assignment`, journalisé dans `planning_change`, avec notifications associées.

## UI Planning PRO V2 (structures préparées)
- **Page Planning PRO** : timeline V2 (zoom jour/semaine), panneau filtres/collaborateurs, panneau conflits + actions publication/auto-assign.
- **Timeline V2** : lignes par site/équipe, badges statut (draft/warning/error/published), couleurs d’équipe, en-tête pour zoom/snapping/mode highlight.
- **Panneau Conflits** : zone dédiée aux erreurs/avertissements (ancres timeline, export CSV/JSON prévu).
- **Préparation interactions** : TODO Step 06/07 pour drag/drop, redimensionnement, assignation depuis la liste latérale et surface temps réel des règles.
- **Connexion API (Step 03)** : la timeline consomme `GET /api/v1/planning/shifts` et affiche assignments, conflits hard/soft et statuts réels ; les badges « proposé » reflètent les assignments issus d auto-assign.

## API & services (squelettes)
- Endpoints prévus : configuration Planning PRO (`hr_rule`/`conflict_rule`), liste/CRUD `shift_template`, `shift_instance`, `assignment`, publication.
- Services squelettes créés pour templates, instances, assignments, disponibilités, règles, audit/publication (logique à compléter Step 03+).

Source de vérité fonctionnelle : `docs/roadmap/phase5/step-02.md`.
