"""Les événements socket de la salle d'attente — une couche mince sur le rooms.

Chaque demande répond par un ack (`ok` vrai, ou le motif du refus) ; l'état de
la salle d'attente, lui, n'existe qu'en diffusion : un seul `salle_attente`
part vers tous les présents, source unique de vérité pour les clients.
"""

import socketio
from pydantic import BaseModel, ValidationError

from jeu.manche import Manche
from jeu.rooms import ErreurRoom, Room, Rooms


class Creation(BaseModel):
    joueur: str
    pseudo: str
    calibrage: str


class Adhesion(BaseModel):
    joueur: str
    code: str
    pseudo: str


def enregistrer(sio: socketio.AsyncServer, rooms: Rooms) -> None:
    """Branche les événements de salle d'attente sur le serveur socket."""
    presences: dict[str, tuple[str, str]] = {}

    async def entrer(sid: str, room: Room, joueur: str) -> None:
        await sio.enter_room(sid, room.code)
        presences[sid] = (room.code, joueur)
        await diffuser(room)

    async def sortir(sid: str) -> None:
        presence = presences.pop(sid, None)
        if presence is None:
            return
        code, joueur = presence
        await sio.leave_room(sid, code)
        room = rooms.quitter(code, joueur)
        if room is not None:
            await diffuser(room)

    async def distribuer(code: str, manche: Manche) -> None:
        """À chacun son personnage, en privé.

        Jamais deux payloads de forme différente, jamais un mot de plus pour
        l'imposteur — un joueur ne sait que ce qu'il a tiré.
        """
        for present, (code_present, joueur) in list(presences.items()):
            if code_present == code:
                await sio.emit("personnage", manche.personnage(joueur), to=present)

    async def diffuser(room: Room) -> None:
        await sio.emit("salle_attente", room.salle_attente(), room=room.code)

    @sio.on("arcs")
    async def arcs(sid) -> dict:
        return {"ok": True, "arcs": rooms.arcs_proposes}

    @sio.on("creer_room")
    async def creer_room(sid, donnees) -> dict:
        try:
            demande = Creation.model_validate(donnees)
            room = rooms.creer(demande.joueur, demande.pseudo, demande.calibrage)
        except ValidationError:
            return _refus("payload_invalide", "demande incomplète")
        except ErreurRoom as err:
            return _refus(err.motif, str(err))
        await entrer(sid, room, demande.joueur)
        return {"ok": True, "code": room.code}

    @sio.on("rejoindre_room")
    async def rejoindre_room(sid, donnees) -> dict:
        try:
            demande = Adhesion.model_validate(donnees)
            room = rooms.rejoindre(demande.code, demande.joueur, demande.pseudo)
        except ValidationError:
            return _refus("payload_invalide", "demande incomplète")
        except ErreurRoom as err:
            return _refus(err.motif, str(err))
        await entrer(sid, room, demande.joueur)
        return {"ok": True, "code": room.code}

    @sio.on("lancer_manche")
    async def lancer_manche(sid) -> dict:
        presence = presences.get(sid)
        if presence is None:
            return _refus("hors_room", "aucune room pour ce client")
        code, joueur = presence
        try:
            manche = rooms.lancer_manche(code, joueur)
        except ErreurRoom as err:
            return _refus(err.motif, str(err))
        await distribuer(code, manche)
        return {"ok": True}

    @sio.on("quitter_room")
    async def quitter_room(sid) -> dict:
        await sortir(sid)
        return {"ok": True}

    @sio.event
    async def disconnect(sid, raison=None) -> None:
        await sortir(sid)


def _refus(motif: str, message: str) -> dict:
    return {"ok": False, "motif": motif, "message": message}
