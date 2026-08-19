# 02 — La tablée : des cadres en ligne, et la révélation qui les retourne

**What to build:** Pendant la manche, l'ordre de parole était une liste verticale de pseudos. Il devient une **tablée** : une rangée de cadres, un par joueur. Le cadre reste masqué (placeholder) tant qu'on n'a pas vu le personnage de ce joueur — c'est-à-dire pour tout le monde sauf soi. Chacun voit **la photo de son personnage**, dans son cadre et en grand au-dessus. À la révélation, tous les cadres se retournent d'un coup et se colorent : **vert** pour le camp qui l'emporte, **rouge** pour l'autre, avec une bannière qui dit à chacun s'il a gagné ou perdu. *(US 6.2)*

**Status:** done

## Les portraits

Le contrat `fabrication/paires.json` ne porte aucune image, et il n'a pas à en porter : une URL n'est pas une donnée de domaine. Les portraits sont un **second artefact figé** fabrication → jeu, extrait du cache wiki déjà présent et posé en statique dans `front/public/personnages/<id>.webp` — le front les résout par l'`id` que le socket lui donne déjà. Le serveur n'en sait rien, le contrat socket ne bouge pas.

## Acceptance

- [x] Pendant la manche, un cadre par joueur en ligne ; seul le sien porte un portrait, les autres un placeholder
- [x] Son propre personnage reste lisible d'un coup d'œil (portrait en grand + nom)
- [x] Rien dans le DOM ne distingue le personnage reçu, portrait et préchargement compris — le test d'anti-fuite tient
- [x] À la révélation, chaque cadre montre le personnage de son joueur, bordé vert (gagné) ou rouge (perdu)
- [x] La bannière dit à chacun son propre sort : l'imposteur gagne tant qu'il n'est pas démasqué, la majorité l'inverse
- [x] Vérifié en navigateur headless mobile (390×844) contre le serveur réel : accueil → salle → manche → vote → révélation

## Tranché à l'implémentation

- **Onglet d'infobox retenu : l'anime d'avant l'ellipse** quand la page en a un.
  Une apparence d'après trahirait déjà la suite à une table calibrée tôt — le
  portrait tombe sous la même règle d'anti-spoil que les paires. Les personnages
  qui n'apparaissent qu'après l'ellipse n'ont qu'un onglet : ils ne sortent de
  toute façon que dans des paires établies tard.
- **Format `webp`, 256 px de large** : le CDN convertit à la volée sur l'en-tête
  `Accept`, une seule extension pour les 37 personnages tirables (940 Ko en tout).
- **Cadrage `object-fit: cover` calé en haut** : les infobox vont du buste au
  plan pied ; c'est le visage qu'il faut garder dans un cadre de 4 rem.
- **L'ordre de la manche est retenu dans l'état** (`etat.ordre`) : la révélation
  n'a pas de liste de joueurs dans sa charge, et on ne touche pas au contrat
  serveur pour lui en ajouter une. Un imposteur parti en cours de manche a
  quitté l'ordre de parole : sa place à table lui est rendue à la révélation.
- Le paragraphe « duo » de la révélation disparaît : les deux personnages sont
  désormais sous les yeux, avec leur nom.

## Comments

- **2026-08-19** — implémenté. `fabrication/portraits_extract.py` (37 portraits,
  rejouable et idempotent : un fichier déjà là n'est pas retéléchargé),
  `front/src/Tablee.tsx` partagé par la manche et la révélation,
  `etat.ts` retient l'ordre, `styles.css` porte les cadres et le verdict.
  Le test d'anti-fuite a dû apprendre à neutraliser `src` **et** `href` :
  React hisse un `<link rel="preload" as="image">` pour le portrait, qui
  nommait le personnage aussi sûrement que l'image. 19 tests front.
