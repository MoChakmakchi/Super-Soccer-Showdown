from typing import Union
from src.utils.models.types import StrategyEnum, UniverseEnum
from src.clients.pokeapi_client import PokeAPIClient
from src.clients.swapi_client import SWAPIClient
from src.entities.team import Team



class TeamGenerator:
    def __init__(self, universe: UniverseEnum):
        self._universe = universe
        self._client: Union[SWAPIClient, PokeAPIClient]

        if self._universe == UniverseEnum.SWAPI:
            self._client = SWAPIClient()
        elif self._universe == UniverseEnum.POKEMON:
            self._client = PokeAPIClient()
        else:
            raise ValueError("Unsupported universe specified.")

    def generate_team(self, count: int = 5, lineup_strategy: StrategyEnum = StrategyEnum.balanced) -> Team:
        if count != 5:
            raise ValueError("A team must have exactly 5 players.")

        players = self._client.return_characters_as_players(count)

        team = Team(players, self._universe, lineup_strategy)
        return team
