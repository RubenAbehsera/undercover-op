# 01 — Accueil : le pseudo demandé une seule fois

**What to build:** L'accueil demandait le pseudo dans la carte « Rejoindre une partie », alors que « Créer une partie » en avait besoin aussi — et le disait par une note (« Le pseudo saisi ci-dessus sera le vôtre »). Le champ remonte dans son propre bloc, au-dessus des deux cartes : il appartient au joueur, pas à l'une des deux actions. Chaque carte ne garde que ce qui lui est propre — le code pour rejoindre, le calibrage pour créer. *(US 6.1)*

**Status:** done

## Acceptance

- [x] Un seul champ pseudo à l'écran, dans un bloc qui ne porte aucune action
- [x] La carte « Rejoindre » ne contient que le code, la carte « Créer » que le calibrage
- [x] Les deux boutons restent inertes tant que le pseudo est vide

## Tranché à l'implémentation

- Le champ vit **hors des deux `<form>`** : la validation native ne peut donc pas
  le rendre obligatoire (un `required` ne vaut que dans son propre formulaire).
  Les deux boutons se désactivent sur un pseudo vide — un refus visible avant
  le tap plutôt qu'après.

## Comments

- **2026-08-19** — implémenté (`front/src/ecrans/Accueil.tsx`). Rien d'autre n'a
  bougé : `App.tsx` passe toujours le même pseudo aux deux intentions.
