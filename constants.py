import enum

class Clusters(enum.Enum):
    ASIA = "https://asia.api.riotgames.com"
    SEA = "https://sea.api.riotgames.com"
    SG2 = "https://sg2.api.riotgames.com"

    def __getattribute__(self, name):
        return super().__getattribute__(name)