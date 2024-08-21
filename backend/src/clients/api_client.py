from typing import Generic, List, TypeVar
from abc import ABC, abstractmethod
from src.entities.player import Player
import requests

T = TypeVar('T', bound=object)


class APIClient(ABC, Generic[T]):
    BASE_URL: str
    IMG_BASE_URL: str

    def get_random_characters(self, count: int = 5) -> List[T]:
        characters: List[T] = []

        while len(characters) < count:
            character = self._fetch_random_character()

            # Keep fetching new characters until we get a unique, valid one
            while character in characters or not self._is_valid_character(character):
                character = self._fetch_random_character()

            # Add the unique, valid character to the list
            characters.append(character)

        return characters

    def return_characters_as_players(self, count: int = 5) -> List[Player]:
        characters = self.get_random_characters(count)
        return [self._map_to_player(character) for character in characters]

    def _fetch_random_character(self, retries: int = 3) -> T:
        # In case a character doesnt exist, fetch another (example char #17 in swapi)
        for _ in range(retries):
            random_id = self._get_random_id()
            try:
                response = requests.get(f"{self.BASE_URL}{random_id}/")
                response.raise_for_status()
                character = response.json()
                character["img_url"] = f"{self.IMG_BASE_URL}{random_id}"
                return character
            except requests.exceptions.HTTPError as e:
                if e.response and e.response.status_code == 404:
                    continue  # Retry with a new random ID
        # After all retries fail
        raise Exception(
            "Failed to fetch a valid character after multiple attempts.")

    @abstractmethod
    def _get_random_id(self) -> int:
        """Generate and return a random ID for fetching a character."""
        pass

    @abstractmethod
    def _map_to_player(self, character: T) -> Player:
        """Must be implemented by subclasses to map API response to Player entity."""
        pass

    @abstractmethod
    def _is_valid_character(self, character: T) -> bool:
        """Must be implemented by subclasses to validate the API response."""
        pass
