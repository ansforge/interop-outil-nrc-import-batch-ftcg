import pytest
import pandas as pd


@pytest.fixture
def null() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": ["1"], "acceptabilityId": ["PREFERRED"], "semtag": ["test"], "fsn": ["test"],
         "term": ["test"]}
    )


@pytest.fixture
def case() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "term": ["Un test", "uN test", "un Test"],
         "caseSignificanceId": ["CS"] * 3}
    )


@pytest.fixture
def case_output() -> pd.DataFrame:
    return pd.DataFrame({"id": ["3"], "caseSignificanceId": ["cI"]}).set_index("id")


###################################
# Fixtures pour règles génériques #
###################################
@pytest.fixture
def ar2() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 7)],
         "term": ["Les deux narines", "lesion du nerf", "le patient", "la patiente", "un patient",
                  "une patiente"]}
    )


@pytest.fixture
def ar2_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 7)],
         "term": ["Les deux narines", "lesion du nerf", "le patient", "la patiente", "un patient",
                  "une patiente"],
         "ar2": ["1", float("nan"), "1", "1", "1", "1"]}
    )


@pytest.fixture
def ar6() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 11)],
         "semtag": ["physical object", "physical object", "physical object", "physical object",
                    "physical object", "physical object", "physical object", "physical object",
                    "physical object", "test"],
         "term": ["prothèse pour les hanches", "prothèse pour le bras", "prothèse de la hanche",
                  "prothèse pour un bras", "prothèse pour une hanche", "prothèse d'un bras",
                  "prothèse d'une hanche", "prothèse d'une_ hanche", "prothèse _d'une hanche",
                  "test"]}
    )


@pytest.fixture
def ar6_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 11)],
         "semtag": ["physical object", "physical object", "physical object", "physical object",
                    "physical object", "physical object", "physical object", "physical object",
                    "physical object", "test"],
         "term": ["prothèse pour les hanches", "prothèse pour le bras", "prothèse de la hanche",
                  "prothèse pour un bras", "prothèse pour une hanche", "prothèse d'un bras",
                  "prothèse d'une hanche", "prothèse d'une_ hanche", "prothèse _d'une hanche",
                  "test"],
         "ar6": ["1", "1", "1", "1", "1", "1", "1", float("nan"), float("nan"), float("nan")]}
    )


#######################################
# Fixtures pour règles Body structure #
#######################################
@pytest.fixture
def bs2() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 5)],
         "semtag": ["body structure"] * 3 + ["test"],
         "fsn": ["femur joint", "joint pain", "knee joint", "test"],
         "term": ["articulation fémorale", "douleur articulaire", "genou", "test"]}
    )


@pytest.fixture
def bs2_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 5)],
         "semtag": ["body structure"] * 3 + ["test"],
         "fsn": ["femur joint", "joint pain", "knee joint", "test"],
         "term": ["articulation fémorale", "douleur articulaire", "genou", "test"],
         "bs2": [float("nan"), float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def bs3() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 13)],
         "acceptabilityId": ["PREFERRED"] * 2 + ["ACCEPTABLE"] * 10,
         "semtag": ["body structure"] * 11 + ["test"],
         "fsn": ["knee structure", "knee structure", "knee structure", "knee structure",
                 "entire knee", "entire hip", "entire feet", "entire shoulders", "entire knee",
                 "knee part", "knee part", "test"],
         "term": ["structure d'un genou", "genou", "genou", "structure d'un genou",
                  "genou entier", "hanche entière", "pieds entiers", "épaules entières", "genou",
                  "partie d'un genou", "genou", "test"]}
    )


@pytest.fixture
def bs3_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 13)],
         "acceptabilityId": ["PREFERRED"] * 2 + ["ACCEPTABLE"] * 10,
         "semtag": ["body structure"] * 11 + ["test"],
         "fsn": ["knee structure", "knee structure", "knee structure", "knee structure",
                 "entire knee", "entire hip", "entire feet", "entire shoulders", "entire knee",
                 "knee part", "knee part", "test"],
         "term": ["structure d'un genou", "genou", "genou", "structure d'un genou", "genou entier",
                  "hanche entière", "pieds entiers", "épaules entières", "genou",
                  "partie d'un genou", "genou", "test"],
         "bs3": [float("nan"), "1", float("nan"), "1", float("nan"), float("nan"), float("nan"),
                 float("nan"), "1", float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def bs5() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["body structure"] * 2 + ["test"],
         "fsn": ["knee region", "knee region", "test"],
         "term": ["région d'un genou", "genou", "test"]}
    )


