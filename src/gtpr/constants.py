import pathlib

TEAM_FOLDER_NAME = "teams"
TEAM_PATH = pathlib.Path.cwd() / TEAM_FOLDER_NAME
EXIT_VALUE = "\\q"

SKILL = ("nope", "barely", "playable", "good", "mastered")
SUBSTAT_VALUE = {
    0.0: "just enough energy",
    0.2: "weak",
    0.4: "mid",
    0.5: "aight",
    0.6: "good",
    0.7: "great",
    0.8: "insane",
    0.9: "perfect",
}
