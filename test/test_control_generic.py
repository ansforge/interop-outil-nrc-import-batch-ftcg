import pandas as pd
from import_batch_ftcg import control


###############################
# Test de gestion de la casse #
###############################
def test_get_correct_case(case: pd.DataFrame, case_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._get_correct_case.

    args:
        case: DataFrame de test à corriger
        case_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._get_correct_case(case), case_output)


################
# Tests de ar2 #
################
def test_no_ar2(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_ar2 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'ar2
    """
    pd.testing.assert_frame_equal(control._check_ar2(null), null)


def test_check_ar2(ar2: pd.DataFrame, ar2_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_ar2.

    args:
        ar2: DataFrame de test à corriger
        ar2_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_ar2(ar2), ar2_output)


################
# Tests de ar6 #
################
def test_no_ar6(null: pd.DataFrame, semtag: pd.Series) -> None:
    """Vérifie que la fonction control._check_ar6 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères de ar6
        semtag: Filtre de test sur les Body structure de `null`
    """
    bs = semtag(len(null))
    pd.testing.assert_frame_equal(control._check_ar6(null, bs), null)


def test_check_ar6(ar6: pd.DataFrame, ar6_output: pd.DataFrame,
                   semtag: pd.Series) -> None:
    """Vérifie le bon fonctionnement de control._check_ar6.

    args:
        ar6: DataFrame de test à corriger
        ar6_output: DataFrame corrigé attendu
        semtag: Filtre de test sur les Body structure de `ar6`
    """
    sb = semtag(len(ar6))
    pd.testing.assert_frame_equal(control._check_ar6(ar6, sb), ar6_output)