@pytest.fixture
def bs5_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["body structure"] * 2 + ["test"],
         "fsn": ["knee region", "knee region", "test"],
         "term": ["région d'un genou", "genou", "test"],
         "bs5": [float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def bs6() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 8)],
         "semtag": ["body structure"] * 6 + ["test"],
         "fsn": ["knee zone", "knee zone", "knee area", "knee area", "knee area", "knee area",
                 "test"],
         "term": ["zone d'un genou", "genou", "zone d'un genou", "surface d'un genou",
                  "aire d'un genou", "genou", "test"]}
    )


@pytest.fixture
def bs6_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 8)],
         "semtag": ["body structure"] * 6 + ["test"],
         "fsn": ["knee zone", "knee zone", "knee area", "knee area", "knee area", "knee area",
                 "test"],
         "term": ["zone d'un genou", "genou", "zone d'un genou", "surface d'un genou",
                  "aire d'un genou", "genou", "test"],
         "bs6": [float("nan"), "1", float("nan"), float("nan"), float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def bs7() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 6)],
         "semtag": ["body structure"] * 4 + ["test"],
         "fsn": ["eye proper", "eye proper", "mouth proper", "eye proper", "test"],
         "term": ["oeil propre", "oeil proprement dit", "bouche proprement dite", "oeil", "test"]}
    )


@pytest.fixture
def bs7_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 6)],
         "semtag": ["body structure"] * 4 + ["test"],
         "fsn": ["eye proper", "eye proper", "mouth proper", "eye proper", "test"],
         "term": ["oeil propre", "oeil proprement dit", "bouche proprement dite", "oeil", "test"],
         "bs7": [float("nan"), float("nan"), float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def bs8() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 8)],
         "acceptabilityId": ["PREFERRED"] * 2 + ["ACCEPTABLE"] * 5,
         "semtag": ["body structure"] * 6 + ["test"],
         "fsn": ["heart apex", "heart apex", "heart apex", "heart apex", "heart apex",
                 "heart apex", "test"],
         "term": ["apex du coeur", "coeur", "pointe du coeur", "bout du coeur", "cime du coeur",
                  "coeur", "test"]}
    )


@pytest.fixture
def bs8_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 8)],
         "acceptabilityId": ["PREFERRED"] * 2 + ["ACCEPTABLE"] * 5,
         "semtag": ["body structure"] * 6 + ["test"],
         "fsn": ["heart apex", "heart apex", "heart apex", "heart apex", "heart apex",
                 "heart apex", "test"],
         "term": ["apex du coeur", "coeur", "pointe du coeur", "bout du coeur", "cime du coeur",
                  "coeur", "test"],
         "bs8": [float("nan"), "1", float("nan"), float("nan"), float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def bs9() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 5)],
         "semtag": ["body structure"] * 3 + ["test"],
         "fsn": ["lesser toe", "lesser toe", "lesser toe", "test"],
         "term": ["orteil excepté l'hallux", "orteil", "petit orteil", "test"]}
    )


@pytest.fixture
def bs9_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 5)],
         "semtag": ["body structure"] * 3 + ["test"],
         "fsn": ["lesser toe", "lesser toe", "lesser toe", "test"],
         "term": ["orteil excepté l'hallux", "orteil", "petit orteil", "test"],
         "bs9": [float("nan"), "1", "1", float("nan")]}
    )


@pytest.fixture
def bs10() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["body structure"] * 2 + ["test"],
         "fsn": ["lower limb", "lower limb", "test"],
         "term": ["membre inférieur", "jambe", "test"]}
    )


