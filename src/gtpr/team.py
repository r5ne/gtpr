import csv
from typing import TYPE_CHECKING, final

if TYPE_CHECKING:
    import pathlib


@final
class Team:
    def __init__(self, name: str, skill: str):
        self.name = name
        self.skill = skill

    def mk_new_file(self, path: pathlib.Path) -> bool:
        try:
            full_path = path / f"{self.name}.csv"
            full_path.touch(exist_ok=False)
        except FileExistsError:
            return False
        with full_path.open('w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["skill"])
            writer.writerow([self.skill])
        return True
