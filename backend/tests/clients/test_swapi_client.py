import unittest
from unittest.mock import patch
from src.clients.swapi_client import SWAPIClient, SWAPICharacter
from src.entities.player import Player


class TestSWAPIClient(unittest.TestCase):

    def setUp(self):
        self.client = SWAPIClient()

    @patch('src.clients.api_client.requests.get')
    def test_fetch_random_character(self, mock_get):
        """Test fetching a random character from SWAPI API."""
        mock_response = {
            "name": "Luke Skywalker",
            "mass": "77",
            "height": "172",
            "img_url": "https://example.com/luke.jpg"
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        character = self.client._fetch_random_character()

        self.assertEqual(character["name"], "Luke Skywalker")
        self.assertEqual(character["mass"], "77")
        self.assertEqual(character["height"], "172")
        self.assertIn("img_url", character)

    @patch('src.clients.api_client.requests.get')
    def test_return_characters_as_players(self, mock_get):
        """Test returning characters as players."""
        # Mock the sequence of two different responses
        mock_response_1 = {
            "name": "Leia Organa",
            "mass": "49",
            "height": "150",
            "img_url": "https://example.com/leia.jpg"
        }
        mock_response_2 = {
            "name": "Luke Skywalker",
            "mass": "77",
            "height": "172",
            "img_url": "https://example.com/luke.jpg"
        }

        # Simulate multiple calls to requests.get by setting side_effect
        mock_get.side_effect = [
            # First response
            unittest.mock.Mock(status_code=200, json=lambda: mock_response_1),
            # Second response
            unittest.mock.Mock(status_code=200, json=lambda: mock_response_2)
        ]

        # Call the method under test
        players = self.client.return_characters_as_players(count=2)

        # Assert that two players were created
        self.assertEqual(len(players), 2)

        # Verify that the players are instances of Player
        self.assertIsInstance(players[0], Player)
        self.assertIsInstance(players[1], Player)

        # Assert correct values were assigned to players
        self.assertEqual(players[0].name, "Leia Organa")
        self.assertEqual(players[1].name, "Luke Skywalker")

    def test_map_to_player(self):
        """Test mapping SWAPI character to Player."""
        character: SWAPICharacter = {
            "name": "Darth Vader",
            "mass": "136",
            "height": "202",
            "img_url": "https://example.com/vader"
        }

        player = self.client._map_to_player(character)

        self.assertEqual(player.name, "Darth Vader")
        self.assertEqual(player.weight, 136.0)
        self.assertEqual(player.height, 202.0)
        self.assertEqual(player.img_url, "https://example.com/vader.jpg")

    def test_safe_float(self):
        """Test the _safe_float conversion for valid and invalid inputs."""
        character: SWAPICharacter = {
            "name": "R2-D2",
            "mass": "unknown",
            "height": "96",
            "img_url": "https://example.com/r2d2"
        }

        player = self.client._map_to_player(character)

        # mass is 'unknown', should be 0.0
        self.assertEqual(player.weight, 0.0)
        self.assertEqual(player.height, 96.0)

    def test_is_valid_character(self):
        """Test validating a character for required fields."""
        valid_character: SWAPICharacter = {
            "name": "Yoda",
            "mass": "17",
            "height": "66",
            "img_url": "https://example.com/yoda"
        }

        invalid_character: SWAPICharacter = {
            "name": "Yoda",
            "mass": "",
            "height": "66",
            "img_url": "https://example.com/yoda"
        }

        self.assertTrue(self.client._is_valid_character(valid_character))
        self.assertFalse(self.client._is_valid_character(invalid_character))


if __name__ == '__main__':
    unittest.main()
