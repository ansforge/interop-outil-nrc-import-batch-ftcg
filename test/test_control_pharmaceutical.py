import pandas as pd
from import_batch_ftcg import control


################
# Tests de me1 #
################
def test_no_me1(null: pd.DataFrame, semtag: pd.Series) -> None:
    """Vérifie que la fonction control._check_me1 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères de me1
        semtag: Filtre de test sur les Body structure de `null`
    """
    me = semtag(len(null))
    pd.testing.assert_frame_equal(control._check_me1(null, me), null)


def test_check_me1(me1: pd.DataFrame, me1_output: pd.DataFrame,
                   semtag: pd.Series) -> None:
    """Vérifie le bon fonctionnement de control._check_me1.

    args:
        me1: DataFrame de test à corriger
        me1_output: DataFrame corrigé attendu
        semtag: Filtre de test sur les Body structure de `me1`
    """
    me = semtag(len(me1))
    pd.testing.assert_frame_equal(control._check_me1(me1, me), me1_output)


################
# Tests de me2 #
################
def test_no_me2(null: pd.DataFrame, semtag: pd.Series) -> None:
    """Vérifie que la fonction control._check_me2 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères de me2
        semtag: Filtre de test sur les Body structure de `null`
    """
    me = semtag(len(null))
    pd.testing.assert_frame_equal(control._check_me2(null, me), null)


def test_check_me2(me2: pd.DataFrame, me2_output: pd.DataFrame,
                   semtag: pd.Series) -> None:
    """Vérifie le bon fonctionnement de control._check_me2.

    args:
        me2: DataFrame de test à corriger
        me2_output: DataFrame corrigé attendu
        semtag: Filtre de test sur les Body structure de `me2`
    """
    me = semtag(len(me2))
    pd.testing.assert_frame_equal(control._check_me2(me2, me), me2_output)


################
# Tests de me3 #
################
def test_no_me3(null: pd.DataFrame, semtag: pd.Series) -> None:
    """Vérifie que la fonction control._check_me3 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères de me3
        semtag: Filtre de test sur les Body structure de `null`
    """
    me = semtag(len(null))
    pd.testing.assert_frame_equal(control._check_me3(null, me), null)


def test_check_me3(me3: pd.DataFrame, me3_output: pd.DataFrame,
                   semtag: pd.Series) -> None:
    """Vérifie le bon fonctionnement de control._check_me3.

    args:
        me3: DataFrame de test à corriger
        me3_output: DataFrame corrigé attendu
        semtag: Filtre de test sur les Body structure de `me3`
    """
    me = semtag(len(me3))
    pd.testing.assert_frame_equal(control._check_me3(me3, me), me3_output)


################
# Tests de me4 #
################
def test_no_me4(null: pd.DataFrame, semtag: pd.Series) -> None:
    """Vérifie que la fonction control._check_me4 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères de me4
        semtag: Filtre de test sur les Body structure de `null`
    """
    me = semtag(len(null))
    pd.testing.assert_frame_equal(control._check_me4(null, me), null)


def test_check_me4(me4: pd.DataFrame, me4_output: pd.DataFrame,
                   semtag: pd.Series) -> None:
    """Vérifie le bon fonctionnement de control._check_me4.

    args:
        me4: DataFrame de test à corriger
        me4_output: DataFrame corrigé attendu
        semtag: Filtre de test sur les Body structure de `me4`
    """
    me = semtag(len(me4))
    pd.testing.assert_frame_equal(control._check_me4(me4, me), me4_output)
