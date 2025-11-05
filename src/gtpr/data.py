import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pathlib

    from team import Team


def write_team(team: Team, path: pathlib.Path, *, override: bool = False) -> bool:
    path.parent.mkdir(exist_ok=True)
    try:
        path.touch(exist_ok=override)
    except FileExistsError:
        return False
    with path.open("w") as jsonfile:
        json.dump(team.model_dump(), jsonfile)
    return True
