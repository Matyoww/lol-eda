import requests
from abc import ABC, abstractmethod
from constants import Clusters

class APIService(ABC):
    @abstractmethod
    def send_get_request(cls, url: str):
        raise NotImplementedError("Subclasses must implement this method")


class RiotAPI(APIService):
    def __init__(self, api_key):
        self.api_key = api_key

    @classmethod
    def send_get_request(cls, url):
        response = requests.get(url)
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(f"Status: {response.status_code}, Message: {response.text['status']['message']}")
        data = response.json()
        return data

    def _url_builder(self, cluster, endpoint):
        url = endpoint
        if cluster == "ASIA":
            url = f"{Clusters.ASIA.value}{url}"
        elif cluster == "SEA":
            url = f"{Clusters.SEA.value}{url}"
        elif cluster == "SG2":
            url = f"{Clusters.SG2.value}{url}"
        else:
            raise ValueError("Invalid cluster specified.")
        url += f"&api_key={self.api_key}"
        return url

class RiotAPIFactory:
    def __init__(self, api_key: RiotAPI):
        self.riot_client = RiotAPI(api_key)

    def get_puuid_by_riot_id(self, game_name, tagline):
        endpoint = f"/riot/account/v1/accounts/by-riot-id/{game_name}/{tagline}?"
        url = self.riot_client._url_builder("ASIA", endpoint)
        data = self.riot_client.send_get_request(url)
        return data['puuid']
    

    def get_riot_id_by_puuid(self, puuid):
        endpoint = f"/riot/account/v1/accounts/by-puuid/{puuid}?"
        url = self.riot_client._url_builder("ASIA", endpoint)
        data = self.riot_client.send_get_request(url)
        return {'game_name': data['gameName'], 'tagline': data['tagLine']}

    
    def get_free_champ_rotation(self, cluster):
        endpoint = "/lol/platform/v3/champion-rotations?"
        url = self.riot_client._url_builder(cluster, endpoint)
        data = self.riot_client.send_get_request(url)
        return data['freeChampionIds']
    

    def get_match_list(self, cluster, puuid, start = 0, count = 20):
        endpoint = f"/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
        url = self.riot_client._url_builder(cluster, endpoint)
        data = self.riot_client.send_get_request(url)
        return data


    def get_match_data(self, cluster, match_id):
        endpoint = f"/lol/match/v5/matches/{match_id}?"
        url = self.riot_client._url_builder(cluster, endpoint)
        data = self.riot_client.send_get_request(url)
        return data