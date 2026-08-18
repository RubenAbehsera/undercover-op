# Jeu

Le service de jeu en production : rooms, distribution des rôles, tours de parole, vote, signaux. Ne connaît du domaine One Piece que ce que contient le fichier de paires.

## Language

### La partie

**Partie**:
Session complète, de la création de la room au feedback final. Composée de manches.
_Avoid_: game, session.

**Manche**:
Un cycle complet : distribution → indices → vote(s) → révélation. Séquence de votes en nombre quelconque — longueur 1 tant qu'il n'y a qu'un imposteur.
_Avoid_: round, tour.

**Tour (de parole)**:
Un passage de tous les joueurs dans l'ordre, à l'intérieur d'une manche.

**Room**:
La salle identifiée par son code, persiste le temps de la partie.
_Avoid_: lobby, salon.

**Salle d'attente**:
L'état d'une room hors manche : pseudos présents, hôte, calibrage — visible de tous, diffusé par l'événement `salle_attente`. C'est le seul moment où l'on peut rejoindre.
_Avoid_: lobby.

**Calibrage**:
L'arc choisi par l'hôte à la création de la room, borne maximale inclusive de l'anti-spoil. Ne sont proposés que les arcs qui changent réellement le pool de paires.

**Orateur**:
Le joueur dont c'est le tour de parole. Il rend la parole lui-même — l'ordre, tiré à chaque manche, est cyclique et sans timer.

**Désigné**:
Le joueur qui réunit la majorité stricte des suffrages exprimés. Sans majorité stricte, personne n'est désigné et l'imposteur l'emporte.

**Révélation**:
L'écran qui clôt la manche : les deux personnages, le pseudo de l'imposteur, le libellé du lien, le dépouillement nominatif. La difficulté n'y figure jamais. C'est aussi ce qui rouvre la room aux arrivants.
_Avoid_: résultat, score.

**Hôte**:
Le joueur qui a créé la partie ; détient les contrôles de flux (lancer une manche, déclencher le vote, terminer la partie).

**Imposteur**:
Joueur recevant le personnage alternatif ; non informé de son rôle.
_Avoid_: undercover, espion, traître.

### Les signaux

**Signal objectif**:
Mesure automatique par manche : imposteur démasqué ou non, nombre de tours, répartition des votes.

**Drapeau « je ne connais pas »**:
Signal par joueur et par manche, strictement confidentiel ; identifie un échec par méconnaissance du personnage. Une manche qui le porte est exclue du calcul de qualité des tirages.

**Signal subjectif**:
Retour en un geste, une fois par partie, commentaire optionnel.
