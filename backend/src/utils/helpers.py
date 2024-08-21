from typing import List, TypedDict
from src.utils.models.types import UniverseEnum, StrategyEnum
from src.entities.team import Team
from src.entities.player import Player
from src.utils.team_generator import TeamGenerator


class TeamCompObject(TypedDict):
    goalie: Player
    attackers: List[Player]
    defenders: List[Player]


def get_team(universe: UniverseEnum, current_teams: List[Team]) -> TeamCompObject:
    for existing_team in current_teams:
        if existing_team.universe == universe:
            return TeamCompObject(
                goalie=existing_team.goalie,
                attackers=existing_team.attackers,
                defenders=existing_team.defenders
            )
    raise ValueError(f"No existing team found for universe: {universe}")


def create_team(universe: UniverseEnum, current_teams: List[Team]) -> TeamCompObject:
    # Generate the team with the specified strategy
    team = TeamGenerator(universe).generate_team(
        lineup_strategy=StrategyEnum.balanced)

    current_teams.append(team)
    return TeamCompObject(
        goalie=team.goalie,
        attackers=team.attackers,
        defenders=team.defenders
    )


def replace_team(universe: UniverseEnum, current_teams: List[Team]) -> TeamCompObject:
    # Generate the team with the specified strategy
    team = TeamGenerator(universe).generate_team(
        lineup_strategy=StrategyEnum.balanced)

    for idx, current_team in enumerate(current_teams):
        if universe == current_team.universe:
            # Replace the existing team with the newly generated team
            current_teams[idx] = team
            return TeamCompObject(
                goalie=team.goalie,
                attackers=team.attackers,
                defenders=team.defenders
            )

    raise ValueError(f"No existing team found for universe: {universe}")


def change_team_strategy(universe: UniverseEnum, strategy: str, current_teams: List[Team]) -> TeamCompObject:
    # Convert the string to the corresponding StrategyEnum
    strategy_enum = getattr(StrategyEnum, strategy)
    for existing_team in current_teams:
        if existing_team.universe == universe:
            existing_team.lineup_strategy = strategy_enum
            return {
                "goalie": existing_team.goalie,
                "attackers": existing_team.attackers,
                "defenders": existing_team.defenders
            }

    # Raise error if team doesnt exist
    raise ValueError(f"No existing team found for universe: {universe}")
