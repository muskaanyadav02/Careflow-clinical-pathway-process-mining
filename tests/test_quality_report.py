
import json

import pandas as pd
import pytest

from scripts.generate_quality_report import (
    generate_quality_report,
    main,
)


def test_quality_report_passes_for_valid_data(tmp_path):
    input_file = tmp_path / "events.csv"

    data = pd.DataFrame({
        "Case_ID": ["P00001", "P00001", "P00002"],
        "Activity_Name": [
            "Patient Registration",
            "Triage",
            "Patient Registration",
        ],
        "Timestamp": [
            "2026-10-01 08:00:00",
            "2026-10-01 08:10:00",
            "2026-10-01 09:00:00",
        ],
    })

    data.to_csv(input_file, index=False)

    report = generate_quality_report(input_file)

    assert report["status"] == "PASSED"
    assert report["total_events"] == 3
    assert report["unique_cases"] == 2
    assert report["invalid_timestamps"] == 0
    assert report["duplicate_events"] == 0


def test_quality_report_detects_missing_required_column(tmp_path):
    input_file = tmp_path / "events.csv"

    pd.DataFrame({
        "Case_ID": ["P00001"],
        "Activity_Name": ["Triage"],
    }).to_csv(input_file, index=False)

    with pytest.raises(ValueError, match="Missing required columns"):
        generate_quality_report(input_file)


def test_quality_report_detects_invalid_timestamp(tmp_path):
    input_file = tmp_path / "events.csv"

    pd.DataFrame({
        "Case_ID": ["P00001"],
        "Activity_Name": ["Triage"],
        "Timestamp": ["not-a-date"],
    }).to_csv(input_file, index=False)

    report = generate_quality_report(input_file)

    assert report["invalid_timestamps"] == 1
    assert report["status"] == "FAILED"


def test_quality_report_handles_missing_file(
    tmp_path, monkeypatch, capsys
):
    input_file = tmp_path / "nonexistent.csv"
    output_file = tmp_path / "report.json"

    monkeypatch.setattr(
        "sys.argv",
        [
            "generate_quality_report.py",
            "--input", str(input_file),
            "--output", str(output_file),
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    captured = capsys.readouterr()

    assert exc_info.value.code == 1
    assert "Input file not found" in captured.err
    assert not output_file.exists()


def test_quality_report_is_saved_as_json(tmp_path):
    input_file = tmp_path / "events.csv"
    output_file = tmp_path / "reports" / "report.json"

    pd.DataFrame({
        "Case_ID": ["P00001"],
        "Activity_Name": ["Triage"],
        "Timestamp": ["2026-10-01 08:00:00"],
    }).to_csv(input_file, index=False)

    monkeypatch_argv = [
        "generate_quality_report.py",
        "--input", str(input_file),
        "--output", str(output_file),
    ]

    import sys

    original_argv = sys.argv

    try:
        sys.argv = monkeypatch_argv
        main()
    finally:
        sys.argv = original_argv

    assert output_file.exists()

    saved_report = json.loads(
        output_file.read_text(encoding="utf-8")
    )

    assert saved_report["status"] == "PASSED"
    assert saved_report["total_events"] == 1
