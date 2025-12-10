# Spécifications fonctionnelles

## Objectif
Fournir une base applicative permettant de tester la stack FastAPI + React + Tailwind tout en préparant l'intégration PostgreSQL.

## Parcours utilisateur actuels
- **Healthcheck backend** : consultation des docs Swagger sur `/docs`.
- **CRUD démo en mémoire** : création, lecture, mise à jour et suppression d'items via l'API `/items`.
- **Interface frontend minimale** : chargement de la page d'accueil et consommation future de l'API.

## Exigences métier immédiates
- Mise à disposition d'un point d'entrée API opérationnel et prêt pour des endpoints CRUD.
- Frontend prêt à consommer des endpoints (mock ou réels) sans dette structurelle.

## Évolutions prévues (court terme)
- Ajouter des endpoints CRUD avec validation Pydantic et gestion d'erreurs claire.
- Introduire l'authentification (JWT) et les rôles pour sécuriser les parcours sensibles.
- Persister les données dans PostgreSQL avec migrations Alembic.

## Critères d'acceptation
- La documentation (README et `docs/`) reflète les capacités réelles de l'application.
- Les tests automatisés couvrent les fonctionnalités critiques introduites.
- Aucun secret ou configuration sensible n'est versionné en clair.
