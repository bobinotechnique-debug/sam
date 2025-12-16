# Phase 5 — Advanced Planning & Team Intelligence

Cette phase introduit le « Planning PRO » avec interactions avancées, workflow de publication, contraintes RH et observabilité dédiée. Elle suit les 30 étapes détaillées dans `docs/roadmap/phase5/step-XX.md`.

## Objectifs clés
- Planning PRO : drag & drop avancé, redimensionnement avec pas configurables, multi-jours et détection de conflits (personne, lieu, règles RH).
- Collaboration & workflow : brouillon vs publication, audit log, notifications (email/Telegram/digests) et publication sécurisée.
- Disponibilités & RH : calendrier d’indisponibilités, contraintes (max heures, repos, pauses) paramétrables par organisation.
- Multi-organisation & permissions : rôles avancés pour l’édition/pubicaton du planning.
- UX/UI v2 : timeline performante (virtualisation), filtres/couleurs d’équipe, responsive desktop/tablette/mobile.
- Observabilité & performances : métriques spécifiques planning, tableaux de bord Prometheus/Grafana, benchmarks de régression.

## Étapes (01 → 30)
1. Initialisation Phase 5
2. Planning PRO specification
3. Backend architecture update (shift_templates, user_availability, conflict_rules, etc.)
4. API Planning PRO v1 (templates, conflict rules, auto-assign endpoints)
5. Tests API Planning PRO v1
6. UI Planning v2 – structure (layout, panels, teams, timeline)
7. UI Planning v2 – interactions (drag, resize, snap, multi-day)
8. Conflict detection (rules + API + UI highlighting)
9. Auto-Assign Intelligence v1
10. Auto-Assign Intelligence v2
11. Mission templates (CRUD, recurring)
12. Draft mode
13. Publish mode
14. Notification engine
15. User availabilities
16. HR constraints
17. Advanced permissions
18. Mobile responsive v2
19. Performance optimizations
20. Observabilité for planning
21. Audit and history
22. Export (PDF, ICS, CSV)
23. Import (CSV, ICS)
24. Team dashboard
25. Production dashboard (costs, hours, actual vs planned)
26. Planning PRO e2e tests
27. CI/CD Phase 5 (pipelines, benchmarks)
28. Final documentation
29. Quality validation (Codex + human review)
30. Phase 5 release

## Gates & exigences
- CI verte en continu (ruff, mypy, pytest, npm lint/test/build, e2e Playwright lorsque disponible).
- Documentation synchronisée : roadmap step-XX, blueprint planning PRO, architecture (diagrammes ASCII/flux), agents mis à jour.
- Non-régression Phase 4 : endpoints et parcours existants restent fonctionnels.
- Observabilité et métriques planning exposées et documentées avant sortie.

## Commandes de référence
- Backend : `cd backend && ruff check app && mypy app && pytest`
- Frontend : `cd frontend && npm run lint && npm run test && npm run build`
- E2E : `cd frontend && npx playwright test`

## Statut
- Phase 4 is closed; Phase 5 is open. Follow-up lives in `docs/roadmap/phase5/`.
- Steps 01 (init) and 02 (spec Planning PRO) are documented. Code already embeds a preview of steps 03-05: in-memory Planning PRO services/routes (`/api/v1/planning/*`), basic rules/auto-assign and the `/planning/pro` page rendering Timeline V2. No DB session, auth or multi-org context yet; migrations are not executed.
- Next actionable items are detailed in `docs/roadmap/next_steps.md`.
