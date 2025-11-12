def calculate_personal_dps_importance(
    original_dps: int,
    no_substat_dps: int,
    original_personal_dps: int,
    no_substat_personal_dps: int,
) -> float:
    dps_difference = original_dps - no_substat_dps
    personal_dps_difference = original_personal_dps - no_substat_personal_dps
    return personal_dps_difference / dps_difference
