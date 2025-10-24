import pandas as pd

from import_batch_ftcg import server


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
    sctid = cf.loc[cf.loc[:, "term"].str.contains("^(?:les?|la|une?) ", case=False), "id"] # noqa
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "ar2": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_ar6(cf: pd.DataFrame, sb: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle ar6.

    args:
        cf: Descriptions de la Common French à importer.
        sb: Filtre sur les Physical object de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle ar6.
    """
    sctid = cf.loc[sb
                   & (cf.loc[:, "term"].str.contains(" (?:les?|la|une?|d'une?) ", case=False)), # noqa
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "ar6": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


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
    sctid = cf.loc[(cf.loc[:, "fsn"].str.contains("joint", regex=False, case=False))
                   & (~cf.loc[:, "term"].str.contains("(?:articulation|articulaire)", case=False)), # noqa
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "bs2": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_bs3(cf: pd.DataFrame, bs: pd.Series, pt: pd.Series,
               syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs3.

    args:
        cf: Descriptions de la Common French à importer.
        bs: Filtre sur les Body structure de `cf`.
        pt: Filtre sur les termes préférés de `cf`.
        syn: Filtre sur les synonymes acceptables de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs3.
    """
    sctid = cf.loc[bs & pt
                   & (cf.loc[:, "fsn"].str.contains("structure", regex=False, case=False)) # noqa
                   & (cf.loc[:, "term"].str.contains("structure", regex=False, case=False)), # noqa
                   "id"]

    sctid = pd.concat([sctid, cf.loc[bs & syn
                                     & (cf.loc[:, "fsn"].str.contains("structure", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("structure", regex=False, case=False)), # noqa
                                     "id"]])

    sctid = pd.concat([sctid, cf.loc[bs
                                     & (cf.loc[:, "fsn"].str.contains("entire", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("(?:entiers?|entières?)", case=False)), # noqa
                                     "id"]])

    sctid = pd.concat([sctid, cf.loc[bs
                                     & (cf.loc[:, "fsn"].str.contains("part", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("partie", regex=False, case=False)), # noqa
                                     "id"]])
    sctid = sctid.drop_duplicates()
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "bs3": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_bs5(cf: pd.DataFrame, bs: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs5.

    args:
        cf: Descriptions de la Common French à importer.
        bs: Filtre sur les Body structure de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs5.
    """
    sctid = cf.loc[bs
                   & (cf.loc[:, "fsn"].str.contains("region", regex=False, case=False))
                   & (~cf.loc[:, "term"].str.contains("région", regex=False, case=False)), # noqa
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "bs5": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_bs6(cf: pd.DataFrame, bs: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs6.

    args:
        cf: Descriptions de la Common French à importer.
        bs: Filtre sur les Body structure de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs6.
    """
    sctid = cf.loc[bs
                   & (cf.loc[:, "fsn"].str.contains("zone", regex=False, case=False))
                   & (~cf.loc[:, "term"].str.contains("zone", regex=False, case=False)),
                   "id"]

    sctid = pd.concat([sctid, cf.loc[bs
                                     & (cf.loc[:, "fsn"].str.contains("area", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("(?:zone|surface|aire)", case=False)), # noqa
                                     "id"]])
    sctid = sctid.drop_duplicates()
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "bs6": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_bs7(cf: pd.DataFrame, bs: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs7.

    args:
        cf: Descriptions de la Common French à importer.
        bs: Filtre sur les Body structure de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs7.
    """
    sctid = cf.loc[bs
                   & (cf.loc[:, "fsn"].str.contains("proper", regex=False, case=False))
                   & (~cf.loc[:, "term"].str.contains("(?:propre|proprement dite?)", case=False)), # noqa
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "bs7": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_bs8(cf: pd.DataFrame, pt: pd.Series, syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs8.

    args:
        cf: Descriptions de la Common French à importer.
        pt: Filtre sur les termes préférés de `cf`.
        syn: Filtre sur les synonymes acceptables de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs8.
    """
    sctid = cf.loc[pt
                   & (cf.loc[:, "fsn"].str.contains("apex", regex=False, case=False))
                   & (~cf.loc[:, "term"].str.contains("apex", regex=False, case=False)),
                   "id"]

    sctid = pd.concat([sctid, cf.loc[syn
                                     & (cf.loc[:, "fsn"].str.contains("apex", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("(?:pointe|bout|cime)", case=False)), # noqa
                                     "id"]])
    sctid = sctid.drop_duplicates()
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "bs8": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_bs9(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs9.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs9.
    """
    sctid = cf.loc[(cf.loc[:, "fsn"].str.contains("lesser toe", regex=False, case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains("orteil excepté l'hallux", regex=False, case=False)), # noqa
                   "id"]

    sctid = pd.concat([sctid, cf.loc[(cf.loc[:, "fsn"].str.contains("lesser toe", regex=False, case=False)) # noqa
                                     & (cf.loc[:, "term"].str.contains("petit orteil", case=False)), # noqa
                                     "id"]])
    sctid = sctid.drop_duplicates()
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "bs9": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_bs10(cf: pd.DataFrame, pt: pd.Series, syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs10-FR.

    args:
        cf: Descriptions de la Common French à importer.
        pt: Filtre sur les termes préférés de `cf`.
        syn: Filtre sur les synonymes acceptables de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs10.
    """
    sctid = cf.loc[(cf.loc[:, "fsn"].str.contains("lower limb", regex=False, case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains("membre inférieur", regex=False, case=False)), # noqa
                   "id"]

    sctid = pd.concat([sctid, cf.loc[pt
                                     & (cf.loc[:, "fsn"].str.contains("lower leg", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("partie inférieure de la jambe", case=False)), # noqa
                                     "id"]])

    sctid = pd.concat([sctid, cf.loc[syn
                                     & (cf.loc[:, "fsn"].str.contains("lower leg", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("(?:partie basse de la jambe|jambe, du genou à la cheville)", case=False)), # noqa
                                     "id"]])
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "bs10": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_bs11(cf: pd.DataFrame, pt: pd.Series, syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs11-FR.

    args:
        cf: Descriptions de la Common French à importer.
        pt: Filtre sur les termes préférés de `cf`.
        syn: Filtre sur les synonymes acceptables de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs11-FR.
    """
    sctid = cf.loc[(cf.loc[:, "fsn"].str.contains("upper limb", regex=False, case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains("membre supérieur", regex=False, case=False)), # noqa
                   "id"]

    sctid = pd.concat([sctid, cf.loc[pt
                                     & (cf.loc[:, "fsn"].str.contains("upper arm", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("partie supérieure du bras", regex=False, case=False)), # noqa
                                     "id"]])

    sctid = pd.concat([sctid, cf.loc[syn
                                     & (cf.loc[:, "fsn"].str.contains("upper arm", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("bras, de l'épaule au coude", regex=False, case=False)), # noqa
                                     "id"]])
    sctid = sctid.drop_duplicates()
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "bs11": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_bs12(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs12.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs12.
    """
    sctid = cf.loc[(cf.loc[:, "fsn"].str.contains("cerebrum", regex=False, case=False))
                   & (~cf.loc[:, "term"].str.contains("cerveau", regex=False, case=False)), # noqa
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "bs12": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_bs13(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs13.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle bs13.
    """
    sctid = cf.loc[(cf.loc[:, "fsn"].str.contains("brain", regex=False, case=False))
                   & (~cf.loc[:, "term"].str.contains("encéphale", regex=False, case=False)), # noqa
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "bs13": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


###########################
# Règles Clinical finding #
###########################
def _check_co2(cf: pd.DataFrame, co: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle co2.

    args:
        cf: Descriptions de la Common French à importer.
        co: Filtre sur les Clinical finding de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle co2.
    """
    sctid = cf.loc[co
                   & (cf.loc[:, "fsn"].str.contains(" finding", regex=False, case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains("constatation", regex=False, case=False)), # noqa
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "co2": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_co6(cf: pd.DataFrame, co: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle co6-FR.

    args:
        cf: Descriptions de la Common French à importer.
        co: Filtre sur les Clinical finding de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle co6-FR.
    """
    sctid = cf.loc[co
                   & (cf.loc[:, "fsn"].str.contains("above reference range", regex=False, case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains("supérieure? (?:à l'intervalle|aux valeurs) de référence", case=False)), # noqa
                   "id"]

    sctid = pd.concat([sctid, cf.loc[co
                                     & (cf.loc[:, "fsn"].str.contains("below reference range", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("inférieure? (?:à l'intervalle|aux valeurs) de référence", case=False)), # noqa
                                     "id"]])

    sctid = pd.concat([sctid, cf.loc[co
                                     & (cf.loc[:, "fsn"].str.contains("within reference range", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("dans (?:l'intervalle|les valeurs) de référence", case=False)), # noqa
                                     "id"]])

    sctid = pd.concat([sctid, cf.loc[co
                                     & (cf.loc[:, "fsn"].str.contains("outside reference range", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("en dehors (?:de l'intervalle|des valeurs) de référence", case=False)), # noqa
                                     "id"]])
    sctid = sctid.drop_duplicates()
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "co6": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_pa3(cf: pd.DataFrame, fts: server.Fts) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pa3.

    args:
        cf: Descriptions de la Common French à importer.
        fts: Serveur de Terminologies FHIR contenant la version de l'édition
            internationale dont dépend votre édition nationale non publiée

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pa3.
    """
    skin_trauma = (cf.loc[:, "conceptId"].isin(fts.ecl("<< 417746004: 363698007 = << 39937001"))) # noqa
    trauma = (cf.loc[:, "conceptId"].isin(fts.ecl("<< 417746004: 363698007 != << 39937001"))) # noqa
    sctid = cf.loc[skin_trauma
                   & (cf.loc[:, "fsn"].str.contains("injury", regex=False, case=False))
                   & (~cf.loc[:, "fsn"].str.contains("(?:crush)", case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains("blessure", regex=False, case=False)), # noqa
                   "id"]

    sctid = pd.concat([sctid, cf.loc[trauma
                                     & (cf.loc[:, "fsn"].str.contains("injury", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "fsn"].str.contains("(?:crush)", case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("(?:traumatisme|lésion traumatique)", case=False)), # noqa
                                     "id"]])

    sctid = pd.concat([sctid, cf.loc[trauma
                                     & (cf.loc[:, "fsn"].str.contains("(?:crush(?:ing)? injury)", case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("écrasement", regex=False, case=False)), # noqa
                                     "id"]])
    sctid = sctid.drop_duplicates()
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "pa3": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_pa3_1(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pa3.1.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pa3.1.
    """
    sctid = cf.loc[(cf.loc[:, "fsn"].str.contains("pressure injury", regex=False, case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains("escarre", regex=False, case=False)), # noqa
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "pa3.1": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_pa4(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pa4.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pa4.
    """
    sctid = cf.loc[(cf.loc[:, "fsn"].str.contains("epilepsy", regex=False, case=False))
                   & (~cf.loc[:, "term"].str.contains("épilepsie", regex=False, case=False)), # noqa
                   "id"]

    sctid = pd.concat([sctid, cf.loc[(cf.loc[:, "fsn"].str.contains("seizure", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("(?:crise|convulsion)", case=False)), # noqa
                                     "id"]])

    sctid = pd.concat([sctid, cf.loc[(cf.loc[:, "fsn"].str.contains("convulsion", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("convulsion", regex=False, case=False)), # noqa
                                     "id"]])
    sctid = sctid.drop_duplicates()
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "pa4": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_pa6(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pa6.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pa6.
    """
    sctid = cf.loc[(cf.loc[:, "fsn"].str.contains("impairment", regex=False, case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains("atteinte", regex=False, case=False)), # noqa
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "pa6": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_pa7(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pa7.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pa7.
    """
    sctid = cf.loc[(cf.loc[:, "fsn"].str.contains("primary", regex=False, case=False))
                   & (~cf.loc[:, "term"].str.contains("(?:primitif|primaire)", case=False)), # noqa
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "pa7": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_pa8(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pa8.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pa8.
    """
    sctid = cf.loc[(cf.loc[:, "fsn"].str.contains("chilblain", regex=False, case=False))
                   & (~cf.loc[:, "term"].str.contains("engelure", regex=False, case=False)), # noqa
                   "id"]

    sctid = pd.concat([sctid, cf.loc[(cf.loc[:, "fsn"].str.contains("(?<!superficial) frostbite", case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("(?:^| )gelure", case=False)), # noqa
                                     "id"]])

    sctid = pd.concat([sctid, cf.loc[(cf.loc[:, "fsn"].str.contains("superficial frostbite", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("(?:^| )gelure superficielle", case=False)), # noqa
                                     "id"]])
    sctid = sctid.drop_duplicates()
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "pa8": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_pa9(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pa9.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pa9.
    """
    sctid = cf.loc[(cf.loc[:, "fsn"].str.contains("carbuncle", regex=False, case=False))
                   & (~cf.loc[:, "term"].str.contains("anthrax", regex=False, case=False)), # noqa
                   "id"]

    sctid = pd.concat([sctid, cf.loc[(cf.loc[:, "fsn"].str.contains("(?:furuncle|boil)", case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("(?:furoncle|folliculite nécrotique|clou)", case=False)), # noqa
                                     "id"]])

    sctid = pd.concat([sctid, cf.loc[(cf.loc[:, "fsn"].str.contains("anthrax", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("maladie du charbon", regex=False, case=False)), # noqa
                                     "id"]])
    sctid = sctid.drop_duplicates()
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "pa9": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


##############################################
# Règles Pharmaceutical / biological product #
##############################################
def _check_me1(cf: pd.DataFrame, me: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle me1.

    args:
        cf: Descriptions de la Common French à importer.
        me: Filtre sur les Pharmaceutical / biological product de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle me1.
    """
    sctid = cf.loc[me
                   & (cf.loc[:, "fsn"].str.contains("product containing (?!only)", case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains("produit contenant (?!uniquement)", case=False)), # noqa
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "me1": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_me2(cf: pd.DataFrame, me: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle me2.

    args:
        cf: Descriptions de la Common French à importer.
        me: Filtre sur les Pharmaceutical / biological product de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle me2.
    """
    sctid = cf.loc[me
                   & (cf.loc[:, "fsn"].str.contains("product containing only", regex=False, case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains("produit contenant uniquement", regex=False, case=False)), # noqa
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "me2": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_me3(cf: pd.DataFrame, me: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle me3.

    args:
        cf: Descriptions de la Common French à importer.
        me: Filtre sur les Pharmaceutical / biological product de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle me3.
    """
    sctid = cf.loc[me
                   & (cf.loc[:, "fsn"].str.endswith("(clinical drug)"))
                   & (~cf.loc[:, "term"].str.contains("produit contenant précisément", regex=False, case=False)), # noqa
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "me3": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_me4(cf: pd.DataFrame, me: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle me4.

    args:
        cf: Descriptions de la Common French à importer.
        me: Filtre sur les Pharmaceutical / biological product de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle me4.
    """
    sctid = cf.loc[me
                   & (cf.loc[:, "term"].str.contains("libération conventionnelle", regex=False, case=False)), # noqa
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "me4": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


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
    sctid = cf.loc[(cf.loc[:, "fsn"].str.contains(r"evacuated [\w\s]+ collection tube", case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains(r"tube sous vide [\w\s]+ pour prélèvement", case=False)), # noqa
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "sb1": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_sb2(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle sb2.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle sb2.
    """
    sctid = cf.loc[(cf.loc[:, "fsn"].str.contains(r"evacuated [\w\s]+ specimen container", case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains(r"support sous vide [\w\s]+ pour prélèvement", case=False)), # noqa
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "sb2": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_sb3(cf: pd.DataFrame, pt: pd.Series, syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle sb3.

    args:
        cf: Descriptions de la Common French à importer.
        pt: Filtre sur les termes préférés de `cf`.
        syn: Filtre sur les synonymes acceptables de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle sb3.
    """
    sctid = cf.loc[pt
                   & (cf.loc[:, "fsn"].str.contains("stent", regex=False, case=False))
                   & (~cf.loc[:, "term"].str.contains("endoprothèse", regex=False, case=False)), # noqa
                   "id"]

    sctid = pd.concat([sctid, cf.loc[syn
                                     & (cf.loc[:, "fsn"].str.contains("stent", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("stent", regex=False, case=False)), # noqa
                                     "id"]])
    sctid = sctid.drop_duplicates()
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "sb3": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


####################
# Règles Procedure #
####################
def _check_pr2(cf: pd.DataFrame, pt: pd.Series, syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr2.

    args:
        cf: Descriptions de la Common French à importer.
        pt: Filtre sur les termes préférés de `cf`.
        syn: Filtre sur les synonymes acceptables de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pr2.
    """
    sctid = cf.loc[pt
                   & (cf.loc[:, "fsn"].str.contains(" procedure", regex=False, case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains("(?:procédure|intervention chirurgicale)", case=False)), # noqa
                   "id"]

    sctid = pd.concat([sctid, cf.loc[pt
                                     & (cf.loc[:, "fsn"].str.contains("operation", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("intervention chirurgicale", regex=False, case=False)), # noqa
                                     "id"]])

    sctid = pd.concat([sctid, cf.loc[syn
                                     & (cf.loc[:, "fsn"].str.contains(" procedure", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("(?:intervention|opération|chirurgie)", case=False)), # noqa
                                     "id"]])

    sctid = pd.concat([sctid, cf.loc[syn
                                     & (cf.loc[:, "fsn"].str.contains("operation", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("(?:opération|chirurgie)", case=False)), # noqa
                                     "id"]])
    sctid = sctid.drop_duplicates()
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "pr2": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_pr3(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr3.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pr3.
    """
    sctid = cf.loc[(cf.loc[:, "fsn"].str.contains("consultation", regex=False, case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains("consultation", regex=False, case=False)), # noqa
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "pr3": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_pr4(cf: pd.DataFrame, pt: pd.Series, syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr4.

    args:
        cf: Descriptions de la Common French à importer.
        pt: Filtre sur les termes préférés de `cf`.
        syn: Filtre sur les synonymes acceptables de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pr4.
    """
    sctid = cf.loc[(cf.loc[:, "fsn"].str.contains("removal of foreign body", regex=False, case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains("retrait d'un corps étranger", regex=False, case=False)), # noqa
                   "id"]

    sctid = pd.concat([sctid, cf.loc[pt
                                     & (cf.loc[:, "fsn"].str.contains("magnet extraction", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("extraction avec un aimant", regex=False, case=False)), # noqa
                                     "id"]])

    sctid = pd.concat([sctid, cf.loc[syn
                                     & (cf.loc[:, "fsn"].str.contains("magnet extraction", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains(r"retrait d'un corps étranger [\w\s]+ à l'aide d'un aimant", case=False)), # noqa
                                     "id"]])
    sctid = sctid.drop_duplicates()
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "pr4": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_pr9(cf: pd.DataFrame, pt: pd.Series, syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr9.

    args:
        cf: Descriptions de la Common French à importer.
        pt: Filtre sur les termes préférés de `cf`.
        syn: Filtre sur les synonymes acceptables de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pr9.
    """
    sctid = cf.loc[pt
                   & (cf.loc[:, "fsn"].str.contains("excisional biopsy", regex=False, case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains("biopsie-exérèse", regex=False, case=False)), # noqa
                   "id"]

    sctid = pd.concat([sctid, cf.loc[syn
                                     & (cf.loc[:, "fsn"].str.contains("excisional biopsy", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("biopsie excisionnelle", regex=False, case=False)), # noqa
                                     "id"]])
    sctid = sctid.drop_duplicates()
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "pr9": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_pr10(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr10.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pr10.
    """
    sctid = cf.loc[(cf.loc[:, "fsn"].str.contains("incisional biopsy", regex=False, case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains("biopsie incisionnelle", regex=False, case=False)), # noqa
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "pr10": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_pr12(cf: pd.DataFrame, pt: pd.Series, syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr12.

    args:
        cf: Descriptions de la Common French à importer.
        pt: Filtre sur les termes préférés de `cf`.
        syn: Filtre sur les synonymes acceptables de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pr12.
    """
    sctid = cf.loc[pt
                   & (cf.loc[:, "fsn"].str.contains("MRI", regex=False))
                   & (~cf.loc[:, "term"].str.contains("IRM", regex=False, case=False)),
                   "id"]

    sctid = pd.concat([sctid, cf.loc[syn
                                     & (cf.loc[:, "fsn"].str.contains("MRI", regex=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("imagerie par résonance magnétique", regex=False, case=False)), # noqa
                                     "id"]])

    sctid = pd.concat([sctid, cf.loc[pt
                                     & (cf.loc[:, "fsn"].str.contains("magnetic resonance angiography", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("angiographie par IRM", regex=False, case=False)), # noqa
                                     "id"]])

    sctid = pd.concat([sctid, cf.loc[syn
                                     & (cf.loc[:, "fsn"].str.contains("magnetic resonance angiography", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("angiographie par imagerie par résonance magnétique", regex=False, case=False)), # noqa
                                     "id"]])
    sctid = sctid.drop_duplicates()
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "pr12": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_pr13(cf: pd.DataFrame, pt: pd.Series, syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr13.

    args:
        cf: Descriptions de la Common French à importer.
        pt: Filtre sur les termes préférés de `cf`.
        syn: Filtre sur les synonymes acceptables de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pr13.
    """
    sctid = cf.loc[pt
                   & (cf.loc[:, "fsn"].str.contains("guided", regex=False, case=False))
                   & (~cf.loc[:, "term"].str.contains("guidée? par", case=False)),
                   "id"]

    sctid = pd.concat([sctid, cf.loc[syn
                                     & (cf.loc[:, "fsn"].str.contains("guided", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("sous guidage", regex=False, case=False)), # noqa
                                     "id"]])
    sctid = sctid.drop_duplicates()
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "pr13": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_pr14(cf: pd.DataFrame, pt: pd.Series, syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr14.

    args:
        cf: Descriptions de la Common French à importer.
        pt: Filtre sur les termes préférés de `cf`.
        syn: Filtre sur les synonymes acceptables de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pr14.
    """
    sctid = cf.loc[pt
                   & (cf.loc[:, "fsn"].str.contains(r"(?:fluoroscopy|fluoroscopic)(?![\w\s]*guided)", case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains("radioscopie", case=False)),
                   "id"]

    sctid = pd.concat([sctid, cf.loc[syn
                                     & (cf.loc[:, "fsn"].str.contains(r"(?:fluoroscopy|fluoroscopic)(?![\w\s]*guided)", case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("fluoroscopie", regex=False, case=False)), # noqa
                                     "id"]])

    sctid = pd.concat([sctid, cf.loc[pt
                                     & (cf.loc[:, "fsn"].str.contains(r"(?:fluoroscopy|fluoroscopic)[\w\s]*guided", case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("guidée? par radioscopie", case=False)), # noqa
                                     "id"]])

    sctid = pd.concat([sctid, cf.loc[syn
                                     & (cf.loc[:, "fsn"].str.contains(r"(?:fluoroscopy|fluoroscopic)[\w\s]*guided", case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("(?:sous guidage radioscopique|guidée? par fluoroscopie)", case=False)), # noqa
                                     "id"]])
    sctid = sctid.drop_duplicates()
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "pr14": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_pr15(cf: pd.DataFrame, pr: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr15-FR.

    Args:
        cf: Descriptions de la Common French à importer.
        pr: Filtre sur les Procedure de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle pr15-FR.
    """
    sctid = cf.loc[pr
                   & (cf.loc[:, "fsn"].str.contains("education", regex=False, case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains("éducation", case=False)),
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "pr15": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


##########################################
# Règles Situation with explicit context #
##########################################
def _check_hs1(cf: pd.DataFrame, hs: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle hs1.

    args:
        cf: Descriptions de la Common French à importer.
        hs: Filtre sur les Situation with explicit context de `cf`.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle hs1.
    """
    sctid = cf.loc[hs
                   & (cf.loc[:, "fsn"].str.contains("history", regex=False, case=False))
                   & (~cf.loc[:, "term"].str.contains("antécédent(?!s)", case=False)), # noqa
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "hs1": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


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
    sctid = cf.loc[(cf.loc[:, "fsn"].str.contains("submitted as specimen", regex=False, case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains("présentée? comme échantillon", case=False)), # noqa
                   "id"]

    sctid = pd.concat([sctid, cf.loc[(cf.loc[:, "fsn"].str.contains("washings", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("liquide de lavage", regex=False, case=False)), # noqa
                                     "id"]])

    sctid = pd.concat([sctid, cf.loc[(cf.loc[:, "fsn"].str.contains("cytologic material", regex=False, case=False)) # noqa
                                     & (~cf.loc[:, "term"].str.contains("matériel cytologique", regex=False, case=False)), # noqa
                                     "id"]])
    sctid = sctid.drop_duplicates()
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "ec2": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def _check_ec4(cf: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle ec4.

    args:
        cf: Descriptions de la Common French à importer.

    returns:
        DataFrame de la Common French avec une colonne identifiant les
        descriptions ne respectant pas la règle ec4.
    """
    sctid = cf.loc[(cf.loc[:, "fsn"].str.contains("fluid sample", regex=False, case=False)) # noqa
                   & (~cf.loc[:, "term"].str.contains("échantillon de liquide", regex=False, case=False)), # noqa
                   "id"]
    if not sctid.empty:
        cf = pd.merge(cf, pd.DataFrame(data={"id": sctid, "ec4": ["1"] * len(sctid)}),
                      how="left", on="id", validate="1:1")

    return cf


def run_quality_control(cf: pd.DataFrame, fts: server.Fts) -> pd.DataFrame:
    """Lance l'ensemble des contrôles qualité et correction automatiques sur les
    traduction à importer.

    args:
        cf: Descriptions de la Common French à importer.
        fts: Serveur de Terminologies FHIR contenant la version de l'édition
            internationale dont dépend votre édition nationale non publiée

    returns:
        DataFrame avec les traductions à importer prête pour la relecture.
    """
    # Précalcul des lignes PT et SYN
    pt = (cf.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (cf.loc[:, "acceptabilityId"] == "ACCEPTABLE")

    # Correction sur les casses
    correction = _get_correct_case(
        cf.loc[cf.loc[:, "caseSignificanceId"] == "CS"])
    cf = cf.set_index("id")
    cf.update(correction)
    cf = cf.reset_index()

    # Contrôles des règles sur les articles
    sb = (cf.loc[:, "conceptId"].isin(fts.ecl("<< 260787004")))
    cf = _check_ar2(cf)
    cf = _check_ar6(cf, sb)

    # Contrôles des règles de Body Structure
    bs = (cf.loc[:, "conceptId"].isin(fts.ecl("<< 123037004")))
    if not cf.loc[bs].empty:
        cf = _check_bs2(cf)
        cf = _check_bs3(cf, bs, pt, syn)
        cf = _check_bs5(cf, bs)
        cf = _check_bs6(cf, bs)
        cf = _check_bs7(cf, bs)
        cf = _check_bs8(cf, pt, syn)
        cf = _check_bs9(cf)
        cf = _check_bs10(cf, pt, syn)
        cf = _check_bs11(cf, pt, syn)
        cf = _check_bs12(cf)
        cf = _check_bs13(cf)

    # Contrôles des règles de Clinical finding
    co = (cf.loc[:, "conceptId"].isin(fts.ecl("<< 123037004 MINUS << 64572001")))
    pa = (cf.loc[:, "fsn"].str.endswith(" (disorder)"))
    if not cf.loc[co].empty:
        cf = _check_co2(cf, co)
        cf = _check_co6(cf, co)
    if not cf.loc[pa].empty:
        cf = _check_pa3(cf, fts)
        cf = _check_pa3_1(cf)
        cf = _check_pa4(cf)
        cf = _check_pa6(cf)
        cf = _check_pa7(cf)
        cf = _check_pa8(cf)
        cf = _check_pa9(cf)

    # Contrôles des règles de Pharmaceutical / biological product
    me = (cf.loc[:, "conceptId"].isin(fts.ecl("<< 373873005")))
    if not cf.loc[me].empty:
        cf = _check_me1(cf, me)
        cf = _check_me2(cf, me)
        cf = _check_me3(cf, me)
        cf = _check_me4(cf, me)

    # Contrôles des règles de Physical object
    if not cf.loc[sb].empty:
        cf = _check_sb1(cf)
        cf = _check_sb2(cf)
        cf = _check_sb3(cf, pt, syn)

    # Contrôles des règles de Procedure
    pr = ((cf.loc[:, "fsn"].str.endswith(" (procedure)"))
          | (cf.loc[:, "fsn"].str.endswith(" (regime/therapy)")))
    if not cf.loc[pr].empty:
        cf = _check_pr2(cf, pt, syn)
        cf = _check_pr3(cf)
        cf = _check_pr4(cf, pt, syn)
        cf = _check_pr9(cf, pt, syn)
        cf = _check_pr10(cf)
        cf = _check_pr12(cf, pt, syn)
        cf = _check_pr13(cf, pt, syn)
        cf = _check_pr14(cf, pt, syn)
        cf = _check_pr15(cf, pr)

    # Contrôles des règles de Situation with explicit context
    hs = (cf.loc[:, "conceptId"].isin(fts.ecl("<< 243796009")))
    if not cf.loc[hs].empty:
        cf = _check_hs1(cf, hs)

    # Contrôles des règles de Specimen
    ec = (cf.loc[:, "conceptId"].isin(fts.ecl("<< 123038009")))
    if not cf.loc[ec].empty:
        cf = _check_ec2(cf)
        cf = _check_ec4(cf)

    return cf
