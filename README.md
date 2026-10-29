# Locomotive Telemetry Pipeline (example)

A small Python data pipeline that ingests engine telemetry logs, cleans invalid
readings, converts US units to SI, and produces per-notch performance summaries
and coolant over-temperature flags.

All data in `data/` is **synthetic** and generated for demonstration.

## Structure
- `loco_pipeline/transform.py` – validation, cleaning, unit conversion
- `loco_pipeline/analyze.py` – notch summaries and health checks
- `loco_pipeline/pipeline.py` – `TelemetryPipeline` class running the full chain
- `tests/` – unit tests (transform, analyze) and an integration test (full pipeline)
- `.github/workflows/ci.yml` – GitHub Actions runs the test suite on every push

## Run locally
    pip install -r requirements.txt
    pytest -v
