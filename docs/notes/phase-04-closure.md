# Phase 4 – Closure & Transition to Phase 5 (Draft)

Ce mémo synthétise l'état final de la Phase 4, les compléments attendus pour la clôturer proprement et le cadrage initial de la Phase 5.

## 1. Objectifs atteints en Phase 4
- Backend core stable (FastAPI, CRUD complet, validations, tests).
- UI CRUD basique opérationnelle.
- Vue Planning visuelle simple : jour/semaine.
- CI/CD stabilisée, tests passants, documentation enrichie.
- Architecture et agents fonctionnels synchronisés.

## 2. Ce qu'il reste à ajouter pour clôturer parfaitement la Phase 4
### 2.1 Documentation finale
- Mise à jour complète du README racine.
- Mise à jour des READMEs backend / frontend.
- Ajout documentation Planning (vues, interactions, modèles).
- Ajout schémas ASCII API <-> Frontend.
- Ajout d'un document "Phase 4 – Release Notes".

### 2.2 Tests & Qualité
- Couverture de tests minimale 85% backend.
- Scénarios e2e Playwright pour CRUD + Planning simple.
- Mises à jour CI : badges, coverage, status.

### 2.3 Observabilité
- Healthchecks + /metrics validés.
- Dashboard Prometheus/Grafana minimal.

### 2.4 Finalisation du Workflow Codex
- Mise à jour AGENT_ROOT pour verrouiller la fin Phase 4.
- Ajout d'un script docs_guard pour obliger mise à jour READMEs.
- Ajout roadmap_guard pour que chaque step Phase 5 soit consigné.

## 3. Prompt Codex – Finalisation Phase 4
Ce prompt sera envoyé à Codex pour terminer automatiquement la Phase 4.

```
SYSTEM:
You are Codex, the autonomous engineering agent responsible for executing Phase 4 completion tasks for the Orga/Coulisses Crew project.
Your goal: fully finalize Phase 4, generate clean, tested, documented output, and prepare the repository for Phase 5.
Follow the roadmap, guard scripts, and documentation policies strictly.

TASKS:
1. Update all documentation blocks:
   - README.md (root)
   - backend/README.md
   - frontend/README.md
   - docs/blueprint
   - docs/architecture (ASCII diagrams)
   - docs/release/phase4.md (new)

2. Add missing tests:
   - FastAPI routes critical paths
   - Minimum 85% coverage
   - 3 Playwright e2e tests for CRUD & Planning simple

3. CI/CD:
   - Add coverage badges
   - Fix any pipeline failures
   - Ensure dev, staging, prod workflows pass

4. Observability:
   - Validate /health and /metrics endpoints
   - Ensure Prometheus config is correct

5. Update agents:
   - AGENT_ROOT.md with Phase 4 closure
   - AGENT_FRONTEND.md, AGENT_BACKEND.md, AGENT_DEVOPS.md, AGENT_DOCS.md

OUTPUT RULES:
- Use PR branches named: codex/phase4-finalization
- Each commit MUST reference docs/roadmap/step-XX.md
- If a file is modified, ensure roadmap + docs + readme are updated accordingly.

END.
```

## 4. Préparation Phase 5 – Vision & Structure
La Phase 5 introduira les fonctionnalités PRO :

### Phase 5 – Advanced Planning & Team Intelligence
- Drag & Drop avancé
- Étirage des shifts
- Détection des conflits
- Auto-assignation intelligente
- Templates de missions
- Filtrage avancé

### 5.1 Planning PRO
- Drag & Drop avancé
- Étirage des shifts
- Détection des conflits
- Auto-assignation intelligente
- Templates de missions
- Filtrage avancé

### 5.2 Collaboration & Communication
- Notifications intelligentes (email / Telegram)
- Mode brouillon / publication du planning
- Historique & audit

### 5.3 Gestion RH / Disponibilités
- Déclarations de disponibilités
- Contraintes horaires
- Règles légales

### 5.4 Workspace & Multi-organisation
- Gestion multi-entreprise
- Permissions avancées

### 5.5 UX/UI Pro (v2)
- Refonte visuelle
- Mode sombre
- Performance Planning optimisée

### 5.6 Observabilité & Performance
- Supervision temps réel
- Logs structurés améliorés

## 5. Prompt Codex – Phase 5 (à valider)
```
SYSTEM:
You are Codex, autonomous engineering agent responsible for executing Phase 5 of the Orga/Coulisses Crew SaaS.
Your mission: implement Advanced Planning & Team Intelligence.

PHASE 5 OBJECTIVES:
1. Planning PRO features:
   - Drag & Drop full
   - Resize missions
   - Conflict detection
   - Templates
   - Smart auto-assign

2. RH & Disponibilités:
   - User availability model
   - Dashboard dispo
   - Rules & constraints

3. Collaboration tools:
   - Draft mode
   - Publish mode
   - Notifications engine

4. UX/UI v2:
   - New layout
   - Optimized timeline rendering
   - Filters & teams colors

5. DevOps:
   - Performance benchmarks
   - Error budget system

RULES:
- Each deliverable must update docs/blueprint, architecture, agents, roadmap.
- Every change must include tests + CI validation.
- Use branch: codex/phase5-advanced-planning

END.
```

## 6. Prochaine étape
- Raffiner entièrement le prompt Codex Phase 5.
- Générer la roadmap Phase 5 (steps 01 à 30).
- Relier la roadmap aux agents et READMEs.
- Lancer officiellement la Phase 5 après validation.
