import requests

from typing import List


class Fts:
    """
    Classe regroupant les interactions avec le serveur de Terminologies FHIR de votre
    choix
    """

    def __init__(self, endpoint: str):
        """
        Args:
            endpoint: Endpoint de votre serveur de Terminologies FHIR
        """
        self.endpoint = endpoint
        self.ecl_base_url = f"{endpoint}/ValueSet/$expand?url=http://snomed.info/sct/900000000000207008?fhir_vs=ecl/" # noqa

    def _ecl(self, ecl: str) -> List[str]:
        """Envoie une requête ECL au FTS

        Args:
            ecl: Requête ECL

        Returns:
            Liste des SCTID correspondant à la requête ECL
        """
        url = f"{self.ecl_base_url}{ecl}"
        response = requests.request("GET", url)
        response.raise_for_status()

        return [r.get("code", "")
                for r in response.json()["expansion"].get("contains", {})]

    def get_descendants(self, sctid: str) -> List[str]:
        """Identifie les descendants d'un concept SNOMED CT

        Args:
            sctid: SCTID du concept d'intérêt

        Returns:
            Liste des SCTID qui sont des descendants de `sctid`
        """
        return self._ecl(f"%3C%3C{sctid}")
