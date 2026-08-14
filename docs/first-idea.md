# Note d'intention — Undercover One Piece

_Document de cadrage destiné à un assistant de développement. Il décrit l'intention, les décisions déjà prises et les refus explicites. Ce qui n'est pas décrit ici doit être proposé avant d'être codé, pas improvisé._

---

## 1. Intention

Une application web de jeu de soirée, inspirée d'Undercover, sur le thème de One Piece. Les joueurs sont **physiquement dans la même pièce**, chacun sur son téléphone. L'application distribue les rôles, cadence les tours de parole et gère le vote ; **toute la discussion se déroule hors de l'application**.

La spécificité du projet, et sa seule vraie difficulté : les deux personnages tirés au sort doivent être **reliés entre eux de manière signifiante**, pour que les indices donnés par les joueurs se recouvrent partiellement. C'est cette proximité contrôlée qui fait la qualité d'une manche.

Objectif secondaire, assumé : le projet sert de terrain d'apprentissage sur un service Python déployé et sur la modélisation en graphe. Une part de sur-ingénierie est acceptée **dans la couche de fabrication des données**, pas dans le serveur de jeu.

---

## 2. Règles du jeu

- Minimum 3 joueurs. Cible réelle d'usage : 4 à 8.
- Chaque joueur reçoit un personnage, visible uniquement de lui.
- La majorité reçoit le **même** personnage. Un joueur (l'imposteur) en reçoit un **autre**, relié au premier.
- À partir de 6 joueurs, prévoir la possibilité de 2 imposteurs (partageant le même personnage alternatif). Le modèle de données doit le permettre dès le départ, même si la v1 ne l'active pas.
- Chaque joueur donne à l'oral un indice sur son personnage, à tour de rôle. L'application affiche **qui doit parler**.
- Après un ou plusieurs tours de parole, vote dans l'application.
- Résultat affiché : l'imposteur est démasqué (victoire du groupe) ou non (victoire de l'imposteur).
- À la révélation, l'application affiche **le lien qui unissait les deux personnages** (« même équipage, rôles opposés »). C'est un moment de jeu, pas une info technique.

---

## 3. Parcours utilisateur

1. Un joueur crée une partie → obtient un **code de room** à partager.
2. À la création, une question de calibrage : **jusqu'où la table a-t-elle avancé dans l'histoire ?** (sélection d'un arc). Sert à filtrer les personnages et à éviter les spoils.
3. Les autres rejoignent via le code, saisissent un pseudo.
4. L'hôte lance la manche. Chacun voit son personnage sur son écran.
5. L'écran indique le joueur dont c'est le tour de parole, et permet de passer au suivant.
6. Pendant la manche, chaque joueur dispose d'un bouton **« je ne connais pas ce personnage »** (voir §6).
7. Phase de vote dans l'application.
8. Résultat, révélation du lien, puis relance d'une manche ou fin de partie.
9. En fin de **partie** (pas de manche) : un retour rapide en un geste, plus un champ commentaire optionnel.

---

## 4. Modèle de données — le graphe

Le graphe est construit **hors ligne**. Il ne tourne pas en production (voir §7).

**Nœuds** : personnages, équipages/factions, arcs, types de pouvoir.

**Arêtes typées**, deux natures distinctes :

- **Liens par nœud partagé** (générés en masse, peu coûteux) : appartenance à un équipage ou une faction, présence dans un arc, type de pouvoir.
- **Liens directs entre personnages** (rares, saisis à la main, les plus qualitatifs) : parenté, mentorat, rivalité.

**Attributs dérivés utiles** :

- _Notoriété_ = degré du nœud. Un personnage très connecté est un personnage connu. Ne pas la saisir à la main.
- _Arc de première apparition_, pour le filtre de calibrage et l'anti-spoil.

**Plafond de périmètre v1 : environ 80 personnages, 5 types de relations.** Ne pas chercher l'exhaustivité du wiki.

---

## 5. Sélection des paires

Une paire n'est pas « deux personnages similaires ». Une bonne paire **partage deux ou trois attributs et diverge nettement sur un seul**, discutable à l'oral.

**Pondération** des liens, du plus fort au plus faible :

| Lien                       | Poids  | Note                                      |
| -------------------------- | ------ | ----------------------------------------- |
| Parenté / relation directe | Fort   | Se suffit à lui-même                      |
| Équipage ou faction        | Fort   |                                           |
| Type de pouvoir            | Moyen  |                                           |
| Arc commun                 | Faible | **Ne valide jamais une paire à lui seul** |

L'arc est le lien le plus généreux et le plus trompeur : deux personnages présents à Impel Down peuvent n'avoir aucun indice commun jouable. Il renforce une paire, il ne la qualifie pas.

**Règles de validité** :

- Le total des poids partagés doit tomber dans une fourchette (ni trop bas, ni trop haut).
- Au moins un **axe de divergence net** est obligatoire.
- Les deux personnages doivent être disponibles selon le filtre d'arc de la table.

**Difficulté** = distance dans le graphe. Lien direct = facile. Deux sauts via un nœud commun = intermédiaire. Trois sauts = injouable, à exclure.

**Le lien retenu est stocké avec la paire**, en clair, pour être affiché à la révélation.

---

## 6. Signaux et mesure

Trois signaux **distincts**, à stocker séparément. Les mélanger rend la boucle inexploitable.

**a) Signal objectif** — automatique, gratuit, à chaque manche : imposteur démasqué ou non, en combien de tours, répartition des votes. C'est la mesure principale.

