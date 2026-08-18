# 04 — La manche : machine à états

**What to build:** La manche complète, de bout en bout, pilotée par l'hôte : distribution → tours de parole → vote → révélation. Ordre de parole tiré aléatoirement à chaque manche, cyclique, nombre de tours illimité, pas de timer. Vote déclenché par l'hôte uniquement, une consultation en v1 : on ne vote pas pour soi, dépouillement nominatif et public, fermeture quand tous les joueurs connectés ont voté ou forçage par l'hôte ; majorité stricte des suffrages exprimés sur une seule personne, sinon victoire de l'imposteur. Écran de révélation : les deux personnages, le pseudo de l'imposteur, le libellé du lien — la difficulté n'est jamais affichée. Rejoindre est refusé pendant une manche (salle d'attente uniquement entre manches). *(US 5.5)*

**Blocked by:** 03 — Lancer une manche : tirage anti-spoil et distribution des rôles.

**Status:** done

- [x] Déroulé complet démontrable sur des clients socket de test : lancer → tours de parole → vote → révélation
- [x] L'ordre de parole change à chaque manche et cycle
- [x] Vote : pas de vote pour soi, dépouillement nominatif public, majorité stricte sinon imposteur vainqueur
- [x] Fermeture du vote par complétude ou forçage par l'hôte
- [x] Révélation complète (duo, pseudo de l'imposteur, libellé du lien) sans la difficulté
- [x] Tentative de rejoindre pendant une manche → refus

## Comments

- **2026-08-18** — implémenté TDD (111 tests verts sur la suite entière, dont 43
  nouveaux). Découpage : `jeu/erreurs.py` (nouveau) accueille `ErreurRoom` —
  la manche doit pouvoir refuser une demande sans dépendre de `rooms` ;
  `jeu/manche.py` porte la machine à états `paroles → vote → revelation`,
  l'ordre de parole tiré, `passer`, `voter`, la majorité stricte et
  `tours_joues()` ; `jeu/rooms.py` porte les contrôles de flux de l'hôte et
  **tous les payloads publics**, traduits en pseudos (`tour()`, `vote_ouvert()`,
  `revelation()`) — la manche, elle, ne connaît que des ID ;
  `jeu/evenements.py` ajoute `passer`, `ouvrir_vote`, `voter`, `forcer_vote`
  et les diffusions `tour`, `vote_ouvert`, `revelation`.
  L'audit anti-fuite du ticket 03 est étendu au déroulé entier : un test rejoue
  lancement, tours de parole, ouverture du vote et un suffrage, puis relit tous
  les paquets émis — rien n'y trahit l'imposteur avant la révélation.
  Démo live sur uvicorn, trois vrais clients socket.io : deux tours de parole
  bouclés, refus `pas_ton_tour`, `pas_hote`, `vote_pour_soi` et
  `manche_en_cours`, révélation complète (duo, pseudo de l'imposteur, libellé
  du lien, dépouillement nominatif, `tours: 2`) sans la difficulté, et la room
  qui se rouvre au retardataire une fois la révélation passée.
  Trois partis pris, faute de tranchage amont : **c'est l'orateur qui rend la
  parole** (l'hôte ne détient que lancer / ouvrir le vote / forcer) ; **la
  révélation clôt la manche**, donc c'est elle qui rouvre la room aux arrivants
  et autorise la manche suivante ; **les abstentions ne comptent pas** — un vote
  forcé sur un seul suffrage exprimé désigne quand même (règle des « suffrages
  exprimés » de `docs/decisions.md`), comportement épinglé par un test.
  Défaut connu, laissé au ticket 05 : un joueur qui part en cours de manche
  disparaît de `room.joueurs` mais reste dans `manche.joueurs` — le vote ne peut
  plus se fermer par complétude (l'hôte doit forcer) et son pseudo sort à `None`
  dans la révélation. C'est exactement l'objet du 05.
