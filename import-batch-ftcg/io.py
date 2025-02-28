import pandas as pd
from os import path as op

CASE = {
    "900000000000448009": "ci",
    "900000000000017005": "CS",
    "900000000000020002": "cI"
}

ACCEPT = {
    "900000000000548007": "PREFERRED",
    "900000000000549004": "ACCEPTABLE"
}
    
def read_common_french(cf_path: str, cf_date: str) -> pd.DataFrame:
    """Lecture de la dernière release de la Common French.
    args:
        cf_path: Chemin vers le dossier Snapshot de la Common French
        cf_date: Date de release de la Common French

    returns:
        DataFrame contenant les informations de descriptions
    """
    # Vérification du dossier donné en paramètre
    if op.basename(op.normpath(cf_path)) != "Snapshot":
        ValueError("Le chemin vers la Common French ne pointe pas vers le dossier Snapshot")
        
    # Lecture des descriptions
    cf_desc_path = op.join(cf_path, f"Terminology/sct2_Description_Snapshot_CommonFrench-Extension_{cf_date}.txt")
    cf_description = pd.read_csv(cf_desc_path, sep="\t", dtype=str, usecols=["id", "active", "conceptId", "typeId", "term", "caseSignificanceId"], 
                                 quoting=3, converters={"caseSignificanceId": lambda x: CASE.get(x)}, encoding="UTF-8")
    # Conserver seulement les synonymes actifs
    cf_description = cf_description.loc[(cf_description.loc[:, "typeId"] == "900000000000013009") & (cf_description.loc[:, "active"] == "1")]
    # Supprimer les colonnes 'active' et 'typeId' qui ne sont plus nécessaires
    cf_description.drop(["active", "typeId"], axis=1, inplace=True)

    # Lecture du refset de langue
    cf_lang_path = op.join(cf_path, f"Refset/Language/der2_cRefset_LanguageSnapshot_CommonFrench-Extension_{cf_date}.txt")
    cf_language = pd.read_csv(cf_lang_path, sep="\t", dtype=str, usecols=["referencedComponentId", "acceptabilityId"], 
                              converters={"acceptabilityId": lambda x: ACCEPT.get(x)}, encoding="UTF-8")
        
    # Ajouter l'acceptabilité au DataFrame des descriptions
    cf_description = pd.merge(cf_description, cf_language, how="left", left_on="id", right_on="referencedComponentId")
    # Supprimer les colonnes 'id' et 'referencedComponentId' qui ne sont plus nécessaires
    cf_description.drop(["id", "referencedComponentId"], axis=1, inplace=True)

    return cf_description