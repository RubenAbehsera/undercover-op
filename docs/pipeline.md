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
   ▼                          ŒIL HUMAIN : 24 paires figées
 import Cypher                          │
   │                                    │
   ▼                                    │        Le LLM (llm_review.py)
 Neo4j (Docker local) ◄──optionnel──────┼───     drapeaute les seeds
   nœuds : personnages, équipages,      │        (difficulté, sens, arc,
   factions, arcs, types de pouvoir     │        libellé), ancré sur le
   relations typées                     │        cache wiki, par lots.
   notoriété = degré du nœud            │        Arbitré par l'humain.
   difficulté = distance                │        Jamais validé seul.
   │                                    │
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
| Œil humain | Périmètre, relecture des fiches, les 24 paires, validation finale | — |
| Neo4j | **Le rapprochement** : notoriété (degré), difficulté (distance), recouvrement (motifs de chemin), pondération | Rédiger les libellés, inventer des faits |
| LLM (`llm_review.py`) | Drapeauter les paires candidates (difficulté, sens, arc, libellé), ancré sur le cache wiki, par lots ; l'humain arbitre et édite les seeds | Être cru : tout drapeau attend l'arbitrage humain ; toucher le graphe, les seeds ou l'export |
| `paires.json` | Le contrat figé entre fabrication et jeu | Être recalculé en production |

## Chronologie

1. **Jalon 1 (clos le 2026-08-18)** : fiches wiki relues + 24 paires choisies à la main (8 sorties du lot initial de 32), directement au format final. Pas besoin de Neo4j pour ça.
2. **Jalon 3** : import des fiches dans Neo4j, requêtes de score. **Contrôle : le classement des 24 doit rester cohérent avec l'œil humain** (duos évidents en tête, obscurs en queue). S'il contredit, ce sont les poids/requêtes qu'on corrige, jamais les 24.
3. Le LLM (`fabrication/llm_review.py`, revue par lots de paires) relit les seeds en amont des requêtes et produit des drapeaux (`seeds/paires.review.yml`, régénérable) ; l'humain arbitre et applique dans les seeds — jamais entre le graphe et l'export.
