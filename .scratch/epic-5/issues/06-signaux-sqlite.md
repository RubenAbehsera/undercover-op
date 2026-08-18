# 06 — Les signaux → SQLite

**What to build:** La mesure, persistée en SQLite mono-fichier (stdlib, pas d'ORM). Signal objectif par manche, écrit à la révélation : imposteur démasqué ou non, nombre de tours, répartition des votes. Drapeau « je ne connais pas » : par joueur et par manche, strictement confidentiel, définitif pour la manche, et une manche qui le porte est exclue du calcul de qualité des tirages. Signal subjectif en fin de partie : trois niveaux en un tap, commentaire optionnel — déclenché par la fin de partie décidée par l'hôte.

**Blocked by:** 04 — La manche : machine à états · 05 — Cycle de vie room & partie.

**Status:** done

- [x] Chaque manche terminée écrit sa ligne de signal objectif en SQLite
- [x] Drapeau « je ne connais pas » : absent de tous les payloads (confidentiel), définitif pour la manche
- [x] Une manche portant le drapeau est exclue du calcul de qualité des tirages
- [x] Fin de partie → signal subjectif (trois niveaux, commentaire optionnel) enregistré

## Comments

- **2026-08-18** — implémenté TDD (182 tests verts sur la suite entière, dont 43
  nouveaux). Découpage : `jeu/signaux.py` (nouveau) — un `sqlite3` de la stdlib,
  deux tables (`manche`, `retour`), `qualite_tirages()` qui agrège par paire en
  écartant `drapeaux > 0` ; `jeu/manche.py` porte le drapeau
  (`meconnaissances`, `signaler_meconnaissance`), la `repartition()` et
  `voix_imposteur()` ; `jeu/rooms.py` construit le `SignalManche` (`Room.signal()`)
  et le consigne à la révélation (`_consigner`, idempotent via `Manche.consignee`)
  quel que soit le chemin qui y mène — dernier suffrage, forçage de l'hôte, ou
  départ du dernier attendu ; `jeu/evenements.py` ajoute `je_ne_connais_pas` et
  `retour`, tous deux **muets** : un ack au seul demandeur, aucune diffusion.
  Parti pris central : **le signal objectif est anonyme**. La répartition des
  votes part en base comme une suite d'effectifs décroissants (`[2, 1]`) plus le
  décompte des voix portées sur l'imposteur — la mesure veut savoir si le groupe
  s'est rangé ou éparpillé, pas qui a voté quoi. Le drapeau, de même, ne laisse
  qu'un nombre : `drapeaux`, jamais l'identité de celui qui l'a levé. Une room
  purgée n'emporte donc aucune donnée nominative, il n'y en a jamais eu.
  La partie a désormais son identifiant propre (`Room.partie`, uuid4) : le code
  de room est recyclable, la ligne de mesure ne peut pas l'être.
  Le retour subjectif est unique par (partie, joueur) — contrainte de clé
  primaire SQLite, pas une vérification en mémoire : elle survit à la
  déconnexion et à la purge de la room. Niveaux 1–3 bornés côté Pydantic
  (`payload_invalide`) *et* côté magasin (`niveau_invalide`).
  Fichier : `SIGNAUX_SQLITE` sinon `server/signaux.db` (gitignoré) — le volume
  Dokploy en production. `Rooms` sans magasin ouvre une base en mémoire : les
  tests ne touchent pas le disque.
  Démo live sur uvicorn, trois vrais clients socket.io : drapeau levé par Zoro
  sans qu'un seul paquet parte vers les deux autres, second drapeau refusé
  (`deja_signale`), drapeau après révélation refusé (`manche_terminee`),
  révélation intacte, ligne écrite (`kid-killer`, `repartition [2,1]`,
  `voix_imposteur 1`, `drapeaux 1`), retour refusé avant la fin
  (`partie_en_cours`), deux retours enregistrés, doublon refusé
  (`deja_repondu`), niveau 7 refusé — et la qualité des tirages vide, la seule
  manche jouée étant drapeautée : le critère d'exclusion vérifié en vrai.
  Limite assumée : le drapeau ne se lève que **pendant** la manche (paroles ou
  vote). Après la révélation il est refusé — c'est un signal d'échec par
  méconnaissance, pas un commentaire d'après-coup, et il doit être clos quand
  la ligne part en base.
