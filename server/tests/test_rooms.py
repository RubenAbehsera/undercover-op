"""Les rooms : salle d'attente, arrivées et départs — sans socket."""

import pytest

from jeu.contrat import charger_contrat
from jeu.rooms import PLAFOND, ErreurRoom, Rooms


@pytest.fixture
def rooms(chemin_contrat) -> Rooms:
    return Rooms(charger_contrat(chemin_contrat))


def _premier_calibrage(rooms: Rooms) -> str:
    return rooms.arcs_proposes[-1]


def test_creer_une_room_enregistre_hote_pseudo_et_calibrage(rooms):
    calibrage = _premier_calibrage(rooms)

    room = rooms.creer(joueur="j-hote", pseudo="Nami", calibrage=calibrage)

    assert room.code
    assert room.hote == "j-hote"
    assert room.calibrage == calibrage
    assert room.salle_attente()["joueurs"] == ["Nami"]
    assert room.salle_attente()["hote"] == "Nami"
    assert room.salle_attente()["calibrage"] == calibrage


def test_le_code_est_lisible_et_unique(rooms):
    calibrage = _premier_calibrage(rooms)

    codes = {rooms.creer(f"j{i}", f"Joueur {i}", calibrage).code for i in range(30)}

    assert len(codes) == 30
    for code in codes:
        assert len(code) == 4
        assert code.isupper() or code.isdigit()
        assert not set(code) & set("O0I1")  # rien d'ambigu à dicter à voix haute


def test_un_code_deja_pris_est_retire(rooms, chemin_contrat):
    codes = iter(["AAAA", "AAAA", "BBBB"])
    rooms = Rooms(charger_contrat(chemin_contrat), generer_code=lambda: next(codes))
    calibrage = _premier_calibrage(rooms)

    premiere = rooms.creer("j-1", "Nami", calibrage)
    seconde = rooms.creer("j-2", "Zoro", calibrage)

    assert (premiere.code, seconde.code) == ("AAAA", "BBBB")


def test_le_depart_de_l_hote_laisse_la_salle_sans_hote(rooms):
    """Comportement actuel — le transfert d'hôte relève du ticket 05."""
    room = rooms.creer("j-hote", "Nami", _premier_calibrage(rooms))
    rooms.rejoindre(room.code, "j-2", "Zoro")

    rooms.quitter(room.code, "j-hote")

    assert room.salle_attente() == {
        "code": room.code,
        "calibrage": room.calibrage,
        "hote": None,
        "joueurs": ["Zoro"],
    }


def test_les_arcs_proposes_sont_ceux_du_contrat(rooms, chemin_contrat):
    from jeu.calibrage import arcs_proposes

    assert rooms.arcs_proposes == arcs_proposes(charger_contrat(chemin_contrat))


def test_calibrage_hors_liste_refuse(rooms):
    with pytest.raises(ErreurRoom) as excinfo:
        rooms.creer("j-hote", "Nami", "la_lune")

    assert excinfo.value.motif == "calibrage_inconnu"


def test_rejoindre_par_code_synchronise_la_salle_attente(rooms):
    room = rooms.creer("j-hote", "Nami", _premier_calibrage(rooms))

    rooms.rejoindre(room.code, joueur="j-2", pseudo="Zoro")
    rooms.rejoindre(room.code, joueur="j-3", pseudo="Usopp")

    assert room.salle_attente()["joueurs"] == ["Nami", "Zoro", "Usopp"]
    assert room.salle_attente()["hote"] == "Nami"


def test_code_inconnu_refuse(rooms):
    with pytest.raises(ErreurRoom) as excinfo:
        rooms.rejoindre("ZZZZ", "j-2", "Zoro")

    assert excinfo.value.motif == "code_inconnu"


def test_pseudo_deja_pris_refuse_meme_en_changeant_la_casse(rooms):
    room = rooms.creer("j-hote", "Nami", _premier_calibrage(rooms))

    with pytest.raises(ErreurRoom) as excinfo:
        rooms.rejoindre(room.code, "j-2", "nami")

    assert excinfo.value.motif == "pseudo_pris"
    assert room.salle_attente()["joueurs"] == ["Nami"]


