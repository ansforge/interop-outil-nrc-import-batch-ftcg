import pandas as pd
from import_batch_ftcg import control


################
# Tests de sb1 #
################
def test_no_sb1(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_sb1 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'sb1
    """
    pd.testing.assert_frame_equal(control._check_sb1(null), null)


def test_check_sb1(sb1: pd.DataFrame, sb1_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_sb1.

    args:
        sb1: DataFrame de test à corriger
        sb1_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_sb1(sb1), sb1_output)


################
# Tests de sb2 #
################
def test_no_sb2(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_sb2 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'sb2
    """
    pd.testing.assert_frame_equal(control._check_sb2(null), null)


def test_check_sb2(sb2: pd.DataFrame, sb2_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_sb2.

    args:
        sb2: DataFrame de test à corriger
        sb2_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_sb2(sb2), sb2_output)


################
# Tests de sb3 #
################
def test_no_sb3(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_sb3 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'sb3
    """
    pd.testing.assert_frame_equal(control._check_sb3(null), null)


def test_check_sb3(sb3: pd.DataFrame, sb3_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_sb3.

    args:
        sb3: DataFrame de test à corriger
        sb3_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_sb3(sb3), sb3_output)
