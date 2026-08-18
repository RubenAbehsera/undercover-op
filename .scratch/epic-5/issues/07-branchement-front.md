# 07 — Branchement front

**What to build:** Le client web qui rend le serveur jouable en soirée, sur les téléphones des joueurs. Vite + React + TypeScript, `socket.io-client`, PWA minimale (manifest + service worker), interface en français. Le serveur reste **l'unique source de vérité** : le front n'a aucune règle de jeu, aucun timer, aucun état dérivé — il affiche ce que les diffusions lui donnent et n'envoie que des intentions. Identité sans compte : un ID opaque tiré au premier passage et rangé en `localStorage`, **clé par room** ; nouveau navigateur = nouveau joueur. Le front buildé est servi par le serveur (un seul conteneur). *(US 5.8)*

**Blocked by:** 06 — Les signaux → SQLite.

**Status:** done

## Le contrat socket, tel que le serveur le tient aujourd'hui

Il est figé et complet : le front n'a rien à inventer, et rien à ajouter côté serveur.

Demandes (toutes répondent par un ack `{ok: true, …}` ou `{ok: false, motif, message}` — le `motif` est une chaîne stable, c'est lui qui s'affiche traduit, jamais le `message`) :

| Événement           | Charge                                | Qui                |
| ------------------- | ------------------------------------- | ------------------ |
| `arcs`              | —                                     | tous (avant room)  |
| `creer_room`        | `{joueur, pseudo, calibrage}`          | l'hôte             |
| `rejoindre_room`    | `{joueur, code, pseudo}`               | les arrivants      |
| `lancer_manche`     | —                                     | **hôte**           |
| `passer`            | —                                     | **l'orateur**      |
| `ouvrir_vote`       | —                                     | **hôte**           |
| `voter`             | `{cible}` (un pseudo)                  | chacun, une fois   |
| `forcer_vote`       | —                                     | **hôte**           |
| `je_ne_connais_pas` | —                                     | chacun, une fois   |
| `terminer_partie`   | —                                     | **hôte**           |
| `retour`            | `{niveau: 1\|2\|3, commentaire?}`      | chacun, une fois   |
| `quitter_room`      | —                                     | chacun             |

Diffusions à écouter : `salle_attente`, `personnage` (privé, à soi seul), `tour`, `vote_ouvert`, `revelation`, `partie_terminee`.

## Les écrans