@pytest.mark.parametrize("pseudo", ["", "   ", "N", "  N  "])
def test_pseudo_trop_court_refuse(rooms, pseudo):
    with pytest.raises(ErreurRoom) as excinfo:
        rooms.creer("j-hote", pseudo, _premier_calibrage(rooms))

    assert excinfo.value.motif == "pseudo_invalide"
    assert "2" in str(excinfo.value)


def test_deux_caracteres_suffisent(rooms):
    room = rooms.creer("j-hote", "Nu", _premier_calibrage(rooms))

    assert room.salle_attente()["joueurs"] == ["Nu"]


def test_un_pseudo_refuse_ne_laisse_pas_de_room_orpheline(chemin_contrat):
    rooms = Rooms(charger_contrat(chemin_contrat), generer_code=lambda: "AAAA")

    with pytest.raises(ErreurRoom):
        rooms.creer("j-hote", "", _premier_calibrage(rooms))

    with pytest.raises(ErreurRoom) as excinfo:
        rooms.room("AAAA")
    assert excinfo.value.motif == "code_inconnu"


def test_le_pseudo_est_deponctue_des_espaces(rooms):
    room = rooms.creer("j-hote", "  Nami  ", _premier_calibrage(rooms))

    assert room.salle_attente()["joueurs"] == ["Nami"]


def test_plafond_de_douze_joueurs(rooms):
    room = rooms.creer("j-hote", "Joueur 0", _premier_calibrage(rooms))
    for i in range(1, PLAFOND):
        rooms.rejoindre(room.code, f"j-{i}", f"Joueur {i}")

    with pytest.raises(ErreurRoom) as excinfo:
        rooms.rejoindre(room.code, "j-treize", "Joueur 13")

    assert excinfo.value.motif == "room_pleine"
    assert len(room.salle_attente()["joueurs"]) == PLAFOND


def test_rejoindre_deux_fois_ne_duplique_pas_le_joueur(rooms):
    room = rooms.creer("j-hote", "Nami", _premier_calibrage(rooms))

    rooms.rejoindre(room.code, "j-2", "Zoro")
    rooms.rejoindre(room.code, "j-2", "Zoro")

    assert room.salle_attente()["joueurs"] == ["Nami", "Zoro"]


def test_un_depart_se_voit_dans_la_salle_attente(rooms):
    room = rooms.creer("j-hote", "Nami", _premier_calibrage(rooms))
    rooms.rejoindre(room.code, "j-2", "Zoro")

    rooms.quitter(room.code, "j-2")

    assert room.salle_attente()["joueurs"] == ["Nami"]


def test_le_pseudo_libere_est_reutilisable(rooms):
    room = rooms.creer("j-hote", "Nami", _premier_calibrage(rooms))
    rooms.rejoindre(room.code, "j-2", "Zoro")
    rooms.quitter(room.code, "j-2")

    rooms.rejoindre(room.code, "j-3", "Zoro")

    assert room.salle_attente()["joueurs"] == ["Nami", "Zoro"]


def test_la_room_videe_disparait(rooms):
    room = rooms.creer("j-hote", "Nami", _premier_calibrage(rooms))

    assert rooms.quitter(room.code, "j-hote") is None

    with pytest.raises(ErreurRoom):
        rooms.rejoindre(room.code, "j-2", "Zoro")


def test_quitter_une_room_inconnue_ne_casse_rien(rooms):
    assert rooms.quitter("ZZZZ", "j-2") is None


def test_la_salle_attente_ne_publie_aucun_id_de_joueur(rooms):
    room = rooms.creer("j-hote", "Nami", _premier_calibrage(rooms))
    rooms.rejoindre(room.code, "j-secret", "Zoro")

    assert "j-secret" not in repr(room.salle_attente())
    assert "j-hote" not in repr(room.salle_attente())
