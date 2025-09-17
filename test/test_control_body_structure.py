import pandas as pd
from import_batch_ftcg import control


################
# Tests de bs2 #
################
def test_no_bs2(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_bs2 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'bs2
    """
    pd.testing.assert_frame_equal(control._check_bs2(null), null)


def test_check_bs2(bs2: pd.DataFrame, bs2_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_bs2.

    args:
        bs2: DataFrame de test à corriger
        bs2_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_bs2(bs2), bs2_output)


################
# Tests de bs3 #
################
def test_no_bs3(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_bs3 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'bs3
    """
    pd.testing.assert_frame_equal(control._check_bs3(null), null)


def test_check_bs3(bs3: pd.DataFrame, bs3_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_bs3.

    args:
        bs3: DataFrame de test à corriger
        bs3_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_bs3(bs3), bs3_output)


################
# Tests de bs5 #
################
def test_no_bs5(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_bs5 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'bs5
    """
    pd.testing.assert_frame_equal(control._check_bs5(null), null)


def test_check_bs5(bs5: pd.DataFrame, bs5_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_bs5.

    args:
        bs5: DataFrame de test à corriger
        bs5_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_bs5(bs5), bs5_output)


################
# Tests de bs6 #
################
def test_no_bs6(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_bs6 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'bs6
    """
    pd.testing.assert_frame_equal(control._check_bs6(null), null)


def test_check_bs6(bs6: pd.DataFrame, bs6_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_bs6.

    args:
        bs6: DataFrame de test à corriger
        bs6_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_bs6(bs6), bs6_output)


################
# Tests de bs7 #
################
def test_no_bs7(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_bs7 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'bs7
    """
    pd.testing.assert_frame_equal(control._check_bs7(null), null)


def test_check_bs7(bs7: pd.DataFrame, bs7_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_bs7.

    args:
        bs7: DataFrame de test à corriger
        bs7_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_bs7(bs7), bs7_output)


################
# Tests de bs8 #
################
def test_no_bs8(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_bs8 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'bs8
    """
    pd.testing.assert_frame_equal(control._check_bs8(null), null)


def test_check_bs8(bs8: pd.DataFrame, bs8_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_bs8.

    args:
        bs8: DataFrame de test à corriger
        bs8_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_bs8(bs8), bs8_output)


################
# Tests de bs9 #
################
def test_no_bs9(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_bs9 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'bs9
    """
    pd.testing.assert_frame_equal(control._check_bs9(null), null)


def test_check_bs9(bs9: pd.DataFrame, bs9_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_bs9.

    args:
        bs9: DataFrame de test à corriger
        bs9_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_bs9(bs9), bs9_output)


#################
# Tests de bs10 #
#################
def test_no_bs10(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_bs10 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'bs10
    """
    pd.testing.assert_frame_equal(control._check_bs10(null), null)


def test_check_bs10(bs10: pd.DataFrame, bs10_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_bs10.

    args:
        bs10: DataFrame de test à corriger
        bs10_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_bs10(bs10), bs10_output)


#################
# Tests de bs11 #
#################
def test_no_bs11(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_bs11 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'bs11
    """
    pd.testing.assert_frame_equal(control._check_bs11(null), null)


def test_check_bs11(bs11: pd.DataFrame, bs11_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_bs11.

    args:
        bs11: DataFrame de test à corriger
        bs11_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_bs11(bs11), bs11_output)


#################
# Tests de bs12 #
#################
def test_no_bs12(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_bs12 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'bs12
    """
    pd.testing.assert_frame_equal(control._check_bs12(null), null)


def test_check_bs12(bs12: pd.DataFrame, bs12_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_bs12.

    args:
        bs12: DataFrame de test à corriger
        bs12_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_bs12(bs12), bs12_output)


#################
# Tests de bs13 #
#################
def test_no_bs13(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_bs13 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'bs13
    """
    pd.testing.assert_frame_equal(control._check_bs13(null), null)


def test_check_bs13(bs13: pd.DataFrame, bs13_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_bs13.

    args:
        bs13: DataFrame de test à corriger
        bs13_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_bs13(bs13), bs13_output)
