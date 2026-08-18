"""Les rooms : salle d'attente, arrivées et départs — sans socket."""

import pytest

from jeu.contrat import charger_contrat
from jeu.erreurs import ErreurRoom
from jeu.rooms import INACTIVITE, PLAFOND, Rooms


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


def test_le_depart_de_l_hote_transmet_au_plus_ancien(rooms):
    room = rooms.creer("j-hote", "Nami", _premier_calibrage(rooms))
    rooms.rejoindre(room.code, "j-2", "Zoro")
    rooms.rejoindre(room.code, "j-3", "Usopp")

    rooms.quitter(room.code, "j-hote")

    assert room.salle_attente() == {
        "code": room.code,
        "calibrage": room.calibrage,
        "hote": "Zoro",
        "joueurs": ["Zoro", "Usopp"],
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


def test_l_hote_lance_une_manche(rooms):
    room = rooms.creer("j-hote", "Nami", _premier_calibrage(rooms))
    rooms.rejoindre(room.code, "j-2", "Zoro")
    rooms.rejoindre(room.code, "j-3", "Usopp")

    manche = rooms.lancer_manche(room.code, "j-hote")

    assert room.manche is manche
    assert manche.joueurs == ["j-hote", "j-2", "j-3"]
    assert manche.imposteur in manche.joueurs


def test_seul_l_hote_lance_une_manche(rooms):
    room = rooms.creer("j-hote", "Nami", _premier_calibrage(rooms))
    rooms.rejoindre(room.code, "j-2", "Zoro")
    rooms.rejoindre(room.code, "j-3", "Usopp")

    with pytest.raises(ErreurRoom) as excinfo:
        rooms.lancer_manche(room.code, "j-2")

    assert excinfo.value.motif == "pas_hote"
    assert room.manche is None


def test_une_manche_demande_au_moins_trois_joueurs(rooms):
    room = rooms.creer("j-hote", "Nami", _premier_calibrage(rooms))
    rooms.rejoindre(room.code, "j-2", "Zoro")

    with pytest.raises(ErreurRoom) as excinfo:
        rooms.lancer_manche(room.code, "j-hote")

    assert excinfo.value.motif == "joueurs_insuffisants"
    assert room.manche is None


def test_chaque_manche_tire_une_paire_neuve(rooms):
    room = rooms.creer("j-hote", "Nami", _premier_calibrage(rooms))
    rooms.rejoindre(room.code, "j-2", "Zoro")
    rooms.rejoindre(room.code, "j-3", "Usopp")

    premiere = rooms.lancer_manche(room.code, "j-hote").paire.id
    rooms.ouvrir_vote(room.code, "j-hote")
    rooms.forcer_vote(room.code, "j-hote")
    seconde = rooms.lancer_manche(room.code, "j-hote").paire.id

    assert premiere != seconde


def test_lancer_dans_une_room_inconnue_refuse(rooms):
    with pytest.raises(ErreurRoom) as excinfo:
        rooms.lancer_manche("ZZZZ", "j-hote")

    assert excinfo.value.motif == "code_inconnu"


def _salle_de_trois(rooms) -> "Room":
    room = rooms.creer("j-hote", "Nami", _premier_calibrage(rooms))
    rooms.rejoindre(room.code, "j-2", "Zoro")
    rooms.rejoindre(room.code, "j-3", "Usopp")
    return room


def _pseudos(rooms) -> dict:
    return {"j-hote": "Nami", "j-2": "Zoro", "j-3": "Usopp"}


def test_le_tour_publie_l_ordre_en_pseudos(rooms):
    room = _salle_de_trois(rooms)
    rooms.lancer_manche(room.code, "j-hote")

    tour = room.tour()

    assert sorted(tour["ordre"]) == ["Nami", "Usopp", "Zoro"]
    assert tour["orateur"] == tour["ordre"][0]
    assert tour["tour"] == 1


def test_la_parole_rendue_avance_l_ordre(rooms):
    room = _salle_de_trois(rooms)
    manche = rooms.lancer_manche(room.code, "j-hote")
    premier = manche.orateur()

    rooms.passer_parole(room.code, premier)

    assert room.tour()["orateur"] == _pseudos(rooms)[manche.ordre[1]]


def test_un_autre_joueur_ne_rend_pas_la_parole(rooms):
    room = _salle_de_trois(rooms)
    manche = rooms.lancer_manche(room.code, "j-hote")
    autre = next(j for j in manche.ordre if j != manche.orateur())

    with pytest.raises(ErreurRoom) as excinfo:
        rooms.passer_parole(room.code, autre)

    assert excinfo.value.motif == "pas_ton_tour"


def test_seul_l_hote_ouvre_le_vote(rooms):
    room = _salle_de_trois(rooms)
    rooms.lancer_manche(room.code, "j-hote")

    with pytest.raises(ErreurRoom) as excinfo:
        rooms.ouvrir_vote(room.code, "j-2")

    assert excinfo.value.motif == "pas_hote"
    assert room.manche.etat == "paroles"


def test_on_vote_par_pseudo(rooms):
    room = _salle_de_trois(rooms)
    rooms.lancer_manche(room.code, "j-hote")
    rooms.ouvrir_vote(room.code, "j-hote")

    rooms.voter(room.code, "j-hote", "Zoro")

    assert room.manche.votes == {"j-hote": "j-2"}


def test_un_pseudo_inconnu_n_est_pas_une_cible(rooms):
    room = _salle_de_trois(rooms)
    rooms.lancer_manche(room.code, "j-hote")
    rooms.ouvrir_vote(room.code, "j-hote")

    with pytest.raises(ErreurRoom) as excinfo:
        rooms.voter(room.code, "j-hote", "Sanji")

    assert excinfo.value.motif == "cible_inconnue"


def test_le_dernier_vote_ferme_la_consultation(rooms):
    room = _salle_de_trois(rooms)
    rooms.lancer_manche(room.code, "j-hote")
    rooms.ouvrir_vote(room.code, "j-hote")

    rooms.voter(room.code, "j-hote", "Zoro")
    rooms.voter(room.code, "j-2", "Nami")
    assert room.manche.etat == "vote"

    rooms.voter(room.code, "j-3", "Zoro")
    assert room.manche.etat == "revelation"


def test_l_hote_force_la_fermeture_du_vote(rooms):
    room = _salle_de_trois(rooms)
    rooms.lancer_manche(room.code, "j-hote")
    rooms.ouvrir_vote(room.code, "j-hote")
    rooms.voter(room.code, "j-hote", "Zoro")

    rooms.forcer_vote(room.code, "j-hote")

    assert room.manche.etat == "revelation"
    assert room.revelation()["designe"] == "Zoro"


def test_seul_l_hote_force_le_vote(rooms):
    room = _salle_de_trois(rooms)
    rooms.lancer_manche(room.code, "j-hote")
    rooms.ouvrir_vote(room.code, "j-hote")

    with pytest.raises(ErreurRoom) as excinfo:
        rooms.forcer_vote(room.code, "j-2")

    assert excinfo.value.motif == "pas_hote"


def test_la_revelation_dit_le_duo_le_lien_et_le_verdict(rooms):
    room = _salle_de_trois(rooms)
    manche = rooms.lancer_manche(room.code, "j-hote")
    rooms.ouvrir_vote(room.code, "j-hote")
    rooms.forcer_vote(room.code, "j-hote")

    revelation = room.revelation()

    assert revelation["majorite"] == {
        "id": manche.personnage_majorite.id,
        "nom": manche.personnage_majorite.nom,
    }
    assert revelation["imposteur"] == {
        "id": manche.personnage_imposteur.id,
        "nom": manche.personnage_imposteur.nom,
    }
    assert revelation["joueur_imposteur"] == _pseudos(rooms)[manche.imposteur]
    assert revelation["lien"] == manche.paire.lien.libelle
    assert revelation["tours"] == 0, "le vote a coupé avant le premier tour"
    assert manche.paire.difficulte not in repr(revelation)


def test_la_revelation_depouille_nominativement(rooms):
    room = _salle_de_trois(rooms)
    rooms.lancer_manche(room.code, "j-hote")
    rooms.ouvrir_vote(room.code, "j-hote")
    rooms.voter(room.code, "j-hote", "Zoro")
    rooms.voter(room.code, "j-2", "Usopp")
    rooms.voter(room.code, "j-3", "Zoro")

    revelation = room.revelation()

    assert revelation["votes"] == [
        {"votant": "Nami", "cible": "Zoro"},
        {"votant": "Zoro", "cible": "Usopp"},
        {"votant": "Usopp", "cible": "Zoro"},
    ]
    assert revelation["designe"] == "Zoro"


def test_rejoindre_est_refuse_pendant_une_manche(rooms):
    room = _salle_de_trois(rooms)
    rooms.lancer_manche(room.code, "j-hote")

    with pytest.raises(ErreurRoom) as excinfo:
        rooms.rejoindre(room.code, "j-4", "Sanji")

    assert excinfo.value.motif == "manche_en_cours"
    assert room.salle_attente()["joueurs"] == ["Nami", "Zoro", "Usopp"]


def test_on_rejoint_de_nouveau_apres_la_revelation(rooms):
    room = _salle_de_trois(rooms)
    rooms.lancer_manche(room.code, "j-hote")
    rooms.ouvrir_vote(room.code, "j-hote")
    rooms.forcer_vote(room.code, "j-hote")

    rooms.rejoindre(room.code, "j-4", "Sanji")

    assert room.salle_attente()["joueurs"] == ["Nami", "Zoro", "Usopp", "Sanji"]


def test_les_controles_de_flux_exigent_une_manche(rooms):
    room = _salle_de_trois(rooms)

    for appel in (rooms.passer_parole, rooms.ouvrir_vote, rooms.forcer_vote):
        with pytest.raises(ErreurRoom) as excinfo:
            appel(room.code, "j-hote")
        assert excinfo.value.motif == "pas_de_manche"


def test_on_ne_relance_pas_une_manche_en_cours(rooms):
    room = _salle_de_trois(rooms)
    premiere = rooms.lancer_manche(room.code, "j-hote")

    with pytest.raises(ErreurRoom) as excinfo:
        rooms.lancer_manche(room.code, "j-hote")

    assert excinfo.value.motif == "manche_en_cours"
    assert room.manche is premiere


def test_la_manche_suivante_se_lance_apres_la_revelation(rooms):
    room = _salle_de_trois(rooms)
    premiere = rooms.lancer_manche(room.code, "j-hote")
    rooms.ouvrir_vote(room.code, "j-hote")
    rooms.forcer_vote(room.code, "j-hote")

    seconde = rooms.lancer_manche(room.code, "j-hote")

    assert seconde is not premiere
    assert seconde.etat == "paroles"


def test_le_vote_ne_s_ouvre_qu_une_fois(rooms):
    room = _salle_de_trois(rooms)
    rooms.lancer_manche(room.code, "j-hote")
    rooms.ouvrir_vote(room.code, "j-hote")

    with pytest.raises(ErreurRoom) as excinfo:
        rooms.ouvrir_vote(room.code, "j-hote")

    assert excinfo.value.motif == "vote_impossible"


def test_le_nouvel_hote_detient_les_controles(rooms):
    room = _salle_de_trois(rooms)
    rooms.quitter(room.code, "j-hote")

    with pytest.raises(ErreurRoom):
        rooms.lancer_manche(room.code, "j-3")
    rooms.rejoindre(room.code, "j-4", "Sanji")
    manche = rooms.lancer_manche(room.code, "j-2")

    assert room.hote == "j-2"
    assert sorted(manche.joueurs) == ["j-2", "j-3", "j-4"]


def test_un_depart_en_cours_de_manche_conserve_le_joueur(rooms):
    room = _salle_de_trois(rooms)
    manche = rooms.lancer_manche(room.code, "j-hote")

    rooms.quitter(room.code, "j-2")

    assert room.salle_attente()["joueurs"] == ["Nami", "Usopp"]
    assert manche.presents() == ["j-hote", "j-3"]
    assert "j-2" in manche.joueurs, "le parti reste connu de la manche"


def test_le_pseudo_d_un_parti_survit_a_la_revelation(rooms):
    room = _salle_de_trois(rooms)
    rooms.lancer_manche(room.code, "j-hote")
    rooms.ouvrir_vote(room.code, "j-hote")
    rooms.voter(room.code, "j-2", "Nami")
    rooms.voter(room.code, "j-hote", "Zoro")

    rooms.quitter(room.code, "j-2")
    assert room.manche.etat == "vote", "Usopp n'a pas encore voté"
    rooms.voter(room.code, "j-3", "Nami")

    assert room.manche.etat == "revelation"
    assert room.revelation()["votes"] == [
        {"votant": "Zoro", "cible": "Nami"},
        {"votant": "Nami", "cible": "Zoro"},
        {"votant": "Usopp", "cible": "Nami"},
    ]


def test_le_depart_de_l_hote_en_cours_de_manche_transmet_aussi(rooms):
    room = _salle_de_trois(rooms)
    rooms.lancer_manche(room.code, "j-hote")

    rooms.quitter(room.code, "j-hote")

    assert room.hote == "j-2"
    assert room.manche.presents() == ["j-2", "j-3"]


def test_l_imposteur_parti_garde_son_pseudo_a_la_revelation(rooms):
    room = _salle_de_trois(rooms)
    manche = rooms.lancer_manche(room.code, "j-hote")
    pseudos = _pseudos(rooms)

    rooms.quitter(room.code, manche.imposteur)
    if room.manche is not None:
        rooms.ouvrir_vote(room.code, room.hote)
        rooms.forcer_vote(room.code, room.hote)
        assert room.revelation()["joueur_imposteur"] == pseudos[manche.imposteur]


def test_la_manche_suivante_oublie_les_partis(rooms):
    room = _salle_de_trois(rooms)
    rooms.lancer_manche(room.code, "j-hote")
    rooms.quitter(room.code, "j-2")
    rooms.ouvrir_vote(room.code, "j-hote")
    rooms.forcer_vote(room.code, "j-hote")
    rooms.rejoindre(room.code, "j-4", "Sanji")

    seconde = rooms.lancer_manche(room.code, "j-hote")

    assert sorted(seconde.joueurs) == ["j-3", "j-4", "j-hote"]
    assert [joueur.pseudo for joueur in room.joueurs] == ["Nami", "Usopp", "Sanji"]


def test_entre_manches_un_depart_retire_vraiment_le_joueur(rooms):
    room = _salle_de_trois(rooms)

    rooms.quitter(room.code, "j-2")

    assert [joueur.id for joueur in room.joueurs] == ["j-hote", "j-3"]


def test_le_depart_du_dernier_attendu_ferme_le_vote(rooms):
    room = _salle_de_trois(rooms)
    rooms.lancer_manche(room.code, "j-hote")
    rooms.ouvrir_vote(room.code, "j-hote")
    rooms.voter(room.code, "j-hote", "Usopp")
    rooms.voter(room.code, "j-3", "Nami")

    rooms.quitter(room.code, "j-2")

    assert room.manche.etat == "revelation", "plus personne n'est attendu"
    assert room.revelation()["designe"] is None


def test_l_hote_termine_la_partie(rooms):
    room = _salle_de_trois(rooms)

    rooms.terminer_partie(room.code, "j-hote")

    assert room.terminee is True


def test_seul_l_hote_termine_la_partie(rooms):
    room = _salle_de_trois(rooms)

    with pytest.raises(ErreurRoom) as excinfo:
        rooms.terminer_partie(room.code, "j-2")

    assert excinfo.value.motif == "pas_hote"
    assert room.terminee is False


def test_une_partie_terminee_ne_relance_pas_de_manche(rooms):
    room = _salle_de_trois(rooms)
    rooms.terminer_partie(room.code, "j-hote")

    with pytest.raises(ErreurRoom) as excinfo:
        rooms.lancer_manche(room.code, "j-hote")

    assert excinfo.value.motif == "partie_terminee"


def test_on_ne_rejoint_pas_une_partie_terminee(rooms):
    room = _salle_de_trois(rooms)
    rooms.terminer_partie(room.code, "j-hote")

    with pytest.raises(ErreurRoom) as excinfo:
        rooms.rejoindre(room.code, "j-4", "Sanji")

    assert excinfo.value.motif == "partie_terminee"


class Horloge:
    """Une horloge de test — le temps n'avance que si on le pousse."""

    def __init__(self):
        self.instant = 1000.0

    def __call__(self) -> float:
        return self.instant

    def avancer(self, secondes: float) -> None:
        self.instant += secondes


@pytest.fixture
def horloge() -> Horloge:
    return Horloge()


@pytest.fixture
def rooms_horlogees(chemin_contrat, horloge) -> Rooms:
    return Rooms(charger_contrat(chemin_contrat), horloge=horloge)


def test_une_room_inactive_deux_heures_disparait(rooms_horlogees, horloge):
    room = rooms_horlogees.creer("j-hote", "Nami", _premier_calibrage(rooms_horlogees))

    horloge.avancer(INACTIVITE + 1)

    with pytest.raises(ErreurRoom) as excinfo:
        rooms_horlogees.room(room.code)
    assert excinfo.value.motif == "code_inconnu"


def test_l_activite_repousse_la_suppression(rooms_horlogees, horloge):
    room = rooms_horlogees.creer("j-hote", "Nami", _premier_calibrage(rooms_horlogees))

    for _ in range(3):
        horloge.avancer(INACTIVITE - 60)
        assert rooms_horlogees.room(room.code) is room


def test_la_purge_n_emporte_que_les_rooms_endormies(rooms_horlogees, horloge):
    calibrage = _premier_calibrage(rooms_horlogees)
    endormie = rooms_horlogees.creer("j-1", "Nami", calibrage)
    horloge.avancer(INACTIVITE - 60)
    vivante = rooms_horlogees.creer("j-2", "Zoro", calibrage)

    horloge.avancer(120)

    assert rooms_horlogees.room(vivante.code) is vivante
    with pytest.raises(ErreurRoom):
        rooms_horlogees.room(endormie.code)


def test_le_bulletin_de_vote_ignore_les_partis(rooms):
    room = _salle_de_trois(rooms)
    rooms.lancer_manche(room.code, "j-hote")
    rooms.quitter(room.code, "j-2")

    rooms.ouvrir_vote(room.code, "j-hote")

    assert room.vote_ouvert() == {"joueurs": ["Nami", "Usopp"]}


def test_une_room_videe_en_cours_de_manche_disparait(rooms):
    room = _salle_de_trois(rooms)
    rooms.lancer_manche(room.code, "j-hote")

    for joueur in ("j-hote", "j-2", "j-3"):
        dernier = rooms.quitter(room.code, joueur)

    assert dernier is None
    with pytest.raises(ErreurRoom):
        rooms.room(room.code)
