import custominput


def calculate_personal_dps_importance(
    original_dps: int,
    no_substat_dps: int,
    original_personal_dps: int,
    no_substat_personal_dps: int,
) -> float:
    dps_difference = original_dps - no_substat_dps
    personal_dps_difference = original_personal_dps - no_substat_personal_dps
    return personal_dps_difference / dps_difference


if __name__ == "__main__":
    original_dps = input("originaldps")
    no_sub_dps = input("no_sub_dps")
    original_personal_dps = input("originalmydps")
    no_sub_personal_dps = input("nosubpersonaldps")
    print(
        calculate_personal_dps_importance(
            original_dps=int(original_dps),
            no_substat_dps=int(no_sub_dps),
            original_personal_dps=int(original_personal_dps),
            no_substat_personal_dps=int(no_sub_personal_dps),
        )
    )
