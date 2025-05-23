import pandas as pd
from collections import defaultdict

RULES = defaultdict(list)


def _get_correct_case(cf_cs: pd.DataFrame) -> pd.DataFrame:
    """Corrige les descriptions labelisée 'CS' en 'cI'.

    args:
        cf_cs: Descriptions de la Common French labelisée comme 'CS'.

    returns:
        DataFrame avec les identifiants de descriptions comme index et
        la correction de casse comme valeur.
    """
    # Récupérer toutes les descriptions dont le premier mot contient une majuscule
    # et qui sont labelisées 'CS'
    upper = cf_cs.loc[[any(w.isupper() for w in word)
                       for word in cf_cs.loc[:, "term"].apply(lambda x: x.split()[0])]]
    incorrect_case = cf_cs.loc[~cf_cs.loc[:, "id"].isin(upper.loc[:, "id"])]
    return pd.DataFrame(data={"caseSignificanceId": ["cI"] * len(incorrect_case)},
                        index=incorrect_case.loc[:, "id"])


#####################
# Règles génériques #
#####################
def _check_ar2(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle ar2.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle ar2.
    """
    id = cf.loc[cf.loc[:, "term"].str.contains("^(?:les?|la|une?) ", case=False), "id"]
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "ar2": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_ar6(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle ar6.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle ar6.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "physical object")
                & (cf.loc[:, "term"].str.contains(" (?:les?|la|une?|d'une?) ", case=False)),
                "id"]
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "ar6": ["1"] * len(id)}),
                                        how="left", on="id")


#########################
# Règles Body structure #
#########################
def _check_bs2(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs2.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs2.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "body structure")
                & (cf.loc[:, "fsn"].str.contains("joint", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("(?:articulation|articulaire)", case=False)),
                "id"]
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "bs2": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_bs3(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs3.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs3.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "body structure")
                & (cf.loc[:, "acceptabilityId"] == "PREFERRED")
                & (cf.loc[:, "fsn"].str.contains("structure", regex=False, case=False))
                & (cf.loc[:, "term"].str.contains("structure", regex=False, case=False)),
                "id"]

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "body structure")
                               & (cf.loc[:, "acceptabilityId"] == "ACCEPTABLE")
                               & (cf.loc[:, "fsn"].str.contains("structure", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("structure", regex=False, case=False)),
                               "id"]])

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "body structure")
                               & (cf.loc[:, "fsn"].str.contains("entire", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("(?:entiers?|entières?)", case=False)),
                               "id"]])

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "body structure")
                               & (cf.loc[:, "fsn"].str.contains("part", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("partie", regex=False, case=False)),
                               "id"]])
    id = id.drop_duplicates()
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "bs3": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_bs5(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs5.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs5.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "body structure")
                & (cf.loc[:, "fsn"].str.contains("region", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("région", regex=False, case=False)),
                "id"]
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "bs5": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_bs6(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs6.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs6.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "body structure")
                & (cf.loc[:, "fsn"].str.contains("zone", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("zone", regex=False, case=False)),
                "id"]

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "body structure")
                               & (cf.loc[:, "fsn"].str.contains("area", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("(?:zone|surface|aire)", case=False)),
                               "id"]])
    id = id.drop_duplicates()
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "bs6": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_bs7(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs7.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs7.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "body structure")
                & (cf.loc[:, "fsn"].str.contains("proper", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("(?:propre|proprement dite?)", case=False)),
                "id"]
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "bs7": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_bs8(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs8.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs8.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "body structure")
                & (cf.loc[:, "acceptabilityId"] == "PREFERRED")
                & (cf.loc[:, "fsn"].str.contains("apex", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("apex", regex=False, case=False)),
                "id"]

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "body structure")
                               & (cf.loc[:, "acceptabilityId"] == "ACCEPTABLE")
                               & (cf.loc[:, "fsn"].str.contains("apex", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("(?:pointe|bout|cime)", case=False)),
                               "id"]])
    id = id.drop_duplicates()
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "bs8": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_bs9(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs9.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs9.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "body structure")
                & (cf.loc[:, "fsn"].str.contains("lesser toe", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("orteil excepté l'hallux", regex=False, case=False)),
                "id"]

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "body structure")
                               & (cf.loc[:, "fsn"].str.contains("lesser toe", regex=False, case=False))
                               & (cf.loc[:, "term"].str.contains("petit orteil", case=False)),
                               "id"]])
    id = id.drop_duplicates()
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "bs9": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_bs10(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs10.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs10.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "body structure")
                & (cf.loc[:, "fsn"].str.contains("lower limb", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("membre inférieur", regex=False, case=False)),
                "id"]
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "bs10": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_bs11(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs11-FR.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs11-FR.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "body structure")
                & (cf.loc[:, "acceptabilityId"] == "PREFERRED")
                & (cf.loc[:, "fsn"].str.contains("lower leg", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("partie basse d'une jambe", regex=False, case=False)),
                "id"]

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "body structure")
                               & (cf.loc[:, "acceptabilityId"] == "ACCEPTABLE")
                               & (cf.loc[:, "fsn"].str.contains("lower leg", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("(?:partie inférieure d'une jambe|jambe, du genou à la cheville)", case=False)),
                               "id"]])
    id = id.drop_duplicates()
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "bs11": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_bs12(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs12.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs12.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "body structure")
                & (cf.loc[:, "fsn"].str.contains("cerebrum", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("cerveau", regex=False, case=False)),
                "id"]
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "bs12": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_bs13(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs13.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs13.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "body structure")
                & (cf.loc[:, "fsn"].str.contains("brain", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("encéphale", regex=False, case=False)),
                "id"]
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "bs13": ["1"] * len(id)}),
                                        how="left", on="id")


###########################
# Règles Clinical finding #
###########################
def _check_co2(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle co2.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle co2.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "clinical finding")
                & (cf.loc[:, "fsn"].str.contains(" finding", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("constatation", regex=False, case=False)),
                "id"]
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "co2": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_co6(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle co6-FR.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle co6-FR.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "clinical finding")
                & (cf.loc[:, "fsn"].str.contains("above reference range", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("supérieure? (?:à l'intervalle|aux valeurs) de référence", case=False)),
                "id"]

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "clinical finding")
                               & (cf.loc[:, "fsn"].str.contains("below reference range", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("inférieure? (?:à l'intervalle|aux valeurs) de référence", case=False)),
                               "id"]])
    id = id.drop_duplicates()
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "co6": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_pa4(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pa4.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pa4.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "clinical finding")
                & (cf.loc[:, "fsn"].str.contains("epilepsy", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("épilepsie", regex=False, case=False)),
                "id"]

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "clinical finding")
                               & (cf.loc[:, "fsn"].str.contains("seizure", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("(?:crise|convulsion)", case=False)),
                               "id"]])

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "clinical finding")
                               & (cf.loc[:, "fsn"].str.contains("convulsion", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("convulsion", regex=False, case=False)),
                               "id"]])
    id = id.drop_duplicates()
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "pa4": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_pa6(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pa6.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pa6.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "clinical finding")
                & (cf.loc[:, "fsn"].str.contains("impairment", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("atteinte", regex=False, case=False)),
                "id"]
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "pa6": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_pa7(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pa7.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pa7.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "clinical finding")
                & (cf.loc[:, "fsn"].str.contains("primary", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("(?:primitif|primaire)", case=False)),
                "id"]
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "pa7": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_pa8(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pa8.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pa8.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "clinical finding")
                & (cf.loc[:, "fsn"].str.contains("chilblain", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("engelure", regex=False, case=False)),
                "id"]

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "clinical finding")
                               & (cf.loc[:, "fsn"].str.contains("(?<!superficial) frostbite", case=False))
                               & (~cf.loc[:, "term"].str.contains("(?:^| )gelure", case=False)),
                               "id"]])

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "clinical finding")
                               & (cf.loc[:, "fsn"].str.contains("superficial frostbite", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("(?:^| )gelure superficielle", case=False)),
                               "id"]])
    id = id.drop_duplicates()
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "pa8": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_pa9(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pa9.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pa9.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "clinical finding")
                & (cf.loc[:, "fsn"].str.contains("carbuncle", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("anthrax", regex=False, case=False)),
                "id"]

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "clinical finding")
                               & (cf.loc[:, "fsn"].str.contains("(?:furuncle|boil)", case=False))
                               & (~cf.loc[:, "term"].str.contains("(?:furoncle|folliculite nécrotique|clou)", case=False)),
                               "id"]])

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "clinical finding")
                               & (cf.loc[:, "fsn"].str.contains("anthrax", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("maladie du charbon", regex=False, case=False)),
                               "id"]])
    id = id.drop_duplicates()
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "pa9": ["1"] * len(id)}),
                                        how="left", on="id")


##############################################
# Règles Pharmaceutical / biological product #
##############################################
def _check_me1(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle me1.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle me1.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "pharmaceutical")
                & (cf.loc[:, "fsn"].str.contains("product containing (?!only)", case=False))
                & (~cf.loc[:, "term"].str.contains("produit contenant (?!uniquement)", case=False)),
                "id"]
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "me1": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_me2(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle me2.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle me2.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "pharmaceutical")
                & (cf.loc[:, "fsn"].str.contains("product containing only", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("produit contenant uniquement", regex=False, case=False)),
                "id"]
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "me2": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_me3(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle me3.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle me3.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "pharmaceutical")
                & (cf.loc[:, "fsn"].str.endswith("(clinical drug)"))
                & (~cf.loc[:, "term"].str.contains("produit contenant précisément", regex=False, case=False)),
                "id"]
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "me3": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_me4(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle me4.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle me4.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "pharmaceutical")
                & (cf.loc[:, "term"].str.contains("libération conventionnelle", regex=False, case=False)),
                "id"]
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "me4": ["1"] * len(id)}),
                                        how="left", on="id")


##########################
# Règles Physical object #
##########################
def _check_sb1(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle sb1.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle sb1.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "physical object")
                & (cf.loc[:, "fsn"].str.contains(r"evacuated [\w\s]+ collection tube", case=False))
                & (~cf.loc[:, "term"].str.contains(r"tube sous vide [\w\s]+ pour prélèvement", case=False)),
                "id"]
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "sb1": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_sb2(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle sb2.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle sb2.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "physical object")
                & (cf.loc[:, "fsn"].str.contains(r"evacuated [\w\s]+ specimen container", case=False))
                & (~cf.loc[:, "term"].str.contains(r"support sous vide [\w\s]+ pour prélèvement", case=False)),
                "id"]
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "sb2": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_sb3(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle sb3.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle sb3.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "physical object")
                & (cf.loc[:, "acceptabilityId"] == "PREFERRED")
                & (cf.loc[:, "fsn"].str.contains("stent", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("endoprothèse", regex=False, case=False)),
                "id"]

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "physical object")
                               & (cf.loc[:, "acceptabilityId"] == "ACCEPTABLE")
                               & (cf.loc[:, "fsn"].str.contains("stent", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("stent", regex=False, case=False)),
                               "id"]])
    id = id.drop_duplicates()
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "sb3": ["1"] * len(id)}),
                                        how="left", on="id")


####################
# Règles Procedure #
####################
def _check_pr2(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr2.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pr2.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "procedure")
                & (cf.loc[:, "acceptabilityId"] == "PREFERRED")
                & (cf.loc[:, "fsn"].str.contains(" procedure", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("(?:procédure|intervention chirurgicale)", case=False)),
                "id"]

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "procedure")
                               & (cf.loc[:, "acceptabilityId"] == "PREFERRED")
                               & (cf.loc[:, "fsn"].str.contains("operation", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("intervention chirurgicale", regex=False, case=False)),
                               "id"]])

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "procedure")
                               & (cf.loc[:, "acceptabilityId"] == "ACCEPTABLE")
                               & (cf.loc[:, "fsn"].str.contains(" procedure", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("(?:intervention|opération|chirurgie)", case=False)),
                               "id"]])

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "procedure")
                               & (cf.loc[:, "acceptabilityId"] == "ACCEPTABLE")
                               & (cf.loc[:, "fsn"].str.contains("operation", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("(?:opération|chirurgie)", case=False)),
                               "id"]])
    id = id.drop_duplicates()
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "pr2": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_pr3(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr3.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pr3.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "procedure")
                & (cf.loc[:, "fsn"].str.contains("consultation", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("consultation", regex=False, case=False)),
                "id"]
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "pr3": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_pr4(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr4.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pr4.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "procedure")
                & (cf.loc[:, "fsn"].str.contains("removal of foreign body", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("retrait d'un corps étranger", regex=False, case=False)),
                "id"]

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "procedure")
                               & (cf.loc[:, "acceptabilityId"] == "PREFERRED")
                               & (cf.loc[:, "fsn"].str.contains("magnet extraction", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("extraction avec un aimant", regex=False, case=False)),
                               "id"]])

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "procedure")
                               & (cf.loc[:, "acceptabilityId"] == "ACCEPTABLE")
                               & (cf.loc[:, "fsn"].str.contains("magnet extraction", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains(r"retrait d'un corps étranger [\w\s]+ à l'aide d'un aimant", case=False)),
                               "id"]])
    id = id.drop_duplicates()
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "pr4": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_pr9(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr9.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pr9.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "procedure")
                & (cf.loc[:, "acceptabilityId"] == "PREFERRED")
                & (cf.loc[:, "fsn"].str.contains("excisional biopsy", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("biopsie-exérèse", regex=False, case=False)),
                "id"]

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "procedure")
                               & (cf.loc[:, "acceptabilityId"] == "ACCEPTABLE")
                               & (cf.loc[:, "fsn"].str.contains("excisional biopsy", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("biopsie excisionnelle", regex=False, case=False)),
                               "id"]])
    id = id.drop_duplicates()
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "pr9": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_pr10(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr10.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pr10.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "procedure")
                & (cf.loc[:, "fsn"].str.contains("incisional biopsy", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("biopsie incisionnelle", regex=False, case=False)),
                "id"]
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "pr10": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_pr12(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr12.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pr12.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "procedure")
                & (cf.loc[:, "acceptabilityId"] == "PREFERRED")
                & (cf.loc[:, "fsn"].str.contains("MRI", regex=False))
                & (~cf.loc[:, "term"].str.contains("IRM", regex=False, case=False)),
                "id"]

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "procedure")
                               & (cf.loc[:, "acceptabilityId"] == "ACCEPTABLE")
                               & (cf.loc[:, "fsn"].str.contains("MRI", regex=False))
                               & (~cf.loc[:, "term"].str.contains("imagerie par résonance magnétique", regex=False, case=False)),
                               "id"]])

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "procedure")
                               & (cf.loc[:, "acceptabilityId"] == "PREFERRED")
                               & (cf.loc[:, "fsn"].str.contains("magnetic resonance angiography", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("angiographie par IRM", regex=False, case=False)),
                               "id"]])

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "procedure")
                               & (cf.loc[:, "acceptabilityId"] == "ACCEPTABLE")
                               & (cf.loc[:, "fsn"].str.contains("magnetic resonance angiography", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("angiographie par imagerie par résonance magnétique", regex=False, case=False)),
                               "id"]])
    id = id.drop_duplicates()
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "pr12": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_pr13(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr13.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pr13.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "procedure")
                & (cf.loc[:, "acceptabilityId"] == "PREFERRED")
                & (cf.loc[:, "fsn"].str.contains("guided", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("guidée? par", case=False)),
                "id"]

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "procedure")
                               & (cf.loc[:, "acceptabilityId"] == "ACCEPTABLE")
                               & (cf.loc[:, "fsn"].str.contains("guided", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("sous guidage", regex=False, case=False)),
                               "id"]])
    id = id.drop_duplicates()
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "pr13": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_pr14(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr14.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pr14.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "procedure")
                & (cf.loc[:, "acceptabilityId"] == "PREFERRED")
                & (cf.loc[:, "fsn"].str.contains(r"(?:fluoroscopy|fluoroscopic)(?![\w\s]*guided)", case=False))
                & (~cf.loc[:, "term"].str.contains("radioscopie", case=False)),
                "id"]

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "procedure")
                               & (cf.loc[:, "acceptabilityId"] == "ACCEPTABLE")
                               & (cf.loc[:, "fsn"].str.contains(r"(?:fluoroscopy|fluoroscopic)(?![\w\s]*guided)", case=False))
                               & (~cf.loc[:, "term"].str.contains("fluoroscopie", regex=False, case=False)),
                               "id"]])

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "procedure")
                               & (cf.loc[:, "acceptabilityId"] == "PREFERRED")
                               & (cf.loc[:, "fsn"].str.contains(r"(?:fluoroscopy|fluoroscopic)[\w\s]*guided", case=False))
                               & (~cf.loc[:, "term"].str.contains("guidée? par radioscopie", case=False)),
                               "id"]])

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "procedure")
                               & (cf.loc[:, "acceptabilityId"] == "ACCEPTABLE")
                               & (cf.loc[:, "fsn"].str.contains(r"(?:fluoroscopy|fluoroscopic)[\w\s]*guided", case=False))
                               & (~cf.loc[:, "term"].str.contains("(?:sous guidage radioscopique|guidée? par fluoroscopie)", case=False)),
                               "id"]])
    id = id.drop_duplicates()
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "pr14": ["1"] * len(id)}),
                                        how="left", on="id")


###################
# Règles Specimen #
###################
def _check_ec2(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle ec2.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle ec2.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "specimen")
                & (cf.loc[:, "fsn"].str.contains("submitted as specimen", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("présentée? comme échantillon", case=False)),
                "id"]

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "specimen")
                               & (cf.loc[:, "fsn"].str.contains("washings", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("liquide de lavage", regex=False, case=False)),
                               "id"]])

    id = pd.concat([id, cf.loc[(cf.loc[:, "semtag"] == "specimen")
                               & (cf.loc[:, "fsn"].str.contains("cytologic material", regex=False, case=False))
                               & (~cf.loc[:, "term"].str.contains("matériel cytologique", regex=False, case=False)),
                               "id"]])
    id = id.drop_duplicates()
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "ec2": ["1"] * len(id)}),
                                        how="left", on="id")


def _check_ec4(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle ec4.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle ec4.
    """
    id = cf.loc[(cf.loc[:, "semtag"] == "specimen")
                & (cf.loc[:, "fsn"].str.contains("fluid sample", regex=False, case=False))
                & (~cf.loc[:, "term"].str.contains("échantillon de liquide", regex=False, case=False)),
                "id"]
    return cf if id.empty else pd.merge(cf, pd.DataFrame(data={"id": id, "ec4": ["1"] * len(id)}),
                                        how="left", on="id")


def run_quality_control(cf: pd.DataFrame) -> pd.DataFrame:
    """Lance l'ensemble des contrôles qualité et correction automatiques sur les traduction à
    importer.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame avec les traductions à importer prête pour la relecture.
    """
    # Correction sur les casses
    correction = _get_correct_case(
        cf.loc[cf.loc[:, "caseSignificanceId"] == "CS"])
    cf = cf.set_index("id")
    cf.update(correction)
    cf = cf.reset_index()

    # Contrôles des règles sur les articles
    cf = _check_ar2(cf)
    cf = _check_ar6(cf)

    # Contrôles des règles de Body Structure
    if not cf.loc[cf.loc[:, "semtag"] == "body structure"].empty:
        cf = _check_bs2(cf)
        cf = _check_bs3(cf)
        cf = _check_bs5(cf)
        cf = _check_bs6(cf)
        cf = _check_bs7(cf)
        cf = _check_bs8(cf)
        cf = _check_bs9(cf)
        cf = _check_bs10(cf)
        cf = _check_bs11(cf)
        cf = _check_bs12(cf)
        cf = _check_bs13(cf)

    # Contrôles des règles de Clinical finding
    if not cf.loc[cf.loc[:, "semtag"] == "clinical finding"].empty:
        cf = _check_co2(cf)
        cf = _check_co6(cf)
        cf = _check_pa4(cf)
        cf = _check_pa6(cf)
        cf = _check_pa7(cf)
        cf = _check_pa8(cf)
        cf = _check_pa9(cf)

    # Contrôles des règles de Pharmaceutical / biological product
    if not cf.loc[cf.loc[:, "semtag"] == "pharmaceutical"].empty:
        cf = _check_me1(cf)
        cf = _check_me2(cf)
        cf = _check_me3(cf)
        cf = _check_me4(cf)

    # Contrôles des règles de Physical object
    if not cf.loc[cf.loc[:, "semtag"] == "physical object"].empty:
        cf = _check_sb1(cf)
        cf = _check_sb2(cf)
        cf = _check_sb3(cf)

    # Contrôles des règles de Procedure
    if not cf.loc[cf.loc[:, "semtag"] == "procedure"].empty:
        cf = _check_pr2(cf)
        cf = _check_pr3(cf)
        cf = _check_pr4(cf)
        cf = _check_pr9(cf)
        cf = _check_pr10(cf)
        cf = _check_pr12(cf)
        cf = _check_pr13(cf)
        cf = _check_pr14(cf)

    # Contrôles des règles de Specimen
    if not cf.loc[cf.loc[:, "semtag"] == "specimen"].empty:
        cf = _check_ec2(cf)
        cf = _check_ec4(cf)

    return cf
