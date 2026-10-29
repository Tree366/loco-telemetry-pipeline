"""Integration test: run the full pipeline on the sample log file."""
from pathlib import Path

from loco_pipeline import TelemetryPipeline

SAMPLE = Path(__file__).parent.parent / "data" / "sample_log.csv"


def test_full_pipeline_on_sample_data():
    result = TelemetryPipeline(overtemp_limit_c=90.0).run(SAMPLE)
    assert result["rows_dropped"] == 3          # the three injected bad rows
    assert set(result["notch_summary"]["notch"]) <= set(range(9))
    assert "UNIT003" in set(result["overtemp_units"]["unit_id"])
    assert result["data"]["fuel_rate_lph"].ge(0).all()
