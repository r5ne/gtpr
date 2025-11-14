def normalise_optimal_character_config(config: list[str]) -> list[str]:
    normalised_config = []
    for line in config:
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith("#"):
            continue
        normalised_config.append(stripped_line[:-1])
    return normalised_config


def get_character_details(config: list[str]) -> dict[str, str]:
    detail_dict = {}
    detail_dict["character"] = config[0].split()[0]
    detail_dict["weapon"] = config[1].split('"')[1]
    detail_dict["artifact_set"] = config[2].split('"')[1]
    return detail_dict
