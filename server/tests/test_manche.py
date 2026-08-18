"""La manche : le tirage anti-spoil et la distribution des rôles.

L'étalon du tirage est `paires_servables` (conftest), recalculé à la main
depuis `docs/decisions.md` — jamais la fonction que l'on teste.
"""

import pytest

from jeu.calibrage import arcs_proposes, pool
from jeu.contrat import charger_contrat
from jeu.erreurs import ErreurRoom
from jeu.manche import Manches

JOUEURS = ["j-1", "j-2", "j-3", "j-4"]


@pytest.fixture
def contrat(chemin_contrat):
    return charger_contrat(chemin_contrat)


def test_aucun_tirage_ne_depasse_le_calibrage(contrat, paires_servables):
    for arc in arcs_proposes(contrat):
        manches = Manches(contrat, arc)
        servables = paires_servables(contrat, arc)

        for _ in range(2 * len(servables) + 1):
            paire = manches.lancer(JOUEURS).paire
            assert paire.id in servables, f"{paire.id} servie sous {arc}"


def test_aucune_repetition_avant_epuisement(contrat):
    calibrage = arcs_proposes(contrat)[-1]
    manches = Manches(contrat, calibrage)
    stock = len(pool(contrat, calibrage))

    tirees = [manches.lancer(JOUEURS).paire.id for _ in range(stock)]

    assert len(set(tirees)) == stock


def test_le_stock_epuise_se_reutilise(contrat):
    calibrage = arcs_proposes(contrat)[-1]
    manches = Manches(contrat, calibrage)
    stock = len(pool(contrat, calibrage))

    tirees = [manches.lancer(JOUEURS).paire.id for _ in range(2 * stock)]

    assert sorted(tirees) == sorted(2 * [paire.id for paire in pool(contrat, calibrage)])


def test_un_calibrage_etroit_tourne_sur_son_maigre_stock(contrat):
    calibrage = arcs_proposes(contrat)[0]
    manches = Manches(contrat, calibrage)
    servables = {paire.id for paire in pool(contrat, calibrage)}

    tirees = {manches.lancer(JOUEURS).paire.id for _ in range(20)}

    assert tirees == servables


def test_deux_parties_ne_tirent_pas_la_meme_suite(contrat):
    calibrage = arcs_proposes(contrat)[-1]

    suites = {
        tuple(Manches(contrat, calibrage).lancer(JOUEURS).paire.id for _ in range(5))
        for _ in range(20)
    }

    assert len(suites) > 1


@pytest.fixture
def manches(contrat):
    return Manches(contrat, arcs_proposes(contrat)[-1])


def test_un_seul_joueur_recoit_le_personnage_imposteur(manches):
    for _ in range(50):
        manche = manches.lancer(JOUEURS)

        vus = [manche.personnage(joueur)["id"] for joueur in JOUEURS]

        assert vus.count(manche.paire.imposteur) == 1
        assert vus.count(manche.paire.majorite) == len(JOUEURS) - 1


def test_le_personnage_porte_le_nom_du_contrat(contrat, manches):
    noms = {personnage.id: personnage.nom for personnage in contrat.personnages}

    manche = manches.lancer(JOUEURS)

    for joueur in JOUEURS:
        vu = manche.personnage(joueur)
        assert vu["nom"] == noms[vu["id"]]


def test_l_imposteur_n_est_pas_toujours_le_meme_joueur(manches):
    porteurs = {manches.lancer(JOUEURS).imposteur for _ in range(50)}

    assert porteurs == set(JOUEURS)


def test_le_payload_a_la_meme_forme_pour_tous(manches):
    manche = manches.lancer(JOUEURS)

    formes = {tuple(sorted(manche.personnage(joueur))) for joueur in JOUEURS}

    assert formes == {("id", "nom")}


def test_le_payload_ne_laisse_fuir_ni_le_lien_ni_la_difficulte_ni_le_role(manches):
    for _ in range(50):
        manche = manches.lancer(JOUEURS)

        for joueur in JOUEURS:
            texte = repr(manche.personnage(joueur))
            assert manche.paire.lien.libelle not in texte
            assert manche.paire.lien.type not in texte
            assert manche.paire.difficulte not in texte
            assert manche.paire.id not in texte
            assert manche.imposteur not in texte


def test_l_ordre_de_parole_contient_tous_les_joueurs(manches):
    manche = manches.lancer(JOUEURS)

    assert sorted(manche.ordre) == sorted(JOUEURS)


def test_l_ordre_de_parole_change_d_une_manche_a_l_autre(manches):
    ordres = {tuple(manches.lancer(JOUEURS).ordre) for _ in range(30)}

    assert len(ordres) > 1


