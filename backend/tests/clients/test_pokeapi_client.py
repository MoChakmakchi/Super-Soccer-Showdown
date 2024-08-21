import unittest
from unittest.mock import patch
from src.clients.pokeapi_client import PokeAPIClient, PokeAPICharacter
from src.entities.player import Player


class TestPokeAPIClient(unittest.TestCase):

    def setUp(self):
        self.client = PokeAPIClient()

    @patch('src.clients.pokeapi_client.random.randint')
    def test_get_random_id(self, mock_randint):
        """Test the _get_random_id method."""
        mock_randint.return_value = 42
        random_id = self.client._get_random_id()
        self.assertEqual(random_id, 42)

    def test_map_to_player(self):
        """Test mapping PokeAPI character to Player."""
        character: PokeAPICharacter = {
            "name": "Pikachu",
            "weight": 60,
            "height": 4,
            "img_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25"
        }

        player = self.client._map_to_player(character)

        self.assertEqual(player.name, "Pikachu")
        self.assertEqual(player.weight, 27)  # 60 lbs to kg
        self.assertEqual(player.height, 40)  # 4 * 10 cm
        self.assertEqual(player.img_url, "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png")

    def test_is_valid_character(self):
        """Test validating a character for required fields."""
        valid_character: PokeAPICharacter = {
            "name": "Bulbasaur",
            "weight": 69,
            "height": 7,
            "img_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1"
        }

        invalid_character_missing_name: PokeAPICharacter = {
            "weight": 69,
            "height": 7,
            "img_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1"
        } # type: ignore

        invalid_character_missing_weight: PokeAPICharacter = {
            "name": "Bulbasaur",
            "height": 7,
            "img_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1"
        } # type: ignore

        self.assertTrue(self.client._is_valid_character(valid_character))
        self.assertFalse(self.client._is_valid_character(invalid_character_missing_name))
        self.assertFalse(self.client._is_valid_character(invalid_character_missing_weight))

if __name__ == '__main__':
    unittest.main()
