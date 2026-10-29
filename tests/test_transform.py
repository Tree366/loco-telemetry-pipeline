import pandas as pd
import pytest

from loco_pipeline import transform


def make_row(**overrides):
    row = {
        "timestamp": "2026-01-01 00:00:00", "unit_id": "U1", "notch": 8,
        "engine_speed_rpm": 1100.0, "fuel_rate_gph": 180.0,
        "coolant_temp_f": 212.0, "oil_pressure_psi": 80.0,
    }
    row.update(overrides)
    return row


def test_f_to_c_known_points():
    assert transform.f_to_c(32) == pytest.approx(0)
    assert transform.f_to_c(212) == pytest.approx(100)


def test_to_si_conversions():
    out = transform.to_si(pd.DataFrame([make_row()]))
    assert out.loc[0, "fuel_rate_lph"] == pytest.approx(180 * 3.78541)
    assert out.loc[0, "coolant_temp_c"] == pytest.approx(100)
    assert out.loc[0, "oil_pressure_kpa"] == pytest.approx(80 * 6.89476)


@pytest.mark.parametrize("bad", [
    {"notch": 9}, {"notch": -1}, {"engine_speed_rpm": -1}, {"fuel_rate_gph": None},
])
def test_clean_drops_invalid_rows(bad):
    df = pd.DataFrame([make_row(), make_row(**bad)])
    assert len(transform.clean(df)) == 1


def test_missing_column_raises():
    df = pd.DataFrame([make_row()]).drop(columns=["notch"])
    with pytest.raises(ValueError, match="notch"):
        transform.clean(df)