@pytest.fixture
def bs10_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["body structure"] * 2 + ["test"],
         "fsn": ["lower limb", "lower limb", "test"],
         "term": ["membre inférieur", "jambe", "test"],
         "bs10": [float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def bs11() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 7)],
         "semtag": ["body structure"] * 5 + ["test"],
         "acceptabilityId": ["PREFERRED"] * 2 + ["ACCEPTABLE"] * 4,
         "fsn": ["lower leg", "lower leg", "lower leg", "lower leg", "lower leg", "test"],
         "term": ["partie basse d'une jambe", "jambe", "partie inférieure d'une jambe",
                  "jambe, du genou à la cheville", "jambe", "test"]}
    )


@pytest.fixture
def bs11_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 7)],
         "semtag": ["body structure"] * 5 + ["test"],
         "acceptabilityId": ["PREFERRED"] * 2 + ["ACCEPTABLE"] * 4,
         "fsn": ["lower leg", "lower leg", "lower leg", "lower leg", "lower leg", "test"],
         "term": ["partie basse d'une jambe", "jambe", "partie inférieure d'une jambe",
                  "jambe, du genou à la cheville", "jambe", "test"],
         "bs11": [float("nan"), "1", float("nan"), float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def bs12() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["body structure"] * 2 + ["test"],
         "fsn": ["cerebrum", "cerebrum", "test"],
         "term": ["cerveau", "encéphale", "test"]}
    )


@pytest.fixture
def bs12_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["body structure"] * 2 + ["test"],
         "fsn": ["cerebrum", "cerebrum", "test"],
         "term": ["cerveau", "encéphale", "test"],
         "bs12": [float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def bs13() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["body structure"] * 2 + ["test"],
         "fsn": ["brain", "brain", "test"],
         "term": ["encéphale", "cerveau", "test"]}
    )


@pytest.fixture
def bs13_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["body structure"] * 2 + ["test"],
         "fsn": ["brain", "brain", "test"],
         "term": ["encéphale", "cerveau", "test"],
         "bs13": [float("nan"), "1", float("nan")]}
    )


#########################################
# Fixtures pour règles Clinical finding #
#########################################
@pytest.fixture
def co2() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 5)],
         "semtag": ["clinical finding"] * 3 + ["test"],
         "fsn": ["test (finding)", "head finding", "head finding", "test"],
         "term": ["test (constatation)", "constatation sur la tête", "observation sur la tête",
                  "test"]}
    )


@pytest.fixture
def co2_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 5)],
         "semtag": ["clinical finding"] * 3 + ["test"],
         "fsn": ["test (finding)", "head finding", "head finding", "test"],
         "term": ["test (constatation)", "constatation sur la tête", "observation sur la tête",
                  "test"],
         "co2": [float("nan"), float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def co6() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 10)],
         "semtag": ["clinical finding"] * 8 + ["test"],
         "fsn": ["calcium above reference range", "protein above reference range",
                 "calcium above reference range", "calcium above reference range",
                 "calcium bellow reference range", "protein bellow reference range",
                 "calcium bellow reference range", "calcium bellow reference range", "test"],
         "term": ["calcium supérieur à l'intervalle de référence",
                  "protéine supérieure à l'intervalle de référence",
                  "calcium supérieur aux valeurs de référence", "calcium augmenté",
                  "calcium inférieur à l'intervalle de référence",
                  "protéine inférieure à l'intervalle de référence",
                  "calcium inférieur aux valeurs de référence", "calcium diminué", "test"]}
    )


@pytest.fixture
def co6_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 10)],
         "semtag": ["clinical finding"] * 8 + ["test"],
         "fsn": ["calcium above reference range", "protein above reference range",
                 "calcium above reference range", "calcium above reference range",
                 "calcium bellow reference range", "protein bellow reference range",
                 "calcium bellow reference range", "calcium bellow reference range", "test"],
         "term": ["calcium supérieur à l'intervalle de référence",
                  "protéine supérieure à l'intervalle de référence",
                  "calcium supérieur aux valeurs de référence", "calcium augmenté",
                  "calcium inférieur à l'intervalle de référence",
                  "protéine inférieure à l'intervalle de référence",
                  "calcium inférieur aux valeurs de référence", "calcium diminué", "test"],
         "co6": [float("nan"), float("nan"), float("nan"), "1", float("nan"), float("nan"),
                 float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def pa4() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 9)],
         "semtag": ["clinical finding"] * 7 + ["test"],
         "fsn": ["epilepsy", "epilepsy", "seizure", "seizure", "seizure", "convulsion",
                 "convulsion", "test"],
         "term": ["épilepsie", "crise", "crise", "convulsion", "épilepsie", "convulsion",
                  "épilepsie", "test"]}
    )


