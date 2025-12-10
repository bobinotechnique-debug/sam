# Spécifications fonctionnelles

## Vision produit
Plateforme SaaS de planning multi-sites pour organiser des missions et shifts d'équipes (intermittents, retail, exploitation multi-sites).
Elle doit fluidifier la collaboration entre responsables planning, managers de site et collaborateurs, avec une traçabilité claire et des notifications futures.

### Enjeux prioritaires
- Unifier la donnée de planification (organisations, sites, référentiels de rôles) et éviter les doublons.
- Garantir la cohérence horaire multi-fuseaux (saisie locale, stockage UTC) et la visibilité consolidée des affectations.
- Préparer l'exposition d'API claires pour itérer rapidement sur le front et les intégrations futures.
- Sécuriser l'accès par rôle et par organisation dès les premières API pour éviter la dette d'autorisation.
- Rendre les validations explicites (formats, fuseaux, chevauchements) afin d'alimenter les schémas front dès le bootstrap.

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

### Hypothèses de périmètre (Phase 1)
- Multi-organisation dans un même schéma, sans partage d'entités entre organisations (filtrage obligatoire dans les parcours et API).
- Les contraintes réglementaires (durée légale, repos) ne sont pas modélisées en Phase 1 ; elles seront traitées en Phase 4+.
- Les notifications et exports restent hors périmètre court terme mais doivent être anticipées dans les modèles (champs de statut, timestamps, notes internes).

### Attributs cibles par domaine (Phase 2-3)
- **Organisation** : nom, fuseau horaire par défaut, paramètres de coût (monnaie, taux horaire moyen), contact administratif.
- **Site** : organisation associée, nom, fuseau, adresse, horaires d'ouverture, capacité maximale par rôle (optionnel).
- **Rôle/compétence** : libellé, description, tags de compétences requis, niveau minimum éventuel.
- **Collaborateur** : identité, coordonnées, rôle principal, compétences, statut (actif/inactif), contrats/quotas hebdomadaires (optionnel).
- **Mission** : site, rôle requis, période (début/fin), budget cible, état (`draft`/`published`), note interne.
- **Shift** : mission, collaborateur, horaires début/fin, statut (`draft`/`confirmed`/`cancelled`), commentaire/raison d'annulation.

## Parcours utilisateur courts terme (Phase 2-3)
- **Gestion du référentiel** : créer/éditer/supprimer organisations, sites, rôles/compétences, collaborateurs.
- **Gestion des missions** : créer une mission avec rôle requis, date/heure et site associé ; lister/filtrer par site/période/statut.
- **Planification des shifts** : affecter un collaborateur à une mission, ajuster horaires, changer le statut, annuler une affectation.
- **Consultation planning** : vues Jour/Semaine/Mois par site et par personne ; recherche par rôle ou compétence.
- **Qualité de données** : validation des champs (horaires cohérents, rôles obligatoires, site requis, doublons évités).

### Parcours critiques détaillés (Phase 2)
1. **Créer une mission** : le responsable planning sélectionne un site (obligatoire), un rôle, une période et un budget ; la mission passe en `draft` tant qu'aucun shift n'est confirmé.
2. **Affecter un collaborateur** : le manager de site choisit un collaborateur compatible (même organisation, rôle/compétence requis) et définit un shift sans chevauchement ; le statut passe à `confirmed` si validé.
3. **Modifier ou annuler un shift** : un shift confirmé peut être ajusté (horaires, collaborateur) ou annulé avec motif ; l'historique d'annulation est conservé pour l'audit futur.
4. **Consulter le planning** : filtres par site/période/rôle/compétence ; affichage des statuts et fuseaux horaires locaux ; mise en avant des collisions potentielles détectées par le service.

## Exigences fonctionnelles immédiates (Phase 1)
- Documentation fondatrice alignée sur le périmètre (présent fichier + `specs_techniques.md`, `architecture.md`, `roadmap.md`).
- Description des domaines métier prioritaires et des parcours cibles pour préparer le bootstrap technique.
- Critères d'acceptation formalisés pour les futures livraisons (CI, sécurité, doc synchronisée).

