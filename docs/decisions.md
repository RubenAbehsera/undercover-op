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
- Retour de fin de partie : trois niveaux en un tap, commentaire optionnel — libellés **« Bof » / « Sympa » / « Excellent »** pour les niveaux 1 / 2 / 3 (tranché le 2026-08-19).

## Cycle de vie

- Identité sans compte : ID joueur opaque en localStorage, clé par room ; nouveau navigateur = nouveau joueur.
- Pseudo saisi à l'entrée, à la Kahoot : l'hôte à la création de la room, les autres en la rejoignant ; unique dans la room. Le pseudo est l'affichage, l'ID opaque reste l'identité réelle.
- Rejoindre uniquement entre manches (salle d'attente) ; plafond dur 12 joueurs.
- Calibrage d'une room : choisi à la création par l'hôte parmi la liste des arcs proposés ; l'arc retenu est la borne maximale **inclusive** pour l'anti-spoil.
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

**Signaux persistés** (SQLite, tranché à l'implémentation le 2026-08-18) : le signal objectif est **anonyme** — la répartition des votes part en base comme une suite d'effectifs décroissants (`[2, 1]`) accompagnée du nombre de voix portées sur l'imposteur, et le drapeau « je ne connais pas » ne laisse qu'un décompte. Aucune donnée nominative n'est persistée : l'identité des joueurs meurt avec la room. La ligne est rattachée à un identifiant de **partie** propre (le code de room est recyclable). Le retour subjectif est unique par (partie, joueur), garanti par la clé primaire.

- Slugs d'arcs en anglais, granularité arc canonique (pas saga), orthographe du wiki (« arabasta »).
- Les paires main du jalon 1 sont écrites d'emblée dans ce schéma (24 retenues à l'issue de la sélection).
- **Alimentation des fiches par le wiki** onepiece.fandom.com (API MediaWiki `api.php`) : infobox rendue en priorité, repli sur le `{{Char Box}}` wikitext, cache local sous `fabrication/cache/`. Sorties brutes (`personnages.brut.yml`, `arcs.yml`) relues par un humain avant tout usage — le wiki alimente les faits, jamais le jugement des paires. Les arcs sans plage de chapitres manga (anime-only) sont écartés d'office.

## Technique

- Monorepo : `server/` (jeu), `fabrication/`, `front/` ; vocabulaire dans `CONTEXT-MAP.md`.
- Serveur : Python 3.13, FastAPI, **python-socketio** (async), états de partie en mémoire, signaux en SQLite mono-fichier (stdlib, pas d'ORM), schéma Pydantic v2 partagé, sert le front buildé — un seul conteneur.
- Front : Vite + React + TypeScript, socket.io-client, PWA minimale (manifest + service worker). Le serveur est l'unique source de vérité. Le bundle (`front/dist`, chemin réglable par `FRONT_DIST`) est servi par FastAPI, `StaticFiles(html=True)` monté à `/` après les routes HTTP — socket.io détourne `/socket.io` en amont ; sans bundle construit, le montage est sauté.
- Fabrication : Neo4j Community en Docker local, driver Python officiel, seeds YAML versionnés, export validé. Passe LLM en amont (`llm_review.py`, par lots) : drapeaute les seeds, arbitrée par l'humain — jamais décideur.
- Interface en français.
- Déploiement : VPS Hostinger (`srv1791681.hstgr.cloud`, Dokploy) via Docker Compose — Traefik + TLS, SQLite sur volume, DNS Hostinger. Hébergement long terme non tranché.

## Refus complémentaires

- Pas de récupération de joueur sans le navigateur d'origine (conséquence assumée de l'absence de comptes).
- Pas de choix de difficulté par l'hôte avant que la boucle de mesure fournisse des données.