def test_la_parole_tourne_en_cycle(manches):
    manche = manches.lancer(JOUEURS)

    orateurs = []
    for _ in range(2 * len(JOUEURS) + 1):
        orateurs.append(manche.orateur())
        manche.passer(manche.orateur())

    assert orateurs == manche.ordre * 2 + [manche.ordre[0]]
    assert manche.tour == 3


def test_seul_l_orateur_rend_la_parole(manches):
    manche = manches.lancer(JOUEURS)
    autre = next(j for j in manche.ordre if j != manche.orateur())

    with pytest.raises(ErreurRoom) as excinfo:
        manche.passer(autre)

    assert excinfo.value.motif == "pas_ton_tour"
    assert manche.orateur() == manche.ordre[0]


def _en_vote(manches):
    manche = manches.lancer(JOUEURS)
    manche.ouvrir_vote()
    return manche


def test_le_vote_s_ouvre_puis_la_revelation_ferme_la_manche(manches):
    manche = manches.lancer(JOUEURS)
    assert manche.etat == "paroles"

    manche.ouvrir_vote()
    assert manche.etat == "vote"

    manche.fermer_vote()
    assert manche.etat == "revelation"


def test_on_ne_vote_pas_avant_l_ouverture(manches):
    manche = manches.lancer(JOUEURS)

    with pytest.raises(ErreurRoom) as excinfo:
        manche.voter("j-1", "j-2")

    assert excinfo.value.motif == "pas_de_vote"


def test_on_ne_vote_pas_pour_soi(manches):
    manche = _en_vote(manches)

    with pytest.raises(ErreurRoom) as excinfo:
        manche.voter("j-1", "j-1")

    assert excinfo.value.motif == "vote_pour_soi"
    assert manche.votes == {}


def test_on_ne_vote_pas_pour_qui_n_est_pas_dans_la_manche(manches):
    manche = _en_vote(manches)

    with pytest.raises(ErreurRoom) as excinfo:
        manche.voter("j-1", "j-inconnu")

    assert excinfo.value.motif == "cible_inconnue"


def test_on_ne_vote_qu_une_fois(manches):
    manche = _en_vote(manches)
    manche.voter("j-1", "j-2")

    with pytest.raises(ErreurRoom) as excinfo:
        manche.voter("j-1", "j-3")

    assert excinfo.value.motif == "deja_vote"
    assert manche.votes == {"j-1": "j-2"}


def test_le_vote_est_complet_quand_tous_ont_vote(manches):
    manche = _en_vote(manches)

    for votant in JOUEURS[:-1]:
        manche.voter(votant, "j-2" if votant != "j-2" else "j-1")
        assert manche.tous_ont_vote() is False

    manche.voter(JOUEURS[-1], "j-1")
    assert manche.tous_ont_vote() is True


def test_la_majorite_stricte_designe_un_joueur(manches):
    manche = _en_vote(manches)

    manche.voter("j-1", "j-4")
    manche.voter("j-2", "j-4")
    manche.voter("j-3", "j-4")
    manche.voter("j-4", "j-1")

    assert manche.designe() == "j-4"


def test_sans_majorite_stricte_personne_n_est_designe(manches):
    manche = _en_vote(manches)

    manche.voter("j-1", "j-2")
    manche.voter("j-2", "j-1")
    manche.voter("j-3", "j-4")
    manche.voter("j-4", "j-3")

    assert manche.designe() is None


def test_une_pluralite_sans_majorite_ne_designe_personne(manches):
    manche = _en_vote(manches)

    manche.voter("j-1", "j-4")
    manche.voter("j-2", "j-4")
    manche.voter("j-3", "j-1")
    manche.voter("j-4", "j-2")

    assert manche.designe() is None


def test_l_imposteur_est_demasque_quand_c_est_lui_le_designe(manches):
    manche = _en_vote(manches)
    autres = [joueur for joueur in JOUEURS if joueur != manche.imposteur]

    for votant in autres:
        manche.voter(votant, manche.imposteur)
    manche.voter(manche.imposteur, autres[0])

    assert manche.designe() == manche.imposteur
    assert manche.demasque() is True


def test_l_imposteur_l_emporte_quand_le_vote_se_trompe(manches):
    manche = _en_vote(manches)
    innocent = next(joueur for joueur in JOUEURS if joueur != manche.imposteur)

    for votant in JOUEURS:
        manche.voter(votant, innocent if votant != innocent else manche.imposteur)

    assert manche.designe() == innocent
    assert manche.demasque() is False


def test_le_forcage_ne_compte_que_les_suffrages_exprimes(manches):
    """Un seul votant, un seul suffrage : c'est une majorité stricte des exprimés."""
    manche = _en_vote(manches)
    manche.voter("j-1", "j-2")

    manche.fermer_vote()

    assert manche.designe() == "j-2"


def test_un_vote_sans_aucun_suffrage_ne_designe_personne(manches):
    manche = _en_vote(manches)

    manche.fermer_vote()

    assert manche.designe() is None
    assert manche.demasque() is False


