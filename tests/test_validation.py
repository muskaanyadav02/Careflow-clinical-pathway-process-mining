
from pathlib import Path

import pandas as pd

from scripts.validate_data import validate_event_log


def create_test_csv(tmp_path, data):
    file_path = tmp_path / "test_event_log.csv"
    pd.DataFrame(data).to_csv(file_path, index=False)
    return file_path


def test_valid_event_log_passes(tmp_path):
    data = {
        "Case_ID": ["P001", "P001", "P001"],
        "Activity_Name": [
            "Patient Registration",
            "Triage",
            "Discharge",
        ],
        "Timestamp": [
            "2026-10-01 08:00:00",
            "2026-10-01 08:15:00",
            "2026-10-01 09:00:00",
        ],
    }

    file_path = create_test_csv(tmp_path, data)
    errors, warnings = validate_event_log(file_path)

    assert errors == []
    assert warnings == []


def test_missing_required_column_is_detected(tmp_path):
    data = {
        "Case_ID": ["P001"],
        "Activity_Name": ["Triage"],
    }

    file_path = create_test_csv(tmp_path, data)
    errors, _ = validate_event_log(file_path)

    assert any("Missing required columns" in error for error in errors)


def test_invalid_timestamp_is_detected(tmp_path):
    data = {
        "Case_ID": ["P001"],
        "Activity_Name": ["Patient Registration"],
        "Timestamp": ["not-a-date"],
    }

    file_path = create_test_csv(tmp_path, data)
    errors, _ = validate_event_log(file_path)

    assert any("invalid timestamps" in error for error in errors)


def test_duplicate_event_is_detected(tmp_path):
    data = {
        "Case_ID": ["P001", "P001"],
        "Activity_Name": ["Triage", "Triage"],
        "Timestamp": [
            "2026-10-01 08:00:00",
            "2026-10-01 08:00:00",
        ],
    }

    file_path = create_test_csv(tmp_path, data)
    errors, _ = validate_event_log(file_path)

    assert any("duplicate events" in error for error in errors)
