import asyncio

import httpx
import pytest

from jeu.__main__ import main
from jeu.app import creer_app
from jeu.contrat import ErreurContrat


def test_le_serveur_demarre_avec_le_contrat(chemin_contrat):
    app = creer_app(chemin_contrat, ":memory:")

    reponse = asyncio.run(_appeler(app, "/sante"))

    assert reponse.status_code == 200
    assert reponse.json() == {"etat": "ok"}


def test_le_serveur_refuse_de_demarrer_sans_contrat(tmp_path):
    with pytest.raises(ErreurContrat, match="introuvable"):
        creer_app(tmp_path / "rien.json")


def test_le_process_plante_proprement_sans_contrat(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("CONTRAT_PAIRES", str(tmp_path / "rien.json"))

    with pytest.raises(SystemExit) as excinfo:
        main()

    assert excinfo.value.code == 1
    assert "introuvable" in capsys.readouterr().err


def test_le_serveur_ouvre_le_fichier_de_signaux(chemin_contrat, tmp_path):
    fichier = tmp_path / "signaux.db"

    creer_app(chemin_contrat, fichier)

    assert fichier.exists()


def test_le_fichier_de_signaux_suit_la_variable_d_environnement(
    chemin_contrat, tmp_path, monkeypatch
):
    fichier = tmp_path / "ailleurs.db"
    monkeypatch.setenv("SIGNAUX_SQLITE", str(fichier))

    creer_app(chemin_contrat)

    assert fichier.exists()


def test_le_serveur_sert_le_bundle_du_front(chemin_contrat, tmp_path, monkeypatch):
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text("<html>le jeu</html>", encoding="utf-8")
    monkeypatch.setenv("FRONT_DIST", str(dist))

    app = creer_app(chemin_contrat, ":memory:")

    assert asyncio.run(_appeler(app, "/")).text == "<html>le jeu</html>"
    assert asyncio.run(_appeler(app, "/sante")).json() == {"etat": "ok"}


def test_le_bundle_ne_marche_pas_sur_le_chemin_socket_io(
    chemin_contrat, tmp_path, monkeypatch
):
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text("<html>le jeu</html>", encoding="utf-8")
    monkeypatch.setenv("FRONT_DIST", str(dist))

    app = creer_app(chemin_contrat, ":memory:")

    poignee = asyncio.run(_appeler(app, "/socket.io/?EIO=4&transport=polling"))

    assert poignee.status_code == 200
    assert "sid" in poignee.text


def test_le_serveur_demarre_sans_bundle(chemin_contrat, tmp_path, monkeypatch):
    monkeypatch.setenv("FRONT_DIST", str(tmp_path / "jamais_construit"))

    app = creer_app(chemin_contrat, ":memory:")

    assert asyncio.run(_appeler(app, "/sante")).status_code == 200


async def _appeler(app, chemin: str) -> httpx.Response:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.get(chemin)
