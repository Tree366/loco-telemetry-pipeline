"""Cleaning and unit conversion for raw engine telemetry."""
import pandas as pd

GAL_TO_L = 3.78541
PSI_TO_KPA = 6.89476

REQUIRED_COLUMNS = [
    "timestamp", "unit_id", "notch", "engine_speed_rpm",
    "fuel_rate_gph", "coolant_temp_f", "oil_pressure_psi",
]


def validate_columns(df: pd.DataFrame) -> None:
    """Raise ValueError if any required column is missing."""
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows with missing values or physically impossible readings."""
    validate_columns(df)
    out = df.dropna(subset=REQUIRED_COLUMNS).copy()
    out = out[out["notch"].between(0, 8)]
    out = out[(out["engine_speed_rpm"] >= 0) & (out["fuel_rate_gph"] >= 0)]
    out["timestamp"] = pd.to_datetime(out["timestamp"])
    return out.reset_index(drop=True)


def f_to_c(temp_f):
    return (temp_f - 32.0) * 5.0 / 9.0


def to_si(df: pd.DataFrame) -> pd.DataFrame:
    """Add SI-unit columns alongside the original US-unit columns."""
    out = df.copy()
    out["fuel_rate_lph"] = out["fuel_rate_gph"] * GAL_TO_L
    out["coolant_temp_c"] = f_to_c(out["coolant_temp_f"])
    out["oil_pressure_kpa"] = out["oil_pressure_psi"] * PSI_TO_KPA
    return out
