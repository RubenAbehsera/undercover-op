# Fabrication

La chaîne hors ligne qui construit le graphe One Piece (Neo4j) et produit le fichier de paires figé consommé par le jeu. Ne tourne jamais en production.

## Language

### Les données

**Paire**:
Les deux personnages d'une manche — celui de la majorité et celui de l'imposteur — avec le lien qui les unit.
_Avoid_: duo, combinaison.

**Lien**:
La relation retenue pour une paire, stockée en clair et affichée à la révélation.
_Avoid_: relation, connexion.

**Relation**:
Arête typée du graphe : équipage/faction, arc, type de pouvoir, ou relation directe entre personnages.
_Avoid_: lien, arc.

**Arc**:
Arc narratif de One Piece. Jamais au sens « arête de graphe ».

**Calibrage**:
Arc maximal déclaré par l'hôte à la création de la partie ; filtre les personnages et les liens (anti-spoil).

**Notoriété**:
Degré du nœud personnage dans le graphe. Jamais saisie à la main.

### Les artefacts

**Fabrication**:
La chaîne hors ligne (graphe, requêtes, validation) qui produit le fichier de paires.

**Fichier de paires**:
L'artefact figé (JSON) consommé par le serveur de jeu. Seul point de contact entre la fabrication et le jeu.
