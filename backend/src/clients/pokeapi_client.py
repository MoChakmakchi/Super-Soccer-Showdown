from typing import TypedDict
import random
from src.entities.player import Player
from src.clients.api_client import APIClient


class PokeAPICharacter(TypedDict):
    name: str
    weight: int
    height: int
    img_url: str


class PokeAPIClient(APIClient[PokeAPICharacter]):
    BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
    IMG_BASE_URL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"

    def _get_random_id(self) -> int:
        return random.randint(1, 900)  # TODO: Limit should not be hardcoded

    def _map_to_player(self, character: PokeAPICharacter) -> Player:
        return Player(
            name=character["name"],
            weight=int(character["weight"]/2.204),  # convert lbs to to kg
            height=int(character["height"])*10,  # convert to cm
            img_url=f'{character["img_url"]}.png'
        )

    def _is_valid_character(self, character: PokeAPICharacter) -> bool:
        required_keys = {'name', 'weight', 'height'}
        return all(character.get(key) for key in required_keys)
