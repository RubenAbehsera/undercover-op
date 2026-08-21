import json

import pytest

from jeu.contrat import ErreurContrat, charger_contrat


def test_charge_le_contrat_reel_des_38_paires(chemin_contrat):
    contrat = charger_contrat(chemin_contrat)

    assert len(contrat.arcs) == 33
    assert len(contrat.personnages) == 89
    assert len(contrat.paires) == 38
    assert contrat.paires[0].id == "kid-killer"  # tête du classement (sprint 3.2)


def test_fichier_absent_erreur_nette(tmp_path):
    absent = tmp_path / "nulle_part.json"

    with pytest.raises(ErreurContrat) as excinfo:
        charger_contrat(absent)

    assert "introuvable" in str(excinfo.value)
    assert str(absent) in str(excinfo.value)


def _ecrire_variante(tmp_path, chemin_contrat, muter):
    """Copie le contrat réel, y applique une mutation, l'écrit ailleurs."""
    brut = json.loads(chemin_contrat.read_text(encoding="utf-8"))
    muter(brut)
    chemin = tmp_path / "variante.json"
    chemin.write_text(json.dumps(brut, ensure_ascii=False), encoding="utf-8")
    return chemin


def test_champ_manquant_nomme_precisement(tmp_path, chemin_contrat):
    chemin = _ecrire_variante(
        tmp_path, chemin_contrat, lambda c: c["paires"][3].pop("difficulte")
    )

    with pytest.raises(ErreurContrat) as excinfo:
        charger_contrat(chemin)

    assert "paires[3].difficulte" in str(excinfo.value)


def test_reference_personnage_cassee_nommee(tmp_path, chemin_contrat):
    chemin = _ecrire_variante(
        tmp_path,
        chemin_contrat,
        lambda c: c["paires"][5].update(majorite="inconnu_du_graphe"),
    )

    with pytest.raises(ErreurContrat) as excinfo:
        charger_contrat(chemin)

    assert "paires[5].majorite" in str(excinfo.value)
    assert "inconnu_du_graphe" in str(excinfo.value)


def test_arc_inconnu_nomme(tmp_path, chemin_contrat):
    chemin = _ecrire_variante(
        tmp_path,
        chemin_contrat,
        lambda c: c["paires"][2].update(arc_etablissement="rage_des_amis"),
    )

    with pytest.raises(ErreurContrat) as excinfo:
        charger_contrat(chemin)

    assert "paires[2].arc_etablissement" in str(excinfo.value)
    assert "rage_des_amis" in str(excinfo.value)


def test_arc_de_premiere_apparition_inconnu_nomme(tmp_path, chemin_contrat):
    chemin = _ecrire_variante(
        tmp_path,
        chemin_contrat,
        lambda c: c["personnages"][4].update(arc_premiere_apparition="la_lune"),
    )

    with pytest.raises(ErreurContrat) as excinfo:
        charger_contrat(chemin)

    assert "personnages[4].arc_premiere_apparition" in str(excinfo.value)
    assert "la_lune" in str(excinfo.value)


def test_difficulte_hors_enum_nomme(tmp_path, chemin_contrat):
    chemin = _ecrire_variante(
        tmp_path, chemin_contrat, lambda c: c["paires"][7].update(difficulte="impossible")
    )

    with pytest.raises(ErreurContrat) as excinfo:
        charger_contrat(chemin)

    assert "paires[7].difficulte" in str(excinfo.value)
    assert "facile" in str(excinfo.value)  # l'erreur cite les valeurs admises
