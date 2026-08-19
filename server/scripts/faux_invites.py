"""Des faux invités, pour tester une room tout seul.

    python scripts/faux_invites.py ABCD      # deux invités
    python scripts/faux_invites.py ABCD 4    # quatre

Ce sont de vrais clients socket : ils rejoignent la room comme un téléphone,
rendent la parole quand c'est leur tour et votent quand le vote s'ouvre. Le
serveur ne sait pas qu'ils sont faux — rien n'a été ajouté de son côté.

Outil de développement, à lancer depuis `server/`. Le serveur écouté est
`JEU_URL` (`http://localhost:8000` par défaut). Ctrl-C les fait sortir : le
serveur les retire comme n'importe quel départ.
"""

import asyncio
import os
import random
import sys

import socketio

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)  # accents et sortie au fil

URL = os.environ.get("JEU_URL", "http://localhost:8000")
PSEUDOS = [
    "Zoro", "Nami", "Usopp", "Sanji", "Robin",
    "Franky", "Brook", "Chopper", "Jinbe", "Law", "Bonney",
]
DELAI_PAROLE = 1.5
DELAI_VOTE = 2.5


class FauxInvite:
    """Un invité : il écoute les diffusions et répond au bout d'un temps humain.

    Le porte-parole est le seul à raconter ce qui arrive à toute la room — à
    onze, le même récit onze fois serait illisible.
    """

    def __init__(self, pseudo: str, code: str, porte_parole: bool = False):
        self.pseudo = pseudo
        self.code = code
        self.identifiant = f"faux-{pseudo.lower()}"
        self.porte_parole = porte_parole
        self.client = socketio.AsyncClient()
        self.client.on("personnage", self._personnage)
        self.client.on("tour", self._tour)
        self.client.on("vote_ouvert", self._vote_ouvert)
        self.client.on("revelation", self._revelation)
        self.client.on("partie_terminee", self._partie_terminee)
        self._passages: set[tuple[int, str]] = set()
        self._taches: set[asyncio.Task] = set()
        self._a_vote = False
        self._vote_annonce = False

    async def entrer(self) -> bool:
        await self.client.connect(URL)
        ack = await self.client.call(
            "rejoindre_room",
            {"joueur": self.identifiant, "code": self.code, "pseudo": self.pseudo},
        )
        if not ack.get("ok"):
            print(f"  {self.pseudo} refusé : {ack['motif']} — {ack['message']}")
            await self.client.disconnect()
            return False
        print(f"  {self.pseudo} est entré")
        return True

    async def _personnage(self, fiche: dict) -> None:
        """Nouvelle manche : on repart à neuf, et on dit ce qu'on a tiré."""
        self._passages.clear()
        self._a_vote = False
        self._vote_annonce = False
        print(f"  {self.pseudo} a tiré {fiche['nom']}")

    async def _tour(self, charge: dict) -> None:
        if self.porte_parole:
            print(f"tour {charge['tour']} — {charge['orateur']} a la parole")
        if charge["orateur"] != self.pseudo:
            return
        passage = (charge["tour"], charge["orateur"])
        if passage in self._passages:
            return
        self._passages.add(passage)
        self._creer_tache(self._parler())

    async def _parler(self) -> None:
        await asyncio.sleep(DELAI_PAROLE)
        await self._demander("passer")

    async def _vote_ouvert(self, charge: dict) -> None:
        """Le bulletin se rediffuse à chaque suffrage : on ne l'annonce qu'une fois."""
        if self.porte_parole and not self._vote_annonce:
            self._vote_annonce = True
            print("le vote est ouvert")
        if self._a_vote:
            return
        self._a_vote = True
        autres = [pseudo for pseudo in charge["joueurs"] if pseudo != self.pseudo]
        self._creer_tache(self._voter(random.choice(autres)))

    async def _voter(self, cible: str) -> None:
        await asyncio.sleep(DELAI_VOTE)
        print(f"  {self.pseudo} vote contre {cible}")
        await self._demander("voter", {"cible": cible})

    async def _revelation(self, charge: dict) -> None:
        if not self.porte_parole:
            return
        issue = "démasqué" if charge["demasque"] else "s'en tire"
        imposteur = charge["imposteur"]["nom"]
        joueur = charge["joueur_imposteur"]
        print(f"révélation — {imposteur} ({joueur}) {issue} · {charge['lien']}")

    async def _partie_terminee(self, _charge: dict) -> None:
        """La partie close, chacun laisse son retour — le chemin est testé aussi."""
        retour = {"niveau": random.choice((1, 2, 3)), "commentaire": "faux invité"}
        await self._demander("retour", retour)
        if self.porte_parole:
            print("partie terminée, retours envoyés")

    async def _demander(self, evenement: str, charge: dict | None = None) -> bool:
        if charge is None:
            ack = await self.client.call(evenement)
        else:
            ack = await self.client.call(evenement, charge)
        if not ack.get("ok"):
            print(f"  {self.pseudo} — {evenement} refusé : {ack['motif']}")
        return bool(ack.get("ok"))

    def _creer_tache(self, coroutine) -> None:
        """Le geste part de côté : un invité qui patiente n'assourdit pas son fil."""
        tache = asyncio.create_task(coroutine)
        self._taches.add(tache)
        tache.add_done_callback(self._taches.discard)


async def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        raise SystemExit(2)
    code = sys.argv[1].strip().upper()
    nombre = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    if not 1 <= nombre <= len(PSEUDOS):
        print(f"entre 1 et {len(PSEUDOS)} invités")
        raise SystemExit(2)

    print(f"room {code} sur {URL}")
    invites = [FauxInvite(PSEUDOS[rang], code, rang == 0) for rang in range(nombre)]
    entres = [invite for invite in invites if await invite.entrer()]
    if not entres:
        raise SystemExit(1)
    print("à toi de jouer — Ctrl-C pour les faire sortir")
    await asyncio.gather(*(invite.client.wait() for invite in entres))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nles faux invités s'en vont")
