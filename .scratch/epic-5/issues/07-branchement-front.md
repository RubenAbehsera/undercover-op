# 07 — Branchement front

**What to build:** Le client web qui rend le serveur jouable en soirée, sur les téléphones des joueurs. Vite + React + TypeScript, `socket.io-client`, PWA minimale (manifest + service worker), interface en français. Le serveur reste **l'unique source de vérité** : le front n'a aucune règle de jeu, aucun timer, aucun état dérivé — il affiche ce que les diffusions lui donnent et n'envoie que des intentions. Identité sans compte : un ID opaque tiré au premier passage et rangé en `localStorage`, **clé par room** ; nouveau navigateur = nouveau joueur. Le front buildé est servi par le serveur (un seul conteneur). *(US 5.8)*

**Blocked by:** 06 — Les signaux → SQLite.

**Status:** ready-for-agent

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

- [ ] Une partie complète se joue à trois vrais téléphones, du code de room au retour de fin, sans jamais toucher au serveur autrement que par le socket
- [ ] Reconnexion : le même navigateur retrouve son joueur dans la même room (ID en `localStorage`, clé par room) ; un navigateur neuf est un joueur neuf
- [ ] Aucune règle de jeu côté front : les contrôles d'hôte s'affichent d'après l'état diffusé, et un refus serveur (`motif`) s'affiche tel quel, traduit
- [ ] Rien à l'écran ni dans le DOM ne distingue l'imposteur avant la révélation, drapeau « je ne connais pas » compris — audit sur les payloads reçus et le rendu
- [ ] PWA minimale : manifest, icône, installable sur mobile, écran plein
- [ ] `npm run build` produit un bundle que le serveur sert lui-même (un seul conteneur, cf. `docs/decisions.md`)

## À trancher au démarrage du ticket

- Le libellé des trois niveaux du retour (le serveur ne connaît que `1 | 2 | 3`, 1 = mauvais, 3 = excellent).
- La route de service du bundle par FastAPI (`StaticFiles` monté à la racine, sans marcher sur le chemin socket.io).
