from typing import Dict
import unittest
from unittest.mock import patch, MagicMock
from src.clients.api_client import APIClient
from src.entities.player import Player

class MockAPIClient(APIClient[Dict[str, str]]):
    BASE_URL = "https://example.com/api/"
    IMG_BASE_URL = "https://example.com/api/images"
    def _get_random_id(self) -> int:
        return 1

    def _map_to_player(self, character: Dict[str, str]) -> Player:
        return Player(
            name=character["name"],
            weight=float(character["mass"]),
            height=float(character["height"])
        )

    def _is_valid_character(self, character: Dict[str, str]) -> bool:
        required_keys = {'name', 'mass', 'height'}
        return all(character.get(key) for key in required_keys)


class TestAPIClient(unittest.TestCase):

    def setUp(self):
        self.client = MockAPIClient()

    @patch('requests.get')
    def test_fetch_random_character(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "Test Character", "mass": "75", "height": "180"}
        mock_get.return_value = mock_response

        character = self.client._fetch_random_character()
        self.assertEqual(character["name"], "Test Character")
        self.assertEqual(character["mass"], "75")
        self.assertEqual(character["height"], "180")

    def test_map_to_player(self):
        character = {"name": "Test Character", "mass": "75", "height": "180"}
        player = self.client._map_to_player(character)
        self.assertEqual(player.name, "Test Character")
        self.assertEqual(player.weight, 75.0)
        self.assertEqual(player.height, 180.0)

    def test_is_valid_character(self):
        valid_character = {"name": "Test Character", "mass": "75", "height": "180"}
        invalid_character = {"name": "Test Character", "mass": None, "height": "180"}

        self.assertTrue(self.client._is_valid_character(valid_character))
        self.assertFalse(self.client._is_valid_character(invalid_character))

    def test_get_random_characters(self):
        with patch.object(self.client, '_fetch_random_character') as mock_fetch:
            mock_fetch.side_effect = [
                {"name": "Character 1", "mass": "70", "height": "170"},
                {"name": "Character 2", "mass": "80", "height": "180"},
            ]
            characters = self.client.get_random_characters(count=2)
            self.assertEqual(len(characters), 2)
            self.assertEqual(characters[0]["name"], "Character 1")
            self.assertEqual(characters[1]["name"], "Character 2")

    def test_return_characters_as_players(self):
        with patch.object(self.client, '_fetch_random_character') as mock_fetch:
            mock_fetch.side_effect = [
                {"name": "Character 1", "mass": "70", "height": "170"},
                {"name": "Character 2", "mass": "80", "height": "180"},
            ]
            players = self.client.return_characters_as_players(count=2)
            self.assertEqual(len(players), 2)
            self.assertEqual(players[0].name, "Character 1")
            self.assertEqual(players[1].name, "Character 2")


if __name__ == '__main__':
    unittest.main()
