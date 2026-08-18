// =============================================================================
// Corrigés commentés des exercices de guide.md.
//
// Méthode : écris TA requête dans le Browser AVANT de lire celle-ci.
//   Browser : http://localhost:7474 (neo4j / mot-de-passe-supprime)
//   Fichier entier :
//     docker exec -i undercover-neo4j cypher-shell -u neo4j -p mot-de-passe-supprime \
//       --format plain < queries.cypher
//
// Niveaux 6–7 : référence directe (apprentissage clos) — requêtes à exécuter
// telles quelles, synchronisées avec guide.md (mêmes numéros, tenu à jour
// par l'agent).
// =============================================================================


// ─────────────────────────────────────────────────────────────────────────
// NIVEAU 1 — Lire : MATCH / WHERE / RETURN / ORDER BY
// Doc : Cypher Manual → clauses MATCH, WHERE, RETURN
// -------------------------------------------------------------------------

// 1.1  Dix personnages.
//      (p:Personnage) : la variable p capture un nœud portant le label.
MATCH (p:Personnage)
RETURN p.nom
LIMIT 10;

// 1.2  Fiche complète de Nami : filtrage par propriété DANS le motif.
//      RETURN p sans projection → le Browser dessine le nœud et ses arêtes.
MATCH (p:Personnage {nom: "Nami"})
RETURN p;

// 1.3  Les vétérans d'East Blue. WHERE filtre le motif — l'équivalent SQL
//      filtre des lignes de table ; ici on filtre des nœuds / chemins.
MATCH (p:Personnage)
WHERE p.chapitre < 50
RETURN p.nom, p.chapitre, p.arc
ORDER BY p.chapitre;

// 1.4  Fruits Zoan. CONTAINS = sous-chaîne, insensible à la casse. On ne peut
//      pas tester l'égalité : les types sont bruts du wiki (« Zoan »,
//      « Ancient Zoan », « Paramecia ( Mythical Zoan ) »…). Le nettoyage de
//      ces valeurs est un travail de fabrication, pas de requête.
MATCH (f:Fruit)
WHERE f.type CONTAINS "Zoan"
RETURN f.nom, f.type;


// ─────────────────────────────────────────────────────────────────────────
// NIVEAU 2 — Motifs : les relations sont de l'ASCII-art
// Doc : Cypher Manual → Patterns
//   (a)-[:REL]->(b)  orienté      (a)-[:REL]-(b)  non orienté
// -------------------------------------------------------------------------

// 2.1  Les groupes de Jinbe. Un même type MEMBRE_DE pointe vers des Equipage
//      ET des Faction : labels() les distingue.
MATCH (:Personnage {nom: "Jinbe"})-[:MEMBRE_DE]->(g)
RETURN labels(g)[0] AS nature, g.nom;

// 2.2  L'équipage fondateur, par ordre d'arrivée dans le manga.
MATCH (p:Personnage)-[:MEMBRE_DE]->(:Equipage {id: "straw_hat_pirates"})
RETURN p.nom, p.chapitre
ORDER BY p.chapitre;

// 2.3  Qui mange quoi : DEUX motifs dans un MATCH, reliés par la variable p
//      partagée — c'est le JOIN du graphe, et il se lit comme une phrase.
MATCH (p:Personnage)-[:MEMBRE_DE]->(:Equipage {id: "straw_hat_pirates"}),
      (p)-[:MANGE]->(f:Fruit)
RETURN p.nom, f.nom;

// 2.4  Le croisement : deux motifs successifs = ET logique.
MATCH (p:Personnage)-[:MEMBRE_DE]->(:Faction {id: "generation_terrible"})
MATCH (p)-[:MEMBRE_DE]->(:Faction {id: "empereurs"})
RETURN p.nom;


// ─────────────────────────────────────────────────────────────────────────
// NIVEAU 3 — Agrégats : le GROUP BY est implicite
// Doc : Cypher Manual → Aggregation
// Règle : les colonnes NON agrégées du RETURN forment la clé de regroupement.
// Depuis 2026.07.0 un GROUP BY explicite existe aussi (alignement GQL) ; il
// est optionnel et ne change pas la règle ci-dessus. Voir la variante en 3.1.
// -------------------------------------------------------------------------

// 3.1  Effectifs. count(p) regroupe par g.nom, seule colonne non agrégée.
MATCH (g:Equipage)<-[:MEMBRE_DE]-(p:Personnage)
RETURN g.nom, count(p) AS effectif
ORDER BY effectif DESC;

