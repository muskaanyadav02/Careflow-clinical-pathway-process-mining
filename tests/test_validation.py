import pandas as pd
import pytest

from process_mining.event_log_validation import (
    load_and_validate_event_log,
)


COLUMNS = ["Case_ID", "Activity_Name", "Timestamp"]


def valid_event_log():
    """Create a small valid event log for testing."""
    return pd.DataFrame({
        "Case_ID": ["P001", "P001"],
        "Activity_Name": ["Triage", "Treatment"],
        "Timestamp": [
            "2026-01-01 09:00:00",
            "2026-01-01 10:00:00",
        ],
    })


def write_event_log(tmp_path, df):
    """Save test data to a temporary CSV file."""
    path = tmp_path / "events.csv"
    df.to_csv(path, index=False)
    return path


def test_valid_event_log_is_loaded_and_sorted(tmp_path):
    """Load a valid event log and check chronological ordering."""
    df = valid_event_log()
    path = write_event_log(tmp_path, df)

    result = load_and_validate_event_log(path)

    assert len(result) == 2
    assert COLUMNS == [
        column for column in result.columns if column in COLUMNS
    ]
    assert result["Timestamp"].is_monotonic_increasing


def test_missing_file_is_rejected(tmp_path):
    """Reject a file that does not exist."""
    with pytest.raises(FileNotFoundError):
        load_and_validate_event_log(tmp_path / "missing.csv")


def test_empty_event_log_is_rejected(tmp_path):
    """Reject a CSV containing column headers but no records."""
    df = pd.DataFrame(columns=COLUMNS)
    path = write_event_log(tmp_path, df)

    with pytest.raises(ValueError, match="no records"):
        load_and_validate_event_log(path)


def test_missing_required_column_is_rejected(tmp_path):
    """Reject an event log missing a required column."""
    df = pd.DataFrame({
        "Case_ID": ["P001"],
        "Timestamp": ["2026-01-01 09:00:00"],
    })
    path = write_event_log(tmp_path, df)

    with pytest.raises(ValueError, match="Missing required columns"):
        load_and_validate_event_log(path)


def test_missing_patient_id_is_rejected(tmp_path):
    """Reject an event log with a missing patient identifier."""
    df = valid_event_log()
    df.loc[0, "Case_ID"] = None
    path = write_event_log(tmp_path, df)

    with pytest.raises(ValueError, match="missing"):
        load_and_validate_event_log(path)


def test_blank_patient_id_is_rejected(tmp_path):
    """Reject an event log with a blank patient identifier."""
    df = valid_event_log()
    df.loc[0, "Case_ID"] = "   "
    path = write_event_log(tmp_path, df)

    with pytest.raises(ValueError, match="blank"):
        load_and_validate_event_log(path)


def test_invalid_timestamp_is_rejected(tmp_path):
    """Reject timestamps that cannot be parsed."""
    df = valid_event_log()
    df.loc[0, "Timestamp"] = "not-a-valid-timestamp"
    path = write_event_log(tmp_path, df)

    with pytest.raises(ValueError):
        load_and_validate_event_log(path)


def test_missing_activity_is_rejected(tmp_path):
    """Reject an event log with a missing activity."""
    df = valid_event_log()
    df.loc[0, "Activity_Name"] = None
    path = write_event_log(tmp_path, df)

    with pytest.raises(ValueError, match="missing"):
        load_and_validate_event_log(path)


def test_blank_timestamp_is_rejected(tmp_path):
    """Reject a blank timestamp."""
    df = valid_event_log()
    df.loc[0, "Timestamp"] = "   "
    path = write_event_log(tmp_path, df)

    with pytest.raises(ValueError, match="blank"):
        load_and_validate_event_log(path)