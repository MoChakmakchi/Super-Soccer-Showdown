import unittest
from unittest.mock import patch, MagicMock
from src.utils.models.types import StrategyEnum, UniverseEnum
from src.entities.team import Team
from src.utils.team_generator import TeamGenerator


class TestTeamGenerator(unittest.TestCase):

    @patch('src.utils.team_generator.SWAPIClient')
    def test_swapi_client_initialization(self, MockSWAPIClient):
        """Test initialization with SWAPI universe."""
        # Create an instance of TeamGenerator with SWAPI universe
        generator = TeamGenerator(UniverseEnum.SWAPI)

        # Ensure the mock client is used
        mock_client = MockSWAPIClient.return_value
        self.assertIs(generator._client, mock_client)

    @patch('src.utils.team_generator.PokeAPIClient')
    def test_pokemon_client_initialization(self, MockPokeAPIClient):
        """Test initialization with Pokemon universe."""
        # Create an instance of TeamGenerator with Pokemon universe
        generator = TeamGenerator(UniverseEnum.POKEMON)

        # Ensure the mock client is used
        mock_client = MockPokeAPIClient.return_value
        self.assertIs(generator._client, mock_client)

    @patch('src.utils.team_generator.SWAPIClient')
    def test_generate_team_swapi(self, MockSWAPIClient):
        """Test generating a team with SWAPI client."""
        # Create concrete mock player instances with realistic attributes
        mock_player_1 = MagicMock()
        mock_player_1.weight = 75
        mock_player_1.height = 180

        mock_player_2 = MagicMock()
        mock_player_2.weight = 80
        mock_player_2.height = 170

        mock_player_3 = MagicMock()
        mock_player_3.weight = 70
        mock_player_3.height = 190

        mock_player_4 = MagicMock()
        mock_player_4.weight = 85
        mock_player_4.height = 160

        mock_player_5 = MagicMock()
        mock_player_5.weight = 90
        mock_player_5.height = 175

        # Set the return value of the mock client method
        mock_client = MockSWAPIClient.return_value
        mock_client.return_characters_as_players.return_value = [
            mock_player_1, mock_player_2, mock_player_3, mock_player_4, mock_player_5
        ]

        # Create an instance of TeamGenerator with SWAPI universe
        generator = TeamGenerator(UniverseEnum.SWAPI)
        team = generator.generate_team(count=5)

        # Verify that the team is created correctly
        self.assertIsInstance(team, Team)
        self.assertEqual(len(team.players), 5)
        self.assertEqual(team._universe, UniverseEnum.SWAPI)

    @patch('src.utils.team_generator.PokeAPIClient')
    def test_generate_team_pokemon(self, MockPokeAPIClient):
        """Test generating a team with Pokemon client."""
        # Create concrete mock player instances with realistic attributes
        mock_player_1 = MagicMock()
        mock_player_1.weight = 50
        mock_player_1.height = 60

        mock_player_2 = MagicMock()
        mock_player_2.weight = 55
        mock_player_2.height = 65

        mock_player_3 = MagicMock()
        mock_player_3.weight = 60
        mock_player_3.height = 70

        mock_player_4 = MagicMock()
        mock_player_4.weight = 65
        mock_player_4.height = 75

        mock_player_5 = MagicMock()
        mock_player_5.weight = 70
        mock_player_5.height = 80

        # Set the return value of the mock client method
        mock_client = MockPokeAPIClient.return_value
        mock_client.return_characters_as_players.return_value = [
            mock_player_1, mock_player_2, mock_player_3, mock_player_4, mock_player_5
        ]

        # Create an instance of TeamGenerator with Pokémon universe
        generator = TeamGenerator(UniverseEnum.POKEMON)
        team = generator.generate_team(count=5)

        # Verify that the team is created correctly
        self.assertIsInstance(team, Team)
        self.assertEqual(len(team.players), 5)
        self.assertEqual(team._universe, UniverseEnum.POKEMON)

    def test_generate_team_invalid_count(self):
        """Test generating a team with an invalid count."""
        generator = TeamGenerator(UniverseEnum.SWAPI)
        with self.assertRaises(ValueError) as context:
            generator.generate_team(count=4)
        self.assertEqual(str(context.exception),
                         "A team must have exactly 5 players.")

    @patch('src.utils.team_generator.SWAPIClient')
    def test_generate_team_strategy(self, MockSWAPIClient):
        """Test generating a team with different strategies."""
        # Create concrete mock player instances with realistic attributes
        mock_player_1 = MagicMock()
        mock_player_1.weight = 75
        mock_player_1.height = 180

        mock_player_2 = MagicMock()
        mock_player_2.weight = 80
        mock_player_2.height = 170

        mock_player_3 = MagicMock()
        mock_player_3.weight = 70
        mock_player_3.height = 190

        mock_player_4 = MagicMock()
        mock_player_4.weight = 85
        mock_player_4.height = 160

        mock_player_5 = MagicMock()
        mock_player_5.weight = 90
        mock_player_5.height = 175

        # Set the return value of the mock client method
        mock_client = MockSWAPIClient.return_value
        mock_client.return_characters_as_players.return_value = [
            mock_player_1, mock_player_2, mock_player_3, mock_player_4, mock_player_5
        ]

        # Test all strategies
        for strategy in StrategyEnum:
            with self.subTest(strategy=strategy):
                # Create an instance of TeamGenerator with SWAPI universe
                generator = TeamGenerator(UniverseEnum.SWAPI)
                team = generator.generate_team(
                    count=5, lineup_strategy=strategy)

                # Verify that the team is created correctly
                self.assertIsInstance(team, Team)
                self.assertEqual(len(team.players), 5)
                self.assertEqual(team._universe, UniverseEnum.SWAPI)
                self.assertEqual(team.lineup_strategy, strategy)

    def test_unsupported_universe(self):
        """Test initialization with unsupported universe."""
        with self.assertRaises(ValueError) as context:
            TeamGenerator("invalid_universe")
        self.assertEqual(str(context.exception),
                         "Unsupported universe specified.")

    @patch('src.utils.team_generator.SWAPIClient')
    def test_generate_team_fewer_players(self, MockSWAPIClient):
        """Test generating a team when fewer than requested number of players are returned."""
        mock_client = MockSWAPIClient.return_value
        mock_client.return_characters_as_players.return_value = [
            MagicMock() for _ in range(3)  # Return fewer players
        ]

        generator = TeamGenerator(UniverseEnum.SWAPI)
        with self.assertRaises(ValueError) as context:
            generator.generate_team(count=5)
        self.assertEqual(str(context.exception),
                         "A team must have exactly 5 players.")


if __name__ == '__main__':
    unittest.main()
