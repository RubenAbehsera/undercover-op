# 04 — La manche : machine à états

**What to build:** La manche complète, de bout en bout, pilotée par l'hôte : distribution → tours de parole → vote → révélation. Ordre de parole tiré aléatoirement à chaque manche, cyclique, nombre de tours illimité, pas de timer. Vote déclenché par l'hôte uniquement, une consultation en v1 : on ne vote pas pour soi, dépouillement nominatif et public, fermeture quand tous les joueurs connectés ont voté ou forçage par l'hôte ; majorité stricte des suffrages exprimés sur une seule personne, sinon victoire de l'imposteur. Écran de révélation : les deux personnages, le pseudo de l'imposteur, le libellé du lien — la difficulté n'est jamais affichée. Rejoindre est refusé pendant une manche (salle d'attente uniquement entre manches). *(US 5.5)*

**Blocked by:** 03 — Lancer une manche : tirage anti-spoil et distribution des rôles.

**Status:** ready-for-agent

- [ ] Déroulé complet démontrable sur des clients socket de test : lancer → tours de parole → vote → révélation
- [ ] L'ordre de parole change à chaque manche et cycle
- [ ] Vote : pas de vote pour soi, dépouillement nominatif public, majorité stricte sinon imposteur vainqueur
- [ ] Fermeture du vote par complétude ou forçage par l'hôte
- [ ] Révélation complète (duo, pseudo de l'imposteur, libellé du lien) sans la difficulté
- [ ] Tentative de rejoindre pendant une manche → refus
