"""L'app ASGI du service de jeu : FastAPI pour le HTTP, socket.io pour le temps réel."""

import os
from pathlib import Path

import socketio
from fastapi import FastAPI

from jeu.contrat import Contrat, charger_contrat


def creer_app(chemin_contrat: Path | None = None):
    """Fabrique l'app complète ; charge et valide le contrat au démarrage.

    Sans contrat valide, refuse de naître — jamais de serveur lancé sur un
    contrat bancal.
    """
    contrat = charger_contrat(chemin_contrat or _chemin_par_defaut())

    api = FastAPI(title="Undercover OP")
    api.state.contrat = contrat

    @api.get("/sante")
    def sante() -> dict:
        return {"etat": "ok"}

    sio = socketio.AsyncServer(async_mode="asgi")
    return socketio.ASGIApp(sio, other_asgi_app=api)


def _chemin_par_defaut() -> Path:
    variable = os.environ.get("CONTRAT_PAIRES")
    if variable:
        return Path(variable)
    return Path(__file__).resolve().parents[2] / "fabrication" / "paires.json"
