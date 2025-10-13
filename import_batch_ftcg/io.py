import pandas as pd

from import_batch_ftcg import server
from os import path as op
from typing import Set

CASE = {
    "900000000000448009": "ci",
    "900000000000017005": "CS",
    "900000000000020002": "cI"
}

ACCEPT = {
    "900000000000548007": "PREFERRED",
    "900000000000549004": "ACCEPTABLE"
}


def read_common_french(path: str, date: str, fts: server.Fts) -> pd.DataFrame:
    """Lecture de la dernière release de la Common French.

    args:
        path: Chemin vers le dossier Snapshot de la Common French
        date: Date de release de la Common French
        fts: Serveur de Terminologies FHIR contenant la version de l'édition
            internationale dont dépend votre édition nationale non publiée

    returns:
        DataFrame contenant les informations de descriptions
    """
    # Vérification du dossier donné en paramètre
    if op.basename(op.normpath(path)) != "Snapshot":
        raise ValueError("Le chemin ne pointe pas vers le dossier Snapshot")

    # Lecture des descriptions de la Common French
    p = op.join(path, f"Terminology/sct2_Description_Snapshot_CommonFrench-Extension_{date}.txt") # noqa
    desc = pd.read_csv(p, sep="\t", quoting=3, na_filter=False,
                       dtype={"id": str, "active": pd.CategoricalDtype(["1", "0"]),
                              "conceptId": str, "typeId": str, "term": str},
                       usecols=["id", "active", "conceptId", "typeId", "term",
                                "caseSignificanceId"],
                       converters={"caseSignificanceId": lambda x: CASE.get(x)})

    # Extraire les FSN
    active = (desc.loc[:, "active"] == "1")
    fsn = desc.loc[(desc.loc[:, "typeId"] == "900000000000003001") & active,
                   ["conceptId", "term"]]
    fsn.columns = ["conceptId", "fsn"]

    # Conserver seulement les synonymes actifs
    desc = desc.loc[(desc.loc[:, "typeId"] == "900000000000013009") & active]
    # Supprimer les colonnes 'active' et 'typeId' qui ne sont plus nécessaires
    desc = desc.drop(["active", "typeId"], axis=1)
    # Ajouter la colonne des FSN
    desc = pd.merge(desc, fsn, how="left", on="conceptId")

    # Lecture du refset de langue de la Common French
    p = op.join(path, f"Refset/Language/der2_cRefset_LanguageSnapshot_CommonFrench-Extension_{date}.txt") # noqa
    lang = pd.read_csv(p, sep="\t", na_filter=False,
                       dtype={"referencedComponentId": str},
                       usecols=["referencedComponentId", "acceptabilityId"],
                       converters={"acceptabilityId": lambda x: ACCEPT.get(x)})

    # Ajouter l'acceptabilité au DataFrame des descriptions
    desc = pd.merge(desc, lang, how="left", left_on="id",
                    right_on="referencedComponentId")
    # Supprimer la colonne 'referencedComponentId' qui n'est plus nécessaire
    desc = desc.drop(["referencedComponentId"], axis=1)

    # Retirer les traductions des hiérarchies
    # 'Environment or geographical location' et 'Organism'
    env = fts.ecl("<< 308916002")
    org = fts.ecl("<< 410607006")
    desc = desc.loc[(~desc.loc[:, "conceptId"].isin(env))
                    & (~desc.loc[:, "conceptId"].isin(org))]

    return desc


def get_fr_edition(path: str, unpub_path: str) -> Set[str]:
    """Liste les SCTID de concepts ayant des descriptions FR actives ou non, mise à
    jour avec les modifications non-publiées.

    args:
        path: Chemin vers le fichier des descriptions FR de l'édition nationale
        unpub_path: Chemin vers l'extrait du rapport "New and change components"

    returns:
        Liste de SCITD
    """
    # Vérification des chemins donné en paramètre
    if not op.isfile(path) or not op.exists(path):
        raise ValueError("Le chemin vers le fichier de descriptions est invalide.")
    if not op.isfile(unpub_path) or not op.exists(unpub_path):
        raise ValueError("Le chemin vers le fichier de modifications est invalide.")

    # Lecture de l'édition nationale publiée
    df = pd.read_csv(path, sep="\t", na_filter=False, dtype=str, usecols=["conceptId"])
    published = set(df.loc[:, "conceptId"].unique())

    # Lecture des modifications non publiées de l'édition nationale
    unpub = pd.read_csv(unpub_path, sep="\t", na_filter=False, dtype=str,
                        usecols=["Id", "isNew"])

    # Ajout des SCTID de nouvelles descriptions
    return published.union(list(unpub.loc[unpub.loc[:, "isNew"] == "Y", "Id"]))


def write_batch_file(cf: pd.DataFrame, path: str) -> None:
    """Sauvegarde des traduction de la Common French à importer en batch sous forme
    de fichier 'Description Additions'.

    args:
        cf: Descriptions de la Common French à importer.
        path: Emplacement et nom du fichier d'import en batch.
    """
    # Supprimer les colonnes inutiles
    cf = cf.drop(["id", "fsn"], axis=1)
    # Ajouter les colonnes nécessaire au respect du fichier d'import en batch
    cf.insert(1, "termRef", [""] * len(cf))
    cf.insert(2, "preferredTerm", [""] * len(cf))
    cf.insert(4, "lang", ["fr"] * len(cf))
    cf.insert(6, "typeId", ["SYNONYM"] * len(cf))
    cf.insert(7, "langRefset1", ["French"] * len(cf))
    cf.insert(9, "langRefset2", [""] * len(cf))
    cf.insert(10, "acceptability2", [""] * len(cf))
    cf.insert(11, "langRefset3", [""] * len(cf))
    cf.insert(12, "acceptability3", [""] * len(cf))
    cf.insert(13, "langRefset4", [""] * len(cf))
    cf.insert(14, "acceptability4", [""] * len(cf))
    cf.insert(15, "langRefset5", [""] * len(cf))
    cf.insert(16, "acceptability5", [""] * len(cf))
    cf.insert(17, "notes", [""] * len(cf))
    # Renommer la colonne d'acceptabilité
    cf.rename(columns={"acceptabilityId": "acceptability1"}, inplace=True)
    # Remplacer les valeurs NaN par des 0
    cf = cf.fillna("")
    cf.to_csv(path, sep="\t", index=False, encoding="UTF-8")
