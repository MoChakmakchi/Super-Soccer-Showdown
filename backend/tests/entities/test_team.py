import unittest
from src.utils.models.types import StrategyEnum, UniverseEnum
from src.entities.player import Player
from src.entities.team import Team


class TestTeam(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        self.players = [
            Player("Player1", 80.0, 1.90),
            Player("Player2", 75.0, 1.85),
            Player("Player3", 70.0, 1.80),
            Player("Player4", 65.0, 1.75),
            Player("Player5", 60.0, 1.70)
        ]
        self.team1 = Team(self.players, UniverseEnum.POKEMON,
                          StrategyEnum.balanced)
        self.team2 = Team(self.players, UniverseEnum.POKEMON,
                          StrategyEnum.balanced)

    def test_valid_initialization(self):
        """Test team initialization with valid input"""
        team = Team(self.players, UniverseEnum.POKEMON, StrategyEnum.balanced)
        self.assertEqual(len(team.players), 5,
                         "Team should have exactly 5 players.")
        self.assertEqual(team.lineup_strategy, StrategyEnum.balanced,
                         "Strategy should be 'balanced'.")

    def test_invalid_team_size(self):
        """Test initialization with an invalid number of players"""
        with self.assertRaises(ValueError) as context:
            Team(self.players[:4], UniverseEnum.SWAPI, StrategyEnum.balanced)
        self.assertEqual(str(context.exception),
                         "A team must have exactly 5 players.")

    def test_lineup_creation(self):
        """Test the lineup creation for different strategies"""
        strategies = [StrategyEnum.extreme_defence, StrategyEnum.defence,
                      StrategyEnum.balanced, StrategyEnum.attack, StrategyEnum.extreme_attack]

        for strategy in strategies:
            with self.subTest(strategy=strategy):
                team = Team(self.players, UniverseEnum.POKEMON, strategy)
                number_of_attackers = strategy
                self.assertEqual(len(team.attackers), number_of_attackers,
                                 "Number of attackers should match the strategy.")
                self.assertEqual(len(team.defenders), 5 - number_of_attackers - 1,
                                 "Number of defenders should match the strategy.")
                self.assertEqual(team.goalie, max(
                    self.players, key=lambda p: p.height), "The goalie should be the tallest player.")

    def test_strategy_change(self):
        """Test changing the strategy"""
        team = Team(self.players, UniverseEnum.POKEMON, StrategyEnum.balanced)
        team.lineup_strategy = StrategyEnum.extreme_attack
        self.assertEqual(team.lineup_strategy, StrategyEnum.extreme_attack,
                         "Strategy should be updated to 'extreme_attack'.")
        self.assertEqual(len(team.attackers), StrategyEnum.extreme_attack,
                         "Number of attackers should be updated according to the new strategy.")

    def test_no_player_in_two_positions(self):
        """Test that no player is assigned to more than one position (goalie, attacker, defender)"""
        strategies = [StrategyEnum.extreme_defence, StrategyEnum.defence,
                      StrategyEnum.balanced, StrategyEnum.attack, StrategyEnum.extreme_attack]

        for strategy in strategies:
            with self.subTest(strategy=strategy):
                team = Team(self.players, UniverseEnum.POKEMON, strategy)
                all_players = {team.goalie} | set(
                    team.attackers) | set(team.defenders)
                self.assertEqual(
                    len(all_players), 5, "No player should be assigned to more than one position.")

    def test_team_roles(self):
        """Test that the team always has a goalie and at least one of defenders or attackers."""
        strategies = [StrategyEnum.extreme_defence, StrategyEnum.defence,
                      StrategyEnum.balanced, StrategyEnum.attack, StrategyEnum.extreme_attack]

        for strategy in strategies:
            with self.subTest(strategy=strategy):
                team = Team(self.players, UniverseEnum.SWAPI, strategy)
                self.assertIsNotNone(
                    team.goalie, "There should always be a goalie.")
                # Check that there is at least one of defenders or attackers
                self.assertTrue(len(team.defenders) > 0 or len(team.attackers) > 0,
                                "There should be at least one defender or attacker.")

    def test_goalie_is_tallest(self):
        """Test that the goalie is always the tallest player."""
        strategies = [StrategyEnum.extreme_defence, StrategyEnum.defence,
                      StrategyEnum.balanced, StrategyEnum.attack, StrategyEnum.extreme_attack]

        for strategy in strategies:
            with self.subTest(strategy=strategy):
                team = Team(self.players, UniverseEnum.POKEMON, strategy)
                self.assertEqual(team.goalie.height, max(
                    p.height for p in self.players), "The goalie should be the tallest player.")

    def test_defenders_are_heaviest_excluding_goalie(self):
        """Test that defenders are the heaviest players, excluding the goalie."""
        strategies = [StrategyEnum.extreme_defence, StrategyEnum.defence,
                      StrategyEnum.balanced, StrategyEnum.attack, StrategyEnum.extreme_attack]

        for strategy in strategies:
            with self.subTest(strategy=strategy):
                team = Team(self.players, UniverseEnum.SWAPI, strategy)
                all_players = set(self.players)
                all_players.remove(team.goalie)  # Exclude the goalie

                sorted_by_weight_excluding_goalie = sorted(
                    all_players, key=lambda p: p.weight, reverse=True)
                # The number of defenders
                expected_defenders = sorted_by_weight_excluding_goalie[:4 - strategy]

                self.assertEqual(sorted(team.defenders, key=lambda p: p.weight, reverse=True),
                                 expected_defenders, "Defenders should be the heaviest players excluding the goalie.")

    def test_equal_teams(self):
        """Test equality of two teams with the same players and strategy"""
        self.assertEqual(
            self.team1, self.team2, "Teams with the same players and strategy should be equal.")

    def test_not_equal_teams(self):
        """Test inequality of teams with different players or strategies"""
        # Modify one player
        self.players[0] = Player("ModifiedPlayer", 85.0, 1.95)
        team3 = Team(self.players, UniverseEnum.POKEMON, StrategyEnum.balanced)
        self.assertNotEqual(
            self.team1, team3, "Teams with different players should not be equal.")

        # Test different strategy
        self.players[0] = Player("Player1", 80.0, 1.90)  # Reset player
        team4 = Team(self.players, UniverseEnum.POKEMON, StrategyEnum.attack)
        self.assertNotEqual(
            self.team1, team4, "Teams with different strategies should not be equal.")


if __name__ == '__main__':
    unittest.main()
