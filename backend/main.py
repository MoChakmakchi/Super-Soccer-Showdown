from typing import List
from src.utils.models.types import UniverseEnum, UpdateStrategyBody
from src.utils.helpers import change_team_strategy, create_team, get_team, replace_team
from src.entities.team import Team
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# TODO: fix origins on deploy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: turn to JSON file for permanence
current_teams: List[Team] = []


@app.get("/api/poketeam")
def get_pokemon_team():
    return get_team(UniverseEnum.POKEMON, current_teams)


@app.post("/api/poketeam")
def create_pokemon_team():
    return create_team(UniverseEnum.POKEMON, current_teams)


@app.put("/api/poketeam")
def replace_pokemon_team():
    return replace_team(UniverseEnum.POKEMON, current_teams)


@app.patch("/api/poketeam/strategy")
def change_pokemon_plan(body: UpdateStrategyBody):
    try:
        return change_team_strategy(UniverseEnum.POKEMON, body.strategy, current_teams)

    except ValueError:
        raise HTTPException(
            status_code=400, detail=f"Invalid strategy: {body.strategy}")


@app.get("/api/swteam")
def get_star_wars_team():
    return get_team(UniverseEnum.SWAPI, current_teams)


@app.post("/api/swteam")
def create_star_wars_team():
    return create_team(UniverseEnum.SWAPI, current_teams)


@app.put("/api/swteam")
def replace_star_wars_team():
    return replace_team(UniverseEnum.SWAPI, current_teams)


@app.patch("/api/swteam/strategy")
def change_star_wars_plan(body: UpdateStrategyBody):
    try:
        return change_team_strategy(UniverseEnum.SWAPI, body.strategy, current_teams)

    except ValueError:
        raise HTTPException(
            status_code=400, detail=f"Invalid strategy: {body.strategy}")
