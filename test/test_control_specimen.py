import pandas as pd
from import_batch_ftcg import control


################
# Tests de ec2 #
################
def test_no_ec2(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_ec2 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'ec2
    """
    pd.testing.assert_frame_equal(control._check_ec2(null), null)


def test_check_ec2(ec2: pd.DataFrame, ec2_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_ec2.

    args:
        ec2: DataFrame de test à corriger
        ec2_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_ec2(ec2), ec2_output)


################
# Tests de ec4 #
################
def test_no_ec4(null: pd.DataFrame) -> None:
    """Vérifie que la fonction control._check_ec4 renvoit le DataFrame original si
    aucune ligne ne correspond aux critères

    args:
        null: DataFrame de test ne correspondant pas aux critères d'ec4
    """
    pd.testing.assert_frame_equal(control._check_ec4(null), null)


def test_check_ec4(ec4: pd.DataFrame, ec4_output: pd.DataFrame) -> None:
    """Vérifie le bon fonctionnement de control._check_ec4.

    args:
        ec4: DataFrame de test à corriger
        ec4_output: DataFrame corrigé attendu
    """
    pd.testing.assert_frame_equal(control._check_ec4(ec4), ec4_output)
