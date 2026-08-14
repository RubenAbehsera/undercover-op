# Pipeline de fabrication

Qui fait quoi dans le rapprochement des paires. Le principe : **les faits viennent du wiki, le rapprochement est fait par le graphe (Neo4j), le jugement reste humain, le LLM n'est jamais décideur.**

```
FABRICATION (hors ligne, jamais en prod)          JEU (production)
══════════════════════════════════════            ═══════════════════

 wiki onepiece.fandom.com
   │  api.php : infobox, Story Arcs
   ▼
 wiki_extract.py ──► cache/ (pages brutes)
 arcs_extract.py
   │
   ▼                 relecture humaine
 seeds/ personnages.yml + arcs.yml
   │
   ├─(jalon 1)──────────────────────────┐
   │                                    │
   │ (jalon 3)                          ▼
   ▼                          ŒIL HUMAIN : 20 paires étalon
 import Cypher                          │
   │                                    │
   ▼                                    │        Le LLM (optionnel,
 Neo4j (Docker local) ◄──optionnel──────┼───     hors v1) propose des
   nœuds : personnages, équipages,      │        relations, paires ou
   factions, arcs, types de pouvoir     │        libellés. Chaque
   relations typées                     │        proposition est
   notoriété = degré du nœud            │        re-vérifiée contre le
   difficulté = distance                │        graphe. Jamais validé
   │                                    │        seul.
   ▼ requêtes Cypher par motifs         │
   poids + fourchette + divergence      │
   + anti-spoil + écart de notoriété    │
   │                                    │
   ▼                                    ▼
 paires candidates ──────► ŒIL HUMAIN (valide)
                                    │
                                    ▼
                          paires.json (figé) ────► serveur FastAPI + front
                                                  socket.io, SQLite (signaux)
```

## Rôles

| Brique | Ce qu'elle fait | Ce qu'elle ne fait pas |
| --- | --- | --- |
| `wiki_extract.py` / `arcs_extract.py` | Collectent les faits (appartenance, première apparition, pouvoir, arcs) | Juger |
| Œil humain | Périmètre, relecture des fiches, 20 paires étalon, validation finale | — |
| Neo4j | **Le rapprochement** : notoriété (degré), difficulté (distance), recouvrement (motifs de chemin), pondération | Rédiger les libellés, inventer des faits |
| LLM (optionnel, hors v1) | Proposer des relations directes mal encodées, des paires candidates, des libellés | Être cru : toute proposition est validée contre le graphe (existence du personnage, véracité des attributs) |
| `paires.json` | Le contrat figé entre fabrication et jeu | Être recalculé en production |

## Chronologie

1. **Jalon 1 (en cours)** : fiches wiki relues + 20 paires choisies à la main, directement au format final. Pas besoin de Neo4j pour ça.
2. **Jalon 3** : import des fiches dans Neo4j, requêtes de sélection. **Test de passage : le pipeline doit retrouver les 20 paires étalon.** S'il ne les retrouve pas, ce sont les poids/requêtes qu'on corrige, pas l'étalon.
3. Le LLM, si activé, intervient en amont des requêtes (enrichissement des relations) — jamais entre le graphe et l'export.
