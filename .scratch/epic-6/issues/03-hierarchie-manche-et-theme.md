# 03 — Hiérarchie des contrôles de manche, et le thème « avis de recherche »

**What to build:** Deux choses liées. **(a)** L'écran de manche empilait trois boutons identiques — « J'ai fini », « Ouvrir le vote », « Je ne connais pas ce personnage » — alors qu'ils n'ont ni le même acteur, ni la même fréquence, ni la même conséquence. Chacun retrouve une place qui dit sa nature. **(b)** L'habillage entier est repris autour d'un objet du domaine : l'avis de recherche. *(US 6.3)*

**Status:** done

## Le diagnostic

| Contrôle | Acteur | Fréquence | Conséquence |
|---|---|---|---|
| rendre la parole | l'orateur | à chaque tour de chaque joueur | réversible au tour suivant |
| ouvrir le vote | l'hôte | une fois par manche | **irréversible** : clôt les tours de parole |
| « je ne connais pas » | chacun | une fois, ou jamais | aucune, signal confidentiel |

Le défaut le plus concret : quand l'hôte est aussi l'orateur, deux boutons primaires identiques se touchent. Un pouce qui rate ouvre le vote au premier tour, sans retour possible.

## Ce qui a été fait

- **« J'ai fini » → « Je passe la parole »** (+ chevron SVG décoratif). Le libellé nomme l'effet, pas un état vague. Pas d'icône seule : c'est l'anti-pattern critique `Icon-only buttons without labels`, et rendre la parole n'a pas de glyphe conventionnel.
- **Hors de son tour, aucun bouton primaire** — pas de bouton grisé qui laisse croire à une action possible.
- **« Ouvrir le vote » quitte la pile** : pastille sobre en haut à droite, hors zone du pouce, confirmée par un `<dialog>` natif (piège à focus et Échap gratuits). Le dialogue **n'est rendu que chez l'hôte** — un autre joueur n'en porte même pas le balisage.
- **« Je ne connais pas ce personnage » devient un lien discret sous l'affiche**, là où est l'objet du doute ; une fois levé, il dit « Signalé ».
- **L'écran de vote** : les candidats ne sont plus trois boutons primaires empilés mais une liste de choix (`button.candidat`). Même défaut, même correction.

## Le thème

L'avis de recherche est l'objet le plus identifiable de One Piece, et c'est **exactement** la disposition demandée au ticket 02 : un portrait encadré, un nom dessous. Le thème ne contrarie pas la mise en page, il lui donne un sens.

- Coque sombre et plate (« la nuit en mer »), ce sont les affiches qui éclairent : `--nuit` `#0b1220`, `--pont` `#16202f`, parchemin `#efe2c2` sur encre `#2b2013`, l'or `#e8b04b` conservé de l'ancien thème.
- Une seule police d'affichage, **Graduate** (slab display), **auto-hébergée** en woff2 (6 Ko, `front/public/polices/`) : la PWA se joue hors ligne sur un réseau local, aucun appel à Google Fonts. Le corps de texte reste en `system-ui`.
- L'affiche vierge porte la **silhouette** de l'inconnu, en CSS pur.
- La révélation **tamponne** chaque affiche : « Gagné » à l'encre verte, « Perdu » à l'encre rouge, posé en travers, animé une fois (`prefers-reduced-motion` respecté). Le mot porte l'information, la couleur ne fait que l'appuyer.
- Le code de room est une plaque de parchemin — c'est ce qu'on dicte à voix haute.

## Acceptance

- [x] Un seul bouton primaire à l'écran au plus, et seulement quand c'est son tour
- [x] Le contrôle irréversible est hors de la zone du pouce et passe par une confirmation
- [x] Un joueur qui n'est pas l'hôte ne porte aucun balisage de contrôle d'hôte
- [x] Cibles ≥ 44 px, focus visible sur tous les contrôles, `prefers-reduced-motion` respecté
- [x] Rien dans le DOM ne distingue le personnage reçu — le test d'anti-fuite tient sans être affaibli
- [x] Aucune dépendance ajoutée, aucun appel réseau tiers, contrat socket inchangé
- [x] Vérifié en navigateur headless mobile (390×844) : accueil, salle, manche (mon tour et hors tour), confirmation, vote, révélation

## Tranché à l'implémentation

- **Skill `ui-ux-pro-max`** installé et interrogé. Retenu : `dark-mode-oled`
  (`cost:low`, `accessibility risk:low`, « low-light entertainment ») comme socle,
  la famille **Graduate** (`--domain google-fonts`, slab serif display), et les
  règles *Confirmation Dialogs*, *Touch Target Size*, *Touch Spacing*,
  *Focus States*, *Focus Not Obscured*, *No Emoji as Structural Icons*.
  **Écarté** : la sortie `--design-system`, qui proposait un pattern de landing
  page et un style *3D & Hyperrealism* WebGL noté `cost:high | risk:high` — le
  cliché esport, à l'opposé d'un manga d'aventure et hors budget d'une PWA sans
  dépendances. Deux requêtes (hiérarchie primaire/secondaire, formulation des
  libellés) sont revenues hors sujet : ces deux points relèvent du jugement, pas
  de la base.
- **La pastille d'hôte est en flux, pas en `position: fixed`** — un élément
  flottant persistant peut recouvrir le focus clavier (*Focus Not Obscured*).
- **Le tampon ne se superpose plus au visage** et porte un fond parchemin :
  `mix-blend-mode: multiply` par-dessus une photo rendait le mot illisible.
- Le portrait de la grande affiche est chargé en priorité (`fetchPriority`), les
  petits en `loading="lazy"`.

## Comments

- **2026-08-19** — implémenté. `styles.css` refait intégralement,
  `Tablee.tsx` expose désormais `Affiche` (l'objet) et `Tablee` (le mur),
  `Manche.tsx` réorganisé en quatre zones, `Vote.tsx` change une classe.
  Relevé au passage par les tests : le `<dialog>` de confirmation était d'abord
  rendu chez tout le monde — un joueur ordinaire portait dans son DOM le
  balisage d'un contrôle qu'il n'a pas. Corrigé, et un test le tient.
  21 tests front, 187 côté serveur.
