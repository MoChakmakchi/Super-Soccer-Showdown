from typing import Union
from src.utils.models.types import StrategyEnum, UniverseEnum
from src.clients.pokeapi_client import PokeAPIClient
from src.clients.swapi_client import SWAPIClient
from src.entities.team import Team



class TeamGenerator:
    def __init__(self, universe: UniverseEnum):
        self.universe = universe
        self.client: Union[SWAPIClient, PokeAPIClient]

        if self.universe == UniverseEnum.SWAPI:
            self.client = SWAPIClient()
        elif self.universe == UniverseEnum.POKEMON:
            self.client = PokeAPIClient()
        else:
            raise ValueError("Unsupported universe specified.")

    def generate_team(self, count: int = 5, lineup_strategy: StrategyEnum = StrategyEnum.balanced) -> Team:
        if count != 5:
            raise ValueError("A team must have exactly 5 players.")

        players = self.client.return_characters_as_players(count)

        team = Team(players, self.universe, lineup_strategy)
        return team
