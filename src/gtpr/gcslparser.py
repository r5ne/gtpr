def normalise_optimal_character_config(config: list[str]) -> list[str]:
    normalised_config = []
    for line in config:
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith("#"):
            continue
        normalised_config.append(stripped_line.rstrip(";"))
    return normalised_config


def get_character_name(config: list[str]) -> str:
    return config[0].split()[0]


def get_character_weapon(config: list[str]) -> str:
    return config[1].split('"')[1]


def get_character_artifact_set(config: list[str]) -> str:
    return config[2].split('"')[1]
