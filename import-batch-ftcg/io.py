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
    """Récupérer le FSN EN et le suffixe sémantique pour les concepts traduits dans l'édition nationale.

    args:
        fr_path: Chemin vers le dossier Snapshot de l'édition nationale
        fr_date: Date de release de l'édition nationale
    
    returns:
        DataFrame représentant pour chaque SCTID son FSN et son suffixe sémantique.
    """
    # Lecture des descriptions EN
    en_desc_path = op.join(fr_path, f"Terminology/sct2_Description_Snapshot-en_FR1000315_{fr_date}.txt")
    en_description = pd.read_csv(en_desc_path, sep="\t", dtype=str, usecols=["active", "conceptId", "typeId", "term"], quoting=3)
    en_description.columns = ["active", "conceptId", "typeId", "fsn"]
    
    # Lecture des concepts de l'édition nationale
    en_concept_path = op.join(fr_path, f"Terminology/sct2_Concept_Snapshot_FR1000315_{fr_date}.txt")
    en_concept = pd.read_csv(en_concept_path, sep="\t", dtype=str, usecols=["id", "active"])
    en_concept = en_concept.loc[en_concept.loc[:, "active"] == "1"]

    # Conserver seulement les FSN actifs
    en_description = en_description.loc[
        (en_description.loc[:, "typeId"] == "900000000000003001")
        & (en_description.loc[:, "active"] == "1")
        & (en_description.loc[:, "conceptId"].isin(en_concept.loc[:, "id"]))
    ]
    
    # Supprimer les colonnes 'active' et 'typeId' qui ne sont plus nécessaires
    en_description = en_description.drop(["active", "typeId"], axis=1)

    # Déduire les suffixes sémantiques des FSN
    en_description.loc[:, "semtag"] = [SEMTAG[c.split("(")[-1].rstrip(")")] for c in en_description.loc[:, "fsn"]]

    return en_description


def read_common_french(cf_path: str, cf_date: str, fr_path: str, fr_date: str) -> pd.DataFrame:
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
        ValueError("Le chemin vers la Common French ne pointe pas vers le dossier Snapshot")
        
    # Lecture des descriptions
    cf_desc_path = op.join(cf_path, f"Terminology/sct2_Description_Snapshot_CommonFrench-Extension_{cf_date}.txt")
    cf_description = pd.read_csv(cf_desc_path, sep="\t", dtype={"id": str, "active": pd.CategoricalDtype(["1", "0"]), "conceptId": str, "typeId": str, "term": str},
                                 usecols=["id", "active", "conceptId", "typeId", "term", "caseSignificanceId"], quoting=3,
                                 converters={"caseSignificanceId": lambda x: CASE.get(x)}, encoding="UTF-8")
    
    # Conserver seulement les synonymes actifs
    cf_description = cf_description.loc[(cf_description.loc[:, "typeId"] == "900000000000013009") & (cf_description.loc[:, "active"] == "1")]
    # Supprimer les colonnes 'active' et 'typeId' qui ne sont plus nécessaires
    cf_description = cf_description.drop(["active", "typeId"], axis=1)

    # Lecture du refset de langue
    cf_lang_path = op.join(cf_path, f"Refset/Language/der2_cRefset_LanguageSnapshot_CommonFrench-Extension_{cf_date}.txt")
    cf_language = pd.read_csv(cf_lang_path, sep="\t", dtype={"referencedComponentId": str}, usecols=["referencedComponentId", "acceptabilityId"], 
                              converters={"acceptabilityId": lambda x: ACCEPT.get(x)}, encoding="UTF-8")
        
    # Ajouter l'acceptabilité au DataFrame des descriptions
    cf_description = pd.merge(cf_description, cf_language, how="left", left_on="id", right_on="referencedComponentId")
    # Supprimer la colonne 'referencedComponentId' qui n'est plus nécessaire
    cf_description = cf_description.drop(["referencedComponentId"], axis=1)

    # Récupérer les FSN et les suffixes sémantiques
    fsn_semtag = _get_fsn_semtag(fr_path, fr_date)
    cf_description = pd.merge(cf_description, fsn_semtag, how="left", on="conceptId")

    # Retirer les traductions des hiérarchies 'Environment or geographical location' et 'Organism'
    cf_description = cf_description.loc[(cf_description.loc[:, "semtag"] != "environment") & (cf_description.loc[:, "semtag"] != "organism")]
    # Retirer les concepts absents de `fsn_semtag`
    cf_description = cf_description.loc[~cf_description.loc[:, "fsn"].isnull()]

    return cf_description


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
    fr_desc_path = op.join(fr_path, f"Terminology/sct2_Description_Snapshot-fr_FR1000315_{fr_date}.txt")
    fr_description = pd.read_csv(fr_desc_path, sep="\t", dtype={"id": str, "active": pd.CategoricalDtype(["1", "0"]), "conceptId": str, "typeId": str, "term": str},
                                 usecols=["id", "active", "conceptId", "typeId", "term", "caseSignificanceId"], quoting=3,
                                 converters={"caseSignificanceId": lambda x: CASE.get(x)}, encoding="UTF-8")
    # Conserver seulement les synonymes
    fr_description = fr_description.loc[fr_description.loc[:, "typeId"] == "900000000000013009"]
    # Supprimer la colonne 'typeId' qui n'est plus nécessaire
    fr_description = fr_description.drop(["typeId"], axis=1)
    
    # Lecture du refset de langue
    fr_lang_path = op.join(fr_path, f"Refset/Language/der2_cRefset_LanguageSnapshot-fr_FR1000315_{fr_date}.txt")
    fr_language = pd.read_csv(fr_lang_path, sep="\t", dtype={"referencedComponentId": str}, usecols=["referencedComponentId", "acceptabilityId"], 
                              converters={"acceptabilityId": lambda x: ACCEPT.get(x)}, encoding="UTF-8")
    
    # Ajouter l'acceptabilité au DataFrame des descriptions
    fr_description = pd.merge(fr_description, fr_language, how="left", left_on="id", right_on="referencedComponentId")
    # Supprimer la colonne 'referencedComponentId' qui n'est plus nécessaire
    fr_description = fr_description.drop(["referencedComponentId"], axis=1)

    return fr_description


