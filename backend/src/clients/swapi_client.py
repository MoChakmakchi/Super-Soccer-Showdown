import random
from typing import TypedDict
from src.entities.player import Player
from src.clients.api_client import APIClient


class SWAPICharacter(TypedDict):
    name: str
    mass: str
    height: str
    img_url: str


class SWAPIClient(APIClient[SWAPICharacter]):
    BASE_URL = "https://swapi.dev/api/people/"
    IMG_BASE_URL = "https://raw.githubusercontent.com/vieraboschkova/swapi-gallery/main/static/assets/img/people/"

    def _get_random_id(self) -> int:
        return random.randint(1, 82)  # TODO: Limit should not be hardcoded

    def _map_to_player(self, character: SWAPICharacter) -> Player:
        # this is to handle some cases where 'mass': 'unknown'
        def _safe_float(value: str) -> float:
            try:
                return float(value)
            except (ValueError, TypeError):
                return 0.0

        return Player(
            name=character["name"],
            weight=_safe_float(character["mass"]),
            height=_safe_float(character["height"]),
            img_url=f'{character["img_url"]}.jpg'
        )

    def _is_valid_character(self, character: SWAPICharacter) -> bool:
        required_keys = {'name', 'mass', 'height'}
        return all(character.get(key) for key in required_keys)