@pytest.fixture
def pa4_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 9)],
         "semtag": ["clinical finding"] * 7 + ["test"],
         "fsn": ["epilepsy", "epilepsy", "seizure", "seizure", "seizure", "convulsion",
                 "convulsion", "test"],
         "term": ["épilepsie", "crise", "crise", "convulsion", "épilepsie", "convulsion",
                  "épilepsie", "test"],
         "pa4": [float("nan"), "1", float("nan"), float("nan"), "1", float("nan"), "1",
                 float("nan")]}
    )


@pytest.fixture
def pa6() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["clinical finding"] * 2 + ["test"],
         "fsn": ["impairment", "impairment", "test"],
         "term": ["atteinte", "impairment", "test"]}
    )


@pytest.fixture
def pa6_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["clinical finding"] * 2 + ["test"],
         "fsn": ["impairment", "impairment", "test"],
         "term": ["atteinte", "impairment", "test"],
         "pa6": [float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def pa7() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 5)],
         "semtag": ["clinical finding"] * 3 + ["test"],
         "fsn": ["primary", "primary", "primary", "test"],
         "term": ["primitif", "primaire", "primordial", "test"]}
    )


@pytest.fixture
def pa7_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 5)],
         "semtag": ["clinical finding"] * 3 + ["test"],
         "fsn": ["primary", "primary", "primary", "test"],
         "term": ["primitif", "primaire", "primordial", "test"],
         "pa7": [float("nan"), float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def pa8() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 8)],
         "semtag": ["clinical finding"] * 6 + ["test"],
         "fsn": ["chilblain", "chilblain", "a frostbite", "a frostbite", "superficial frostbite",
                 "superficial frostbite", "test"],
         "term": ["engelure", "gelure", "gelure", "engelure", "gelure superficielle",
                  "engelure superficielle", "test"]}
    )


@pytest.fixture
def pa8_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 8)],
         "semtag": ["clinical finding"] * 6 + ["test"],
         "fsn": ["chilblain", "chilblain", "a frostbite", "a frostbite", "superficial frostbite",
                 "superficial frostbite", "test"],
         "term": ["engelure", "gelure", "gelure", "engelure", "gelure superficielle",
                  "engelure superficielle", "test"],
         "pa8": [float("nan"), "1", float("nan"), "1", float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def pa9() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 13)],
         "semtag": ["clinical finding"] * 11 + ["test"],
         "fsn": ["carbuncle", "carbuncle", "furuncle", "furuncle", "furuncle", "furuncle",
                 "furuncle", "furuncle", "furuncle", "anthrax", "anthrax", "test"],
         "term": ["anthrax", "maladie du charbon", "furoncle", "folliculite nécrotique", "clou",
                  "furoncle", "folliculite nécrotique", "clou", "anthrax", "maladie du charbon",
                  "anthrax", "test"]}
    )


@pytest.fixture
def pa9_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 13)],
         "semtag": ["clinical finding"] * 11 + ["test"],
         "fsn": ["carbuncle", "carbuncle", "furuncle", "furuncle", "furuncle", "furuncle",
                 "furuncle", "furuncle", "furuncle", "anthrax", "anthrax", "test"],
         "term": ["anthrax", "maladie du charbon", "furoncle", "folliculite nécrotique", "clou",
                  "furoncle", "folliculite nécrotique", "clou", "anthrax", "maladie du charbon",
                  "anthrax", "test"],
         "pa9": [float("nan"), "1", float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), "1", float("nan"), "1", float("nan")]}
    )


