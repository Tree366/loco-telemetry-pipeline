import pandas as pd

from loco_pipeline import analyze


def test_summarize_by_notch_means():
    df = pd.DataFrame({
        "notch": [1, 1, 8],
        "engine_speed_rpm": [300.0, 340.0, 1100.0],
        "fuel_rate_lph": [10.0, 20.0, 600.0],
    })
    s = analyze.summarize_by_notch(df).set_index("notch")
    assert s.loc[1, "samples"] == 2
    assert s.loc[1, "mean_rpm"] == 320.0
    assert s.loc[8, "mean_fuel_lph"] == 600.0


def test_flag_overtemp_only_hot_units():
    df = pd.DataFrame({
        "unit_id": ["A", "A", "B"],
        "coolant_temp_c": [95.0, 104.0, 90.0],
    })
    flagged = analyze.flag_overtemp(df, limit_c=100.0)
    assert list(flagged["unit_id"]) == ["A"]
    assert flagged.loc[0, "peak_coolant_c"] == 104.0
