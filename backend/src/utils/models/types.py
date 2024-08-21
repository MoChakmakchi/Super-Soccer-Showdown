from enum import Enum, IntEnum
from pydantic import BaseModel


class UniverseEnum(Enum):
    POKEMON = 'pokemon'
    SWAPI = 'swapi'


class StrategyEnum(IntEnum):
    # A class selects the attacker-defender distribution.
    # The number indicates the number of attackers.
    extreme_defence = 0
    defence = 1
    balanced = 2
    attack = 3
    extreme_attack = 4

class UpdateStrategyBody(BaseModel):
    strategy: str