############################################################
# Fixtures pour règles Pharmaceutical / biological product #
############################################################
@pytest.fixture
def me1() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["pharmaceutical"] * 2 + ["test"],
         "fsn": ["product containing x", "product containing x", "test"],
         "term": ["produit contenant x", "produit contenant uniquement x", "test"]}
    )


@pytest.fixture
def me1_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["pharmaceutical"] * 2 + ["test"],
         "fsn": ["product containing x", "product containing x", "test"],
         "term": ["produit contenant x", "produit contenant uniquement x", "test"],
         "me1": [float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def me2() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["pharmaceutical"] * 2 + ["test"],
         "fsn": ["product containing only", "product containing only", "test"],
         "term": ["produit contenant uniquement", "produit contenant", "test"]}
    )


@pytest.fixture
def me2_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["pharmaceutical"] * 2 + ["test"],
         "fsn": ["product containing only", "product containing only", "test"],
         "term": ["produit contenant uniquement", "produit contenant", "test"],
         "me2": [float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def me3() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["pharmaceutical"] * 2 + ["test"],
         "fsn": ["x (clinical drug)", "x (clinical drug)", "test"],
         "term": ["produit contenant précisément x", "x", "test"]}
    )


@pytest.fixture
def me3_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["pharmaceutical"] * 2 + ["test"],
         "fsn": ["x (clinical drug)", "x (clinical drug)", "test"],
         "term": ["produit contenant précisément x", "x", "test"],
         "me3": [float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def me4() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["pharmaceutical"] * 2 + ["test"],
         "term": ["x", "x libération conventionnelle", "test"]}
    )


@pytest.fixture
def me4_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["pharmaceutical"] * 2 + ["test"],
         "term": ["x", "x libération conventionnelle", "test"],
         "me4": [float("nan"), "1", float("nan")]}
    )


########################################
# Fixtures pour règles Physical object #
########################################
@pytest.fixture
def sb1() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["physical object"] * 2 + ["test"],
         "fsn": ["evacuated x collection tube", "evacuated x collection tube", "test"],
         "term": ["tube sous vide x pour prélèvement", "échantillon x", "test"]}
    )


@pytest.fixture
def sb1_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["physical object"] * 2 + ["test"],
         "fsn": ["evacuated x collection tube", "evacuated x collection tube", "test"],
         "term": ["tube sous vide x pour prélèvement", "échantillon x", "test"],
         "sb1": [float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def sb2() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["physical object"] * 2 + ["test"],
         "fsn": ["evacuated x specimen container", "evacuated x specimen container", "test"],
         "term": ["support sous vide x pour prélèvement", "échantillon x", "test"]}
    )


@pytest.fixture
def sb2_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["physical object"] * 2 + ["test"],
         "fsn": ["evacuated x specimen container", "evacuated x specimen container", "test"],
         "term": ["support sous vide x pour prélèvement", "échantillon x", "test"],
         "sb2": [float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def sb3() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 6)],
         "semtag": ["physical object"] * 4 + ["test"],
         "acceptabilityId": ["PREFERRED"] * 2 + ["ACCEPTABLE"] * 3,
         "fsn": ["stent", "stent", "stent", "stent", "test"],
         "term": ["endoprothèse", "stent", "stent", "endoprothèse", "test"]}
    )


@pytest.fixture
def sb3_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 6)],
         "semtag": ["physical object"] * 4 + ["test"],
         "acceptabilityId": ["PREFERRED"] * 2 + ["ACCEPTABLE"] * 3,
         "fsn": ["stent", "stent", "stent", "stent", "test"],
         "term": ["endoprothèse", "stent", "stent", "endoprothèse", "test"],
         "sb3": [float("nan"), "1", float("nan"), "1", float("nan")]}
    )


