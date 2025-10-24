import pandas as pd
import pytest

from import_batch_ftcg import control, server
from typing import Generator


def test_no_missing_arguments(control_cf: pd.DataFrame, fts: Generator,
                              pytestconfig: pytest.Config) -> None:
    """Vérifie que la fonction `run_quality_control` lance toutes les fonctions de
    contrôles avec les bons arguments

    Args:
        control_cf: DataFrame vide (mimant un DataFrame de la Common French)
        fts: Mock les requêtes envoyées par `run_quality_control`
        pytestconfig: Récupère l'argument contenant la base de l'URL du FTS à utiliser
    """
    fts = server.Fts(pytestconfig.getoption("endpoint"))
    pd.testing.assert_frame_equal(control.run_quality_control(control_cf, fts),
                                  control_cf)
