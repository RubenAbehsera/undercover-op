"""La couche socket : acks de refus et salle d'attente diffusée aux présents.

Le serveur socket.io est réel — seuls les paquets sont interceptés au fil, ce
qui laisse le routage par room faire son travail.
"""

import asyncio
import json
from collections import Counter

import pytest
import socketio

from jeu.contrat import charger_contrat
from jeu.evenements import enregistrer
from jeu.rooms import Rooms


class Fil:
    """Un serveur réel, ses clients factices, et les paquets qu'ils reçoivent."""

    def __init__(self, rooms: Rooms):
        self.rooms = rooms
        self.sio = socketio.AsyncServer(async_mode="asgi")
        enregistrer(self.sio, rooms)
        self.recus: dict[str, list[tuple[str, dict]]] = {}
        self.sio._send_eio_packet = self._capter

    async def _capter(self, eio_sid, paquet) -> None:
        brut = paquet.data
        evenement, charge = json.loads(brut[brut.index("[") :])
        self.recus[eio_sid].append((evenement, charge))

    async def connecter(self, nom: str) -> str:
        self.recus[nom] = []
        return await self.sio.manager.connect(nom, "/")

    async def envoyer(self, sid: str, evenement: str, *donnees):
        return await self.sio._trigger_event(evenement, "/", sid, *donnees)

    async def deconnecter(self, sid: str) -> None:
        raison = self.sio.reason.CLIENT_DISCONNECT
        await self.sio._trigger_event("disconnect", "/", sid, raison)


@pytest.fixture
def fil(chemin_contrat) -> Fil:
    return Fil(Rooms(charger_contrat(chemin_contrat)))


@pytest.fixture
def calibrage(chemin_contrat) -> str:
    from jeu.calibrage import arcs_proposes

    return arcs_proposes(charger_contrat(chemin_contrat))[-1]


def test_l_hote_demande_les_arcs_proposes(fil):
    async def scenario():
        hote = await fil.connecter("eio-hote")
        return await fil.envoyer(hote, "arcs")

    ack = asyncio.run(scenario())

    assert ack["ok"] is True
    assert "romance_dawn" in ack["arcs"]


def test_creer_une_room_ouvre_la_salle_attente(fil, calibrage):
    async def scenario():
        hote = await fil.connecter("eio-hote")
        return await fil.envoyer(
            hote,
            "creer_room",
            {"joueur": "j-hote", "pseudo": "Nami", "calibrage": calibrage},
        )

    ack = asyncio.run(scenario())

    assert ack["ok"] is True
    assert len(ack["code"]) == 4
    assert fil.recus["eio-hote"] == [
        (
            "salle_attente",
            {
                "code": ack["code"],
                "calibrage": calibrage,
                "hote": "Nami",
                "joueurs": ["Nami"],
            },
        )
    ]


def test_rejoindre_synchronise_tous_les_presents(fil, calibrage):
    async def scenario():
        hote = await fil.connecter("eio-hote")
        ack = await fil.envoyer(
            hote,
            "creer_room",
            {"joueur": "j-hote", "pseudo": "Nami", "calibrage": calibrage},
        )
        invite = await fil.connecter("eio-invite")
        return await fil.envoyer(
            invite,
            "rejoindre_room",
            {"joueur": "j-2", "code": ack["code"], "pseudo": "Zoro"},
        )

    ack = asyncio.run(scenario())

    assert ack["ok"] is True
    for eio_sid in ("eio-hote", "eio-invite"):
        evenement, charge = fil.recus[eio_sid][-1]
        assert evenement == "salle_attente"
        assert charge["joueurs"] == ["Nami", "Zoro"]


def test_un_client_hors_de_la_room_ne_recoit_rien(fil, calibrage):
    async def scenario():
        hote = await fil.connecter("eio-hote")
        await fil.envoyer(
            hote,
            "creer_room",
            {"joueur": "j-hote", "pseudo": "Nami", "calibrage": calibrage},
        )
        await fil.connecter("eio-badaud")

    asyncio.run(scenario())

    assert fil.recus["eio-badaud"] == []


def test_un_depart_est_diffuse_aux_restants(fil, calibrage):
    async def scenario():
        hote = await fil.connecter("eio-hote")
        ack = await fil.envoyer(
            hote,
            "creer_room",
            {"joueur": "j-hote", "pseudo": "Nami", "calibrage": calibrage},
        )
        invite = await fil.connecter("eio-invite")
        await fil.envoyer(
            invite,
            "rejoindre_room",
            {"joueur": "j-2", "code": ack["code"], "pseudo": "Zoro"},
        )
        await fil.envoyer(invite, "quitter_room")

    asyncio.run(scenario())

    assert fil.recus["eio-hote"][-1] == (
        "salle_attente",
        {
            "code": fil.recus["eio-hote"][-1][1]["code"],
            "calibrage": calibrage,
            "hote": "Nami",
            "joueurs": ["Nami"],
        },
    )


def test_une_deconnexion_vaut_un_depart(fil, calibrage):
    async def scenario():
        hote = await fil.connecter("eio-hote")
        ack = await fil.envoyer(
            hote,
            "creer_room",
            {"joueur": "j-hote", "pseudo": "Nami", "calibrage": calibrage},
        )
        invite = await fil.connecter("eio-invite")
        await fil.envoyer(
            invite,
            "rejoindre_room",
            {"joueur": "j-2", "code": ack["code"], "pseudo": "Zoro"},
        )
        await fil.deconnecter(invite)

    asyncio.run(scenario())

    assert fil.recus["eio-hote"][-1][1]["joueurs"] == ["Nami"]


