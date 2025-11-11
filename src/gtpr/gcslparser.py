import genshinconstants


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


def get_optimal_character_config_stats(config: list[str]) -> dict[str, float]:
    stats = config[4].split()[3:]
    return {stat.split("=")[0]: float(stat.split("=")[1]) for stat in stats}


def get_roll_amount_from_stats(stats: dict[str, float]) -> dict[str, float]:
    for stat, single_roll in genshinconstants.SUBSTATS.items():
        stats[stat] = round(stats[stat] / single_roll, 2)
    return stats
