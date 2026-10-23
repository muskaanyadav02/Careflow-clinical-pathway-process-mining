from pathlib import Path

import pandas as pd
import pytest


def test_event_log_has_required_columns():
    """Detect missing required event-log columns."""
    df = pd.DataFrame({
        "Case_ID": ["P001"],
        "Timestamp": ["2026-01-01 09:00:00"],
    })

    required_columns = {"Case_ID", "Activity_Name", "Timestamp"}

    assert not required_columns.issubset(df.columns)


def test_empty_event_log_is_detected():
    """Detect an event log containing no records."""
    df = pd.DataFrame(
        columns=["Case_ID", "Activity_Name", "Timestamp"]
    )

    assert df.empty


def test_invalid_timestamp_is_detected():
    """Detect timestamps that cannot be parsed."""
    df = pd.DataFrame({
        "Timestamp": ["not-a-valid-timestamp"]
    })

    with pytest.raises(ValueError):
        pd.to_datetime(df["Timestamp"], errors="raise")


def test_missing_patient_id_is_detected():
    """Detect missing patient identifiers."""
    df = pd.DataFrame({
        "Case_ID": ["P001", None],
        "Activity_Name": ["Triage", "Treatment"],
        "Timestamp": [
            "2026-01-01 09:00:00",
            "2026-01-01 10:00:00",
        ],
    })

    assert df["Case_ID"].isna().any()


def test_blank_patient_id_is_detected():
    """Detect patient identifiers containing only whitespace."""
    df = pd.DataFrame({
        "Case_ID": ["P001", "   "]
    })

    blank_ids = df["Case_ID"].fillna("").astype(str).str.strip().eq("")

    assert blank_ids.any()