def test_une_deconnexion_hors_room_ne_casse_rien(fil):
    async def scenario():
        badaud = await fil.connecter("eio-badaud")
        await fil.deconnecter(badaud)

    asyncio.run(scenario())

    assert fil.recus["eio-badaud"] == []


def test_code_inconnu_refuse_sans_rien_diffuser(fil):
    async def scenario():
        invite = await fil.connecter("eio-invite")
        return await fil.envoyer(
            invite, "rejoindre_room", {"joueur": "j-2", "code": "ZZZZ", "pseudo": "Zoro"}
        )

    ack = asyncio.run(scenario())

    assert ack == {"ok": False, "motif": "code_inconnu", "message": "code inconnu : ZZZZ"}
    assert fil.recus["eio-invite"] == []


def test_pseudo_pris_refuse(fil, calibrage):
    async def scenario():
        hote = await fil.connecter("eio-hote")
        ack = await fil.envoyer(
            hote,
            "creer_room",
            {"joueur": "j-hote", "pseudo": "Nami", "calibrage": calibrage},
        )
        invite = await fil.connecter("eio-invite")
        return await fil.envoyer(
            invite,
            "rejoindre_room",
            {"joueur": "j-2", "code": ack["code"], "pseudo": "Nami"},
        )

    ack = asyncio.run(scenario())

    assert ack["ok"] is False
    assert ack["motif"] == "pseudo_pris"


def test_payload_incomplet_refuse(fil):
    async def scenario():
        hote = await fil.connecter("eio-hote")
        return await fil.envoyer(hote, "creer_room", {"pseudo": "Nami"})

    ack = asyncio.run(scenario())

    assert ack["ok"] is False
    assert ack["motif"] == "payload_invalide"


CLIENTS = ["eio-1", "eio-2", "eio-3"]


async def _salle(fil: Fil, calibrage: str) -> tuple[list[str], str]:
    """Une room de trois joueurs prête à lancer ; renvoie (sids, code), hôte en tête."""
    hote = await fil.connecter(CLIENTS[0])
    ack = await fil.envoyer(
        hote, "creer_room", {"joueur": "j-1", "pseudo": "Nami", "calibrage": calibrage}
    )
    sids = [hote]
    for rang, pseudo in ((2, "Zoro"), (3, "Usopp")):
        sid = await fil.connecter(CLIENTS[rang - 1])
        await fil.envoyer(
            sid,
            "rejoindre_room",
            {"joueur": f"j-{rang}", "code": ack["code"], "pseudo": pseudo},
        )
        sids.append(sid)
    return sids, ack["code"]


def _derniers(fil: Fil) -> list[dict]:
    return [fil.recus[client][-1][1] for client in CLIENTS]


def test_l_hote_lance_la_manche_chacun_recoit_son_personnage(fil, calibrage):
    async def scenario():
        sids, _ = await _salle(fil, calibrage)
        return await fil.envoyer(sids[0], "lancer_manche")

    ack = asyncio.run(scenario())

    assert ack == {"ok": True}
    for client in CLIENTS:
        evenement, charge = fil.recus[client][-1]
        assert evenement == "personnage"
        assert sorted(charge) == ["id", "nom"]
    recus = Counter(charge["id"] for charge in _derniers(fil))
    assert sorted(recus.values()) == [1, 2], "un imposteur, deux majorités"


def test_aucun_evenement_de_distribution_ne_trahit_l_imposteur(fil, calibrage):
    async def scenario():
        sids, code = await _salle(fil, calibrage)
        for client in CLIENTS:
            fil.recus[client].clear()
        await fil.envoyer(sids[0], "lancer_manche")
        return fil.rooms.room(code).manche

    manche = asyncio.run(scenario())

    emis = repr([fil.recus[client] for client in CLIENTS])
    for secret in (
        manche.paire.id,
        manche.paire.lien.libelle,
        manche.paire.lien.type,
        manche.paire.difficulte,
        manche.imposteur,
        "imposteur",
        "majorite",
    ):
        assert secret not in emis, f"fuite : {secret}"


def test_un_joueur_qui_n_est_pas_l_hote_ne_lance_rien(fil, calibrage):
    async def scenario():
        sids, _ = await _salle(fil, calibrage)
        for client in CLIENTS:
            fil.recus[client].clear()
        return await fil.envoyer(sids[1], "lancer_manche")

    ack = asyncio.run(scenario())

    assert ack["ok"] is False
    assert ack["motif"] == "pas_hote"
    assert all(fil.recus[client] == [] for client in CLIENTS)


def test_lancer_a_deux_refuse(fil, calibrage):
    async def scenario():
        hote = await fil.connecter(CLIENTS[0])
        ack = await fil.envoyer(
            hote,
            "creer_room",
            {"joueur": "j-1", "pseudo": "Nami", "calibrage": calibrage},
        )
        invite = await fil.connecter(CLIENTS[1])
        await fil.envoyer(
            invite,
            "rejoindre_room",
            {"joueur": "j-2", "code": ack["code"], "pseudo": "Zoro"},
        )
        return await fil.envoyer(hote, "lancer_manche")

    ack = asyncio.run(scenario())

    assert ack["motif"] == "joueurs_insuffisants"


def test_lancer_sans_room_refuse(fil):
    async def scenario():
        badaud = await fil.connecter("eio-badaud")
        return await fil.envoyer(badaud, "lancer_manche")

    ack = asyncio.run(scenario())

    assert ack["motif"] == "hors_room"
