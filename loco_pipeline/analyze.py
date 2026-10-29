"""Summary statistics and simple health checks."""
import pandas as pd


def summarize_by_notch(df: pd.DataFrame) -> pd.DataFrame:
    """Mean engine speed and fuel rate at each throttle notch."""
    return (
        df.groupby("notch")
        .agg(
            samples=("engine_speed_rpm", "size"),
            mean_rpm=("engine_speed_rpm", "mean"),
            mean_fuel_lph=("fuel_rate_lph", "mean"),
        )
        .reset_index()
    )


def flag_overtemp(df: pd.DataFrame, limit_c: float = 100.0) -> pd.DataFrame:
    """Units with any coolant reading above limit_c, with peak temperature."""
    hot = df[df["coolant_temp_c"] > limit_c]
    return (
        hot.groupby("unit_id")["coolant_temp_c"]
        .max()
        .rename("peak_coolant_c")
        .reset_index()
    )