// 3.1 bis  La même, clé de regroupement déclarée. Utile quand le RETURN est
//          long : la clé devient lisible au lieu d'être déduite de ce qui
//          reste. Erreur de syntaxe avant 2026.07.0 — vérifie ta version
//          avec CALL dbms.components() avant de croire le Cypher Manual.
MATCH (p:Personnage)-[:MEMBRE_DE]->(e:Equipage)
RETURN e.nom AS equipage, count(p) AS effectif
GROUP BY e.nom
ORDER BY effectif DESC;

// 3.2  LA notoriété. -[r]- (sans flèche) = toute relation, tout sens.
//      OPTIONAL MATCH : garde les nœuds sans relations (degré 0) au lieu
//      de les éliminer silencieusement — l'équivalent du LEFT JOIN.
MATCH (p:Personnage)
OPTIONAL MATCH (p)-[r]-()
RETURN p.nom, count(r) AS degre
ORDER BY degre DESC LIMIT 15;

// 3.3  collect() transforme le groupe en liste (l'inverse : UNWIND).
//      Le regroupement se fait sur f.type, colonne non agrégée.
MATCH (p:Personnage)-[:MANGE]->(f:Fruit)
RETURN f.type AS type, collect(p.nom) AS mangeurs
ORDER BY size(mangeurs) DESC;

// 3.4  Zoro et Sanji d'un coup : WHERE ... IN, puis le regroupement par p.nom
//      fait le reste. Un seul motif, zéro UNION.
MATCH (p:Personnage)
WHERE p.nom IN ["Roronoa Zoro", "Sanji"]
OPTIONAL MATCH (p)-[r]-()
RETURN p.nom, count(r) AS degre;


// ─────────────────────────────────────────────────────────────────────────
// NIVEAU 4 — Chemins : là où le graphe écrase le relationnel
// Doc : Cypher Manual → variable-length patterns, shortestPath
//   -[:MEMBRE_DE|PREMIERE_APPARITION|MANGE*..6]-   1 à 6 sauts, types au choix
// -------------------------------------------------------------------------

// 4.1  Plus court chemin Luffy ↔ Garp SANS LIE_A. En restreignant les types
//      dans le motif, LIE_A n'est même pas candidate. Variante générique,
//      quand on ne peut pas lister les types :
//        WHERE none(rel IN relationships(p) WHERE type(rel) = "LIE_A")
MATCH (a:Personnage {nom: "Monkey D. Luffy"}), (b:Personnage {nom: "Monkey D. Garp"})
MATCH p = shortestPath((a)-[:MEMBRE_DE|PREMIERE_APPARITION|MANGE*..6]-(b))
RETURN [n IN nodes(p) | coalesce(n.nom, n.id)] AS etapes, length(p) AS distance;

// 4.1 bis  La même en syntaxe GQL de Cypher 25 : SHORTEST k remplace
//          shortestPath(), et le quantificateur '+' (1 saut ou plus) remplace
//          '*..6'. Les deux formes coexistent sur 2026.x ; la doc « current »
//          ne montre plus que celle-ci, d'où le dépaysement quand on lit le
//          Cypher Manual avec nos corrigés sous les yeux.
MATCH p = SHORTEST 1 (a:Personnage {nom: "Monkey D. Luffy"})
          -[:MEMBRE_DE|PREMIERE_APPARITION|MANGE]-+
          (b:Personnage {nom: "Monkey D. Garp"})
RETURN [n IN nodes(p) | coalesce(n.nom, n.id)] AS etapes, length(p) AS distance;

// 4.2  Luffy ↔ Bonney : lis le chemin à voix haute — « Luffy appartient à la
//      Génération Terrible, Bonney aussi ». Deux sauts, l'équerre du graphe.
MATCH (a:Personnage {nom: "Monkey D. Luffy"}), (b:Personnage {nom: "Jewelry Bonney"})
MATCH p = shortestPath((a)-[:MEMBRE_DE|PREMIERE_APPARITION|MANGE*..6]-(b))
RETURN [n IN nodes(p) | coalesce(n.nom, n.id)] AS etapes, length(p) AS distance;

