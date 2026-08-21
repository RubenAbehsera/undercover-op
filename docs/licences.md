# Licences — le détail

Le [README](../README.md) donne la version courte. Ce document garde le
raisonnement : pourquoi les portraits ne sont pas versionnés, ce que le
partage à l'identique entraîne, et les options écartées.

## Licences et réutilisation

Le projet agrège trois matières juridiquement distinctes. Les confondre est le
piège : citer correctement le wiki règle la deuxième, pas la troisième.

*Ce qui suit décrit les licences applicables et leurs sources ; ce n'est pas un
avis juridique.*

### 1. Le code — MIT

Le code du serveur, du front et de la chaîne de fabrication est sous licence MIT
([LICENSE](../LICENSE)).

Attention à la conséquence, contre-intuitive et volontaire : **le dépôt n'est pas
sous une licence unique**. MIT couvre le code, pas les données — le partage à
l'identique de CC BY-SA se transmet à `paires.json` et aux seeds, c'est-à-dire à
l'artefact le plus intéressant du projet. Qui reprend le code est libre ; qui
reprend les paires hérite du CC BY-SA 3.0. Et les portraits ne sont couverts par
ni l'un ni l'autre : ils ne sont pas redistribués (section 3).

### 2. Les données issues du One Piece Wiki — CC BY-SA 3.0

