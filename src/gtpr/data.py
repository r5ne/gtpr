import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pathlib

    from team import Team


def write_team(
    team: Team,
    path: pathlib.Path,
    *,
    override: bool = False,
) -> None:
    path.parent.mkdir(exist_ok=True)
    path.touch(exist_ok=override)
    with path.open("w") as jsonfile:
        json.dump(team.model_dump_json(), jsonfile)


def read_team(path: pathlib.Path) -> str:
    with path.open() as jsonfile:
        return json.load(jsonfile)
