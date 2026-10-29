"""Object-oriented wrapper that runs the full ingest -> clean -> analyze chain."""
from pathlib import Path

import pandas as pd

from . import analyze, transform


class TelemetryPipeline:
    def __init__(self, overtemp_limit_c: float = 100.0):
        self.overtemp_limit_c = overtemp_limit_c

    def ingest(self, source) -> pd.DataFrame:
        """Load raw data. Accepts a CSV path or an existing DataFrame.

        In a production version this method would call the data API instead.
        """
        if isinstance(source, pd.DataFrame):
            return source.copy()
        return pd.read_csv(Path(source))

    def run(self, source) -> dict:
        raw = self.ingest(source)
        data = transform.to_si(transform.clean(raw))
        return {
            "data": data,
            "notch_summary": analyze.summarize_by_notch(data),
            "overtemp_units": analyze.flag_overtemp(data, self.overtemp_limit_c),
            "rows_dropped": len(raw) - len(data),
        }
