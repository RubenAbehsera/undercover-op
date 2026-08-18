# 03 — Lancer une manche : tirage anti-spoil et distribution des rôles

**What to build:** Depuis la salle d'attente, l'hôte lance une manche. Le serveur tire une paire dans le pool valide pour le calibrage de la room : arc_etablissement ≤ calibrage (borne inclusive) ET arc_premiere_apparition des deux personnages ≤ calibrage. Tirage aléatoire, sans répétition dans la partie ; stock épuisé → réutilisation autorisée. Puis la distribution des rôles : exactement un joueur reçoit le personnage imposteur, tous les autres le personnage majorité ; l'imposteur n'est pas informé — chaque joueur reçoit un payload identique en forme (son personnage), et rien dans aucun payload ni événement, broadcasts compris, ne révèle qui est l'imposteur ni le sens du lien. *(US 5.2 + 5.3 + 5.4, fusionnées)*

**Blocked by:** 02 — Room & salle d'attente.

**Status:** ready-for-agent

- [ ] Propriété anti-spoil testée sur les 24 paires : aucun tirage servi au-delà du calibrage (les deux filtres)
- [ ] Aucune répétition avant épuisement du stock valide ; réutilisation après épuisement
- [ ] Le personnage imposteur attribué à exactement un joueur, tiré au hasard
- [ ] Audit des payloads : aucun champ ne distingue l'imposteur, sur tous les événements émis pendant la distribution
- [ ] La difficulte de la paire n'est jamais émise
