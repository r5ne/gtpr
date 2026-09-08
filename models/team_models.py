import math

from pydantic import BaseModel, Field

MAX_ROLL_VALUE = 4500

class CharacterBuild(BaseModel):
    name: str = "Empty slot"
    dps_floor: int = 0
    dps_ceiling: int = 0
    roll_value: int = 0

    def get_progress(self, team_dps: int) -> float:
        if self.dps_floor == self.dps_ceiling:
            return 0.0
        return (team_dps - self.dps_floor) / (self.dps_ceiling - self.dps_floor)

    def get_upgrade_difficulty(self) -> float:
        # MAX ROLL VALUE (max_rolls) = 45
        # ROLL DISTRIBUTION STANDARD DEVIATION (sd) = 15
        # ( e^-( (roll_value/sd)^2 ) - e^-( (max_rolls/sd)^2 ) ) ) / ( 1-e^-( (max_rolls/sd)^2 ) )

        core_term = math.exp(-(self.roll_value ** 2) / 2250000)
        return (core_term - 0.00012341) / 0.99987659

    def get_raw_priority_score(self, team_dps: int) -> float:
        return self.get_upgrade_difficulty() * (self.dps_ceiling - team_dps)


class Team(BaseModel):
    name: str
    team_dps: int = 0
    character_builds: list[CharacterBuild] = Field(
        default_factory=lambda: [CharacterBuild(name=f"Character {i+1}") for i in range(4)]
    )

    @property
    def total_raw_priority(self) -> float:
        return sum(char.get_raw_priority_score(self.team_dps) for char in self.character_builds)

    def get_relative_priority_score(self, character: CharacterBuild) -> float:
        total = self.total_raw_priority
        if total == 0:
            return 0.0
        return character.get_raw_priority_score(self.team_dps) / total
