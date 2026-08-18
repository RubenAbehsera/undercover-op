# 02 — Room & salle d'attente

**What to build:** Un hôte crée une partie : il choisit le calibrage parmi la liste des arcs proposés — limitée aux valeurs qui changent réellement le pool de paires (valeurs distinctes utiles), l'arc retenu étant la borne maximale inclusive. La room naît avec son code. Chaque joueur entre sous un pseudo, à la Kahoot : l'hôte saisit le sien en créant la room, les autres en la rejoignant (code + pseudo) ; le pseudo est unique dans la room et l'ID opaque en localStorage reste l'identité réelle (sans compte). On rejoint uniquement en salle d'attente (entre manches), plafond dur 12 joueurs. L'état de la salle d'attente (pseudos présents, hôte, calibrage) est visible de tous ; les événements socket reflètent arrivées et départs. *(US 5.7, première moitié + choix du calibrage)*

**Blocked by:** 01 — Charger le contrat au démarrage.

**Status:** ready-for-agent

- [x] Créer une room : code généré, hôte défini, pseudo de l'hôte enregistré, calibrage enregistré, liste d'arcs = valeurs qui changent le pool
- [x] Rejoindre par code + pseudo, salle d'attente synchronisée chez tous les présents
- [x] Refus au-delà de 12 joueurs, refus sur code inconnu, refus d'un pseudo déjà pris dans la room
- [x] Un joueur qui repart : la salle d'attente reflète le départ

## Comments

- **2026-08-18** — implémenté TDD (43 tests verts sur la suite entière, dont 33 nouveaux).
  Découpage : `jeu/calibrage.py` (les 15 arcs qui changent réellement le pool — borne =
  max de `arc_etablissement` et des deux `arc_premiere_apparition`, la définition complète
  de l'anti-spoil de `docs/decisions.md`), `jeu/rooms.py` (domaine pur : rooms, code à 4
  signes sans caractère ambigu, pseudos uniques insensibles à la casse, plafond 12,
  départs), `jeu/evenements.py` (couche socket mince : acks `ok`/`motif`, un seul
  `salle_attente` diffusé à tous les présents comme source unique de vérité côté client).
  La salle d'attente ne publie que des pseudos — les ID opaques restent au serveur.
  Tests socket sur un vrai `AsyncServer` avec interception des paquets au fil : le routage
  par room fait son travail (un client hors room ne reçoit rien). Démo live sur uvicorn
  avec trois clients socket.io réels en polling : arcs, création, adhésion synchronisée,
  refus `pseudo_pris` et `code_inconnu`, départ répercuté.
  Deux défauts trouvés en relecture et corrigés : un pseudo vide laissait une room
  orpheline enregistrée ; le handler `disconnect` ignorait l'argument `reason` que
  python-socketio passe réellement (il ne survivait que par le repli « legacy » de la
  bibliothèque).
  Laissé volontairement au ticket 05 : le transfert d'hôte. Le départ de l'hôte laisse
  aujourd'hui `hote: null` dans la salle d'attente — comportement épinglé par un test.
  Le registre s'appelle `Rooms` et non `Salon` : `server/CONTEXT.md` proscrit « salon » pour
  la room. Deux entrées ajoutées à ce vocabulaire — **Salle d'attente** et **Calibrage**.
- **2026-08-18** — pseudo : minimum 2 caractères après déponctuation des espaces
  (`PSEUDO_MINIMUM`), refus `pseudo_invalide` à la création comme à l'adhésion. 47 tests verts.