Le One Piece Wiki (Fandom) publie son **texte** sous
[Creative Commons Attribution-ShareAlike 3.0 Unported](https://creativecommons.org/licenses/by-sa/3.0/),
licence par défaut des communautés Fandom et déclarée par le wiki lui-même
(`meta=siteinfo` → `rightsinfo: CC-BY-SA`, <https://www.fandom.com/licensing>).

Fichiers concernés dans ce dépôt :

| Fichier | Contenu repris |
| --- | --- |
| `fabrication/seeds/personnages.brut.yml` | champs d'infobox extraits verbatim (noms, romanisations, épithètes, affiliations, fruits…) |
| `fabrication/seeds/personnages.yml` | la même matière, nettoyée |
| `fabrication/seeds/arcs.yml`, `equipages.yml`, `factions.yml` | bornes d'arcs, compositions d'équipages et de factions |
| `fabrication/paires.json` | sections `arcs` et `personnages` |

Ce que la licence exige, concrètement :

- **Attribution** — nommer la source, pointer la page ou le wiki, indiquer la
  licence. Le bloc ci-dessous fait l'affaire.
- **Indiquer les modifications** — c'est le cas : les données sont filtrées,
  renommées en identifiants, et enrichies d'une notoriété calculée.
- **Partage dans les mêmes conditions** — toute redistribution de ces données,
  même transformées, doit rester sous CC BY-SA 3.0.

Bloc d'attribution à reprendre tel quel (dépôt, et page « à propos » du jeu si
vous en ajoutez une — l'attribution doit suivre l'œuvre là où elle est diffusée,
pas seulement dans le dépôt) :

> Données de personnages, d'arcs et d'affiliations dérivées du
> [One Piece Wiki](https://onepiece.fandom.com) (Fandom), sous licence
> [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/).
> Extraites, filtrées et remaniées pour les besoins de ce projet.

Le cas des `paires` de `paires.json` est différent : les libellés de lien
(« Le chapeau confié, la promesse ») sont écrits pour le projet, pas repris du
wiki. Le choix des duos, lui, s'appuie sur la matière du wiki — le plus prudent
est de traiter l'ensemble du fichier comme relevant du partage à l'identique.

Note : le cache HTML brut du wiki (`fabrication/cache/`) est ignoré par git et
n'est donc **pas** redistribué. C'est bien ainsi — le garder ainsi.

### 3. Les portraits — le vrai point de blocage

`front/public/personnages/*.webp` sont des captures d'anime extraites du wiki.
**Elles ne sont pas sous CC BY-SA.** Le wiki le dit lui-même, sur sa page
[One Piece Wiki:Copyrights](https://onepiece.fandom.com/wiki/One_Piece_Wiki:Copyrights) :

> *All pictures are not owned by the One Piece Wiki and are subject to copyright
> status by Shueisha's Jump Comics division, Toei Animation and related media
> based groups.*
>
> *All images submitted into the One Piece Wiki are used under a fair use
> rationale.*

Autrement dit : ces images appartiennent à Shueisha, Toei Animation et Eiichiro
Oda. Le wiki ne détient aucun droit dessus et n'en concède aucun.

#### Ce que fait ce dépôt

**Les portraits ne sont pas versionnés.** `front/public/personnages/` est dans
`.gitignore` : le dépôt public ne redistribue aucune image sous droits. Qui veut
les visages les moissonne lui-même — `docker build` s'en charge, ou les scripts
de fabrication en développement (voir « Lancer »). Chaque instance se sert donc
à la source, pour un usage privé qui n'est plus une diffusion.

Corollaire à ne pas perdre de vue : **l'image Docker construite, elle, contient
les portraits**. Elle se déploie sur une instance fermée, et ne se pousse pas sur
un registre public.

C'est la seule combinaison qui tienne les deux bouts : un dépôt ouvert, dont on
peut parler publiquement, et une instance privée jouable entre amis.

#### Pourquoi reprendre leur mention ne suffit pas

Le *fair use* que le wiki invoque n'est pas une licence : c'est un **moyen de
défense** de droit américain (17 U.S.C. §107), apprécié au cas par cas par un
juge, sur quatre facteurs. On ne se l'accorde pas en le déclarant. Afficher la
même mention ne change donc rien à la situation juridique — elle décrit une
analyse, elle ne confère pas de droit.

Et l'analyse en question est celle *de leur usage*, pas du nôtre. Le wiki est une
encyclopédie éditée par une société américaine : vignette basse définition,
illustrant l'article qui décrit précisément ce personnage, entourée de texte
original — plus, côté hébergeur, le régime de retrait sur notification (DMCA).
Dans le jeu, l'image n'illustre aucun propos : **elle est le contenu**, ce qu'on
sert aux joueurs. C'est le facteur qui pèse le plus lourd, et il joue dans
l'autre sens.

#### Le point décisif : le *fair use* n'existe pas en droit français

Le droit français et européen ne connaît pas d'exception ouverte. Il fonctionne
par **liste fermée** d'exceptions (art. L122-5 du Code de la propriété
intellectuelle), et aucune ne couvre cet usage :

- **Courte citation** (L122-5 3° a) — exclue pour les images. La Cour de
  cassation juge de façon constante que la reproduction intégrale d'une œuvre
  visuelle ne peut pas s'analyser en courte citation, quel qu'en soit le format :
  on ne peut pas « citer un bout » d'une image sans la reproduire tout entière.
- **Exception d'information** (L122-5 9°) — réservée à la presse et à
  l'information immédiate. Un jeu n'y entre pas.
- **Parodie** (L122-5 4°) — le jeu ne parodie rien, il utilise les personnages
  au premier degré.

Il n'y a donc pas de mention à afficher qui rendrait la publication régulière.
La seule question qui reste est celle du **périmètre de diffusion**.

#### La voie qui tient réellement : le cercle privé

L122-5 1° dispense les « représentations privées et gratuites effectuées
exclusivement dans un cercle de famille ». C'est exactement ce pour quoi le jeu a
été écrit : gratuit, entre proches, sur invitation. Deux réserves à garder en
tête — le cercle est interprété strictement (la famille et les amis proches, pas
un serveur Discord de deux cents personnes), et une URL publiquement accessible
fait tomber le caractère privé, même si personne ne la partage. Ce qui compte
est le contrôle d'accès réel, pas la discrétion.

#### Les sorties, par risque décroissant

1. **Garder le partage privé** — dépôt privé, image Docker non publiée, accès au
   jeu fermé (le code de room ne suffit pas : il faut que l'instance ne soit pas
   ouverte à tout venant). C'est la seule option qui s'appuie sur une exception
   réelle plutôt que sur la tolérance.
2. **Publier sans les portraits** — sortir `front/public/personnages/` du dépôt
   et laisser chaque instance les moissonner à la construction. Le dépôt ne
   redistribue alors aucune image ; c'est la voie retenue ici.
   Attention : en l'état, `Affiche` (`front/src/Tablee.tsx`) ne montre la
   silhouette que tant que le personnage n'est pas révélé — un fichier manquant
   donne une image cassée, pas un repli. Cette option demande donc un `onError`
   qui bascule sur la silhouette.
3. **Remplacer par des visuels originaux** — dessins ou silhouettes maison, sous
   votre propre licence. Coûteux, mais entièrement propre.
4. **Publier en l'état en connaissance de cause** — usage non commercial, retrait
   sur simple demande, contact visible. C'est un choix assumé, pas une
   conformité : Toei et Shueisha font partie des ayants droit les plus actifs en
   matière de retrait. Le scénario réaliste n'est pas le procès, c'est la
   notification — et il faut pouvoir y répondre vite.

#### Et pointer vers les images du wiki, sans les héberger ?

L'idée est bonne et améliore réellement la position, mais ne la règle pas.

Côté droit, elle fait sortir du cas le plus défavorable. La CJUE distingue
recopier et pointer : republier une copie sur son propre site est une
**nouvelle communication au public** (*Renckhoff*, C-161/17) — c'est exactement
ce que fait l'hébergement actuel des `.webp` — tandis que le simple lien vers une
œuvre déjà librement accessible **avec l'accord de l'ayant droit** n'en est pas
une (*Svensson*, C-466/12). Le problème est la condition : les captures du wiki
n'ont jamais reçu l'accord de Toei ni de Shueisha. On retombe alors sur
*GS Media* (C-160/15), qui juge que pointer vers un contenu mis en ligne sans
l'accord du titulaire peut constituer une communication au public — la
connaissance du caractère illicite étant le critère décisif, présumée en cas de
but lucratif, à démontrer sinon. Un projet non lucratif échappe à la présomption,
mais ce README établit noir sur blanc que ces images sont sous droits : c'est de
la connaissance effective.

Côté technique, c'est faisable — le CDN Fandom sert bien les images à un
référent tiers (`access-control-allow-origin: *`, pas de protection anti-lien) —
mais le projet y perd trois propriétés achetées volontairement :

- **le hors-ligne**. `sw.js` ne met en cache que les réponses `type === "basic"`,
  donc same-origin : des portraits distants ne seraient jamais mis en cache. Une
  soirée sur un wifi capricieux se joue sans visages.
- **l'indépendance à l'exécution**. L'[ADR-0001](./adr/0001-fichier-de-paires-fige.md)
  a écarté toute dépendance externe pendant la partie ; ce serait la réintroduire
  à chaque manche, chez un tiers qu'on ne maîtrise pas.
- **la stabilité et l'anti-spoil**. Les URL ne se déduisent pas de l'`id`
  (chemins hachés du type `e/e9/…`) : il faudrait les stocker par personnage dans
  le contrat figé. Et une image renommée, re-téléversée ou supprimée sur le wiki
  casse le portrait en pleine partie — ou remplace en douce l'onglet d'avant
  l'ellipse par une apparence qui vend la suite.

La sortie 2 (publier sans les portraits) offre le même bénéfice juridique — aucun
contenu sous droits redistribué — sans aucun de ces coûts.

### 4. « One Piece », l'œuvre et la marque

Les personnages, leurs noms et l'univers sont l'œuvre d'Eiichiro Oda, publiée par
Shueisha et adaptée par Toei Animation. Un jeu de fan non commercial est
largement toléré en pratique, ce qui n'en fait pas un droit. Trois réflexes :
ne rien monétiser (pas de dons, pas de pub), n'utiliser aucun logo officiel ni
rien qui suggère une licence, et afficher une mention de non-affiliation :

> Projet de fan non officiel, sans lien avec Eiichiro Oda, Shueisha, Toei
> Animation ou leurs ayants droit. *One Piece* et ses personnages leur
> appartiennent.
