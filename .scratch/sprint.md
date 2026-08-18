# Sprint planning

Le plan vivant : épiques, user stories, statut — tenu à jour par l'agent au
fil des séances. Le pourquoi vit dans `docs/pipeline.md`, le comment
fabrication dans `fabrication/neo4j/guide.md`, le vocabulaire jeu dans
`server/CONTEXT.md`.

Conventions :

- Statuts : `[ ]` à faire · `[~]` en cours · `[x]` clos.
- Une US qui démarre obtient son ticket `.scratch/<epic>/issues/NN-<slug>.md`
  (cf. `docs/agents/issue-tracker.md`). Les épiques 1–4 ont été menées avant
  cette convention : leur détail (décisions, livrables) vit directement ici.
- Chaque US close porte sa date ; les décisions de fond sont reprises dans
  `docs/decisions.md` ou un ADR, le sprint n'en garde que la trace.

## Où on en est

| Jalon                                 | État                | Contenu                                                                         |
| ------------------------------------- | ------------------- | ------------------------------------------------------------------------------- |
| Jalon 1 — l'étalon                    | **clos 2026-08-18** | 24 paires figées dans les seeds, arbitrées à l'œil (LLM drapeauteur uniquement) |
| Jalon 3 — la validation par le graphe | **clos 2026-08-18** | score 7.2, classement 7.3 relu et validé, poids inchangés                       |
| Contrat figé                          | **clos 2026-08-18** | `fabrication/paires.json` exporté, relu, committé (ADR 0001)                    |
| Jeu                                   | **ouvert**          | le serveur consomme le contrat — Épic 5                                         |

---

## Epic 1 — Parcours Cypher (apprentissage, clos le 2026-08-15)

Objectif : savoir lire et écrire le graphe soi-même. Livrable :
`fabrication/neo4j/guide.md` (7 niveaux) + `queries.cypher` (corrigés).
Fondations 2026-08-14 : extraction wiki (`wiki_extract.py`, cache local),
seeds, import Cypher (commits 31505ae, 7a41b8b).

- [x] 1.1 Niveaux 1–4 : lire, motifs, agrégats, chemins
- [x] 1.2 Niveau 5 : étalon de validation, proposeur, anti-spoil
- [x] 1.3 Niveau 6 : écriture — générateur `neo4j_import.py` (idempotence
      MERGE, patron MATCH-then-MERGE), `import.cypher` jetable, non suivi
- [x] 1.4 Niveau 7 : score de paire + classement — `l.difficulte` exclue du
      score par design (donnée humaine = tautologie)
- [x] 1.5 Figer le parcours : guide + corrigés committés (922dc20)

## Epic 2 — Étalon : trancher 32 → 24 (clos le 2026-08-18)

Objectif : des paires dont le duo est connu du grand public, en anti-spoil,
sous jugement humain exclusif. Doctrine : **le LLM drapeaute, l'humain
arbitre, jamais l'inverse** (inscrite dans `docs/pipeline.md`).

- [x] 2.1 Revue LLM v0 (2026-08-16) : drapeaux sur les 32 candidates ;
      repérage du défaut kid-killer (second emblématique ≠ difficile) →
      règle réécrite dans l'en-tête des seeds, paire passée facile
- [x] 2.2 Arbitrage v0 (2026-08-16) : zoro-sanji facile ; kuma-dragon
      inversé (Kuma en majorité) + egghead ; création des types `trahison`
      et `couple` ; sanji-judge → whole_cake_island
- [x] 2.3 Script de revue rejouable : `fabrication/llm_review.py` — Z.ai en
      direct (GLM, route coding, stdlib seule), **revue par lots de 8** (sur
      le corpus entier, la réflexion consomme tout le budget de tokens) ;
      sortie `seeds/paires.review.yml`, régénérable
