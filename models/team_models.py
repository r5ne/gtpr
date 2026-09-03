from pydantic import BaseModel

class Character(BaseModel):
    name: str

class Team(BaseModel):
    # Directly passed in stats
    name: str
    characters: list[Character] = []
    dps: int = 0
    per_character_dps_floor: list[int] = []
    dps_ceil: int = 0

    # Derived stats
    per_character_artifact_dps_diff: list[int] = []
    build_progress: int = 0
    unrealised_dps: int = 0

