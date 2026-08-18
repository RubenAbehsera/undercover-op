"""Les signaux : ce que la mesure retient d'une manche, et d'une partie.

Le magasin est testé sans room ni socket — une base en mémoire suffit, sauf
là où c'est justement la persistance sur disque qui est en cause.
"""

import pytest

from jeu.erreurs import ErreurRoom
from jeu.signaux import SignalManche, Signaux


@pytest.fixture
def signaux() -> Signaux:
    return Signaux(":memory:")


def _signal(**remplacements) -> SignalManche:
    champs = {
        "partie": "p-1",
        "calibrage": "marineford",
        "paire": "luffy-ace",
        "joueurs": 4,
        "tours": 2,
        "demasque": True,
        "suffrages": 4,
        "voix_imposteur": 3,
        "repartition": [3, 1],
        "drapeaux": 0,
    }
    return SignalManche(**{**champs, **remplacements})


def test_une_manche_terminee_laisse_sa_ligne(signaux):
    signaux.enregistrer_manche(_signal())

    (ligne,) = signaux.manches()
    assert ligne["partie"] == "p-1"
    assert ligne["calibrage"] == "marineford"
    assert ligne["paire"] == "luffy-ace"
    assert ligne["joueurs"] == 4
    assert ligne["tours"] == 2
    assert ligne["demasque"] is True
    assert ligne["suffrages"] == 4
    assert ligne["voix_imposteur"] == 3
    assert ligne["repartition"] == [3, 1]
    assert ligne["drapeaux"] == 0
    assert ligne["horodatage"]


def test_les_manches_s_accumulent(signaux):
    signaux.enregistrer_manche(_signal(paire="luffy-ace"))
    signaux.enregistrer_manche(_signal(paire="zoro-mihawk", demasque=False))

    assert [ligne["paire"] for ligne in signaux.manches()] == [
        "luffy-ace",
        "zoro-mihawk",
    ]


def test_la_qualite_des_tirages_agrege_par_paire(signaux):
    signaux.enregistrer_manche(_signal(paire="luffy-ace", demasque=True, tours=2))
    signaux.enregistrer_manche(_signal(paire="luffy-ace", demasque=False, tours=4))

    assert signaux.qualite_tirages() == [
        {"paire": "luffy-ace", "manches": 2, "demasquees": 1, "tours_moyens": 3.0}
    ]


def test_une_manche_drapeautee_est_exclue_de_la_qualite_des_tirages(signaux):
    signaux.enregistrer_manche(_signal(paire="luffy-ace", demasque=True, tours=2))
    signaux.enregistrer_manche(
        _signal(paire="luffy-ace", demasque=False, tours=8, drapeaux=1)
    )

    assert signaux.qualite_tirages() == [
        {"paire": "luffy-ace", "manches": 1, "demasquees": 1, "tours_moyens": 2.0}
    ]


def test_une_paire_entierement_drapeautee_sort_du_calcul(signaux):
    signaux.enregistrer_manche(_signal(paire="luffy-ace", drapeaux=2))

    assert signaux.qualite_tirages() == []


def test_le_retour_de_fin_de_partie_est_enregistre(signaux):
    signaux.enregistrer_retour("p-1", "j-1", niveau=3, commentaire="excellent")

    assert signaux.retours() == [
        {
            "partie": "p-1",
            "joueur": "j-1",
            "niveau": 3,
            "commentaire": "excellent",
            "horodatage": signaux.retours()[0]["horodatage"],
        }
    ]


def test_le_commentaire_est_optionnel(signaux):
    signaux.enregistrer_retour("p-1", "j-1", niveau=2, commentaire=None)

    assert signaux.retours()[0]["commentaire"] is None


def test_un_joueur_ne_donne_qu_un_retour_par_partie(signaux):
    signaux.enregistrer_retour("p-1", "j-1", niveau=2, commentaire=None)

    with pytest.raises(ErreurRoom) as excinfo:
        signaux.enregistrer_retour("p-1", "j-1", niveau=3, commentaire="je me ravise")

    assert excinfo.value.motif == "deja_repondu"
    assert signaux.retours()[0]["niveau"] == 2


def test_chaque_joueur_a_son_retour(signaux):
    signaux.enregistrer_retour("p-1", "j-1", niveau=2, commentaire=None)
    signaux.enregistrer_retour("p-1", "j-2", niveau=3, commentaire=None)
    signaux.enregistrer_retour("p-2", "j-1", niveau=1, commentaire=None)

    assert len(signaux.retours()) == 3


@pytest.mark.parametrize("niveau", [0, 4, -1])
def test_un_niveau_hors_des_trois_est_refuse(signaux, niveau):
    with pytest.raises(ErreurRoom) as excinfo:
        signaux.enregistrer_retour("p-1", "j-1", niveau=niveau, commentaire=None)

    assert excinfo.value.motif == "niveau_invalide"
    assert signaux.retours() == []


def test_la_base_survit_a_une_reouverture(tmp_path):
    fichier = tmp_path / "signaux.db"
    premier = Signaux(fichier)
    premier.enregistrer_manche(_signal())
    premier.enregistrer_retour("p-1", "j-1", niveau=3, commentaire=None)
    premier.fermer()

    second = Signaux(fichier)

    assert len(second.manches()) == 1
    assert len(second.retours()) == 1
