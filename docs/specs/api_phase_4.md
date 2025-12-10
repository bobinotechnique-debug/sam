# API Phase 4 – Surface normalisée

Cette note aligne les endpoints livrés en Phase 4 (4.1 → 4.4) et l'état final « Ultimate ».

## Principes
- Namespace unique : `/api/v1`.
- Erreurs normalisées via handlers globaux (trace_id + message).
- Validation stricte Pydantic (datetime tz-aware, statuts contrôlés, fenêtres horaires cohérentes).
- Logs JSON structurés avec `trace_id` propagé par middleware.

## Endpoints clés
- `GET /api/v1/health` → détails status/version/dépendances + compteurs d'entités.
- `GET /api/v1/health/metrics` → exposition texte compatible Prometheus (counts + uptime + app info).
- `CRUD /organizations` → validation des dépendances (sites/roles/collaborateurs empêchent la suppression).
- `CRUD /sites` → héritage automatique du timezone organisation.
- `CRUD /roles` → rattachement organisationnel obligatoire.
- `CRUD /collaborators` → rôle principal obligatoire + validation organisationnelle.
- `CRUD /missions` → fenêtre horaire valide, rattachement à un site + rôle d'organisation.
- `CRUD /shifts` → validation des collisions (chevauchement sur collaborateur bloqué) et alignement mission.

## Flux de référence
```
[Client] --POST /organizations--> [Service Organization]
        --POST /sites-----------> [Service Site]
        --POST /roles-----------> [Service Role]
        --POST /collaborators--> [Service Collaborator]
        --POST /missions-------> [Service Mission]
        --POST /shifts---------> [Service Shift]
```

## Erreurs et statuts
- `400` : payload invalide (schema/validation métier).
- `404` : ressource manquante.
- `409` : conflit métier (suppression impossible, chevauchement de shift, incohérence organisationnelle).
- `500` : erreur interne (loggée avec `trace_id`).

## Observabilité minimale
- Logs : format JSON `{timestamp, level, logger, message, trace_id?, ...extra}`.
- Headers HTTP : `X-Request-ID` et `X-App-Timestamp` ajoutés par middleware.
- Metrics : compteur par entité + uptime et app_info exposés sous `/api/v1/health/metrics`.

## Tests attendus (CI parité)
- `ruff check app`
- `mypy app`
- `pytest` (flux CRUD, validations, health/metrics)
