from pathlib import Path

from models.team_models import Team

DATA_PATH = Path.cwd() / "data"
TEAM_PATH = DATA_PATH / "teams"

def create_directories():
    TEAM_PATH.mkdir(parents=True, exist_ok=True)

def write_teams(teams: list[Team]) -> None:
    if not teams:
        return
    create_directories()

    for team in teams:
        write_team(team)

def write_team(team: Team) -> None:
    team_file_path = TEAM_PATH / f"{team.name.lower().replace(" ", "-")}.json"
    with team_file_path.open("w") as json_file:
        json_file.write(team.model_dump_json(indent=4))
