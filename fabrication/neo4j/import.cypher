// Généré par neo4j_import.py — ne pas éditer à la main.

MATCH (n) DETACH DELETE n;

MERGE (:Arc {id: "romance_dawn", debut: 1, fin: 7});
MERGE (:Arc {id: "orange_town", debut: 8, fin: 21});
MERGE (:Arc {id: "syrup_village", debut: 22, fin: 41});
MERGE (:Arc {id: "baratie", debut: 42, fin: 68});
MERGE (:Arc {id: "arlong_park", debut: 69, fin: 95});
MERGE (:Arc {id: "loguetown", debut: 96, fin: 100});
MERGE (:Arc {id: "reverse_mountain", debut: 101, fin: 105});
MERGE (:Arc {id: "whisky_peak", debut: 106, fin: 114});
MERGE (:Arc {id: "little_garden", debut: 115, fin: 129});
MERGE (:Arc {id: "drum_island", debut: 130, fin: 154});
MERGE (:Arc {id: "arabasta", debut: 155, fin: 217});
MERGE (:Arc {id: "jaya", debut: 218, fin: 236});
MERGE (:Arc {id: "skypiea", debut: 237, fin: 302});
MERGE (:Arc {id: "long_ring_long_land", debut: 303, fin: 321});
MERGE (:Arc {id: "water_7", debut: 322, fin: 374});
MERGE (:Arc {id: "enies_lobby", debut: 375, fin: 430});
MERGE (:Arc {id: "post_enies_lobby", debut: 431, fin: 441});
MERGE (:Arc {id: "thriller_bark", debut: 442, fin: 489});
MERGE (:Arc {id: "sabaody_archipelago", debut: 490, fin: 513});
MERGE (:Arc {id: "amazon_lily", debut: 514, fin: 524});
MERGE (:Arc {id: "impel_down", debut: 525, fin: 549});
MERGE (:Arc {id: "marineford", debut: 550, fin: 580});
MERGE (:Arc {id: "post_war", debut: 581, fin: 597});
MERGE (:Arc {id: "return_to_sabaody", debut: 598, fin: 602});
MERGE (:Arc {id: "fish_man_island", debut: 603, fin: 653});
MERGE (:Arc {id: "punk_hazard", debut: 654, fin: 699});
MERGE (:Arc {id: "dressrosa", debut: 700, fin: 801});
MERGE (:Arc {id: "zou", debut: 802, fin: 824});
MERGE (:Arc {id: "whole_cake_island", debut: 825, fin: 902});
MERGE (:Arc {id: "levely", debut: 903, fin: 908});
MERGE (:Arc {id: "wano_country", debut: 909, fin: 1057});
MERGE (:Arc {id: "egghead", debut: 1058, fin: 1125});
MERGE (:Arc {id: "elbaph", debut: 1126, fin: 1126});

MERGE (:Equipage {id: "straw_hat_pirates", nom: "Straw Hat Pirates"});
MERGE (:Equipage {id: "red_hair_pirates", nom: "Red Hair Pirates"});
MERGE (:Equipage {id: "roger_pirates", nom: "Roger Pirates"});
MERGE (:Equipage {id: "rocks_pirates", nom: "Rocks Pirates"});
MERGE (:Equipage {id: "whitebeard_pirates", nom: "Whitebeard Pirates"});
MERGE (:Equipage {id: "spade_pirates", nom: "Spade Pirates"});
MERGE (:Equipage {id: "heart_pirates", nom: "Heart Pirates"});
MERGE (:Equipage {id: "kid_pirates", nom: "Kid Pirates"});
MERGE (:Equipage {id: "kuja_pirates", nom: "Kuja Pirates"});
MERGE (:Equipage {id: "buggy_pirates", nom: "Buggy Pirates"});
MERGE (:Equipage {id: "cross_guild", nom: "Cross Guild"});
MERGE (:Equipage {id: "blackbeard_pirates", nom: "Blackbeard Pirates"});
MERGE (:Equipage {id: "big_mom_pirates", nom: "Big Mom Pirates"});
MERGE (:Equipage {id: "beasts_pirates", nom: "Beasts Pirates"});
MERGE (:Equipage {id: "sun_pirates", nom: "Sun Pirates"});
MERGE (:Equipage {id: "fire_tank_pirates", nom: "Fire Tank Pirates"});
MERGE (:Faction {id: "marines", nom: "Marines"});
MERGE (:Faction {id: "sept_capitaines", nom: "Seven Warlords of the Sea"});
MERGE (:Faction {id: "generation_terrible", nom: "Worst Generation"});
MERGE (:Faction {id: "revolutionnaires", nom: "Revolutionaries"});
MERGE (:Faction {id: "empereurs", nom: "Four Emperors"});

