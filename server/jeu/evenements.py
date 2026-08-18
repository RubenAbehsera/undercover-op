"""Les événements socket de la salle d'attente — une couche mince sur le rooms.

Chaque demande répond par un ack (`ok` vrai, ou le motif du refus) ; l'état de
la salle d'attente, lui, n'existe qu'en diffusion : un seul `salle_attente`
part vers tous les présents, source unique de vérité pour les clients.
"""

import socketio
from pydantic import BaseModel, ValidationError

from jeu.erreurs import ErreurRoom
from jeu.manche import Manche
from jeu.rooms import Room, Rooms


class Creation(BaseModel):
    joueur: str
    pseudo: str
    calibrage: str


class Adhesion(BaseModel):
    joueur: str
    code: str
    pseudo: str


class Suffrage(BaseModel):
    cible: str


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
        en_manche = _manche_en_cours(code)
        room = rooms.quitter(code, joueur)
        if room is None:
            return
        await diffuser(room)
        if en_manche:
            await diffuser_manche(room)

    def _manche_en_cours(code: str) -> bool:
        """Le départ d'un joueur ne rebat les cartes que si une manche court."""
        try:
            room = rooms.room(code)
        except ErreurRoom:
            return False
        return room.manche is not None and room.manche.en_cours()

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

    async def diffuser_manche(room: Room) -> None:
        """L'état public de la manche : le tour de parole, ou la révélation."""
        if room.manche.etat == "revelation":
            await sio.emit("revelation", room.revelation(), room=room.code)
        elif room.manche.etat == "vote":
            await sio.emit("vote_ouvert", room.vote_ouvert(), room=room.code)
        else:
            await sio.emit("tour", room.tour(), room=room.code)

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
        await diffuser_manche(rooms.room(code))
        return {"ok": True}

    @sio.on("passer")
    async def passer(sid) -> dict:
        return await _flux(sid, rooms.passer_parole)

    @sio.on("ouvrir_vote")
    async def ouvrir_vote(sid) -> dict:
        return await _flux(sid, rooms.ouvrir_vote)

    @sio.on("forcer_vote")
    async def forcer_vote(sid) -> dict:
        return await _flux(sid, rooms.forcer_vote)

    @sio.on("voter")
    async def voter(sid, donnees) -> dict:
        try:
            suffrage = Suffrage.model_validate(donnees)
        except ValidationError:
            return _refus("payload_invalide", "demande incomplète")
        return await _flux(sid, rooms.voter, suffrage.cible)

    async def _flux(sid, demande, *arguments, diffusion=None) -> dict:
        """Un contrôle de flux : on agit, puis on republie l'état qui en découle."""
        presence = presences.get(sid)
        if presence is None:
            return _refus("hors_room", "aucune room pour ce client")
        code, joueur = presence
        try:
            room = demande(code, joueur, *arguments)
        except ErreurRoom as err:
            return _refus(err.motif, str(err))
        await (diffusion or diffuser_manche)(room)
        return {"ok": True}

    @sio.on("terminer_partie")
    async def terminer_partie(sid) -> dict:
        return await _flux(sid, rooms.terminer_partie, diffusion=annoncer_fin)

    async def annoncer_fin(room: Room) -> None:
        await sio.emit("partie_terminee", {"code": room.code}, room=room.code)

    @sio.on("quitter_room")
    async def quitter_room(sid) -> dict:
        await sortir(sid)
        return {"ok": True}

    @sio.event
    async def disconnect(sid, raison=None) -> None:
        await sortir(sid)


def _refus(motif: str, message: str) -> dict:
    return {"ok": False, "motif": motif, "message": message}
