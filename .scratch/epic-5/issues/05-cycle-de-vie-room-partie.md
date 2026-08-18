# 05 — Cycle de vie room & partie

**What to build:** Les règles de vie d'une room au long cours. Un joueur qui part en cours de manche est conservé dans l'état et sauté à l'ordre de parole — il ne bloque ni les tours ni le vote. Départ de l'hôte : transfert au joueur le plus ancien, les contrôles de flux suivent. La partie est terminée par l'hôte (c'est ce qui déclenchera le feedback, ticket 06). Une room est supprimée après 2 h d'inactivité. *(US 5.7, seconde moitié)*

**Blocked by:** 04 — La manche : machine à états.

**Status:** done

- [x] Départ d'un joueur en cours de manche : conservé dans l'état, sauté à l'ordre de parole, tours et vote non bloqués
- [x] Départ de l'hôte : transfert au joueur le plus ancien, contrôles de flux opérationnels
- [x] Fin de partie décidée par l'hôte : signal de fin émis à tous
- [x] Room inactive depuis 2 h → supprimée (testable sans attendre : horloge injectable)

## Comments

- **2026-08-18** — implémenté TDD (139 tests verts sur la suite entière, dont 28
  nouveaux). Le défaut que le ticket 04 avait laissé ouvert est refermé :
  `Joueur.present` distingue les partis, `Manche.retirer()` les sort du cycle
  de parole (`ordre_present()`), du bulletin (`vote_ouvert`) et du décompte de
  `tous_ont_vote()` — leur pseudo, lui, survit jusqu'à la révélation, et leur
  suffrage déjà exprimé reste au dépouillement. Un départ peut donc désormais
  *fermer* le vote : si plus personne n'est attendu, la révélation part toute
  seule.
  Transfert d'hôte dans `Rooms.quitter` : le plus ancien présent reprend les
  contrôles, en salle d'attente comme en pleine manche.
  Fin de partie : `terminer_partie` (hôte), diffusion `partie_terminee` ; la
  room survit — le ticket 06 y branchera le feedback — mais refuse `rejoindre`
  et `lancer_manche` avec le motif `partie_terminee`.
  Inactivité : horloge injectable (`Rooms(..., horloge=)`, `time.monotonic` par
  défaut), `INACTIVITE = 2 h`, purge à chaque accès via `Rooms.room()` /
  `creer()`. Pas de tâche de fond : une room endormie n'est réellement libérée
  qu'au premier accès suivant — sans conséquence fonctionnelle, mais à savoir
  si l'empreinte mémoire devient un sujet.
  Démo live sur uvicorn, quatre vrais clients socket.io : Sanji déconnecté en
  pleine parole (ordre republié sans lui, la parole suit à Zoro), bulletin sans
  le parti, Usopp déconnecté sans voter → révélation immédiate avec les deux
  suffrages exprimés, hôte déconnecté → main à Zoro, fin de partie diffusée,
  relance refusée.
  Parti pris : **un parti n'est plus une cible de vote** (`cible_inconnue`) —
  rien ne le tranchait, mais on n'accuse pas quelqu'un qui n'est plus là ;
  conséquence assumée, si l'imposteur part la manche devient ingagnable pour
  le groupe.