// 4.3  Longueur EXACTEMENT 2 entre Zoro et Sanji : leurs points communs.
//      Une seule ligne : l'équipage. Pas d'arc commun (Romance Dawn vs
//      Baratie), pas de fruit commun. Une réponse courte EST une information.
MATCH (a:Personnage {nom: "Roronoa Zoro"}), (b:Personnage {nom: "Sanji"})
MATCH p = (a)-[*2]-(b)
RETURN [n IN nodes(p) | coalesce(n.nom, n.id)] AS etapes;

// 4.4  Pourquoi 4 pour usopp-yasopp ? Aucun arc commun, aucun groupe commun :
//      le lien père-fils n'existe nulle part dans les catégories wiki, le
//      chemin doit contourner (Usopp → équipage → Luffy → faction → Shanks
//      → Roger Pirates → Yasopp, à quelques variantes près).
//      PREUVE que LIE_A est indispensable : le graphe structure, l'humain relie.
MATCH (a:Personnage {nom: "Usopp"}), (b:Personnage {nom: "Yasopp"})
MATCH p = shortestPath((a)-[:MEMBRE_DE|PREMIERE_APPARITION|MANGE*..6]-(b))
RETURN [n IN nodes(p) | coalesce(n.nom, n.id)] AS etapes, length(p) AS distance;


// ─────────────────────────────────────────────────────────────────────────
// NIVEAU 5 — Le proposeur : la requête métier de la fabrication
// Doc : Cypher Manual → négation de motifs, pattern comprehension
// -------------------------------------------------------------------------

// 5.1  L'étalon : quelles paires LIE_A ont un support structurel ?
//      (a)-[:MEMBRE_DE]->(g)<-[:MEMBRE_DE]-(b) = le motif « nœud partagé »,
//      l'équerre du graphe.
//      elementId(a) < elementId(b) : un match non orienté produit les DEUX
//      orientations (a,b) et (b,a) — comparer des identifiants internes
//      déduplique. N'importe quel ordre total strict marche (même lexicographique
//      sur des chaînes) : on garde UNE orientation, on ne trie pas.
//      elementId() et non id() : l'entier id() est déprécié depuis Neo4j 5.
MATCH (a:Personnage)-[l:LIE_A]-(b:Personnage)
WHERE elementId(a) < elementId(b)
OPTIONAL MATCH (a)-[:MEMBRE_DE]->(g)<-[:MEMBRE_DE]-(b)
WITH a, b, l, collect(DISTINCT g.nom) AS groupes
WHERE size(groupes) > 0
RETURN a.nom AS majorite, b.nom AS imposteur, l.type AS type, groupes
ORDER BY size(groupes) DESC;

// 5.2  LE proposeur : deux membres d'un même groupe, pas déjà liés, écart de
//      notoriété maximal — la majorité doit être connue, l'imposteur moins.
//        NOT (a)-[:LIE_A]-(b) : négation d'un MOTIF (impossible en SQL pur).
//        [(a)-[r]-() | r]     : pattern comprehension, toutes les relations
//                              de a dans une liste — le degré, avant la mue.
MATCH (a:Personnage)-[:MEMBRE_DE]->(g)<-[:MEMBRE_DE]-(b:Personnage)
WHERE elementId(a) < elementId(b) AND NOT (a)-[:LIE_A]-(b)
WITH a, b, g,
     [(a)-[r]-() | r] AS ra,
     [(b)-[r]-() | r] AS rb
RETURN a.nom AS majorite, b.nom AS imposteur, g.nom AS groupe,
       size(ra) AS deg_a, size(rb) AS deg_b, size(ra) - size(rb) AS ecart
ORDER BY ecart DESC
LIMIT 12;

// 5.3  Anti-spoil : uniquement les liens établis avant l'arc de calibrage.
//      Deux Arcs comparés par leur chapitre de début (propriétés debut/fin).
//      C'est exactement la règle « arc d'établissement ≤ calibrage » du jeu.
MATCH (a:Personnage)-[l:LIE_A]->(b:Personnage)
MATCH (calibrage:Arc {id: "dressrosa"})
MATCH (lien:Arc {id: l.arc})
WHERE lien.debut <= calibrage.debut
RETURN a.nom, b.nom, l.type, l.arc AS arc_du_lien
ORDER BY lien.debut;

