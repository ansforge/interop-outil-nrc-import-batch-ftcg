import pandas as pd
from os import path as op

SEMTAG = {
    # SNOMED RT+CTV3
    "SNOMED RT+CTV3": "root",
    # Body structure
    "body structure": "body structure",
    "cell": "body structure",
    "cell structure": "body structure",
    "morphologic abnormality": "body structure",
    # Clinical finding
    "finding": "clinical finding",
    "disorder": "clinical finding",
    # Environment and/or geographical location
    "environment / location": "environment",
    "environment": "environment",
    "geographic location": "environment",
    # Event
    "event": "event",
    # Observable entity
    "observable entity": "observable entity",
    # Organism
    "organism": "organism",
    # Pharmaceutical or biological product
    "clinical drug": "pharmaceutical",
    "medicinal product": "pharmaceutical",
    "medicinal product form": "pharmaceutical",
    # Physical force
    "physical force": "physical force",
    # Physical object
    "physical object": "physical object",
    "product": "product",
    # Procedure
    "procedure": "procedure",
    "regime/therapy": "procedure",
    # Qualifier value
    "qualifier value": "qualifier value",
    "administration method": "qualifier value",
    "administrative concept": "qualifier value",
    "basic dose form": "qualifier value",
    "disposition": "qualifier value",
    "dose form": "qualifier value",
    "intended site": "qualifier value",
    "number": "qualifier value",
    "product name": "qualifier value",
    "release characteristic": "qualifier value",
    "role": "qualifier value",
    "state of matter": "qualifier value",
    "transformation": "qualifier value",
    "supplier": "qualifier value",
    "unit of presentation": "qualifier value",
    # Record artifact
    "record artifact": "record artifact",
    # SWEC
    "situation": "situation",
    # SNOMED CT Model component
    "attribute": "model component",
    "core metadata concept": "model component",
    "foundation metadata concept": "model component",
    "link assertion": "model component",
    "linkage concept": "model component",
    "metadata": "model component",
    "namespace concept": "model component",
    "OWL metadata concept": "model component",
    # Social context
    "social concept": "social context",
    "ethnic group": "social context",
    "life style": "social context",
    "occupation": "social context",
    "person": "social context",
    "racial group": "social context",
    "religion/philosophy": "social context",
    # Special concept
    "inactive concept": "special concept",
    "navigational concept": "special concept",
    "special concept": "special concept",
    # Specimen
    "specimen": "specimen",
    # Staging and scales
    "assessment scale": "staging scales",
    "staging scale": "staging scales",
    "staging scales": "staging scales",
    "tumor staging": "staging scales",
    # Substance
    "substance": "substance",
    "": ""
}

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


def _get_fsn_semtag(fr_path: str, fr_date: str) -> pd.DataFrame:
    """Récupérer le FSN EN et le suffixe sémantique pour chaque concept traduit
    dans l'édition nationale.

    args:
        fr_path: Chemin vers le dossier Snapshot de l'édition nationale
        fr_date: Date de release de l'édition nationale

    returns:
        DataFrame contenant le FSN et suffixe sémantique associé à un SCTID.
    """
    # Lecture des descriptions EN de l'édition nationale
    path = op.join(fr_path, "Terminology/sct2_Description_Snapshot-en_FR1000315_{fr_date}.txt")
    desc = pd.read_csv(path, sep="\t", dtype=str, quoting=3,
                       usecols=["active", "conceptId", "typeId", "term"])
    desc.columns = ["active", "conceptId", "typeId", "fsn"]

    # Lecture des concepts de l'édition nationale
    path = op.join(fr_path, f"Terminology/sct2_Concept_Snapshot_FR1000315_{fr_date}.txt")
    concept = pd.read_csv(path, sep="\t", dtype=str, usecols=["id", "active"])
    concept = concept.loc[concept.loc[:, "active"] == "1"]

    # Conserver seulement les FSN actifs
    desc = desc.loc[(desc.loc[:, "typeId"] == "900000000000003001")
                    & (desc.loc[:, "active"] == "1")
                    & (desc.loc[:, "conceptId"].isin(concept.loc[:, "id"]))]

    # Supprimer les colonnes 'active' et 'typeId' qui ne sont plus nécessaires
    desc = desc.drop(["active", "typeId"], axis=1)

    # Extraire les suffixes sémantiques des FSN
    desc.loc[:, "semtag"] = [
        SEMTAG[c.split("(")[-1].rstrip(")")] for c in desc.loc[:, "fsn"]
    ]

    return desc


def read_common_french(cf_path: str, cf_date: str, fr_path: str,
                       fr_date: str) -> pd.DataFrame:
    """Lecture de la dernière release de la Common French.

    args:
        cf_path: Chemin vers le dossier Snapshot de la Common French
        cf_date: Date de release de la Common French
        fr_path: Chemin vers le dossier Snapshot de l'édition nationale
        fr_date: Date de release de l'édition nationale

    returns:
        DataFrame contenant les informations de descriptions
    """
    # Vérification du dossier donné en paramètre
    if op.basename(op.normpath(cf_path)) != "Snapshot":
        ValueError("Le chemin ne pointe pas vers le dossier Snapshot")

    # Lecture des descriptions de la Common French
    path = op.join(cf_path, f"Terminology/sct2_Description_Snapshot_CommonFrench-Extension_{cf_date}.txt")
    desc = pd.read_csv(path, sep="\t", quoting=3, encoding="UTF-8",
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
    path = op.join(cf_path, f"Refset/Language/der2_cRefset_LanguageSnapshot_CommonFrench-Extension_{cf_date}.txt")
    lang = pd.read_csv(path, sep="\t", encoding="UTF-8", dtype={"referencedComponentId": str},
                       usecols=["referencedComponentId", "acceptabilityId"],
                       converters={"acceptabilityId": lambda x: ACCEPT.get(x)})

    # Ajouter l'acceptabilité au DataFrame des descriptions
    desc = pd.merge(desc, lang, how="left", left_on="id", right_on="referencedComponentId")
    # Supprimer la colonne 'referencedComponentId' qui n'est plus nécessaire
    desc = desc.drop(["referencedComponentId"], axis=1)

    # Récupérer les FSN et les suffixes sémantiques
    fsn_semtag = _get_fsn_semtag(fr_path, fr_date)
    desc = pd.merge(desc, fsn_semtag, how="left", on="conceptId")

    # Retirer les traductions des hiérarchies
    # 'Environment or geographical location' et 'Organism'
    desc = desc.loc[(desc.loc[:, "semtag"] != "environment")
                    & (desc.loc[:, "semtag"] != "organism")]
    # Retirer les concepts absents de `fsn_semtag`
    desc = desc.loc[~desc.loc[:, "fsn"].isnull()]

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
    cf.columns = ["Concept ID", "Translated Term", "Case significance", "Acceptability"]
    cf.insert(2, "Language Code", ["fr"] * len(cf))
    cf.insert(4, "Type", ["SYNONYM"] * len(cf))
    cf.insert(5, "Language reference set", ["French"] * len(cf))
    cf.to_csv(path, sep="\t", index=False, encoding="UTF-8")
