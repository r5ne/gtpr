import csv


class Team:
    def __init__(self, name: str):
        self.name = name

    def mk_new_file(self):
        with open(f"{self.name}.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["skill"])