// 5.4  Deux groupes partagés : les paires les plus faciles à relier pour un
//      joueur (buggy-shanks : Roger Pirates + Empereurs). Combien sont déjà
//      dans LIE_A ? Ce sont les premières validées par le graphe.
//      Piège Neo4j 5 : un motif nu dans le RETURN est refusé (« A pattern
//      expression should only be used in order to test the existence of a
//      pattern »). Un motif n'est pas une valeur : pour en tirer un booléen il
//      faut le demander, avec la sous-requête EXISTS { }.
MATCH (a:Personnage)-[:MEMBRE_DE]->(g1)<-[:MEMBRE_DE]-(b:Personnage),
      (a)-[:MEMBRE_DE]->(g2)<-[:MEMBRE_DE]-(b)
WHERE elementId(a) < elementId(b) AND elementId(g1) < elementId(g2)
RETURN a.nom, b.nom, g1.nom AS groupe_1, g2.nom AS groupe_2,
       exists { (a)-[:LIE_A]-(b) } AS deja_lie
ORDER BY deja_lie DESC
LIMIT 10;


// ─────────────────────────────────────────────────────────────────────────
// NIVEAU 6 — Écrire dans le graphe : SET / MERGE / UNWIND
// Doc : Cypher Manual → clauses MERGE, SET, UNWIND
// -------------------------------------------------------------------------

// 6.1  La notoriété, matérialisée. SET affecte une propriété sur chaque nœud
//      matché ; la pattern comprehension de 5.2 est une expression, elle vit
//      dans le SET sans agrégat ni sous-requête. Désormais zéro recalcul :
//      les requêtes downstream lisent p.notoriete comme n'importe quelle
//      propriété (visible dans :schema).
MATCH (p:Personnage)
SET p.notoriete = size([(p)-[r]-() | r])
RETURN count(p) AS personnages;

// 6.2  Normalisation. Premier pipeline : UNE ligne (le max). Second : on
//      repart d'elle pour re-parcourir — c'est le re-scope après WITH.
//      100.0 et pas 100 : en Cypher, entier / entier = division entière
//      (100 * 3 / 17 = 0). Un littéral à virgule force la division réelle.
MATCH (p:Personnage)
WITH max(p.notoriete) AS maxi
MATCH (q:Personnage)
SET q.notoriete_norm = toInteger(round(100.0 * q.notoriete / maxi))
RETURN q.nom, q.notoriete, q.notoriete_norm
ORDER BY q.notoriete_norm DESC LIMIT 10;

// 6.3  Le lot en paramètre (commande du Browser, pas du Cypher).
//      UNWIND = collect() à l'envers : une ligne par élément de liste.
//      Le lot vit dans le paramètre, pas dans la requête : changer d'étalon
//      = changer le :param, pas la requête. C'est la brique du 7.3.
//      Attention à l'orientation : majorite d'abord (shanks|buggy, pas
//      l'inverse — voir paires.candidates.yml).
:param etalon => [{a: 'roronoa_zoro', b: 'kuina'}, {a: 'usopp', b: 'yasopp'},
                  {a: 'sanji', b: 'zeff'}, {a: 'shanks', b: 'buggy'}]

UNWIND $etalon AS e
MATCH (a:Personnage {id: e.a})-[l:LIE_A]->(b:Personnage {id: e.b})
OPTIONAL MATCH (a)-[:MEMBRE_DE]->(g)<-[:MEMBRE_DE]-(b)
RETURN e.a + ' / ' + e.b AS paire, l.type AS type,
       collect(DISTINCT g.nom) AS groupes;

// 6.4  MERGE = trouve-ou-crée sur le motif COMPLET. CREATE crée, point.
//      Rejoue chaque bloc et compte : CREATE duplique, MERGE n'y touche plus.
CREATE (:Personnage {id: 'test_create'});
CREATE (:Personnage {id: 'test_create'});
MATCH (t:Personnage {id: 'test_create'}) RETURN count(t);   // 2

MERGE (t:Personnage {id: 'test_merge'});
MERGE (t:Personnage {id: 'test_merge'});
MATCH (t:Personnage {id: 'test_merge'}) RETURN count(t);    // 1

//      C'est la clause qui rend neo4j_import.py rejouable : le graphe est
//      jetable PARCE QUE tout l'import passe par MERGE.
//      Piège classique : MERGE sur un motif partiel (juste le label), puis
//      SET des propriétés — deux exécutions produisent deux nœuds, car le
//      MERGE ne « voit » pas ce qui n'est pas dans son motif. Règle : ce qui
//      identifie va DANS le MERGE, le reste dans ON CREATE SET.
//      Nettoyage — DETACH DELETE retire aussi les relations pendantes :
MATCH (t:Personnage) WHERE t.id IN ['test_create', 'test_merge']
DETACH DELETE t;


