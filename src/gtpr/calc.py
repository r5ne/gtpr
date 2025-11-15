from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import team


def calculate_dps_diffs(team: team.Team, team_build: team.TeamBuild) -> None:
    for character in team.characters:
        team_build.character_no_substat_dps_diff[character.id] = (
            team_build.team_dps - team_build.character_no_substat_dps[character.id]
        )
        team_build.character_no_substat_optimal_dps_diff[character.id] = (
            team_build.character_optimal_artifact_dps[character.id]
            - team_build.character_no_substat_dps[character.id]
        )
    team_build.team_no_substat_optimal_dps_diff = sum(
        team_build.character_no_substat_optimal_dps_diff.values()
    )


def calculate_substat_importance(team: team.Team, team_build: team.TeamBuild) -> None:
    for character in team.characters:
        team_build.absolute_character_substat_power[character.id] = (
            team_build.character_no_substat_dps_diff[character.id]
            / team_build.character_no_substat_optimal_dps_diff[character.id]
        )
        team_build.relative_character_substat_power[character.id] = (
            team_build.character_no_substat_dps_diff[character.id]
            / team_build.team_no_substat_optimal_dps_diff
        )
        team_build.character_substat_importance[character.id] = (
            team_build.character_no_substat_optimal_dps_diff[character.id]
            / team_build.team_no_substat_optimal_dps_diff
        )
