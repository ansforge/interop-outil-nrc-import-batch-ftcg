import pandas as pd
from import_batch_ftcg import control


################
# Tests de pr2 #
################
def test_no_pr2(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_pr2 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'pr2
    """
    pd.testing.assert_frame_equal(control._check_pr2(null), null)


def test_check_pr2(pr2: pd.DataFrame, pr2_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_pr2.

    args:
        pr2: DataFrame de test à corriger
        pr2_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_pr2(pr2), pr2_output)


################
# Tests de pr3 #
################
def test_no_pr3(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_pr3 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'pr3
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
def test_no_pr4(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_pr4 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'pr4
    """
    pd.testing.assert_frame_equal(control._check_pr4(null), null)


def test_check_pr4(pr4: pd.DataFrame, pr4_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_pr4.

    args:
        pr4: DataFrame de test à corriger
        pr4_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_pr4(pr4), pr4_output)


################
# Tests de pr9 #
################
def test_no_pr9(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_pr9 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'pr9
    """
    pd.testing.assert_frame_equal(control._check_pr9(null), null)


def test_check_pr9(pr9: pd.DataFrame, pr9_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_pr9.

    args:
        pr9: DataFrame de test à corriger
        pr9_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_pr9(pr9), pr9_output)


################
# Tests de pr10 #
################
def test_no_pr10(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_pr10 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'pr10
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
def test_no_pr12(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_pr12 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'pr12
    """
    pd.testing.assert_frame_equal(control._check_pr12(null), null)


def test_check_pr12(pr12: pd.DataFrame, pr12_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_pr12.

    args:
        pr12: DataFrame de test à corriger
        pr12_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_pr12(pr12), pr12_output)


################
# Tests de pr13 #
################
def test_no_pr13(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_pr13 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'pr13
    """
    pd.testing.assert_frame_equal(control._check_pr13(null), null)


def test_check_pr13(pr13: pd.DataFrame, pr13_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_pr13.

    args:
        pr13: DataFrame de test à corriger
        pr13_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_pr13(pr13), pr13_output)


################
# Tests de pr14 #
################
def test_no_pr14(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_pr14 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'pr14
    """
    pd.testing.assert_frame_equal(control._check_pr14(null), null)


def test_check_pr14(pr14: pd.DataFrame, pr14_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_pr14.

    args:
        pr14: DataFrame de test à corriger
        pr14_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_pr14(pr14), pr14_output)