1. **Accueil** — créer (pseudo + calibrage choisi dans la liste rendue par `arcs`) ou rejoindre (code + pseudo). Le code de room se dicte à voix haute : 4 signes, gros, sans caractère ambigu.
2. **Salle d'attente** — code bien visible, pseudos présents, hôte repéré ; le bouton « lancer » n'existe que chez l'hôte.
3. **Manche** — son personnage (rien d'autre : rien ne doit distinguer l'imposteur, ni à l'écran ni dans le DOM), l'ordre de parole, qui parle. « J'ai fini » chez l'orateur seul, « ouvrir le vote » chez l'hôte seul. Le bouton **« je ne connais pas ce personnage »** est là, en un tap, sans confirmation ni retour visible pour les autres — une fois levé, il reste levé.
4. **Vote** — la liste des joueurs, soi excepté ; l'attente une fois voté ; « forcer » chez l'hôte.
5. **Révélation** — le duo, le pseudo de l'imposteur, le libellé du lien, le dépouillement nominatif. La difficulté n'existe pas côté front.
6. **Fin de partie** — sur `partie_terminee`, l'écran de retour : trois niveaux en un tap, commentaire optionnel, une seule fois.

## Acceptance

- [x] Une partie complète se joue à trois vrais téléphones, du code de room au retour de fin, sans jamais toucher au serveur autrement que par le socket
- [x] Reconnexion : le même navigateur retrouve son joueur dans la même room (ID en `localStorage`, clé par room) ; un navigateur neuf est un joueur neuf
- [x] Aucune règle de jeu côté front : les contrôles d'hôte s'affichent d'après l'état diffusé, et un refus serveur (`motif`) s'affiche tel quel, traduit
- [x] Rien à l'écran ni dans le DOM ne distingue l'imposteur avant la révélation, drapeau « je ne connais pas » compris — audit sur les payloads reçus et le rendu
- [x] PWA minimale : manifest, icône, installable sur mobile, écran plein
- [x] `npm run build` produit un bundle que le serveur sert lui-même (un seul conteneur, cf. `docs/decisions.md`)

## Tranché au démarrage du ticket

- **Libellés du retour** : 1 « Bof » · 2 « Sympa » · 3 « Excellent » (`front/src/libelles.ts`).
- **Service du bundle** : `StaticFiles(directory=front/dist, html=True)` monté à `/`
  **après** les routes HTTP déjà déclarées ; socket.io détourne `/socket.io` en
  amont du FastAPI, la racine ne peut donc pas marcher dessus. Chemin réglable
  par `FRONT_DIST` ; sans `index.html` construit, le montage est sauté et le
  serveur vit très bien en API seule.

## Comments

- **2026-08-19** — implémenté. `front/` : Vite + React + TypeScript,
  `socket.io-client`, PWA à la main (manifest, service worker maison,
  icônes générées par `scripts/icones.py` — aucune dépendance de build en plus).
  Découpage : trois modules purs testés (`etat.ts` range les 6 diffusions et les
  gestes locaux puis en déduit l'écran, `identite.ts` tient l'ID opaque par room
  et la session, `motifs.ts` traduit les 24 motifs de refus), six écrans
  purement présentationnels au-dessus, `App.tsx` pour le câblage.
  Parti pris : **aucun état dérivé**. Chaque diffusion remplace un créneau,
  `ecran()` lit ce qui est là — pas un tour compté, pas une majorité calculée.
  Les contrôles d'hôte s'affichent sur `salle_attente.hote === mon pseudo`, la
  parole sur `tour.orateur`. Un refus s'affiche par son `motif` traduit, jamais
  par le `message` du serveur (un motif inconnu tombe sur « Demande refusée. »).
  Reconnexion : à chaque `connect`, le client redemande `arcs` puis rejoue
  `rejoindre_room` avec la session retenue ; l'ID vit sous
  `undercover-op:joueur:<CODE>`, la session sous `undercover-op:session`.
  Anti-fuite : test de rendu qui compare le squelette DOM de l'écran de manche
  pour deux personnages différents (identique) et vérifie qu'aucun mot de rôle,
  de duo ou de difficulté n'y figure — le drapeau « je ne connais pas » ne
  change que le libellé d'un bouton, pour soi seul.
  Vérifié en vrai : partie complète menée en headless mobile (390×844) contre
  le serveur réel qui servait son propre bundle — l'hôte dans le navigateur,
  deux joueurs en clients socket ; accueil → salle → manche → tour bouclé →
  vote → révélation → fin → retour, plus la reconnexion (même navigateur, même
  place) et le refus `pseudo_pris` d'un navigateur neuf. Signaux retrouvés en
  base à l'issue (`repartition [2, 1]`, `drapeaux 1`, retours 1 et 3).
  14 tests front (vitest), 185 côté serveur.
- **2026-08-19** — revue de code, sept points relevés, tous traités.
  Deux étaient **côté serveur**, rendus atteignables par la reconnexion
  automatique du front — corrigés, le contrat socket n'en bouge pas :
  `rooms.rejoindre` ne remettait jamais `present = True` sur un ID déjà connu
  (un joueur déconnecté en pleine manche restait absent à vie, invisible dans
  la salle et exclu de la manche suivante) ; `Manche.voter` ne vérifiait pas
  que le votant participe encore, si bien que le bulletin d'un parti revenu
  gonflait le total et faisait perdre la majorité stricte à une cible pourtant
  désignée — nouveau refus `hors_manche`. Deux tests neufs les tiennent.
  Côté front : l'ID opaque ne passe plus par `crypto.randomUUID`, réservé aux
  contextes sécurisés — une soirée se joue en HTTP sur le réseau local, et les
  boutons y échouaient en silence ; le personnage de la manche est retenu sous
  `undercover-op:personnage:<CODE>` et relu au démarrage, le serveur ne le
  redistribuant qu'à la manche suivante (sans quoi un rechargement en pleine
  manche donnait un écran vide) ; la session ne s'efface plus sur un refus
  passager (`serveur_muet`, `manche_en_cours`) ; un retour sur une room déjà
  connue renvoie le pseudo retenu, le serveur gardant celui de l'ID qu'il
  connaît ; le service worker ne met plus en cache que les réponses complètes.
  Vérifié à nouveau en navigateur : rechargement en pleine manche, le
  personnage revient et l'écran tient ; et en clients socket : départ, retour,
  vote refusé pour la manche quittée, retour à l'ordre de parole à la suivante.
  16 tests front, 187 côté serveur.

  Reste connu, non traité (règle tranchée au ticket 05) : un rechargement en
  pleine manche fait de vous un **parti** pour cette manche — vous la suivez,
  sans parler ni voter, et vous revenez à la manche suivante.
