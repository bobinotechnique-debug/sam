# Spécification visuelle UX/UI du planning (source de vérité)

## 1. Introduction / Contexte
L'application de planning multi-sites sert les responsables planning, managers de site, responsables RH et intervenants/ intérimaires. Elle vise la planification rapide, la réduction des erreurs (chevauchements, dépassements d'horaires) et la collaboration entre équipes.

## 2. Personas & cas d'usage clés
- **Responsable planning** : structure les organisations, gère les rôles/compétences, arbitre les ressources rares.
- **Manager de site** : affecte les missions locales, suit les indisponibilités et valide les heures.
- **Intervenant / intermittent** : consulte ses shifts, confirme ses disponibilités, déclare des absences.
- **Responsable RH** : suit la conformité (heures sup, contrats), valide et exporte les relevés.

Cas d'usage majeurs : créer une mission, remplir un planning par personne ou par lieu, gérer les disponibilités, valider les heures réalisées, ajuster en urgence (glisser-déposer), suivre les alertes de conflits.

## 3. Vue globale de l'interface
- **Barre supérieure** : sélecteur d'organisation, navigation (Dashboard, Planning, Collaborateurs, Lieux, Inventaire), recherche et filtres globaux, actions rapides (créer mission), notifications.
- **Sidebar (optionnelle desktop)** : filtres persistants (équipe, rôle, site, statut), légende des couleurs.
- **Zone centrale** : planning principal avec contrôles de période (jour/semaine/mois/chronologique), zoom (15/30/60 min), et grille ressources × temps.
- **Panneau latéral / modal** : fiches détaillées (Mission, Collaborateur, Inventaire) ouvertes en contexte.
- **Footer compact** : indicateurs de charges (total heures, alertes de conflits), raccourcis vers validations.

## 4. Écrans principaux
### 4.1 Vue Planning (jour/semaine/mois/chronologique)
- Colonnes = ressources (personnes, équipes, lieux) ; lignes temporelles graduées.
- Blocs missions : couleurs par rôle/équipe, icônes d'état (brouillon, confirmé, annulé), barres de progression pour temps prévu vs confirmé.
- Interactions : drag & drop pour créer/assigner/déplacer, redimensionnement pour ajuster les durées, double-clic pour ouvrir la fiche.
- États vides : placeholders expliquant comment créer une mission ou importer.

Wireframe ASCII (vue semaine par personne) :
```
[Date picker][Vue: Jour | Semaine | Mois][Zoom 15/30/60]
Filters: [Equipe][Site][Role] [Rechercher]

       Lun  Mar  Mer  Jeu  Ven
Alice  [===Mission A===]   [Mission B]
Bob    [Mission C][==Mission D==]
Chloé       [Mission E----------]
```

### 4.2 Fiche Mission (modal/panneau)
- Sections : Informations clés (titre, lieu, rôle, horaires, état), Affectations (ressources, compétences requises), Notes internes, Historique.
- Actions : Dupliquer, Annuler, Publier/Confirmer, Ajouter affectation, Exporter.
- États : brouillon (modifications libres), publié (verrous partiels), annulé (lecture seule, raison requise).

Wireframe ASCII (modal) :
```
+------------------------------------------------+
| Mission "Concert"  Etat: Brouillon   [Publier] |
| Lieu: Salle A  Rôle: Technicien son            |
| Date: 12/05 18:00-23:00  Fuseau: Europe/Paris  |
|------------------------------------------------|
| Affectations (drag & drop):                    |
| - Intervenant: Alice (confirmé)                |
| - Intervenant: Bob (brouillon)                 |
|------------------------------------------------|
| Notes internes: [............................] |
| Historique: Créé le 10/05 par RP               |
+------------------------------------------------+
```

### 4.3 Fiche Collaborateur / Intervenant
- Onglets : Identité, Compétences/rôles, Disponibilités, Historique missions, Préférences.
- Highlights : alertes de conflits horaires, quotas hebdo, préférences de lieux.

