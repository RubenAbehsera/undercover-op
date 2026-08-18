# Sprint planning

Le plan vivant : epics, user stories, statut — tenu à jour par l'agent au fil
des séances, rien à renseigner à la main. Quand un US démarre, il obtient son
fichier ticket dans `.scratch/<epic>/issues/NN-<slug>.md` (convention :
docs/agents/issue-tracker.md). Ici on ne garde que la vue d'ensemble — le
pourquoi vit dans docs/pipeline.md, le comment dans fabrication/neo4j/guide.md.

## Epic 1 — Parcours Cypher

- [x] 1.1 Niveaux 1–4 : lire, motifs, agrégats, chemins
- [x] 1.2 Niveau 5 : étalon de validation, proposeur, anti-spoil
- [x] 1.3 Niveau 6 : écriture dans le graphe — fourni en référence
      (apprentissage clos), requêtes validées en live
- [x] 1.4 Niveau 7 : score de paire + classement des 32 — fourni en
      référence, validé en live (le réglage des poids suit en épic 3)
- [ ] 1.5 Figer le parcours : committer guide + corrigés (fichiers en cours
      de modification sur feat/fabrication-neo4j)

## Epic 2 — Étalon : trancher 32 → 24 (fin du jalon 1, clos le 2026-08-18)

Les 32 candidates vivaient dans fabrication/seeds/paires.candidates.yml.
L'œil humain en a retiré 8 à la main, sans le graphe, puis gardé le
reste : 24 figées — le juge a tranché.

- [x] 2.1 Choisir l'étalon — 2026-08-18 : 8 sorties (zoro-kuina,
      nami-bell-mere, chopper-hiriluk, teach-thatch, franky-iceburg,
      lucci-kaku, hancock-sandersonia, shirahoshi-otohime), les 24
      restantes figées
- [x] 2.2 Revue LLM v0 des 32 : drapeaux dans
      fabrication/seeds/paires.review.yml ; kid-killer passé en facile
      (décision humaine), graphe régénéré, 7.3 revérifié (rang 1, score
      inchangé — la difficulté n'est pas scorée)
- [x] 2.3 Arbitrage humain des drapeaux v0 (2026-08-16 : zoro-sanji facile,
      kuma-dragon inversé+egghead, types trahison/couple ajoutés, sanji-judge
      à whole_cake_island) — appliqué dans les seeds, graphe régénéré
- [x] 2.4 Script de revue rejouable : fabrication/llm_review.py (Z.ai en
      direct, GLM, revue par lots de paires — le corpus entier fait diverger
      le raisonnement) ; docs/pipeline.md mis à jour (le LLM quitte le
      « hors v1 » : il drapeaute, l'humain arbitre)
- [x] 2.5 Arbitrer les drapeaux régénérés (paires.review.yml) — clos le
      2026-08-17 : 1re salve (6 « bien vus » : lucci-kaku faction,
      buggy-shanks equipage, doflamingo-rosinante fraternite, zoro-sanji
      baratie, 2 libellés) puis 2e salve (teach-thatch post_enies_lobby,
      luffy-ace libellé neutre, hancock-sandersonia fraternite, luffy-garp
      famille) ; série D et inversions de sens rejetées (reste facile, sens
      conservés) ; convention types figée dans l'en-tête des seeds

## Epic 3 — Score & contrôle du classement (jalon 3)

L'étalon est le lot entier (24) : plus de filtre de sélection. Contrôle :
le classement structurel doit rester cohérent avec l'œil humain — duos
évidents en tête, obscurs en queue. Si ça contredit, on corrige les poids,
jamais les 24.

- [x] 3.1 Score v1 sur les 24 (corrigé 7.2 comme point de départ)
- [x] 3.2 Classement des 24 (7.3) relu par l'œil humain — cohérent
      (équipages partagés en tête, liens minces en queue), validé le
      2026-08-18
- [x] 3.3 Aucun réglage nécessaire — coefficients 7.2 conservés
      (écart 25/15/5, support ×15, précoce +10, calibrage dressrosa)

## Epic 4 — paires.json (contrat figé, ADR 0001)

- [x] 4.1 Script d'export : fabrication/paires_export.py → fabrication/
      paires.json (33 arcs, 87 personnages avec notoriétés, 24 paires dans
      l'ordre du classement ; recoupe graphe/seeds champ à champ — un graphe
      pas régénéré fait échouer l'export)
- [x] 4.2 Relecture humaine du fichier figé avant tout branchement jeu —
      validé le 2026-08-18

## Epic 5 — Côté jeu

- [ ] 5.1 Serveur FastAPI consomme paires.json (calibrage, anti-spoil)
- [ ] 5.2 À détailler avec server/CONTEXT.md
