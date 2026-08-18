# Décisions de conception

Issues du cadrage du 2026-08-14. Complète `docs/first-idea.md` ; en cas de silence de la note d'intention, ce document fait foi.

## Règles du jeu

- L'imposteur n'est **pas informé** de son rôle : écran identique pour tous, déduction pure.
- Ordre de parole tiré aléatoirement à chaque manche, cyclique, nombre de tours illimité, pas de timer.
- Vote : déclenché par l'hôte uniquement ; une consultation en v1 ; on ne vote pas pour soi ; dépouillement nominatif et public ; majorité stricte des suffrages exprimés sur une seule personne, sinon victoire de l'imposteur ; fermeture quand tous les joueurs connectés ont voté, ou forçage par l'hôte.
- Anti-spoil : filtre sur l'arc de première apparition des deux personnages **et** sur l'arc d'établissement du lien (≤ calibrage).
- Validité d'une paire : fourchette de poids + divergence nette + arcs, **plus écart de notoriété borné** (même ordre de grandeur).
- Une manche est une **séquence de votes** (longueur 1 en v1). Avec 2 imposteurs : éliminations successives — un civil éliminé fait gagner les imposteurs, tous les imposteurs démasqués font gagner le groupe.
- Paire tirée aléatoirement parmi les valides pour le calibrage, sans répétition dans la partie ; stock épuisé → réutilisation autorisée.
- Écran de révélation : les deux personnages, le pseudo de l'imposteur, le libellé du lien. La difficulté n'est jamais affichée aux joueurs.
- Drapeau « je ne connais pas » : strictement confidentiel, définitif pour la manche.
- Retour de fin de partie : trois niveaux en un tap, commentaire optionnel.

## Cycle de vie

- Identité sans compte : ID joueur opaque en localStorage, clé par room ; nouveau navigateur = nouveau joueur.
- Rejoindre uniquement entre manches (salle d'attente) ; plafond dur 12 joueurs.
- Départ en cours de manche : joueur conservé dans l'état, sauté à l'ordre de parole ; départ de l'hôte : transfert au joueur le plus ancien.
- Room supprimée après 2 h d'inactivité ; la partie est terminée par l'hôte (déclenche le feedback).

## Données

Schéma du fichier de paires (contrat partagé fabrication → jeu) :

```jsonc
{
  "arcs": ["romance_dawn", "orange_town", /* … */ "elbaph"],   // 33 arcs canoniques, slugs anglais
  "personnages": [{
    "id": "luffy", "nom": "Monkey D. Luffy",
    "arc_premiere_apparition": "east_blue",
    "notoriete": 14
  }],
  "paires": [{
    "id": "luffy-ace",
    "majorite": "luffy", "imposteur": "ace",
    "lien": { "type": "parente", "libelle": "Frères par serment" },
    "difficulte": "facile",           // facile | intermediaire
    "arc_etablissement": "marineford" // anti-spoil du lien
  }]
}
```

- Slugs d'arcs en anglais, granularité arc canonique (pas saga), orthographe du wiki (« arabasta »).
- Les paires main du jalon 1 sont écrites d'emblée dans ce schéma (24 retenues à l'issue de la sélection).
- **Alimentation des fiches par le wiki** onepiece.fandom.com (API MediaWiki `api.php`) : infobox rendue en priorité, repli sur le `{{Char Box}}` wikitext, cache local sous `fabrication/cache/`. Sorties brutes (`personnages.brut.yml`, `arcs.yml`) relues par un humain avant tout usage — le wiki alimente les faits, jamais le jugement des paires. Les arcs sans plage de chapitres manga (anime-only) sont écartés d'office.

## Technique

- Monorepo : `server/` (jeu), `fabrication/`, `front/` ; vocabulaire dans `CONTEXT-MAP.md`.
- Serveur : Python 3.13, FastAPI, **python-socketio** (async), états de partie en mémoire, signaux en SQLite mono-fichier (stdlib, pas d'ORM), schéma Pydantic v2 partagé, sert le front buildé — un seul conteneur.
- Front : Vite + React + TypeScript, socket.io-client, PWA minimale (manifest + service worker). Le serveur est l'unique source de vérité.
- Fabrication : Neo4j Community en Docker local, driver Python officiel, seeds YAML versionnés, export validé. Passe LLM en amont (`llm_review.py`, par lots) : drapeaute les seeds, arbitrée par l'humain — jamais décideur.
- Interface en français.
- Déploiement : VPS Hostinger (`srv1791681.hstgr.cloud`, Dokploy) via Docker Compose — Traefik + TLS, SQLite sur volume, DNS Hostinger. Hébergement long terme non tranché.

## Refus complémentaires

- Pas de récupération de joueur sans le navigateur d'origine (conséquence assumée de l'absence de comptes).
- Pas de choix de difficulté par l'hôte avant que la boucle de mesure fournisse des données.
