import pandas as pd

from import_batch_ftcg import control
from typing import Callable


################
# Tests de pr2 #
################
def test_no_pr2(null: pd.DataFrame, null_pt: pd.Series, null_syn: pd.Series) -> None:
    """Vérifie que la fonction control._check_pr2 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères de pr2
        null_pt: Filtre de test sur les termes préférés de `null`
        null_pt: Filtre de test sur les synonymes acceptables de `null`
    """
    pd.testing.assert_frame_equal(control._check_pr2(null, null_pt, null_syn), null)


def test_check_pr2(pr2: pd.DataFrame, pr2_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_pr2.

    args:
        pr2: DataFrame de test à corriger
        pr2_output: DataFrame corrigé attendu
    """
    pt = (pr2.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (pr2.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(control._check_pr2(pr2, pt, syn), pr2_output)


################
# Tests de pr3 #
################
def test_no_pr3(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_pr3 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères de pr3
    """
    pd.testing.assert_frame_equal(control._check_pr3(null), null)


def test_check_pr3(pr3: pd.DataFrame, pr3_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_pr3.

    args:
        pr3: DataFrame de test à corriger
        pr3_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_pr3(pr3), pr3_output)


################
# Tests de pr4 #
################
def test_no_pr4(null: pd.DataFrame, null_pt: pd.Series, null_syn: pd.Series) -> None:
    """Vérifie que la fonction control._check_pr4 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères de pr4
        null_pt: Filtre de test sur les termes préférés de `null`
        null_pt: Filtre de test sur les synonymes acceptables de `null`
    """
    pd.testing.assert_frame_equal(control._check_pr4(null, null_pt, null_syn), null)


def test_check_pr4(pr4: pd.DataFrame, pr4_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_pr4.

    args:
        pr4: DataFrame de test à corriger
        pr4_output: DataFrame corrigé attendu
    """
    pt = (pr4.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (pr4.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(control._check_pr4(pr4, pt, syn), pr4_output)


################
# Tests de pr9 #
################
def test_no_pr9(null: pd.DataFrame, null_pt: pd.Series, null_syn: pd.Series) -> None:
    """Vérifie que la fonction control._check_pr9 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères de pr9
        null_pt: Filtre de test sur les termes préférés de `null`
        null_pt: Filtre de test sur les synonymes acceptables de `null`
    """
    pd.testing.assert_frame_equal(control._check_pr9(null, null_pt, null_syn), null)


def test_check_pr9(pr9: pd.DataFrame, pr9_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_pr9.

    args:
        pr9: DataFrame de test à corriger
        pr9_output: DataFrame corrigé attendu
    """
    pt = (pr9.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (pr9.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(control._check_pr9(pr9, pt, syn), pr9_output)


################
# Tests de pr10 #
################
def test_no_pr10(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_pr10 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères de pr10
    """
    pd.testing.assert_frame_equal(control._check_pr10(null), null)


def test_check_pr10(pr10: pd.DataFrame, pr10_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_pr10.

    args:
        pr10: DataFrame de test à corriger
        pr10_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_pr10(pr10), pr10_output)


################
# Tests de pr12 #
################
def test_no_pr12(null: pd.DataFrame, null_pt: pd.Series, null_syn: pd.Series) -> None:
    """Vérifie que la fonction control._check_pr12 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères de pr12
        null_pt: Filtre de test sur les termes préférés de `null`
        null_pt: Filtre de test sur les synonymes acceptables de `null`
    """
    pd.testing.assert_frame_equal(control._check_pr12(null, null_pt, null_syn), null)


def test_check_pr12(pr12: pd.DataFrame, pr12_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_pr12.

    args:
        pr12: DataFrame de test à corriger
        pr12_output: DataFrame corrigé attendu
    """
    pt = (pr12.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (pr12.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(control._check_pr12(pr12, pt, syn), pr12_output)


################
# Tests de pr13 #
################
def test_no_pr13(null: pd.DataFrame, null_pt: pd.Series, null_syn: pd.Series) -> None:
    """Vérifie que la fonction control._check_pr13 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères de pr13
        null_pt: Filtre de test sur les termes préférés de `null`
        null_pt: Filtre de test sur les synonymes acceptables de `null`
    """
    pd.testing.assert_frame_equal(control._check_pr13(null, null_pt, null_syn), null)


def test_check_pr13(pr13: pd.DataFrame, pr13_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_pr13.

    args:
        pr13: DataFrame de test à corriger
        pr13_output: DataFrame corrigé attendu
    """
    pt = (pr13.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (pr13.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(control._check_pr13(pr13, pt, syn), pr13_output)


################
# Tests de pr14 #
################
def test_no_pr14(null: pd.DataFrame, null_pt: pd.Series, null_syn: pd.Series) -> None:
    """Vérifie que la fonction control._check_pr14 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères de pr14
        null_pt: Filtre de test sur les termes préférés de `null`
        null_pt: Filtre de test sur les synonymes acceptables de `null`
    """
    pd.testing.assert_frame_equal(control._check_pr14(null, null_pt, null_syn), null)


def test_check_pr14(pr14: pd.DataFrame, pr14_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_pr14.

    args:
        pr14: DataFrame de test à corriger
        pr14_output: DataFrame corrigé attendu
    """
    pt = (pr14.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (pr14.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(control._check_pr14(pr14, pt, syn), pr14_output)


####################
# Tests de pr15-FR #
####################
def test_no_pr15(null: pd.DataFrame, semtag: Callable[[int], pd.Series]) -> None:
    """Vérifie que la fonction control._check_pr15 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères de pr15-FR
        null_pt: Filtre de test sur les termes préférés de `null`
        null_pt: Filtre de test sur les synonymes acceptables de `null`
        semtag: Filtre de test sur les Procedure de `null`
    """
    pr = semtag(len(null))
    pd.testing.assert_frame_equal(control._check_pr15(null, pr), null)


def test_check_pr15(pr15: pd.DataFrame, pr15_output: pd.DataFrame,
                    semtag: Callable[[int], pd.Series]) -> None:
    """Vérifie le bon fonctionnement de control._check_pr15.

    args:
        pr15: DataFrame de test à corriger
        pr15_output: DataFrame corrigé attendu
        semtag: Callable[[int], pd.Series]
    """
    pr = semtag(len(pr15))
    pd.testing.assert_frame_equal(control._check_pr15(pr15, pr), pr15_output)