// ─────────────────────────────────────────────────────────────────────────
// NIVEAU 7 — Le score, puis le test de passage
// Assemblage de 5.1 + 5.2 + 5.3 ; suppose le 6.1 fait (p.notoriete).
// -------------------------------------------------------------------------

// 7.1  La fiche. MATCH dirigé : LIE_A est orientée majorite → imposteur à
//      l'import, donc une ligne par paire dans le bon sens — le
//      elementId(a) < elementId(b) du 5.1 ne sert plus à rien ici.
//      Un écart négatif n'est pas un bug : l'imposteur mieux connecté que la
//      majorité, c'est une information sur la paire.
MATCH (a:Personnage)-[l:LIE_A]->(b:Personnage)
OPTIONAL MATCH (a)-[:MEMBRE_DE]->(g)<-[:MEMBRE_DE]-(b)
MATCH (arc:Arc {id: l.arc})
WITH a, b, l, arc, collect(DISTINCT g.nom) AS groupes
RETURN a.nom AS majorite, b.nom AS imposteur, l.type AS type,
       a.notoriete AS deg_maj, b.notoriete AS deg_imp,
       a.notoriete - b.notoriete AS ecart, size(groupes) AS support,
       arc.debut AS etabli_au_chapitre
ORDER BY ecart DESC;

// 7.2  Le score. Trois signaux, tous structurels : le graphe seul note.
//      l.difficulte est exclue : humaine, elle transformerait le test en
//      tautologie. Les coefficients sont des HYPOTHÈSES de départ — le
//      réglage se fera contre l'étalon (7.3) en bougeant ces nombres.
MATCH (a:Personnage)-[l:LIE_A]->(b:Personnage)
OPTIONAL MATCH (a)-[:MEMBRE_DE]->(g)<-[:MEMBRE_DE]-(b)
MATCH (arc:Arc {id: l.arc}), (calibrage:Arc {id: 'dressrosa'})
WITH a, b, l, arc, calibrage, collect(DISTINCT g.nom) AS groupes
WITH a, b, l,
     a.notoriete - b.notoriete AS ecart,
     size(groupes) AS support,
     arc.debut <= calibrage.debut AS precoce
RETURN a.nom AS majorite, b.nom AS imposteur, l.type AS type,
       ecart, support, precoce,
       CASE WHEN ecart > 10 THEN 25 WHEN ecart > 4 THEN 15 ELSE 5 END
       + support * 15
       + CASE WHEN precoce THEN 10 ELSE 0 END AS score
ORDER BY score DESC;

// 7.3  Le test de passage. D'abord TOUTES les paires dans une liste
//      (collect), puis UNWIND pour re-déplierer — le couple exact du 6.3.
//      Le rang d'une paire = nombre de scores strictement supérieurs + 1 ;
//      les ex æquo partagent leur rang (classement de compétition, 1-2-2-4).
//      Le calcul du score est recopié de 7.2 : Cypher n'a pas de pipeline
//      réutilisable entre requêtes, la factorisation viendra du script
//      d'export.
:param etalon_ids => ['roronoa_zoro|kuina', 'usopp|yasopp',
                      'sanji|zeff', 'shanks|buggy']

MATCH (a:Personnage)-[l:LIE_A]->(b:Personnage)
OPTIONAL MATCH (a)-[:MEMBRE_DE]->(g)<-[:MEMBRE_DE]-(b)
MATCH (arc:Arc {id: l.arc}), (calibrage:Arc {id: 'dressrosa'})
WITH a, b, arc, calibrage, collect(DISTINCT g.nom) AS groupes
WITH a.id + '|' + b.id AS cle, a.nom + ' / ' + b.nom AS paire,
     CASE WHEN a.notoriete - b.notoriete > 10 THEN 25
          WHEN a.notoriete - b.notoriete > 4 THEN 15 ELSE 5 END
     + size(groupes) * 15
     + CASE WHEN arc.debut <= calibrage.debut THEN 10 ELSE 0 END AS score
WITH collect({cle: cle, paire: paire, score: score}) AS classement
UNWIND classement AS c
WITH c, [autre IN classement WHERE autre.score > c.score | 1] AS devant
RETURN size(devant) + 1 AS rang, c.paire AS paire, c.score AS score,
       c.cle IN $etalon_ids AS etalon
ORDER BY rang, paire;