def _read_unpublished_fr_edition(unpub_fr_path: str) -> pd.DataFrame:
    """Lecture des modifications de l'édition nationale depuis la dernière relase.
    
    args:
        unpub_fr_path: Chemin vers le fichier extrait du rapport "New and change components" de SNOMED Int.
    
    returns:
        DataFrame contenant les informations de modifications
    """
    if not op.isfile(unpub_fr_path) or not op.exists(unpub_fr_path):
        ValueError("Le fichier des modifications non-publiées de l'édition nationale est invalide.")

    # Lecture du fichier concepts
    unpublished = pd.read_csv(unpub_fr_path, sep=";", dtype={"Id": str, " Description": str, " LangRefset": str, " isChanged": str},
                                 usecols=["Id", " Description", " LangRefset", " isChanged", " wasInactivated"], quoting=3,
                                 converters={" wasInactivated": lambda x: ACTIVE.get(x)}, encoding="UTF-8")
    # Renommer les colonnes du fichier
    unpublished.columns = ["conceptId", "description", "language", "isChanged", "active"]

    # Extraire les SCTID de descriptions
    unpublished.insert(0, "id", [d.split(" ")[0].lstrip("*") for d in unpublished.loc[:, "description"]])
    # Extraire les descriptions
    unpublished.insert(2, "term", [" ".join(d.split(" ")[3:-1]) for d in unpublished.loc[:, "description"]])    
    # Extraire les valeurs de casses
    unpublished.insert(3, "caseSignificanceId", [d.split(" ")[-1][1:3] for d in unpublished.loc[:, "description"]])
    # Extraire l'acceptabilité
    unpublished.insert(4, "acceptabilityId", ["PREFERRED" if "PREFERRED" in l else "ACCEPTABLE" for l in unpublished.loc[:, "language"]])
    # Supprimer les colonnes 'description' et 'language' qui ne sont plus nécessaires
    unpublished = unpublished.drop(["description", "language"], axis=1)

    return unpublished


def get_fr_edition(fr_path: str, fr_date: str, unpub_fr_path: str) -> pd.DataFrame:
    """Regroupement de la dernière release publiée de l'édition nationale et de l'état actuel des modifications.
    
    args:
        fr_path: Chemin vers le dossier Snapshot de l'édition nationale
        fr_date: Date de release de l'édition nationale
        unpub_fr_path: Chemin vers le fichier extrait du rapport "New and change components" de SNOMED Int.

    returns:
        DataFrame contenant les informations de description à jour
    """
    # Lecture des fichiers
    published = _read_published_fr_edition(fr_path, fr_date)
    unpublished = _read_unpublished_fr_edition(unpub_fr_path)

    # Division des modifications non publiées
    new = unpublished.loc[(unpublished.loc[:, "isChanged"] == "N") & (unpublished.loc[:, "active"] == "1")]
    new = new.drop(["isChanged"], axis=1)
    changed = unpublished.loc[unpublished.loc[:, "isChanged"] == "Y"]
    changed = changed.drop(["conceptId", "term", "isChanged", "active"], axis=1)
    changed = changed.set_index("id")
    inactive = unpublished.loc[(unpublished.loc[:, "isChanged"] == "N") & (unpublished.loc[:, "active"] == "0")]
    inactive = inactive.drop(["conceptId", "term", "caseSignificanceId", "acceptabilityId", "isChanged"], axis=1)
    inactive = inactive.set_index("id")
    # Contrôle de perte
    if len(new) + len(changed) + len(inactive) != len(unpublished):
        Exception("Il existe d'autres modifications que ajout, modification & inactivation dans le fichier.")
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