### Backlog priorisé pour le bootstrap (Phase 1 ➜ 2)
1. **Référentiel organisations/sites** : CRUD + validation fuseaux horaires ; base pour filtrer tout le reste.
2. **Rôles/compétences** : CRUD + tags ; utilisé par missions/shifts pour filtrer les affectations.
3. **Collaborateurs** : CRUD + rattachement organisation ; recherche par rôle/compétence.
4. **Missions** : création/listing/filtre ; bloque la planification tant que rôle ou site manquants.
5. **Shifts** : affectation et gestion des statuts ; contrôle de chevauchement et compatibilité.

### Résultats attendus pour sortie de Phase 1
- Périmètre validé et partagé (documents synchronisés).
- Règles métier structurées pour guider les schémas Pydantic/SQL et les validations front.
- Parcours cibles listés pour alimenter les user stories du bootstrap.

### Livrables réalisés pour le bootstrap (Phase 2)
- Endpoints `/api/v1` disponibles pour le référentiel (organizations, sites, roles, collaborators, missions, shifts) avec validations de base (timezone, chevauchement des shifts, héritage du fuseau site ➜ mission/shift).
- Healthcheck exposé et consommé par le frontend pour vérifier le lien front/back dès le démarrage.
- Docker compose prêt pour lancer API + frontend + PostgreSQL, avec configuration via `.env.example`.

### Avancement Phase 4.1 – Modèle de données & API core (MVP – validée)
- CRUD REST complet pour organisation, site, collaborateur, mission/shift (affectation) avec schémas de validation dédiés.
- Règles métiers minimales : fuseaux horaires valides, cohérence organisation/site/rôle, pas de chevauchement d'affectations par collaborateur, fenêtres temporelles ordonnées.
- Journalisation des actions critiques (création, mise à jour, suppression) pour faciliter l'audit et le support.
- Tests API couvrant les parcours principaux : CRUD organisation, validations rôle/collaborateur, cohérence mission, cycle de vie d'un shift avec annulation.
- Erreurs d'API normalisées avec une enveloppe `{code, message, detail, trace_id}` et entête `X-Request-ID` renvoyé pour suivre les requêtes.
- Statut : livrables validés, feu vert pour engager l'UI CRUD basique de la phase 4.2.

### Avancement Phase 4.2 – UI CRUD basique (validée)
- Pages React dédiées pour lister et gérer organisations, sites, rôles/compétences, collaborateurs et missions/shifts avec formulaires simples (création, édition, suppression, annulation pour shifts) et validations alignées sur l'API.
- Intégration des appels API réels (chargement, succès, erreurs) avec affichage d'états explicites et gestion des erreurs normalisées côté front.
- Navigation cohérente via le layout existant (liste ➜ détail/édition), champs pré-remplis lors des éditions et messages de confirmation pour les opérations destructives.
- Alignement avec la spécification visuelle maître (`docs/blueprint/03_ux_ui_planning.md`) pour les composants de base (boutons, inputs, badges de statut) avant toute extension UX.