##################################
# Fixtures pour règles Procedure #
##################################
@pytest.fixture
def pr2() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 15)],
         "semtag": ["procedure"] * 13 + ["test"],
         "acceptabilityId": ["PREFERRED"] * 6 + ["ACCEPTABLE"] * 8,
         "fsn": ["test (procedure)", "imaging procedure", "surgical procedure",
                 "imaging procedure", "operation", "operation", "imaging procedure",
                 "surgical procedure", "surgical procedure", "surgical procedure", "operation",
                 "operation", "operation", "test"],
         "term": ["test (procedure)", "procédure d'imagerie", "intervention chirurgicale",
                  "imagerie", "intervention chirurgicale", "opération", "intervention d'imagerie",
                  "opération chirurgicale", "chirurgie", "procédure chirurgicale", "opération",
                  "chirurgie", "procédure chirurgicale", "test"]}
    )


@pytest.fixture
def pr2_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 15)],
         "semtag": ["procedure"] * 13 + ["test"],
         "acceptabilityId": ["PREFERRED"] * 6 + ["ACCEPTABLE"] * 8,
         "fsn": ["test (procedure)", "imaging procedure", "surgical procedure",
                 "imaging procedure", "operation", "operation", "imaging procedure",
                 "surgical procedure", "surgical procedure", "surgical procedure", "operation",
                 "operation", "operation", "test"],
         "term": ["test (procedure)", "procédure d'imagerie", "intervention chirurgicale",
                  "imagerie", "intervention chirurgicale", "opération", "intervention d'imagerie",
                  "opération chirurgicale", "chirurgie", "procédure chirurgicale", "opération",
                  "chirurgie", "procédure chirurgicale", "test"],
         "pr2": [float("nan"), float("nan"), float("nan"), "1", float("nan"), "1", float("nan"),
                 float("nan"), float("nan"), "1", float("nan"), float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def pr3() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["procedure"] * 2 + ["test"],
         "fsn": ["consultation", "consultation", "test"],
         "term": ["consultation", "x", "test"]}
    )


@pytest.fixture
def pr3_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["procedure"] * 2 + ["test"],
         "fsn": ["consultation", "consultation", "test"],
         "term": ["consultation", "x", "test"],
         "pr3": [float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def pr4() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 8)],
         "semtag": ["procedure"] * 6 + ["test"],
         "acceptabilityId": ["PREFERRED"] * 4 + ["ACCEPTABLE"] * 3,
         "fsn": ["removal of foreign body", "removal of foreign body", "magnet extraction",
                 "magnet extraction", "magnet extraction", "magnet extraction", "test"],
         "term": ["retrait d'un corps étranger", "extraction d'un corps étranger",
                  "extraction avec un aimant", "retrait avec un aimant",
                  "retrait d'un corps étranger x à l'aide d'un aimant",
                  "extraction d'un corps étranger x à l'aide d'un aimant", "test"]}
    )


@pytest.fixture
def pr4_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 8)],
         "semtag": ["procedure"] * 6 + ["test"],
         "acceptabilityId": ["PREFERRED"] * 4 + ["ACCEPTABLE"] * 3,
         "fsn": ["removal of foreign body", "removal of foreign body", "magnet extraction",
                 "magnet extraction", "magnet extraction", "magnet extraction", "test"],
         "term": ["retrait d'un corps étranger", "extraction d'un corps étranger",
                  "extraction avec un aimant", "retrait avec un aimant",
                  "retrait d'un corps étranger x à l'aide d'un aimant",
                  "extraction d'un corps étranger x à l'aide d'un aimant", "test"],
         "pr4": [float("nan"), "1", float("nan"), "1", float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def pr9() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 6)],
         "semtag": ["procedure"] * 4 + ["test"],
         "acceptabilityId": ["PREFERRED"] * 2 + ["ACCEPTABLE"] * 3,
         "fsn": ["excisional biopsy", "excisional biopsy", "excisional biopsy",
                 "excisional biopsy", "test"],
         "term": ["biopsie-exérèse", "biopsie excisionnelle", "biopsie excisionnelle",
                  "biopsie-exérèse", "test"]}
    )


