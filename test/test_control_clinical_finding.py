import pandas as pd
import pytest

from import_batch_ftcg import control, server
from typing import Generator


################
# Tests de co2 #
################
def test_no_co2(null: pd.DataFrame, semtag: pd.Series) -> None:
    """Vérifie que la fonction control._check_co2 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères de co2
        semtag: Filtre de test sur les Clinical finding de `null`
    """
    co = semtag(len(null))
    pd.testing.assert_frame_equal(control._check_co2(null, co), null)


def test_check_co2(co2: pd.DataFrame, co2_output: pd.DataFrame,
                   semtag: pd.Series) -> None:
    """Vérifie le bon fonctionnement de control._check_co2.

    args:
        co2: DataFrame de test à corriger
        co2_output: DataFrame corrigé attendu
        semtag: Filtre de test sur les Clinical finding de `co2`
    """
    co = semtag(len(co2))
    pd.testing.assert_frame_equal(control._check_co2(co2, co), co2_output)


################
# Tests de co6 #
################
def test_no_co6(null: pd.DataFrame, semtag: pd.Series) -> None:
    """Vérifie que la fonction control._check_co6 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères de co2
        semtag: Filtre de test sur les Clinical finding de `null`
    """
    co = semtag(len(null))
    pd.testing.assert_frame_equal(control._check_co6(null, co), null)


def test_check_co6(co6: pd.DataFrame, co6_output: pd.DataFrame,
                   semtag: pd.Series) -> None:
    """Vérifie le bon fonctionnement de control._check_co6.

    args:
        co6: DataFrame de test à corriger
        co6_output: DataFrame corrigé attendu
        semtag: Filtre de test sur les Clinical finding de `co6`
    """
    co = semtag(len(co6))
    pd.testing.assert_frame_equal(control._check_co6(co6, co), co6_output)


################
# Tests de pa3 #
################
def test_no_pa3(null: pd.DataFrame, fts_pa3: Generator,
                pytestconfig: pytest.Config) -> None:
    """Vérifie que la fonction control._check_pa3 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères de pa3
    """
    fts = server.Fts(pytestconfig.getoption("endpoint"))
    pd.testing.assert_frame_equal(control._check_pa3(null, fts), null)


def test_check_pa3(pa3: pd.DataFrame, pa3_output: pd.DataFrame,
                   fts_pa3: Generator, pytestconfig: pytest.Config) -> None:
    """Vérifie le bon fonctionnement de control._check_pa3.

    args:
        pa3: DataFrame de test à corriger
        pa3_output: DataFrame corrigé attendu
    """
    fts = server.Fts(pytestconfig.getoption("endpoint"))
    pd.testing.assert_frame_equal(control._check_pa3(pa3, fts), pa3_output)


##################
# Tests de pa3.1 #
##################
def test_no_pa3_1(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_pa3_1 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères de pa3.1
    """
    pd.testing.assert_frame_equal(control._check_pa3_1(null), null)


def test_check_pa3_1(pa3_1: pd.DataFrame, pa3_1_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_pa3.

    args:
        pa3_1: DataFrame de test à corriger
        pa3_1_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_pa3_1(pa3_1), pa3_1_output)


################
# Tests de pa4 #
################
def test_no_pa4(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_pa4 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

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
    """Vérifie que la fonction control._check_pa6 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

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
    """Vérifie que la fonction control._check_pa7 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

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
    """Vérifie que la fonction control._check_pa8 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

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
    """Vérifie que la fonction control._check_pa9 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

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
