# Context Map

## Contexts

- [Jeu](./server/CONTEXT.md) — le service de jeu en production : rooms, manches, votes, signaux
- [Fabrication](./fabrication/CONTEXT.md) — la chaîne hors ligne : graphe Neo4j, génération et validation des paires

## Relationships

- **Fabrication → Jeu** : la fabrication produit le fichier de paires figé (JSON), validé par un schéma commun, plus les portraits des personnages tirables (servis en statique par le front, jamais lus par le serveur). Le jeu n'a aucune dépendance au graphe (voir [ADR-0001](./docs/adr/0001-fichier-de-paires-fige.md)).
- **Vocabulaire partagé** : Arc, Calibrage, Paire, Lien et Fichier de paires sont définis côté Fabrication, qui en est propriétaire ; le Jeu les consomme.
