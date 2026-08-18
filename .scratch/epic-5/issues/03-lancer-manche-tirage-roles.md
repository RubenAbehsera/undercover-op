# 03 — Lancer une manche : tirage anti-spoil et distribution des rôles

**What to build:** Depuis la salle d'attente, l'hôte lance une manche. Le serveur tire une paire dans le pool valide pour le calibrage de la room : arc_etablissement ≤ calibrage (borne inclusive) ET arc_premiere_apparition des deux personnages ≤ calibrage. Tirage aléatoire, sans répétition dans la partie ; stock épuisé → réutilisation autorisée. Puis la distribution des rôles : exactement un joueur reçoit le personnage imposteur, tous les autres le personnage majorité ; l'imposteur n'est pas informé — chaque joueur reçoit un payload identique en forme (son personnage), et rien dans aucun payload ni événement, broadcasts compris, ne révèle qui est l'imposteur ni le sens du lien. *(US 5.2 + 5.3 + 5.4, fusionnées)*

**Blocked by:** 02 — Room & salle d'attente.

**Status:** done

- [x] Propriété anti-spoil testée sur les 24 paires : aucun tirage servi au-delà du calibrage (les deux filtres)
- [x] Aucune répétition avant épuisement du stock valide ; réutilisation après épuisement
- [x] Le personnage imposteur attribué à exactement un joueur, tiré au hasard
- [x] Audit des payloads : aucun champ ne distingue l'imposteur, sur tous les événements émis pendant la distribution
- [x] La difficulte de la paire n'est jamais émise

## Comments

- **2026-08-18** — implémenté TDD (68 tests verts sur la suite entière, dont 20
  nouveaux). Découpage : `jeu/calibrage.py` gagne `pool(contrat, calibrage)` —
  l'anti-spoil complet (arc du lien **et** première apparition des deux
  personnages) tient désormais en un seul endroit, `arcs_proposes` et `pool`
  partageant la même borne par paire ; `jeu/manche.py` (domaine pur) porte
  `Manches`, le stock d'une partie — liste mélangée, dépilée sans répétition,
  rechargée à l'épuisement — et `Manche`, la distribution ; `jeu/rooms.py`
  ajoute `lancer_manche(code, joueur)`, contrôle de flux de l'hôte ;
  `jeu/evenements.py` ajoute l'événement `lancer_manche` et la distribution
  privée `personnage`, un envoi par sid.
  Anti-fuite : le payload d'un joueur est `{id, nom}` et rien d'autre — même
  forme pour tous, aucune diffusion collective au moment de la distribution.
  Un test relit **tous** les paquets émis pendant le lancement et échoue si
  l'on y trouve l'id de la paire, le libellé ou le type du lien, la difficulté,
  l'ID du joueur imposteur, ou même les mots « imposteur » / « majorite ».
  L'étalon anti-spoil est monté en fixture `paires_servables` (conftest),
  recalculé à la main depuis `docs/decisions.md` : le tirage est vérifié contre
  la règle, jamais contre lui-même.
  Démo live sur uvicorn, trois vrais clients socket.io : refus `pas_hote`,
  lancement par l'hôte, deux joueurs sur le même personnage et un seul sur
  l'autre, seconde manche sur une paire neuve.
  Décision prise au passage, à confirmer : **minimum 3 joueurs** pour lancer
  (`MINIMUM`, refus `joueurs_insuffisants`) — rien ne le tranchait dans
  `docs/decisions.md`, mais une manche à deux n'a pas de sens.
  Laissé au ticket 04 : refuser de rejoindre pendant une manche, et refuser de
  relancer une manche déjà en cours — aujourd'hui l'hôte peut redistribuer.