@pytest.fixture
def pr9_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 6)],
         "semtag": ["procedure"] * 4 + ["test"],
         "acceptabilityId": ["PREFERRED"] * 2 + ["ACCEPTABLE"] * 3,
         "fsn": ["excisional biopsy", "excisional biopsy", "excisional biopsy",
                 "excisional biopsy", "test"],
         "term": ["biopsie-exérèse", "biopsie excisionnelle", "biopsie excisionnelle",
                  "biopsie-exérèse", "test"],
         "pr9": [float("nan"), "1", float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def pr10() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["procedure"] * 2 + ["test"],
         "fsn": ["incisional biopsy", "incisional biopsy", "test"],
         "term": ["biopsie incisionnelle", "biopsie", "test"]}
    )


@pytest.fixture
def pr10_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["procedure"] * 2 + ["test"],
         "fsn": ["incisional biopsy", "incisional biopsy", "test"],
         "term": ["biopsie incisionnelle", "biopsie", "test"],
         "pr10": [float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def pr12() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 10)],
         "semtag": ["procedure"] * 8 + ["test"],
         "acceptabilityId": ["PREFERRED"] * 4 + ["ACCEPTABLE"] * 5,
         "fsn": ["MRI", "MRI", "magnetic resonance angiography",
                 "magnetic resonance angiography", "MRI", "MRI", "magnetic resonance angiography",
                 "magnetic resonance angiography", "test"],
         "term": ["IRM", "imagerie par résonance magnétique",
                  "angiographie par IRM", "angiographie par imagerie par résonance magnétique",
                  "imagerie par résonance magnétique", "IRM",
                  "angiographie par imagerie par résonance magnétique",
                  "angiographie par IRM", "test"]}
    )


@pytest.fixture
def pr12_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 10)],
         "semtag": ["procedure"] * 8 + ["test"],
         "acceptabilityId": ["PREFERRED"] * 4 + ["ACCEPTABLE"] * 5,
         "fsn": ["MRI", "MRI", "magnetic resonance angiography",
                 "magnetic resonance angiography", "MRI", "MRI", "magnetic resonance angiography",
                 "magnetic resonance angiography", "test"],
         "term": ["IRM", "imagerie par résonance magnétique",
                  "angiographie par IRM", "angiographie par imagerie par résonance magnétique",
                  "imagerie par résonance magnétique", "IRM",
                  "angiographie par imagerie par résonance magnétique",
                  "angiographie par IRM", "test"],
         "pr12": [float("nan"), "1", float("nan"), "1", float("nan"), "1", float("nan"), "1",
                  float("nan")]}
    )


@pytest.fixture
def pr13() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 8)],
         "semtag": ["procedure"] * 6 + ["test"],
         "acceptabilityId": ["PREFERRED"] * 3 + ["ACCEPTABLE"] * 4,
         "fsn": ["procedure guided by imaging", "act guided by imaging", "act guided by imaging",
                 "procedure guided by imaging", "act guided by imaging", "act guided by imaging",
                 "test"],
         "term": ["procédure guidée par imagerie", "acte guidé par imagerie",
                  "acte sous guidage par imagerie", "procédure sous guidage par imagerie",
                  "acte sous guidage par imagerie", "acte guidé par imagerie", "test"]}
    )


@pytest.fixture
def pr13_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 8)],
         "semtag": ["procedure"] * 6 + ["test"],
         "acceptabilityId": ["PREFERRED"] * 3 + ["ACCEPTABLE"] * 4,
         "fsn": ["procedure guided by imaging", "act guided by imaging", "act guided by imaging",
                 "procedure guided by imaging", "act guided by imaging", "act guided by imaging",
                 "test"],
         "term": ["procédure guidée par imagerie", "acte guidé par imagerie",
                  "acte sous guidage par imagerie", "procédure sous guidage par imagerie",
                  "acte sous guidage par imagerie", "acte guidé par imagerie", "test"],
         "pr13": [float("nan"), float("nan"), "1", float("nan"), float("nan"), "1", float("nan")]}
    )


