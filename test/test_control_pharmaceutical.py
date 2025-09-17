import pandas as pd
from import_batch_ftcg import control


################
# Tests de me1 #
################
def test_no_me1(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_me1 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'me1
    """
    pd.testing.assert_frame_equal(control._check_me1(null), null)


def test_check_me1(me1: pd.DataFrame, me1_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_me1.

    args:
        me1: DataFrame de test à corriger
        me1_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_me1(me1), me1_output)


################
# Tests de me2 #
################
def test_no_me2(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_me2 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'me2
    """
    pd.testing.assert_frame_equal(control._check_me2(null), null)


def test_check_me2(me2: pd.DataFrame, me2_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_me2.

    args:
        me2: DataFrame de test à corriger
        me2_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_me2(me2), me2_output)


################
# Tests de me3 #
################
def test_no_me3(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_me3 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'me3
    """
    pd.testing.assert_frame_equal(control._check_me3(null), null)


def test_check_me3(me3: pd.DataFrame, me3_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_me3.

    args:
        me3: DataFrame de test à corriger
        me3_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_me3(me3), me3_output)


################
# Tests de me4 #
################
def test_no_me4(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_me4 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'me4
    """
    pd.testing.assert_frame_equal(control._check_me4(null), null)


def test_check_me4(me4: pd.DataFrame, me4_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_me4.

    args:
        me4: DataFrame de test à corriger
        me4_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_me4(me4), me4_output)