- [x] 2.4 Arbitrage des drapeaux régénérés (2026-08-17) : - appliqués — lucci-kaku `faction`, buggy-shanks `equipage`,
      doflamingo-rosinante `fraternite`, zoro-sanji `baratie`,
      teach-thatch `post_enies_lobby`, luffy-ace libellé neutre
      (« Le grand frère de Luffy »), hancock-sandersonia `fraternite`,
      luffy-garp `famille`, libellés otohime et yamato corrigés ; - rejetés — toute la série D « facile → intermediaire » (le lot reste
      facile), les inversions de sens, les 3 drapeaux kuma-dragon
      (contredisaient l'arbitrage du 16) ; - convention types figée dans les seeds : `fraternite` = fratrie
      (sang ou serment) · `parente` = parent-enfant · `famille` =
      au-delà (grand-parent, oncle…) ; vocabulaire complet : rivalite,
      mentorat, parente, fraternite, famille, equipage, alliance, faction,
      trahison, couple ; difficulté : facile | intermediaire
- [x] 2.5 Sélection finale (2026-08-18) : 8 sorties (zoro-kuina,
      nami-bell-mere, chopper-hiriluk, teach-thatch, franky-iceburg,
      lucci-kaku, hancock-sandersonia, shirahoshi-otohime), **les 24
      restantes figées** — arbitrage explicite de garder le lot entier

Incohérences assumées, ne pas corriger : ids de factions en français, slug
accentué `bell_mère` (mémoire `ids-factions-francais`).

## Epic 3 — Score & contrôle du classement (clos le 2026-08-18)

Objectif : vérifier que la structure du graphe « voit » ce que l'œil a
choisi — l'étalon étant le lot entier, plus de filtre : le contrôle est la
cohérence du classement.

- [x] 3.1 Score v1 sur les 24 (7.2) : écart de notoriété 25/15/5 par
      paliers, support ×15 par groupe partagé, précoce +10 (lien établi
      avant dressrosa) ; coefficients conservés — rien à régler
- [x] 3.2 Classement relu (7.3) : équipages partagés en tête (Shanks/Buggy,
      Kid/Killer 45), liens structurellement minces en queue
      (Sanji/Judge, Bonney/Kuma 5) — validé par l'œil humain
- Limite connue et assumée : la notoriété-degré est un proxy brut
  (5 paires ont un écart négatif — la « majorité » moins connectée que
  l'imposteur) ; le score n'est pas une valeur de jeu, seul son ordre
  survit dans l'export

## Epic 4 — paires.json, contrat figé (clos le 2026-08-18)

Objectif : figer le contrat fabrication → jeu (ADR 0001 : pas de graphe en
production).

- [x] 4.1 Script d'export : `fabrication/paires_export.py` →
      `fabrication/paires.json` — 33 arcs (ordre canonique), 87 personnages
      (notoriétés en nombres), 24 paires dans l'ordre du classement ;
      garde-fous : recoupement graphe/seeds champ à champ (un graphe non
      régénéré fait échouer l'export), enum de difficulté, références et
      unicité des ids, UTF-8 vérifié
- [x] 4.2 Relecture humaine du fichier figé — validée le 2026-08-18
      (commit 0465a62)

---

## Epic 5 — Jeu : le serveur consomme le contrat (ouvert)

Objectif : le serveur FastAPI ne connaît du domaine One Piece que
`paires.json` (vocabulaire : `server/CONTEXT.md`). Stack et règles de jeu
figées dans `docs/decisions.md` : python-socketio async, états en mémoire,
signaux SQLite, sans compte (ID joueur en localStorage), plafond 12 joueurs.

Règles déjà tranchées, à implémenter telles quelles :

- rejoindre uniquement entre manches ; départ en cours → joueur conservé,
  sauté à l'ordre de parole ; départ de l'hôte → transfert au plus ancien ;
- room supprimée après 2 h d'inactivité ; partie terminée par l'hôte
  (déclenche le feedback).

User stories proposées — critère d'acceptation = la démonstration qui fait
fermer l'US :

- [x] 5.1 Charger le contrat au démarrage — schéma Pydantic v2 d'arcs /
      personnages / paires, validation immédiate, message d'erreur net sur
      fichier absent ou invalide. _Acceptance : le serveur démarre avec
      `paires.json`, plante proprement sans lui._
- [x] 5.2 Tirer une manche en anti-spoil — calibrage tranché le
      2026-08-18 : choisi **à la création de la room par l'hôte**, parmi
      la liste des arcs proposés ; l'arc retenu est la borne maximale
      **inclusive** (inscrit dans `docs/decisions.md`). Ne servir que des
      paires d'`arc_etablissement` ≤ calibrage. _Acceptance : propriété
      testée sur les 24 paires, aucune fuite au-delà du calibrage._
      (Note d'implémentation : la liste peut se limiter aux arcs qui
      changent réellement le pool — valeurs distinctes d'arc_etablissement.)
- [x] 5.3 Équilibrer les tirages — déjà tranché dans `docs/decisions.md` :
      tirage aléatoire parmi les paires valides, sans répétition dans la
      partie, stock épuisé → réutilisation. Reste ouvert seulement si l'on
      veut piloter le mélange facile/intermediaire (rien de prévu en v1).
- [x] 5.4 Distribuer les rôles — majorité vs imposteur (sens du lien),
      l'imposteur non informé ; rien ne fuit dans les payloads socket.
- [x] 5.5 La manche — machine à états distribution → tours de parole →
      vote(s) → révélation ; l'hôte détient les contrôles de flux.
- [ ] 5.6 Les signaux — objectif par manche (démasqué ou non, nombre de
      tours, répartition des votes), drapeau « je ne connais pas »
      confidentiel (exclut la manche du calcul qualité des tirages),
      subjectif en fin de partie → SQLite.
- [x] 5.7 Room & partie — cycle de vie complet, règles ci-dessus, code de
      room, transfert d'hôte.
- [ ] 5.8 Branchement front — socket.io-client, PWA minimale ; à détailler
      quand le serveur tient une manche de bout en bout.

Chaque US qui démarre → ticket dans `.scratch/epic-5/issues/` (commencer
par 5.1, `01-chargement-contrat.md`).
