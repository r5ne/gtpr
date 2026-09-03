from typing import TYPE_CHECKING
from pathlib import Path
import json

if TYPE_CHECKING:
    from models.team_models import Team

TEAM_PATH = Path.cwd() / "teams"

def write_team(team: Team, *, override: bool = False) -> None:
    TEAM_PATH.mkdir(exist_ok=True)
    path = TEAM_PATH / f"{team.name}.json"
    path.touch(exist_ok=override)
    with path.open("w") as jsonfile:
        json.dump(team.model_dump_json(), jsonfile, indent=4)
