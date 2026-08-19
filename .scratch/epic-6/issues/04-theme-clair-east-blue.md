# 04 — Le thème clair « East Blue »

**What to build:** Le thème sombre du ticket 03 ne tenait pas avec les avis de recherche : du parchemin sur du bleu nuit, ça fait cave, pas grand large. On garde les affiches telles quelles et on bascule tout le reste en clair — ciel, nuages, mer — d'après les planches de référence fournies. Plus un chapeau de paille posé de travers sur le nom du jeu. *(US 6.4, remplace la moitié « habillage » du ticket 03)*

**Status:** done

## Le décor

Trois calques de fond sur `body`, **aucun élément dans le DOM** : un ciel en dégradé, une bande de nuages blancs posée à l'horizon, une houle en bas de l'écran. Tous en `background-attachment: fixed` et en SVG *data URI* — pas un fichier, pas une requête.

Règle qui tient tout l'écran : **le bleu ne porte jamais un mot à lire.** Chaque texte vit sur du blanc (cartes, listes, bandeaux) ou sur du parchemin (affiches, code de room). C'est ce qui permet un fond aussi coloré sans jamais descendre sous les seuils de contraste.

## La palette

| Rôle | Valeur | Contraste |
|---|---|---|
| Encre (texte) | `#0f3550` | 13:1 sur blanc |
| Discret | `#476a80` | 5,7:1 sur blanc |
| Profond (titres, liens) | `#0a6395` | 6,5:1 sur blanc |
| Or (boutons) | `#f0c264`, creux `#d3a133` | texte `#3a2a05` dessus |
| Or fort (trait) | `#dd9b12` | contour de l'orateur, filet du candidat |
| Ciel / mer | `#eaf6fd` → `#b9dff3` | décor seul |
| Gagné / perdu | `#1f7a45` / `#c03a26` | blanc dessus, 5,3:1 et 5,0:1 |

Le parchemin des affiches ne bouge pas — c'est ce qui plaisait.

## Le chapeau

SVG inline dans le titre d'accueil (calotte, ruban rouge, bord), incliné de 18°, posé sur le « O » de « OP » et débordant légèrement. Décoratif : `aria-hidden`, hors du flux, `pointer-events: none`.

L'icône de la PWA devient le même chapeau : `scripts/icones.py` dessine désormais une calotte, un ruban et un bord sur fond de ciel, toujours sans dépendance.

## Acceptance

- [x] Aucun texte posé directement sur le bleu ; contraste ≥ 4,5:1 partout (≥ 3:1 pour le grand texte)
- [x] Les affiches sont inchangées
- [x] Le chapeau est posé sur une lettre du nom, penché, et ne gêne aucun tap
- [x] `theme-color`, `background_color` du manifeste et barre d'état iOS suivent le thème clair
- [x] Aucun fichier d'image ajouté : nuages, houle et chapeau sont des SVG inline
- [x] Vérifié en navigateur headless mobile sur les six écrans

## Tranché à l'implémentation

- **Les nuages sont à l'horizon, pas en haut de page.** Placés en haut, ils
  passaient derrière le titre et les étiquettes et faisaient une tache. Ancrés
  au-dessus de la houle (`bottom 96px center`), ils lisent comme un décor.
- **Plus de blanc translucide.** Les bandeaux d'état et les boutons discrets
  étaient à `rgb(255 255 255 / .72)` : les nuages transparaissaient et rendaient
  le fond sale. Tout est passé en blanc plein, avec le filet et l'ombre des cartes.
- **L'or a été éclairci vers la paille de l'affiche** (`#dd9b12` → `#f0c264`) :
  l'ancien virait au brun sur fond clair. Un ton soutenu (`--or-fort`) reste pour
  les traits fins — contour de l'orateur, filet du candidat — qui disparaîtraient
  en clair.

## Comments

- **2026-08-19** — implémenté. `styles.css` refait, `Accueil.tsx` porte le
  chapeau, `scripts/icones.py` redessine l'icône, `index.html` et
  `manifest.webmanifest` suivent les couleurs. Aucun composant restructuré : la
  hiérarchie des contrôles du ticket 03 est intacte, et les 21 tests front
  passent sans modification.