**b) Drapeau « je ne connais pas »** — par joueur, pendant la manche, en un tap. Il identifie un **mode d'échec différent** : la manche a raté par méconnaissance du personnage, pas par mauvaise calibration de la paire. Une manche portant ce drapeau est **exclue** du calcul de qualité des règles de tirage.

**c) Signal subjectif** — une fois par **partie**, pas par manche, en un seul geste. Commentaire libre optionnel. L'attention des joueurs en soirée est une ressource rare : ne pas la dépenser à chaque manche.

**Analyse** : ne pas viser une note moyenne. Classer les retours en 3 ou 4 catégories d'échec (« trop obscur », « aucun indice commun », « trop évident »), et ne suivre que des **familles de paires grossières** (3 familles maximum), sinon chaque case n'aura que deux observations.

---

## 7. Architecture technique

**Principe directeur : complexité dans la fabrication, simplicité dans le service.**

**Chaîne hors ligne (fabrication)**

- Base graphe (Neo4j ou équivalent), en local via Docker ou en offre hébergée gratuite. **Jamais sur le serveur de jeu.**
- Requêtes de sélection des paires par motifs de chemin.
- Optionnel : une passe LLM proposant des paires candidates ou extrayant des relations depuis des fiches de personnages. **Toute proposition d'un LLM est validée contre le graphe avant d'être retenue** — existence du personnage, véracité des attributs. Le générateur peut se tromper, le filtre le rattrape.
- **Sortie : un fichier de paires validées, figé (JSON).**

**Service de jeu (production)**

- Backend Python **FastAPI**, **WebSockets** pour l'état partagé de la partie.
- Il ne connaît que le fichier de paires. Aucune dépendance au graphe à l'exécution.
- Conteneurisé, déployé sur du cloud managé.
- **Gestion de la reconnexion obligatoire dès la v1** : un joueur qui verrouille son téléphone et revient doit retrouver son personnage et l'état exact du tour. C'est le premier point de rupture des jeux de soirée web.

**Front**

- PWA dans le navigateur. Pas d'application native, pas de store.
- Partage par lien et code de room.

---

## 8. Hors périmètre — refus explicites

À ne pas implémenter, même si c'est facile :

- Pas de comptes utilisateurs.
- Pas de chat dans l'application (les joueurs sont dans la même pièce).
- Pas d'historique de parties consultable au-delà de la session.
- Pas de mode spectateur.
- Pas de microservices, pas d'event sourcing, pas de file de messages dans le serveur de jeu.
- Pas de redistribution d'images officielles. Noms et attributs de personnages uniquement. Projet non commercial.

---

## 9. Jalons

1. **Vingt paires écrites à la main**, et une première soirée jouée avec. Ces vingt paires deviennent l'étalon : le graphe devra les retrouver. Sans référence de ce qu'est une bonne paire, un pipeline sophistiqué ne prouve rien.
2. Serveur de jeu minimal jouable : room, rôles, tour de parole, vote, résultat, reconnexion.
3. Construction du graphe et génération automatique des paires.
4. Boucle de mesure : signaux enregistrés, catégories d'échec, ajustement des poids.
