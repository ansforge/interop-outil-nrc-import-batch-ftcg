import pandas as pd

from import_batch_ftcg import control
from typing import Callable


################
# Tests de hs1 #
################
def test_no_hs1(null: pd.DataFrame, semtag: Callable[[int], pd.Series]) -> None:
    """Vérifie que la fonction control._check_hs1 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères de hs1
        semtag: Filtre de test sur les Body structure de `null`
    """
    hs = semtag(len(null))
    pd.testing.assert_frame_equal(control._check_hs1(null, hs), null)


def test_check_hs1(hs1: pd.DataFrame, hs1_output: pd.DataFrame,
                   semtag: Callable[[int], pd.Series]) -> None:
    """Vérifie le bon fonctionnement de control._check_hs1.

    args:
        hs1: DataFrame de test à corriger
        hs1_output: DataFrame corrigé attendu
        semtag: Filtre de test sur les Body structure de `hs1`
    """
    hs = semtag(len(hs1))
    pd.testing.assert_frame_equal(control._check_hs1(hs1, hs), hs1_output)