def test_les_tours_joues_comptent_les_passages_effectifs(manches):
    manche = manches.lancer(JOUEURS)
    assert manche.tours_joues() == 0

    manche.passer(manche.orateur())
    assert manche.tours_joues() == 1

    for _ in range(len(JOUEURS) - 1):
        manche.passer(manche.orateur())
    assert manche.tours_joues() == 1, "le tour suivant n'est pas entamé"

    manche.passer(manche.orateur())
    assert manche.tours_joues() == 2


def test_un_parti_est_saute_a_l_ordre_de_parole(manches):
    manche = manches.lancer(JOUEURS)

    manche.retirer(manche.ordre[1])

    assert manche.orateur() == manche.ordre[0]
    manche.passer(manche.ordre[0])
    assert manche.orateur() == manche.ordre[2]


def test_le_depart_de_l_orateur_passe_la_parole_au_suivant(manches):
    manche = manches.lancer(JOUEURS)

    manche.retirer(manche.ordre[0])

    assert manche.orateur() == manche.ordre[1]


def test_un_tour_se_boucle_meme_ampute(manches):
    manche = manches.lancer(JOUEURS)
    manche.retirer(manche.ordre[3])

    for _ in range(3):
        manche.passer(manche.orateur())

    assert manche.tour == 2
    assert manche.orateur() == manche.ordre[0]


def test_le_vote_se_ferme_sans_attendre_les_partis(manches):
    manche = _en_vote(manches)
    manche.retirer("j-4")

    for votant in ("j-1", "j-2", "j-3"):
        manche.voter(votant, "j-1" if votant != "j-1" else "j-2")

    assert manche.tous_ont_vote() is True


def test_on_ne_vote_pas_pour_un_parti(manches):
    manche = _en_vote(manches)
    manche.retirer("j-4")

    with pytest.raises(ErreurRoom) as excinfo:
        manche.voter("j-1", "j-4")

    assert excinfo.value.motif == "cible_inconnue"


def test_le_suffrage_d_un_parti_reste_au_depouillement(manches):
    manche = _en_vote(manches)
    manche.voter("j-4", "j-1")

    manche.retirer("j-4")

    assert manche.votes == {"j-4": "j-1"}
    assert manche.designe() == "j-1", "un suffrage exprimé le reste"


def test_le_drapeau_je_ne_connais_pas_se_leve_pendant_la_manche(manches):
    manche = manches.lancer(JOUEURS)

    manche.signaler_meconnaissance("j-2")

    assert manche.meconnaissances == {"j-2"}


def test_le_drapeau_est_definitif_pour_la_manche(manches):
    manche = manches.lancer(JOUEURS)
    manche.signaler_meconnaissance("j-2")

    with pytest.raises(ErreurRoom) as excinfo:
        manche.signaler_meconnaissance("j-2")

    assert excinfo.value.motif == "deja_signale"
    assert manche.meconnaissances == {"j-2"}


def test_le_drapeau_se_leve_encore_pendant_le_vote(manches):
    manche = _en_vote(manches)

    manche.signaler_meconnaissance("j-2")

    assert manche.meconnaissances == {"j-2"}


def test_le_drapeau_ne_se_leve_plus_apres_la_revelation(manches):
    manche = _en_vote(manches)
    manche.fermer_vote()

    with pytest.raises(ErreurRoom) as excinfo:
        manche.signaler_meconnaissance("j-2")

    assert excinfo.value.motif == "manche_terminee"
    assert manche.meconnaissances == set()


def test_le_drapeau_ne_change_rien_a_ce_que_voit_le_joueur(manches):
    manche = manches.lancer(JOUEURS)
    avant = [manche.personnage(joueur) for joueur in JOUEURS]

    manche.signaler_meconnaissance("j-2")

    assert [manche.personnage(joueur) for joueur in JOUEURS] == avant


def test_la_repartition_des_votes_est_anonyme_et_decroissante(manches):
    manche = _en_vote(manches)
    manche.voter("j-1", "j-2")
    manche.voter("j-3", "j-2")
    manche.voter("j-4", "j-1")

    assert manche.repartition() == [2, 1]


def test_les_voix_portees_sur_l_imposteur_se_comptent(manches):
    manche = _en_vote(manches)
    autre = next(joueur for joueur in JOUEURS if joueur != manche.imposteur)
    for votant in JOUEURS:
        if votant != manche.imposteur:
            manche.voter(votant, manche.imposteur)
    manche.voter(manche.imposteur, autre)

    assert manche.voix_imposteur() == 3


def test_un_vote_vide_ne_repartit_rien(manches):
    manche = _en_vote(manches)

    assert manche.repartition() == []
    assert manche.voix_imposteur() == 0
