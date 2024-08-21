from typing import List
from src.utils.models.types import StrategyEnum, UniverseEnum
from src.entities.player import Player


class Team:
    def __init__(self, players: List[Player], universe: UniverseEnum, lineup_strategy: StrategyEnum):
        if len(players) != 5:
            raise ValueError("A team must have exactly 5 players.")

        self.players: List[Player] = players
        self._universe: UniverseEnum = universe
        # lineup_strategy indicates number of attackers
        self._lineup_strategy: StrategyEnum = lineup_strategy
        self._goalie: Player
        self._attackers: List[Player]
        self._defenders: List[Player]
        self._create_lineup()

    # Note: assumption is that the order of importance is:
    # 'Goalie'(The tallest player) > 'Defence'(The heaviest players) > 'Offence'(The shortest players)
    # as per order in case description
    def _create_lineup(self):
        """Create attackers and defenders based on the strategy."""
        # Sort players by weight (heaviest first)
        sorted_by_weight = sorted(
            self.players, key=lambda p: p.weight, reverse=True)

        # Find the index of the tallest player
        tallest_player_index = max(
            range(len(sorted_by_weight)), key=lambda i: sorted_by_weight[i].height)

        # Assign the tallest player as the goalie
        self._goalie = sorted_by_weight[tallest_player_index]

        # Remove the tallest player from the list and assign as the goalie
        self._goalie = sorted_by_weight.pop(tallest_player_index)

        # Determine the number of attackers based on the strategy
        number_of_attackers = self._lineup_strategy

        # Assign players to attackers and defenders
        self._attackers = sorted_by_weight[-number_of_attackers:
                                           ] if number_of_attackers > 0 else []
        self._defenders = sorted_by_weight[:4-number_of_attackers]

    @property
    def lineup_strategy(self) -> StrategyEnum:
        return self._lineup_strategy

    @lineup_strategy.setter
    def lineup_strategy(self, new_strategy: StrategyEnum):
        """Set a new strategy and update the lineup (attackers & defenders)."""
        # Check that the strategy changed
        if new_strategy == self.lineup_strategy:
            return
        self._lineup_strategy = new_strategy
        self._create_lineup()  # Recompute lineup based on new strategy

    @property
    def universe(self) -> UniverseEnum:
        """Get the universe players are from"""
        return self._universe

    @property
    def goalie(self) -> Player:
        """Get the goalie"""
        return self._goalie

    @property
    def attackers(self) -> List[Player]:
        """Get the list of attackers"""
        return self._attackers

    @property
    def defenders(self) -> List[Player]:
        """Get the list of defenders"""
        return self._defenders

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Team):
            return False
        return (self.goalie == other.goalie and
                self.attackers == other.attackers and
                self.defenders == other.defenders)

    def __hash__(self) -> int:
        # Create a hash based on the attributes used in equality check
        return hash((self.goalie, tuple(self.attackers), tuple(self.defenders)))