MERGE (p:Personnage {id: "monkey_d_luffy", nom: "Monkey D. Luffy", chapitre: 1, arc: "romance_dawn"})
MERGE (a:Arc {id: "romance_dawn"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "monkey_d_luffy"}) MATCH (g:Equipage {id: "straw_hat_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "monkey_d_luffy"}) MATCH (g:Faction {id: "empereurs"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "monkey_d_luffy"}) MATCH (g:Faction {id: "generation_terrible"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Gomu Gomu no Mi (Hito Hito no Mi, Model: Nika )", type: "Paramecia ( Mythical Zoan )"});
MATCH (p:Personnage {id: "monkey_d_luffy"}) MATCH (f:Fruit {nom: "Gomu Gomu no Mi (Hito Hito no Mi, Model: Nika )"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "roronoa_zoro", nom: "Roronoa Zoro", chapitre: 3, arc: "romance_dawn"})
MERGE (a:Arc {id: "romance_dawn"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "roronoa_zoro"}) MATCH (g:Equipage {id: "straw_hat_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "roronoa_zoro"}) MATCH (g:Faction {id: "generation_terrible"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "nami", nom: "Nami", chapitre: 8, arc: "orange_town"})
MERGE (a:Arc {id: "orange_town"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "nami"}) MATCH (g:Equipage {id: "straw_hat_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "usopp", nom: "Usopp", chapitre: 23, arc: "syrup_village"})
MERGE (a:Arc {id: "syrup_village"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "usopp"}) MATCH (g:Equipage {id: "straw_hat_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "sanji", nom: "Sanji", chapitre: 43, arc: "baratie"})
MERGE (a:Arc {id: "baratie"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "sanji"}) MATCH (g:Equipage {id: "straw_hat_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "tony_tony_chopper", nom: "Tony Tony Chopper", chapitre: 134, arc: "drum_island"})
MERGE (a:Arc {id: "drum_island"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "tony_tony_chopper"}) MATCH (g:Equipage {id: "straw_hat_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Hito Hito no Mi", type: "Zoan"});
MATCH (p:Personnage {id: "tony_tony_chopper"}) MATCH (f:Fruit {nom: "Hito Hito no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "nico_robin", nom: "Nico Robin", chapitre: 114, arc: "whisky_peak"})
MERGE (a:Arc {id: "whisky_peak"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "nico_robin"}) MATCH (g:Equipage {id: "straw_hat_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Hana Hana no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "nico_robin"}) MATCH (f:Fruit {nom: "Hana Hana no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "franky", nom: "Franky", chapitre: 329, arc: "water_7"})
MERGE (a:Arc {id: "water_7"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "franky"}) MATCH (g:Equipage {id: "straw_hat_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "brook", nom: "Brook", chapitre: 442, arc: "thriller_bark"})
MERGE (a:Arc {id: "thriller_bark"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "brook"}) MATCH (g:Equipage {id: "straw_hat_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Yomi Yomi no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "brook"}) MATCH (f:Fruit {nom: "Yomi Yomi no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "jinbe", nom: "Jinbe", chapitre: 528, arc: "impel_down"})
MERGE (a:Arc {id: "impel_down"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "jinbe"}) MATCH (g:Equipage {id: "big_mom_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "jinbe"}) MATCH (g:Equipage {id: "straw_hat_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "jinbe"}) MATCH (g:Equipage {id: "sun_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "jinbe"}) MATCH (g:Equipage {id: "whitebeard_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "jinbe"}) MATCH (g:Faction {id: "sept_capitaines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "zeff", nom: "Zeff", chapitre: 43, arc: "baratie"})
MERGE (a:Arc {id: "baratie"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (p:Personnage {id: "kuina", nom: "Shimotsuki Kuina", chapitre: 5, arc: "romance_dawn"})
MERGE (a:Arc {id: "romance_dawn"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (p:Personnage {id: "bell_mère", nom: "Bell-mère", chapitre: 77, arc: "arlong_park"})
MERGE (a:Arc {id: "arlong_park"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "bell_mère"}) MATCH (g:Faction {id: "marines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "nojiko", nom: "Nojiko", chapitre: 70, arc: "arlong_park"})
MERGE (a:Arc {id: "arlong_park"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (p:Personnage {id: "arlong", nom: "Arlong", chapitre: 69, arc: "arlong_park"})
MERGE (a:Arc {id: "arlong_park"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "arlong"}) MATCH (g:Equipage {id: "sun_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "yasopp", nom: "Yasopp", chapitre: 1, arc: "romance_dawn"})
MERGE (a:Arc {id: "romance_dawn"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "yasopp"}) MATCH (g:Equipage {id: "red_hair_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "koby", nom: "Koby", chapitre: 2, arc: "romance_dawn"})
MERGE (a:Arc {id: "romance_dawn"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "koby"}) MATCH (g:Faction {id: "marines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "smoker", nom: "Smoker", chapitre: 97, arc: "loguetown"})
MERGE (a:Arc {id: "loguetown"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "smoker"}) MATCH (g:Faction {id: "marines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Moku Moku no Mi", type: "Logia"});
MATCH (p:Personnage {id: "smoker"}) MATCH (f:Fruit {nom: "Moku Moku no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "tashigi", nom: "Tashigi", chapitre: 96, arc: "loguetown"})
MERGE (a:Arc {id: "loguetown"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "tashigi"}) MATCH (g:Faction {id: "marines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "sakazuki", nom: "Sakazuki", chapitre: 397, arc: "enies_lobby"})
MERGE (a:Arc {id: "enies_lobby"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "sakazuki"}) MATCH (g:Faction {id: "marines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Magu Magu no Mi", type: "Logia"});
MATCH (p:Personnage {id: "sakazuki"}) MATCH (f:Fruit {nom: "Magu Magu no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "borsalino", nom: "Borsalino", chapitre: 504, arc: "sabaody_archipelago"})
MERGE (a:Arc {id: "sabaody_archipelago"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "borsalino"}) MATCH (g:Faction {id: "marines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Pika Pika no Mi", type: "Logia"});
MATCH (p:Personnage {id: "borsalino"}) MATCH (f:Fruit {nom: "Pika Pika no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "kuzan", nom: "Kuzan", chapitre: 303, arc: "long_ring_long_land"})
MERGE (a:Arc {id: "long_ring_long_land"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "kuzan"}) MATCH (g:Equipage {id: "blackbeard_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "kuzan"}) MATCH (g:Faction {id: "marines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Hie Hie no Mi", type: "Logia"});
MATCH (p:Personnage {id: "kuzan"}) MATCH (f:Fruit {nom: "Hie Hie no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "issho", nom: "Issho", chapitre: 701, arc: "dressrosa"})
MERGE (a:Arc {id: "dressrosa"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "issho"}) MATCH (g:Faction {id: "marines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Zushi Zushi no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "issho"}) MATCH (f:Fruit {nom: "Zushi Zushi no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "sengoku", nom: "Sengoku", chapitre: 234, arc: "jaya"})
MERGE (a:Arc {id: "jaya"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "sengoku"}) MATCH (g:Faction {id: "marines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Hito Hito no Mi, Model: Daibutsu", type: "Mythical Zoan"});
MATCH (p:Personnage {id: "sengoku"}) MATCH (f:Fruit {nom: "Hito Hito no Mi, Model: Daibutsu"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "vegapunk", nom: "Vegapunk", chapitre: 684, arc: "punk_hazard"})
MERGE (a:Arc {id: "punk_hazard"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "vegapunk"}) MATCH (g:Faction {id: "marines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Nomi Nomi no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "vegapunk"}) MATCH (f:Fruit {nom: "Nomi Nomi no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "gol_d_roger", nom: "Gol D. Roger", chapitre: 1, arc: "romance_dawn"})
MERGE (a:Arc {id: "romance_dawn"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "gol_d_roger"}) MATCH (g:Equipage {id: "roger_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "silvers_rayleigh", nom: "Silvers Rayleigh", chapitre: 19, arc: "orange_town"})
MERGE (a:Arc {id: "orange_town"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "silvers_rayleigh"}) MATCH (g:Equipage {id: "roger_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "shanks", nom: "Shanks", chapitre: 1, arc: "romance_dawn"})
MERGE (a:Arc {id: "romance_dawn"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "shanks"}) MATCH (g:Equipage {id: "red_hair_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "shanks"}) MATCH (g:Equipage {id: "roger_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "shanks"}) MATCH (g:Faction {id: "empereurs"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "edward_newgate", nom: "Edward Newgate", chapitre: 159, arc: "arabasta"})
MERGE (a:Arc {id: "arabasta"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "edward_newgate"}) MATCH (g:Equipage {id: "rocks_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "edward_newgate"}) MATCH (g:Equipage {id: "whitebeard_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "edward_newgate"}) MATCH (g:Faction {id: "empereurs"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Gura Gura no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "edward_newgate"}) MATCH (f:Fruit {nom: "Gura Gura no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "marco", nom: "Polo Marco", chapitre: 234, arc: "jaya"})
MERGE (a:Arc {id: "jaya"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (f:Fruit {nom: "Tori Tori no Mi, Model: Phoenix", type: "Mythical Zoan"});
MATCH (p:Personnage {id: "marco"}) MATCH (f:Fruit {nom: "Tori Tori no Mi, Model: Phoenix"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "portgas_d_ace", nom: "Portgas D. Ace", chapitre: 154, arc: "drum_island"})
MERGE (a:Arc {id: "drum_island"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "portgas_d_ace"}) MATCH (g:Equipage {id: "spade_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "portgas_d_ace"}) MATCH (g:Equipage {id: "whitebeard_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Mera Mera no Mi", type: "Logia"});
MATCH (p:Personnage {id: "portgas_d_ace"}) MATCH (f:Fruit {nom: "Mera Mera no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "kozuki_oden", nom: "Kouzuki Oden", chapitre: 920, arc: "wano_country"})
MERGE (a:Arc {id: "wano_country"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (p:Personnage {id: "monkey_d_garp", nom: "Monkey D. Garp", chapitre: 92, arc: "arlong_park"})
MERGE (a:Arc {id: "arlong_park"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "monkey_d_garp"}) MATCH (g:Faction {id: "marines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "thatch", nom: "Thatch", chapitre: 440, arc: "post_enies_lobby"})
MERGE (a:Arc {id: "post_enies_lobby"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "thatch"}) MATCH (g:Equipage {id: "whitebeard_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "monkey_d_dragon", nom: "Monkey D. Dragon", chapitre: 100, arc: "loguetown"})
MERGE (a:Arc {id: "loguetown"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "monkey_d_dragon"}) MATCH (g:Faction {id: "marines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "monkey_d_dragon"}) MATCH (g:Faction {id: "revolutionnaires"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "sabo", nom: "Sabo", chapitre: 583, arc: "post_war"})
MERGE (a:Arc {id: "post_war"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "sabo"}) MATCH (g:Faction {id: "revolutionnaires"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Mera Mera no Mi", type: "Logia"});
MATCH (p:Personnage {id: "sabo"}) MATCH (f:Fruit {nom: "Mera Mera no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "emporio_ivankov", nom: "Emporio Ivankov", chapitre: 537, arc: "impel_down"})
MERGE (a:Arc {id: "impel_down"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "emporio_ivankov"}) MATCH (g:Faction {id: "revolutionnaires"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Horu Horu no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "emporio_ivankov"}) MATCH (f:Fruit {nom: "Horu Horu no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "dracule_mihawk", nom: "Dracule Mihawk", chapitre: 49, arc: "baratie"})
MERGE (a:Arc {id: "baratie"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "dracule_mihawk"}) MATCH (g:Equipage {id: "cross_guild"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "dracule_mihawk"}) MATCH (g:Faction {id: "sept_capitaines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "crocodile", nom: "Crocodile", chapitre: 126, arc: "little_garden"})
MERGE (a:Arc {id: "little_garden"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "crocodile"}) MATCH (g:Equipage {id: "cross_guild"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "crocodile"}) MATCH (g:Faction {id: "sept_capitaines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Suna Suna no Mi", type: "Logia"});
MATCH (p:Personnage {id: "crocodile"}) MATCH (f:Fruit {nom: "Suna Suna no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "donquixote_doflamingo", nom: "Donquixote Doflamingo", chapitre: 233, arc: "jaya"})
MERGE (a:Arc {id: "jaya"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "donquixote_doflamingo"}) MATCH (g:Faction {id: "sept_capitaines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Ito Ito no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "donquixote_doflamingo"}) MATCH (f:Fruit {nom: "Ito Ito no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "boa_hancock", nom: "Boa Hancock", chapitre: 516, arc: "amazon_lily"})
MERGE (a:Arc {id: "amazon_lily"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "boa_hancock"}) MATCH (g:Equipage {id: "kuja_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "boa_hancock"}) MATCH (g:Faction {id: "sept_capitaines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Mero Mero no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "boa_hancock"}) MATCH (f:Fruit {nom: "Mero Mero no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "bartholomew_kuma", nom: "Bartholomew Kuma", chapitre: 233, arc: "jaya"})
MERGE (a:Arc {id: "jaya"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "bartholomew_kuma"}) MATCH (g:Faction {id: "revolutionnaires"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "bartholomew_kuma"}) MATCH (g:Faction {id: "sept_capitaines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Nikyu Nikyu no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "bartholomew_kuma"}) MATCH (f:Fruit {nom: "Nikyu Nikyu no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "gecko_moria", nom: "Gecko Moria", chapitre: 449, arc: "thriller_bark"})
MERGE (a:Arc {id: "thriller_bark"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "gecko_moria"}) MATCH (g:Faction {id: "sept_capitaines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Kage Kage no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "gecko_moria"}) MATCH (f:Fruit {nom: "Kage Kage no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "buggy", nom: "Buggy", chapitre: 9, arc: "orange_town"})
MERGE (a:Arc {id: "orange_town"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "buggy"}) MATCH (g:Equipage {id: "buggy_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "buggy"}) MATCH (g:Equipage {id: "cross_guild"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "buggy"}) MATCH (g:Equipage {id: "roger_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "buggy"}) MATCH (g:Faction {id: "empereurs"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "buggy"}) MATCH (g:Faction {id: "sept_capitaines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Bara Bara no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "buggy"}) MATCH (f:Fruit {nom: "Bara Bara no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "boa_sandersonia", nom: "Boa Sandersonia", chapitre: 516, arc: "amazon_lily"})
MERGE (a:Arc {id: "amazon_lily"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "boa_sandersonia"}) MATCH (g:Equipage {id: "kuja_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Hebi Hebi no Mi, Model: Anaconda", type: "Zoan"});
MATCH (p:Personnage {id: "boa_sandersonia"}) MATCH (f:Fruit {nom: "Hebi Hebi no Mi, Model: Anaconda"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "shakuyaku", nom: "Shakuyaku", chapitre: 498, arc: "sabaody_archipelago"})
MERGE (a:Arc {id: "sabaody_archipelago"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "shakuyaku"}) MATCH (g:Equipage {id: "kuja_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "eustass_kid", nom: "Eustass Kid", chapitre: 498, arc: "sabaody_archipelago"})
MERGE (a:Arc {id: "sabaody_archipelago"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "eustass_kid"}) MATCH (g:Equipage {id: "kid_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "eustass_kid"}) MATCH (g:Faction {id: "generation_terrible"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Jiki Jiki no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "eustass_kid"}) MATCH (f:Fruit {nom: "Jiki Jiki no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "killer", nom: "Killer", chapitre: 498, arc: "sabaody_archipelago"})
MERGE (a:Arc {id: "sabaody_archipelago"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "killer"}) MATCH (g:Equipage {id: "kid_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "killer"}) MATCH (g:Faction {id: "generation_terrible"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "marshall_d_teach", nom: "Marshall D. Teach", chapitre: 223, arc: "jaya"})
MERGE (a:Arc {id: "jaya"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "marshall_d_teach"}) MATCH (g:Equipage {id: "blackbeard_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "marshall_d_teach"}) MATCH (g:Equipage {id: "whitebeard_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "marshall_d_teach"}) MATCH (g:Faction {id: "empereurs"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "marshall_d_teach"}) MATCH (g:Faction {id: "generation_terrible"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "marshall_d_teach"}) MATCH (g:Faction {id: "sept_capitaines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Yami Yami no Mi", type: "Logia"});
MATCH (p:Personnage {id: "marshall_d_teach"}) MATCH (f:Fruit {nom: "Yami Yami no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "trafalgar_d_water_law", nom: "Trafalgar D. Water Law", chapitre: 498, arc: "sabaody_archipelago"})
MERGE (a:Arc {id: "sabaody_archipelago"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "trafalgar_d_water_law"}) MATCH (g:Equipage {id: "heart_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "trafalgar_d_water_law"}) MATCH (g:Faction {id: "generation_terrible"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "trafalgar_d_water_law"}) MATCH (g:Faction {id: "sept_capitaines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Ope Ope no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "trafalgar_d_water_law"}) MATCH (f:Fruit {nom: "Ope Ope no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "jewelry_bonney", nom: "Jewelry Bonney", chapitre: 498, arc: "sabaody_archipelago"})
MERGE (a:Arc {id: "sabaody_archipelago"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "jewelry_bonney"}) MATCH (g:Faction {id: "generation_terrible"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Toshi Toshi no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "jewelry_bonney"}) MATCH (f:Fruit {nom: "Toshi Toshi no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "nefertari_vivi", nom: "Nefertari Vivi", chapitre: 103, arc: "reverse_mountain"})
MERGE (a:Arc {id: "reverse_mountain"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "nefertari_vivi"}) MATCH (g:Equipage {id: "straw_hat_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "nefertari_cobra", nom: "Nefertari Cobra", chapitre: 142, arc: "drum_island"})
MERGE (a:Arc {id: "drum_island"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (p:Personnage {id: "bentham", nom: "Bentham", chapitre: 129, arc: "little_garden"})
MERGE (a:Arc {id: "little_garden"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (f:Fruit {nom: "Mane Mane no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "bentham"}) MATCH (f:Fruit {nom: "Mane Mane no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "daz_bones", nom: "Daz Bonez", chapitre: 160, arc: "arabasta"})
MERGE (a:Arc {id: "arabasta"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (f:Fruit {nom: "Supa Supa no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "daz_bones"}) MATCH (f:Fruit {nom: "Supa Supa no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "rob_lucci", nom: "Rob Lucci", chapitre: 323, arc: "water_7"})
MERGE (a:Arc {id: "water_7"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (f:Fruit {nom: "Neko Neko no Mi, Model: Leopard", type: "Zoan"});
MATCH (p:Personnage {id: "rob_lucci"}) MATCH (f:Fruit {nom: "Neko Neko no Mi, Model: Leopard"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "kaku", nom: "Kaku", chapitre: 323, arc: "water_7"})
MERGE (a:Arc {id: "water_7"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (f:Fruit {nom: "Ushi Ushi no Mi, Model: Giraffe", type: "Zoan"});
MATCH (p:Personnage {id: "kaku"}) MATCH (f:Fruit {nom: "Ushi Ushi no Mi, Model: Giraffe"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "iceburg", nom: "Iceburg", chapitre: 323, arc: "water_7"})
MERGE (a:Arc {id: "water_7"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (p:Personnage {id: "enel", nom: "Enel", chapitre: 254, arc: "skypiea"})
MERGE (a:Arc {id: "skypiea"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (f:Fruit {nom: "Goro Goro no Mi", type: "Logia"});
MATCH (p:Personnage {id: "enel"}) MATCH (f:Fruit {nom: "Goro Goro no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "wyper", nom: "Wyper", chapitre: 237, arc: "skypiea"})
MERGE (a:Arc {id: "skypiea"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (p:Personnage {id: "gan_fall", nom: "Gan Fall", chapitre: 237, arc: "skypiea"})
MERGE (a:Arc {id: "skypiea"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (p:Personnage {id: "perona", nom: "Perona", chapitre: 443, arc: "thriller_bark"})
MERGE (a:Arc {id: "thriller_bark"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (f:Fruit {nom: "Horo Horo no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "perona"}) MATCH (f:Fruit {nom: "Horo Horo no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "shirahoshi", nom: "Shirahoshi", chapitre: 612, arc: "fish_man_island"})
MERGE (a:Arc {id: "fish_man_island"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (p:Personnage {id: "otohime", nom: "Otohime", chapitre: 621, arc: "fish_man_island"})
MERGE (a:Arc {id: "fish_man_island"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (p:Personnage {id: "neptune", nom: "Neptune", chapitre: 611, arc: "fish_man_island"})
MERGE (a:Arc {id: "fish_man_island"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (p:Personnage {id: "hody_jones", nom: "Hody Jones", chapitre: 608, arc: "fish_man_island"})
MERGE (a:Arc {id: "fish_man_island"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (p:Personnage {id: "fisher_tiger", nom: "Fisher Tiger", chapitre: 521, arc: "amazon_lily"})
MERGE (a:Arc {id: "amazon_lily"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "fisher_tiger"}) MATCH (g:Equipage {id: "sun_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (p:Personnage {id: "hiriluk", nom: "Hiriluk", chapitre: 141, arc: "drum_island"})
MERGE (a:Arc {id: "drum_island"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (p:Personnage {id: "caesar_clown", nom: "Caesar Clown", chapitre: 658, arc: "punk_hazard"})
MERGE (a:Arc {id: "punk_hazard"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "caesar_clown"}) MATCH (g:Faction {id: "marines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Gasu Gasu no Mi", type: "Logia"});
MATCH (p:Personnage {id: "caesar_clown"}) MATCH (f:Fruit {nom: "Gasu Gasu no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "donquixote_rosinante", nom: "Donquixote Rosinante", chapitre: 761, arc: "dressrosa"})
MERGE (a:Arc {id: "dressrosa"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "donquixote_rosinante"}) MATCH (g:Faction {id: "marines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Nagi Nagi no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "donquixote_rosinante"}) MATCH (f:Fruit {nom: "Nagi Nagi no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "rebecca", nom: "Rebecca", chapitre: 704, arc: "dressrosa"})
MERGE (a:Arc {id: "dressrosa"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (p:Personnage {id: "kyros", nom: "Kyros", chapitre: 702, arc: "dressrosa"})
MERGE (a:Arc {id: "dressrosa"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (p:Personnage {id: "monet", nom: "Monet", chapitre: 657, arc: "punk_hazard"})
MERGE (a:Arc {id: "punk_hazard"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (f:Fruit {nom: "Yuki Yuki no Mi", type: "Logia"});
MATCH (p:Personnage {id: "monet"}) MATCH (f:Fruit {nom: "Yuki Yuki no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "charlotte_linlin", nom: "Charlotte Linlin", chapitre: 651, arc: "fish_man_island"})
MERGE (a:Arc {id: "fish_man_island"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "charlotte_linlin"}) MATCH (g:Equipage {id: "big_mom_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "charlotte_linlin"}) MATCH (g:Equipage {id: "rocks_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "charlotte_linlin"}) MATCH (g:Faction {id: "empereurs"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Soru Soru no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "charlotte_linlin"}) MATCH (f:Fruit {nom: "Soru Soru no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "charlotte_katakuri", nom: "Charlotte Katakuri", chapitre: 860, arc: "whole_cake_island"})
MERGE (a:Arc {id: "whole_cake_island"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "charlotte_katakuri"}) MATCH (g:Equipage {id: "big_mom_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Mochi Mochi no Mi", type: "Special Paramecia"});
MATCH (p:Personnage {id: "charlotte_katakuri"}) MATCH (f:Fruit {nom: "Mochi Mochi no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "charlotte_pudding", nom: "Charlotte Pudding", chapitre: 651, arc: "fish_man_island"})
MERGE (a:Arc {id: "fish_man_island"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "charlotte_pudding"}) MATCH (g:Equipage {id: "big_mom_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Memo Memo no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "charlotte_pudding"}) MATCH (f:Fruit {nom: "Memo Memo no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "charlotte_brûlée", nom: "Charlotte Brûlée", chapitre: 831, arc: "whole_cake_island"})
MERGE (a:Arc {id: "whole_cake_island"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "charlotte_brûlée"}) MATCH (g:Equipage {id: "big_mom_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Mira Mira no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "charlotte_brûlée"}) MATCH (f:Fruit {nom: "Mira Mira no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "kaidou", nom: "Kaidou", chapitre: 795, arc: "dressrosa"})
MERGE (a:Arc {id: "dressrosa"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "kaidou"}) MATCH (g:Equipage {id: "beasts_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "kaidou"}) MATCH (g:Equipage {id: "rocks_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "kaidou"}) MATCH (g:Faction {id: "empereurs"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Uo Uo no Mi, Model: Seiryu", type: "Mythical Zoan"});
MATCH (p:Personnage {id: "kaidou"}) MATCH (f:Fruit {nom: "Uo Uo no Mi, Model: Seiryu"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "king", nom: "King", chapitre: 920, arc: "wano_country"})
MERGE (a:Arc {id: "wano_country"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "king"}) MATCH (g:Equipage {id: "beasts_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Ryu Ryu no Mi, Model: Pteranodon", type: "Ancient Zoan"});
MATCH (p:Personnage {id: "king"}) MATCH (f:Fruit {nom: "Ryu Ryu no Mi, Model: Pteranodon"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "queen", nom: "Queen", chapitre: 920, arc: "wano_country"})
MERGE (a:Arc {id: "wano_country"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "queen"}) MATCH (g:Equipage {id: "beasts_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Ryu Ryu no Mi, Model: Brachiosaurus", type: "Ancient Zoan"});
MATCH (p:Personnage {id: "queen"}) MATCH (f:Fruit {nom: "Ryu Ryu no Mi, Model: Brachiosaurus"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "yamato", nom: "Yamato", chapitre: 971, arc: "wano_country"})
MERGE (a:Arc {id: "wano_country"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "yamato"}) MATCH (g:Equipage {id: "beasts_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Inu Inu no Mi, Model: Okuchi no Makami", type: "Mythical Zoan"});
MATCH (p:Personnage {id: "yamato"}) MATCH (f:Fruit {nom: "Inu Inu no Mi, Model: Okuchi no Makami"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "kozuki_momonosuke", nom: "Kouzuki Momonosuke", chapitre: 684, arc: "punk_hazard"})
MERGE (a:Arc {id: "punk_hazard"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (f:Fruit {nom: "Uo Uo no Mi, Model: Seiryu ( Artificial )", type: "Mythical Zoan ( Artificial )"});
MATCH (p:Personnage {id: "kozuki_momonosuke"}) MATCH (f:Fruit {nom: "Uo Uo no Mi, Model: Seiryu ( Artificial )"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "kinemon", nom: "Kin'emon", chapitre: 656, arc: "punk_hazard"})
MERGE (a:Arc {id: "punk_hazard"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (f:Fruit {nom: "Fuku Fuku no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "kinemon"}) MATCH (f:Fruit {nom: "Fuku Fuku no Mi"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "x_drake", nom: "X Drake", chapitre: 498, arc: "sabaody_archipelago"})
MERGE (a:Arc {id: "sabaody_archipelago"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MATCH (p:Personnage {id: "x_drake"}) MATCH (g:Equipage {id: "beasts_pirates"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "x_drake"}) MATCH (g:Faction {id: "generation_terrible"}) MERGE (p)-[:MEMBRE_DE]->(g);
MATCH (p:Personnage {id: "x_drake"}) MATCH (g:Faction {id: "marines"}) MERGE (p)-[:MEMBRE_DE]->(g);
MERGE (f:Fruit {nom: "Ryu Ryu no Mi, Model: Allosaurus", type: "Ancient Zoan"});
MATCH (p:Personnage {id: "x_drake"}) MATCH (f:Fruit {nom: "Ryu Ryu no Mi, Model: Allosaurus"}) MERGE (p)-[:MANGE]->(f);
MERGE (p:Personnage {id: "vinsmoke_judge", nom: "Vinsmoke Judge", chapitre: 832, arc: "whole_cake_island"})
MERGE (a:Arc {id: "whole_cake_island"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (p:Personnage {id: "vinsmoke_reiju", nom: "Vinsmoke Reiju", chapitre: 826, arc: "whole_cake_island"})
MERGE (a:Arc {id: "whole_cake_island"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (p:Personnage {id: "magellan", nom: "Magellan", chapitre: 528, arc: "impel_down"})
MERGE (a:Arc {id: "impel_down"}) MERGE (p)-[:PREMIERE_APPARITION]->(a);
MERGE (f:Fruit {nom: "Doku Doku no Mi", type: "Paramecia"});
MATCH (p:Personnage {id: "magellan"}) MATCH (f:Fruit {nom: "Doku Doku no Mi"}) MERGE (p)-[:MANGE]->(f);

MATCH (a:Personnage {id: "roronoa_zoro"}), (b:Personnage {id: "kuina"}) MERGE (a)-[:LIE_A {type: "rivalite", libelle: "Rivalité d'enfance, promesse du plus grand sabreur", difficulte: "facile", arc: "romance_dawn"}]->(b);
MATCH (a:Personnage {id: "monkey_d_luffy"}), (b:Personnage {id: "shanks"}) MERGE (a)-[:LIE_A {type: "mentorat", libelle: "Le chapeau confié, la promesse", difficulte: "facile", arc: "romance_dawn"}]->(b);
MATCH (a:Personnage {id: "usopp"}), (b:Personnage {id: "yasopp"}) MERGE (a)-[:LIE_A {type: "parente", libelle: "Père et fils tireurs d'élite", difficulte: "facile", arc: "syrup_village"}]->(b);
MATCH (a:Personnage {id: "sanji"}), (b:Personnage {id: "zeff"}) MERGE (a)-[:LIE_A {type: "mentorat", libelle: "La jambe donnée, la dette du cuisinier", difficulte: "facile", arc: "baratie"}]->(b);
MATCH (a:Personnage {id: "roronoa_zoro"}), (b:Personnage {id: "dracule_mihawk"}) MERGE (a)-[:LIE_A {type: "rivalite", libelle: "Battre le plus grand sabreur du monde", difficulte: "facile", arc: "baratie"}]->(b);
MATCH (a:Personnage {id: "nami"}), (b:Personnage {id: "bell_mère"}) MERGE (a)-[:LIE_A {type: "parente", libelle: "Mère adoptive, les clémentines", difficulte: "facile", arc: "arlong_park"}]->(b);
MATCH (a:Personnage {id: "roronoa_zoro"}), (b:Personnage {id: "sanji"}) MERGE (a)-[:LIE_A {type: "equipage", libelle: "Le duo qui ne s'entend jamais, même équipage", difficulte: "intermediaire", arc: "arlong_park"}]->(b);
MATCH (a:Personnage {id: "shanks"}), (b:Personnage {id: "buggy"}) MERGE (a)-[:LIE_A {type: "fraternite", libelle: "Mousses ensemble sur l'Oro Jackson", difficulte: "facile", arc: "loguetown"}]->(b);
MATCH (a:Personnage {id: "monkey_d_luffy"}), (b:Personnage {id: "portgas_d_ace"}) MERGE (a)-[:LIE_A {type: "fraternite", libelle: "Frères par serment", difficulte: "facile", arc: "arabasta"}]->(b);
MATCH (a:Personnage {id: "nefertari_vivi"}), (b:Personnage {id: "crocodile"}) MERGE (a)-[:LIE_A {type: "rivalite", libelle: "L'ennemi qui a mis Arabasta à genoux", difficulte: "facile", arc: "arabasta"}]->(b);
MATCH (a:Personnage {id: "tony_tony_chopper"}), (b:Personnage {id: "hiriluk"}) MERGE (a)-[:LIE_A {type: "mentorat", libelle: "Le médecin et son cerisier", difficulte: "facile", arc: "drum_island"}]->(b);
MATCH (a:Personnage {id: "marshall_d_teach"}), (b:Personnage {id: "thatch"}) MERGE (a)-[:LIE_A {type: "rivalite", libelle: "Le meurtre qui a tout déclenché", difficulte: "facile", arc: "jaya"}]->(b);
MATCH (a:Personnage {id: "enel"}), (b:Personnage {id: "wyper"}) MERGE (a)-[:LIE_A {type: "rivalite", libelle: "Le dieu et le guerrier de Shandia", difficulte: "facile", arc: "skypiea"}]->(b);
MATCH (a:Personnage {id: "franky"}), (b:Personnage {id: "iceburg"}) MERGE (a)-[:LIE_A {type: "fraternite", libelle: "Disciples de Tom, frères de chantier", difficulte: "facile", arc: "water_7"}]->(b);
MATCH (a:Personnage {id: "rob_lucci"}), (b:Personnage {id: "kaku"}) MERGE (a)-[:LIE_A {type: "equipage", libelle: "Le duo inséparable de CP9", difficulte: "intermediaire", arc: "enies_lobby"}]->(b);
MATCH (a:Personnage {id: "monkey_d_luffy"}), (b:Personnage {id: "monkey_d_garp"}) MERGE (a)-[:LIE_A {type: "parente", libelle: "Le petit-fils du héros de la Marine", difficulte: "facile", arc: "post_enies_lobby"}]->(b);
MATCH (a:Personnage {id: "gol_d_roger"}), (b:Personnage {id: "monkey_d_garp"}) MERGE (a)-[:LIE_A {type: "rivalite", libelle: "La rivalité fondatrice, pirate contre Marine", difficulte: "facile", arc: "post_enies_lobby"}]->(b);
MATCH (a:Personnage {id: "portgas_d_ace"}), (b:Personnage {id: "marshall_d_teach"}) MERGE (a)-[:LIE_A {type: "rivalite", libelle: "Le duel de Banaro", difficulte: "facile", arc: "post_enies_lobby"}]->(b);
MATCH (a:Personnage {id: "portgas_d_ace"}), (b:Personnage {id: "sabo"}) MERGE (a)-[:LIE_A {type: "fraternite", libelle: "Frères par serment, le second frère", difficulte: "facile", arc: "post_war"}]->(b);
MATCH (a:Personnage {id: "boa_hancock"}), (b:Personnage {id: "boa_sandersonia"}) MERGE (a)-[:LIE_A {type: "parente", libelle: "Sœurs Gorgon", difficulte: "facile", arc: "amazon_lily"}]->(b);
MATCH (a:Personnage {id: "silvers_rayleigh"}), (b:Personnage {id: "shakuyaku"}) MERGE (a)-[:LIE_A {type: "alliance", libelle: "Le couple légendaire de Sabaody", difficulte: "facile", arc: "sabaody_archipelago"}]->(b);
MATCH (a:Personnage {id: "eustass_kid"}), (b:Personnage {id: "killer"}) MERGE (a)-[:LIE_A {type: "equipage", libelle: "Équipage et Génération Terrible", difficulte: "intermediaire", arc: "sabaody_archipelago"}]->(b);
MATCH (a:Personnage {id: "monkey_d_luffy"}), (b:Personnage {id: "trafalgar_d_water_law"}) MERGE (a)-[:LIE_A {type: "alliance", libelle: "L'alliance de Punk Hazard", difficulte: "facile", arc: "punk_hazard"}]->(b);
MATCH (a:Personnage {id: "donquixote_doflamingo"}), (b:Personnage {id: "donquixote_rosinante"}) MERGE (a)-[:LIE_A {type: "parente", libelle: "Frères ennemis, l'oiseau et la colombe", difficulte: "facile", arc: "dressrosa"}]->(b);
MATCH (a:Personnage {id: "rebecca"}), (b:Personnage {id: "kyros"}) MERGE (a)-[:LIE_A {type: "parente", libelle: "Le père gladiateur et sa fille", difficulte: "facile", arc: "dressrosa"}]->(b);
MATCH (a:Personnage {id: "monkey_d_dragon"}), (b:Personnage {id: "bartholomew_kuma"}) MERGE (a)-[:LIE_A {type: "faction", libelle: "Le loyal silencieux et le chef révolutionnaire", difficulte: "intermediaire", arc: "marineford"}]->(b);
MATCH (a:Personnage {id: "shirahoshi"}), (b:Personnage {id: "otohime"}) MERGE (a)-[:LIE_A {type: "parente", libelle: "Mère et fille, la voix des Poséidons", difficulte: "facile", arc: "fish_man_island"}]->(b);
MATCH (a:Personnage {id: "arlong"}), (b:Personnage {id: "fisher_tiger"}) MERGE (a)-[:LIE_A {type: "equipage", libelle: "L'équipage du Soleil et sa dérive", difficulte: "intermediaire", arc: "fish_man_island"}]->(b);
MATCH (a:Personnage {id: "charlotte_linlin"}), (b:Personnage {id: "charlotte_katakuri"}) MERGE (a)-[:LIE_A {type: "parente", libelle: "Mère et fils, le mur de Big Mom", difficulte: "facile", arc: "whole_cake_island"}]->(b);
MATCH (a:Personnage {id: "sanji"}), (b:Personnage {id: "vinsmoke_judge"}) MERGE (a)-[:LIE_A {type: "parente", libelle: "Le rejet du père, la cuisine contre la science", difficulte: "facile", arc: "zou"}]->(b);
MATCH (a:Personnage {id: "kaidou"}), (b:Personnage {id: "yamato"}) MERGE (a)-[:LIE_A {type: "parente", libelle: "Père ogre, fille rebelle", difficulte: "facile", arc: "wano_country"}]->(b);
MATCH (a:Personnage {id: "jewelry_bonney"}), (b:Personnage {id: "bartholomew_kuma"}) MERGE (a)-[:LIE_A {type: "parente", libelle: "Père et fille, la vérité d'Egghead", difficulte: "facile", arc: "egghead"}]->(b);