@pytest.fixture
def pr14() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 14)],
         "semtag": ["procedure"] * 12 + ["test"],
         "acceptabilityId": ["PREFERRED"] * 6 + ["ACCEPTABLE"] * 7,
         "fsn": ["fluoroscopy of knee", "fluoroscopic procedure of knee", "fluoroscopy of knee",
                 "fluoroscopy guided procedure", "fluoroscopic procedure guided act",
                 "fluoroscopy guided procedure", "fluoroscopy of knee",
                 "fluoroscopic procedure of knee", "fluoroscopy of knee",
                 "fluoroscopy guided procedure", "fluoroscopic procedure guided procedure",
                 "fluoroscopy guided procedure", "test"],
         "term": ["radioscopie d'un genou", "radioscopie d'un genou", "fluoroscopie d'un genou",
                  "procédure guidée par radioscopie", "acte guidé par radioscopie",
                  "procédure sous guidage radioscopique", "fluoroscopie d'un genou",
                  "fluoroscopie d'un genou", "radioscopie d'un genou",
                  "procédure sous guidage radioscopique", "procédure guidée par fluoroscopie",
                  "procédure guidée par radioscopie", "test"]}
    )


@pytest.fixture
def pr14_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 14)],
         "semtag": ["procedure"] * 12 + ["test"],
         "acceptabilityId": ["PREFERRED"] * 6 + ["ACCEPTABLE"] * 7,
         "fsn": ["fluoroscopy of knee", "fluoroscopic procedure of knee", "fluoroscopy of knee",
                 "fluoroscopy guided procedure", "fluoroscopic procedure guided act",
                 "fluoroscopy guided procedure", "fluoroscopy of knee",
                 "fluoroscopic procedure of knee", "fluoroscopy of knee",
                 "fluoroscopy guided procedure", "fluoroscopic procedure guided procedure",
                 "fluoroscopy guided procedure", "test"],
         "term": ["radioscopie d'un genou", "radioscopie d'un genou", "fluoroscopie d'un genou",
                  "procédure guidée par radioscopie", "acte guidé par radioscopie",
                  "procédure sous guidage radioscopique", "fluoroscopie d'un genou",
                  "fluoroscopie d'un genou", "radioscopie d'un genou",
                  "procédure sous guidage radioscopique", "procédure guidée par fluoroscopie",
                  "procédure guidée par radioscopie", "test"],

         "pr14": [float("nan"), float("nan"), "1", float("nan"), float("nan"), "1", float("nan"),
                  float("nan"), "1", float("nan"), float("nan"), "1", float("nan")]}
    )


#################################
# Fixtures pour règles Specimen #
#################################
@pytest.fixture
def ec2() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 9)],
         "semtag": ["specimen"] * 7 + ["test"],
         "fsn": ["implant submitted as specimen", "plaque submitted as specimen",
                 "implant submitted as specimen", "washings", "washings", "cytologic material",
                 "cytologic material", "test"],
         "term": ["implant présenté comme échantillon", "plaque présentée comme échantillon",
                  "implant comme échantillon", "liquide de lavage", "lavage",
                  "matériel cytologique", "cytologie", "test"]}
    )


@pytest.fixture
def ec2_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 9)],
         "semtag": ["specimen"] * 7 + ["test"],
         "fsn": ["implant submitted as specimen", "plaque submitted as specimen",
                 "implant submitted as specimen", "washings", "washings", "cytologic material",
                 "cytologic material", "test"],
         "term": ["implant présenté comme échantillon", "plaque présentée comme échantillon",
                  "implant comme échantillon", "liquide de lavage", "lavage",
                  "matériel cytologique", "cytologie", "test"],
         "ec2": [float("nan"), float("nan"), "1", float("nan"), "1", float("nan"), "1",
                 float("nan")]}
    )


@pytest.fixture
def ec4() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["specimen"] * 2 + ["test"],
         "fsn": ["fluid sample", "fluid sample", "test"],
         "term": ["échantillon de liquide", "liquide", "test"]}
    )


@pytest.fixture
def ec4_output() -> pd.DataFrame:
    return pd.DataFrame(
        {"id": [str(i) for i in range(1, 4)],
         "semtag": ["specimen"] * 2 + ["test"],
         "fsn": ["fluid sample", "fluid sample", "test"],
         "term": ["échantillon de liquide", "liquide", "test"],
         "ec4": [float("nan"), "1", float("nan")]}
    )
