import pandas as pd
from import_batch_ftcg import control


################
# Tests de co2 #
################
def test_no_co2(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_co2 renvoit le DataFrame original si aucune ligne ne
    correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'co2
    """
    pd.testing.assert_frame_equal(control._check_co2(null), null)


def test_check_co2(co2: pd.DataFrame, co2_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_co2.

    args:
        co2: DataFrame de test à corriger
        co2_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_co2(co2), co2_output)


################
# Tests de co6 #
################
def test_no_co6(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_co6 renvoit le DataFrame original si aucune ligne ne
    correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'co6
    """
    pd.testing.assert_frame_equal(control._check_co6(null), null)


def test_check_co6(co6: pd.DataFrame, co6_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_co6.

    args:
        co6: DataFrame de test à corriger
        co6_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_co6(co6), co6_output)


################
# Tests de pa4 #
################
def test_no_pa4(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_pa4 renvoit le DataFrame original si aucune ligne ne
    correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'pa4
    """
    pd.testing.assert_frame_equal(control._check_pa4(null), null)


def test_check_pa4(pa4: pd.DataFrame, pa4_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_pa4.

    args:
        pa4: DataFrame de test à corriger
        pa4_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_pa4(pa4), pa4_output)


################
# Tests de pa6 #
################
def test_no_pa6(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_pa6 renvoit le DataFrame original si aucune ligne ne
    correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'pa6
    """
    pd.testing.assert_frame_equal(control._check_pa6(null), null)


def test_check_pa6(pa6: pd.DataFrame, pa6_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_pa6.

    args:
        pa6: DataFrame de test à corriger
        pa6_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_pa6(pa6), pa6_output)


################
# Tests de pa7 #
################
def test_no_pa7(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_pa7 renvoit le DataFrame original si aucune ligne ne
    correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'pa7
    """
    pd.testing.assert_frame_equal(control._check_pa7(null), null)


def test_check_pa7(pa7: pd.DataFrame, pa7_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_pa7.

    args:
        pa7: DataFrame de test à corriger
        pa7_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_pa7(pa7), pa7_output)


################
# Tests de pa8 #
################
def test_no_pa8(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_pa8 renvoit le DataFrame original si aucune ligne ne
    correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'pa8
    """
    pd.testing.assert_frame_equal(control._check_pa8(null), null)


def test_check_pa8(pa8: pd.DataFrame, pa8_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_pa8.

    args:
        pa8: DataFrame de test à corriger
        pa8_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_pa8(pa8), pa8_output)


################
# Tests de pa9 #
################
def test_no_pa9(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_pa9 renvoit le DataFrame original si aucune ligne ne
    correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'pa9
    """
    pd.testing.assert_frame_equal(control._check_pa9(null), null)


def test_check_pa9(pa9: pd.DataFrame, pa9_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_pa9.

    args:
        pa9: DataFrame de test à corriger
        pa9_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_pa9(pa9), pa9_output)
