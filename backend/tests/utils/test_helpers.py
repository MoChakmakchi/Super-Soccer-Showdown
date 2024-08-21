import unittest
from unittest.mock import patch, MagicMock
from src.utils.models.types import UniverseEnum, StrategyEnum
from src.entities.team import Team
from src.entities.player import Player
from src.utils.helpers import get_team, create_team, replace_team, change_team_strategy


class TestTeamOperations(unittest.TestCase):

    @patch('src.utils.helpers.TeamGenerator')
    def test_get_team_existing(self, MockTeamGenerator):
        """Test getting an existing team."""
        # Create mock players
        mock_goalie = MagicMock(Player)
        mock_attackers = [MagicMock(Player) for _ in range(3)]
        mock_defenders = [MagicMock(Player) for _ in range(2)]

        # Create a mock team
        mock_team = MagicMock(Team)
        mock_team.universe = UniverseEnum.SWAPI
        mock_team.goalie = mock_goalie
        mock_team.attackers = mock_attackers
        mock_team.defenders = mock_defenders

        current_teams = [mock_team]

        # Test the function
        result = get_team(UniverseEnum.SWAPI, current_teams)

        # Verify that the correct team details are returned
        self.assertEqual(result['goalie'], mock_goalie)
        self.assertEqual(result['attackers'], mock_attackers)
        self.assertEqual(result['defenders'], mock_defenders)

    def test_get_team_not_found(self):
        """Test getting a team when no team exists for the universe."""
        current_teams = []
        with self.assertRaises(ValueError) as context:
            get_team(UniverseEnum.SWAPI, current_teams)
        self.assertEqual(str(context.exception),
                         "No existing team found for universe: UniverseEnum.SWAPI")

    @patch('src.utils.helpers.TeamGenerator')
    def test_create_team(self, MockTeamGenerator):
        """Test creating a new team and adding it to the list."""
        # Create mock players
        mock_goalie = MagicMock(Player)
        mock_attackers = [MagicMock(Player) for _ in range(3)]
        mock_defenders = [MagicMock(Player) for _ in range(2)]

        # Create a mock team
        mock_team = MagicMock(Team)
        mock_team.goalie = mock_goalie
        mock_team.attackers = mock_attackers
        mock_team.defenders = mock_defenders
        mock_team.universe = UniverseEnum.SWAPI

        # Mock TeamGenerator
        MockTeamGenerator.return_value.generate_team.return_value = mock_team

        current_teams = []

        # Test the function
        result = create_team(UniverseEnum.SWAPI, current_teams)

        # Verify that the created team is added to the list and has the correct details
        self.assertEqual(result['goalie'], mock_goalie)
        self.assertEqual(result['attackers'], mock_attackers)
        self.assertEqual(result['defenders'], mock_defenders)
        self.assertIn(mock_team, current_teams)

    @patch('src.utils.helpers.TeamGenerator')
    def test_replace_team(self, MockTeamGenerator):
        """Test replacing an existing team with a new one."""
        # Create mock players
        mock_goalie = MagicMock(Player)
        mock_attackers = [MagicMock(Player) for _ in range(3)]
        mock_defenders = [MagicMock(Player) for _ in range(2)]

        # Create old and new mock teams
        old_team = MagicMock(Team)
        old_team.universe = UniverseEnum.SWAPI

        new_team = MagicMock(Team)
        new_team.goalie = mock_goalie
        new_team.attackers = mock_attackers
        new_team.defenders = mock_defenders
        new_team.universe = UniverseEnum.SWAPI

        # Mock TeamGenerator
        MockTeamGenerator.return_value.generate_team.return_value = new_team

        current_teams = [old_team]

        # Test the function
        result = replace_team(UniverseEnum.SWAPI, current_teams)

        # Verify that the new team replaces the old team and has the correct details
        self.assertEqual(result['goalie'], mock_goalie)
        self.assertEqual(result['attackers'], mock_attackers)
        self.assertEqual(result['defenders'], mock_defenders)
        self.assertEqual(current_teams[0], new_team)

    def test_replace_team_not_found(self):
        """Test replacing a team when no team exists for the universe."""
        current_teams = []
        with self.assertRaises(ValueError) as context:
            replace_team(UniverseEnum.SWAPI, current_teams)
        self.assertEqual(str(context.exception),
                         "No existing team found for universe: UniverseEnum.SWAPI")

    @patch('src.utils.helpers.TeamGenerator')
    def test_change_team_strategy(self, MockTeamGenerator):
        """Test changing the strategy of an existing team."""
        # Create mock players
        mock_goalie = MagicMock(Player)
        mock_attackers = [MagicMock(Player) for _ in range(3)]
        mock_defenders = [MagicMock(Player) for _ in range(2)]

        # Create a mock team
        mock_team = MagicMock(Team)
        mock_team.universe = UniverseEnum.SWAPI
        mock_team.goalie = mock_goalie
        mock_team.attackers = mock_attackers
        mock_team.defenders = mock_defenders

        # Set initial strategy
        mock_team.lineup_strategy = StrategyEnum.balanced

        current_teams = [mock_team]

        # Test changing the strategy
        result = change_team_strategy(
            UniverseEnum.SWAPI, 'balanced', current_teams)

        # Verify that the strategy is updated and the team details are correct
        self.assertEqual(result['goalie'], mock_goalie)
        self.assertEqual(result['attackers'], mock_attackers)
        self.assertEqual(result['defenders'], mock_defenders)
        self.assertEqual(
            current_teams[0].lineup_strategy, StrategyEnum.balanced)

    def test_change_team_strategy_not_found(self):
        """Test changing the strategy when no team exists for the universe."""
        current_teams = []
        with self.assertRaises(ValueError) as context:
            change_team_strategy(UniverseEnum.SWAPI, 'balanced', current_teams)
        self.assertEqual(str(context.exception),
                         "No existing team found for universe: UniverseEnum.SWAPI")

if __name__ == '__main__':
    unittest.main()