## Phase 5 – Planning PRO (spécification)
### Modèle de données cible
- **Référentiels** : `organisation`, `site`, `team` (couleurs), `role`, `skill`, `user`, `collaborator`.
- **Missions & modèles** : `mission`, `shift_template` (récurrence, durée par défaut, effectif attendu), `shift_instance` (issu du template ou ad-hoc, statut brouillon/publié, source).
- **Affectations & verrous** : `assignment` (statut proposé/confirmé, origine auto-assign/manuelle, commentaires horodatés), `assignment_lock` (édition/période de publication protégée).
- **Disponibilités & absences** : `user_availability` (périodes dispo/indispo), `leave` (congés/arrêts), `blackout` (interdits par site/org), `capacity_override` (surbooking consenti).
- **Contraintes & audit** : `hr_rule` (repos, plafonds d'heures, pauses obligatoires, limites rôle/site), `conflict_rule` (double booking, capacité, compétence manquante), `planning_change` (journal), `publication` (versioning brouillon/publié), `notification_event` (alertes).

### Interactions UI V2 (desktop/tablette)
- Timeline zoomable jour/semaine avec scroll horizontal virtualisé et groupement par site ou collaborateur ; segments colorés par team/rôle avec labels (mission, statut, conflit) et handles de redimensionnement.
- Création/édition rapide (double-clic ou drag sur plage vide) puis modale avancée pour les options de récurrence, contraintes et publipostage.
- Drag & drop : déplacement avec snap 15/30/60min, multi-jour autorisé, duplication via ALT+drag, undo/redo ; glisser un collaborateur depuis la liste vers un slot ou un shift sélectionné pour créer/mettre à jour une assignment.
- Redimensionnement avec validation en temps réel (repos minimum, pauses, capacité lieu) affichant avertissement ou blocage selon la sévérité de la règle.
- Filtres par site/team/rôle/collaborateur/statut/conflits et mode « highlights » pour ne montrer que les éléments en erreur/avertissement.
- Surfacing des conflits : badges/contours colorés, panneau latéral trié avec ancrage vers le shift concerné et détail de la règle violée ; navigation clavier (tab/shift+tab, enter, espace) et raccourcis (zoom, duplication, assignation rapide).
- Collaboration : indicateur de verrou `assignment_lock` lorsque quelqu'un édite/publie ; différenciation brouillon vs publié (bandeau/couleur) ; bouton de publication avec résumé des deltas.

### Règles de conflits & contraintes RH
- Conflits d’agenda : double booking collaborateur, chevauchement même site/rôle, dépassement capacité site/team, absence de compétence requise, collision avec blackout.
- Repos & limites horaires : repos minimum entre shifts, plafonds d'heures jour/semaine/mois, interdits nuit/jours fériés, pauses obligatoires selon durée/rôle, durée max de shift.
- Statuts & sévérité : erreurs bloquantes (double booking, repos minimum non respecté, absence/leave, compétence manquante, capacité dure) vs avertissements (plafond soft, dispo déclarée non respectée, pause recommandée manquante).
- Surfacing : prévalidation front en temps réel puis validation backend à la sauvegarde/publication ; panneau de conflits filtrable, surlignage local sur timeline, export CSV/JSON pour audit ; option de « forcer » une règle soft avec justification loggée.

### Auto-assign v1
- Entrées : shifts brouillon, collaborateurs éligibles (skills/roles/sites/teams), disponibilités/absences, contraintes RH (repos, max heures), préférences simples (site favori, équipes assignables), poids de priorisation.
- Heuristique : tri des shifts par criticité (publication proche, rôle rare), filtrage des candidats par compatibilité et repos/absences, scoring (affinité site/team, charge hebdo, continuité de mission, préférences déclarées), assignation du meilleur candidat en marquant l'origine « auto-assign v1 ».
- Sorties : assignments proposées (statut « proposé ») avec score, justification des règles appliquées, indicateur de confiance ; métriques d'exécution (nb shifts traités, taux de couverture, conflits rencontrés) ; API asynchrone idempotente via `job_id` et logs/metrics Prometheus.

## Règles métier clés (préparatoires)
- Un shift appartient à une mission et à un site ; un collaborateur ne peut avoir deux shifts qui se chevauchent sur le même créneau.
- Les horaires sont stockés en UTC et présentés dans le fuseau du site.
- Les missions définissent un rôle/compétence requis ; seules les personnes compatibles peuvent être affectées (vérification côté service).
- Statuts prévus : `draft`, `confirmed`, `cancelled`. Une annulation conserve l'historique (audit ultérieur).

### Règles de validation initiales (Phase 2)
- Horaires : `start < end` ; chevauchements interdits par collaborateur sur un même site et plage.
- Référentiel : aucune suppression dure si entité référencée (prévoir soft-delete ou blocage).
- Compatibilité : rôle requis d'une mission doit exister et être associé à l'organisation ; un collaborateur doit partager l'organisation et posséder le rôle/compétence.
- Fuseaux : tout nouvel horaire saisit un fuseau explicite (du site) avant conversion UTC.
- Statuts : transitions autorisées `draft` ➜ `confirmed` ➜ `cancelled`; retour à `draft` uniquement si aucune affectation confirmée.
- Cohérence planning : une mission ne peut être publiée sans site ni rôle ; un shift ne peut être confirmé si la mission est annulée ou inactive.

## Critères d'acceptation transverses
- **Documentation** : chaque évolution de périmètre met à jour `docs/` et `agent.md` avant code.
- **Qualité** : tests automatisés pour chaque parcours ajouté (API + front) et CI verte obligatoire pour merger.
- **Sécurité** : aucun secret en clair ; validation d'entrée stricte et logs structurés d'erreur/acquisition.
- **Expérience** : les vues planning affichent les fuseaux et statuts ; les erreurs bloquantes sont explicites et actionnables pour l'utilisateur final.