### 4.4 Inventaire / Matériel
- Liste filtrable par site/état ; cartes matériel avec disponibilité temporelle.
- Assignation aux missions via glisser-déposer ou sélection dans la fiche mission.

### 4.5 Dashboard synthétique
- KPIs : missions planifiées cette semaine, taux de couverture par rôle, alertes (chevauchements, heures sup, indisponibilités non traitées).
- Widgets : calendrier compact, liste des validations en attente, flux d'activité récent.

Wireframe ASCII :
```
+------------------+ +---------------------+
| Couverture roles | | Validations en cours|
| 85% global       | | - Mission A (Alice) |
| Alerts: 3        | | - Mission D (Bob)   |
+------------------+ +---------------------+
| Calendrier compact (mois)                   |
| [ ][ ][X][X] ...                           |
+--------------------------------------------+
```

### 4.6 Vue mobile (intervenant)
- Accueil : planning personnel (liste ou agenda compact), alertes de validation, bouton "Confirmer mes heures".
- Détails mission : horaires, lieu avec carte statique, contacts, état, bouton confirmer/refuser.
- Navigation réduite : onglets Bas (Planning, Notifications, Profil).

Wireframe ASCII :
```
+----------------------+
| Lun 12 mai           |
| 18:00-23:00 Concert  |
| Salle A - Confirmé   |
| [Confirmer] [Signaler]
+----------------------+
```

## 5. Interactions & comportements
- **Drag & drop** : créer/assigner/déplacer des blocs ; prévisualisation du créneau ; snap sur la grille (15/30/60 min).
- **Redimensionnement** : poignée sur les extrémités du bloc ; mise à jour en temps réel des durées.
- **Zoom & scroll** : zoom temporel 15/30/60 minutes ; scroll horizontal/vertical ; raccourcis clavier (+/-).
- **Filtres** : par équipe, lieu, type de mission, statut ; sauvegarde des vues favorisées.
- **Conflits** : badge rouge sur les blocs, panneau d'alertes listant les chevauchements ou quotas dépassés ; actions rapides pour replanifier.
- **États** : chargement (squelettes), erreurs (messages actionnables), vide (CTA pour créer mission/importer).

## 6. Responsive design
- **Desktop (≥1280px)** : grille complète, sidebar filtres visible, panneaux latéraux parallèles au planning.
- **Tablette (768–1279px)** : sidebar repliable, panneau détails en plein écran, grille resserrée.
- **Mobile (≤767px)** : bascule en liste ou agenda compact ; actions principales en bas d'écran ; filtres via bottom sheet.

## 7. Design system fonctionnel
- **Composants clés** : Button (primaire/secondaire/danger), Badge (statut), Avatar (photo/initiales), Card, Tooltip, Modal, Drawer, Tabs, Tag pour rôles/compétences, Timeline/Calendar strip.
- **Hiérarchie visuelle** : titres H1/H2/H3, sous-titres légers, corps de texte 14–16 px, labels en capitales légères.
- **Couleurs d'exemple** : par équipe/role (ex: bleu = technique, vert = logistique, orange = artistique), statuts (brouillon gris, confirmé bleu/vert, annulé rouge, en attente jaune).
- **Iconographie** : état (check, clock, ban), conflit (warning), actions (duplicate, drag).

## 8. Accessibilité & principes
- Contrastes respectant WCAG AA, tailles de cible ≥44px sur mobile.
- Navigation clavier pour le planning (tab/shift+tab, flèches pour naviguer entre blocs).
- Labels explicites, messages d'erreur actionnables, focus visible sur tous les composants interactifs.
- Annonces ARIA pour drag & drop et changements d'état (publication, annulation).

## 9. Roadmap UX/UI
- **MVP visuel** : vues Planning multi-vues (jour/semaine/mois), fiche mission complète, drag & drop basique, filtres essentiels, alertes de conflit, vue mobile personnelle.
- **V2+** : thèmes personnalisables, animation fine des déplacements, vues Gantt consolidées multi-projets, collaboration temps réel (curseurs partagés), exports imprimables stylés, personnalisation avancée des couleurs/avatars.
