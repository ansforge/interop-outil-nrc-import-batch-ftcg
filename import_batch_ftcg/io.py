import pandas as pd

from import_batch_ftcg import server
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

ACTIVE = {
    "Y": "0",
    "N": "1"
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
        ValueError("Le chemin ne pointe pas vers le dossier Snapshot")

    # Lecture des descriptions de la Common French
    p = op.join(path, f"Terminology/sct2_Description_Snapshot_CommonFrench-Extension_{date}.txt")
    desc = pd.read_csv(p, sep="\t", quoting=3, na_filter=False,
                       dtype={"id": str, "active": pd.CategoricalDtype(["1", "0"]),
                              "conceptId": str, "typeId": str, "term": str},
                       usecols=["id", "active", "conceptId", "typeId", "term",
                                "caseSignificanceId"],
                       converters={"caseSignificanceId": lambda x: CASE.get(x)})

    # Conserver seulement les synonymes actifs
    desc = desc.loc[(desc.loc[:, "typeId"] == "900000000000013009")
                    & (desc.loc[:, "active"] == "1")]
    # Supprimer les colonnes 'active' et 'typeId' qui ne sont plus nécessaires
    desc = desc.drop(["active", "typeId"], axis=1)

    # Lecture du refset de langue de la Common French
    p = op.join(path, f"Refset/Language/der2_cRefset_LanguageSnapshot_CommonFrench-Extension_{date}.txt")
    lang = pd.read_csv(p, sep="\t", dtype={"referencedComponentId": str},
                       usecols=["referencedComponentId", "acceptabilityId"],
                       converters={"acceptabilityId": lambda x: ACCEPT.get(x)})

    # Ajouter l'acceptabilité au DataFrame des descriptions
    desc = pd.merge(desc, lang, how="left", left_on="id", right_on="referencedComponentId")
    # Supprimer la colonne 'referencedComponentId' qui n'est plus nécessaire
    desc = desc.drop(["referencedComponentId"], axis=1)

    # Retirer les traductions des hiérarchies
    # 'Environment or geographical location' et 'Organism'
    env = fts.get_descendants("308916002")
    org = fts.get_descendants("410607006")
    desc = desc.loc[(~desc.loc[:, "conceptId"].isin(env))
                    & (~desc.loc[:, "conceptId"].isin(org))]

    return desc


def _read_published_fr_edition(fr_path: str, fr_date: str) -> pd.DataFrame:
    """Lecture de la dernière release publiée de l'édition nationale.

    args:
        fr_path: Chemin vers le dossier Snapshot de l'édition nationale
        fr_date: Date de release de l'édition nationale

    returns:
        DataFrame contenant les informations de descriptions
    """
    # Vérification du dossier donné en paramètre
    if op.basename(op.normpath(fr_path)) != "Snapshot":
        ValueError("Le chemin vers l'édition nationale ne pointe pas vers le dossier Snapshot")

    # Lecture des descriptions FR
    path = op.join(fr_path, f"Terminology/sct2_Description_Snapshot-fr_FR1000315_{fr_date}.txt")
    desc = pd.read_csv(path, sep="\t", quoting=3, encoding="UTF-8",
                       dtype={"id": str, "active": pd.CategoricalDtype(["1", "0"]),
                              "conceptId": str, "typeId": str, "term": str},
                       usecols=["id", "active", "conceptId", "typeId", "term",
                                "caseSignificanceId"],
                       converters={"caseSignificanceId": lambda x: CASE.get(x)})
    # Conserver seulement les synonymes
    desc = desc.loc[desc.loc[:, "typeId"] == "900000000000013009"]
    # Supprimer la colonne 'typeId' qui n'est plus nécessaire
    desc = desc.drop(["typeId"], axis=1)

    # Lecture du refset de langue
    path = op.join(fr_path, f"Refset/Language/der2_cRefset_LanguageSnapshot-fr_FR1000315_{fr_date}.txt")
    lang = pd.read_csv(path, sep="\t", encoding="UTF-8", dtype={"referencedComponentId": str},
                       usecols=["referencedComponentId", "acceptabilityId"],
                       converters={"acceptabilityId": lambda x: ACCEPT.get(x)})

    # Ajouter l'acceptabilité au DataFrame des descriptions
    desc = pd.merge(desc, lang, how="left", left_on="id", right_on="referencedComponentId")
    # Supprimer la colonne 'referencedComponentId' qui n'est plus nécessaire
    desc = desc.drop(["referencedComponentId"], axis=1)

    return desc


def _read_unpublished_fr_edition(unpub_fr_path: str) -> pd.DataFrame:
    """Lecture des modifications de l'édition nationale depuis la dernière relase.

    args:
        unpub_fr_path: Chemin vers l'extrait du rapport "New and change components"

    returns:
        DataFrame contenant les informations de modifications
    """
    if not op.isfile(unpub_fr_path) or not op.exists(unpub_fr_path):
        ValueError("Le chemin vers le fichier est invalide.")

    # Lecture du fichier concepts
    unpub = pd.read_csv(unpub_fr_path, sep=";", quoting=3, encoding="UTF-8",
                        dtype={"Id": str, " Description": str, " LangRefset": str,
                               " isChanged": str},
                        usecols=["Id", " Description", " LangRefset", " isChanged",
                                 " wasInactivated"],
                        converters={" wasInactivated": lambda x: ACTIVE.get(x)})
    # Renommer les colonnes du fichier
    unpub.columns = ["conceptId", "description", "language", "isChanged", "active"]

    # Extraire les SCTID de descriptions
    unpub.insert(0, "id", [d.split(" ")[0].lstrip("*") for d in unpub.loc[:, "description"]])
    # Extraire les descriptions
    unpub.insert(2, "term", [" ".join(d.split(" ")[3:-1]) for d in unpub.loc[:, "description"]])
    # Extraire les valeurs de casses
    unpub.insert(3, "caseSignificanceId",
                 [d.split(" ")[-1][1:3] for d in unpub.loc[:, "description"]])
    # Extraire l'acceptabilité
    unpub.insert(4, "acceptabilityId", ["PREFERRED" if "PREFERRED" in l else "ACCEPTABLE"
                                        for l in unpub.loc[:, "language"]])
    # Supprimer les colonnes 'description' et 'language' qui ne sont plus nécessaires
    unpub = unpub.drop(["description", "language"], axis=1)

    return unpub


def get_fr_edition(fr_path: str, fr_date: str, unpub_fr_path: str) -> pd.DataFrame:
    """Regroupement de la dernière release publiée de l'édition nationale et des modifications
    non-publiées.

    args:
        fr_path: Chemin vers le dossier Snapshot de l'édition nationale
        fr_date: Date de release de l'édition nationale
        unpub_fr_path: Chemin vers l'extrait du rapport "New and change components"

    returns:
        DataFrame contenant les informations de description à jour
    """
    # Lecture des fichiers
    published = _read_published_fr_edition(fr_path, fr_date)
    unpublished = _read_unpublished_fr_edition(unpub_fr_path)

    # Division des modifications non publiées
    new = unpublished.loc[(unpublished.loc[:, "isChanged"] == "N")
                          & (unpublished.loc[:, "active"] == "1")]
    new = new.drop(["isChanged"], axis=1)
    changed = unpublished.loc[unpublished.loc[:, "isChanged"] == "Y"]
    changed = changed.drop(["conceptId", "term", "isChanged", "active"], axis=1)
    changed = changed.set_index("id")
    inactive = unpublished.loc[(unpublished.loc[:, "isChanged"] == "N")
                               & (unpublished.loc[:, "active"] == "0")]
    inactive = inactive.drop(["conceptId", "term", "caseSignificanceId", "acceptabilityId",
                              "isChanged"], axis=1)
    inactive = inactive.set_index("id")
    # Contrôle de perte
    if len(new) + len(changed) + len(inactive) != len(unpublished):
        Exception("Il existe d'autres modifications non prises en charge dans le fichier.")
    else:
        del unpublished

    # Ajout des nouvelles descriptions
    published = pd.concat([published, new])

    # Application des modifications des descriptions existantes
    published = published.set_index("id")
    published.update(changed)

    # Inactivation des descriptions inactivées
    published.update(inactive)

    return published


def write_batch_file(cf: pd.DataFrame, path: str) -> None:
    """Sauvegarde des traduction de la Common French à importer en batch sous forme
    de fichier 'Description Additions'.

    args:
        cf: Descriptions de la Common French à importer.
        path: Emplacement et nom du fichier d'import en batch.
    """
    # Supprimer les colonnes inutiles
    cf = cf.drop(["id", "fsn", "semtag"], axis=1)
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
