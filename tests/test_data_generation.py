
import pandas as pd

from scripts.generate_data import generate_dataset


def test_generator_creates_requested_number_of_cases(tmp_path):
    output_file = tmp_path / "test_events.csv"

    generate_dataset(10, output_file, seed=42)

    data = pd.read_csv(output_file)

    assert data["Case_ID"].nunique() == 10


def test_generator_creates_required_columns(tmp_path):
    output_file = tmp_path / "test_events.csv"

    generate_dataset(10, output_file, seed=42)

    data = pd.read_csv(output_file)

    assert list(data.columns) == [
        "Case_ID",
        "Activity_Name",
        "Timestamp",
    ]


def test_timestamps_are_chronological_within_each_case(tmp_path):
    output_file = tmp_path / "test_events.csv"

    generate_dataset(10, output_file, seed=42)

    data = pd.read_csv(output_file)
    data["Timestamp"] = pd.to_datetime(data["Timestamp"])

    for _, group in data.groupby("Case_ID"):
        assert group["Timestamp"].is_monotonic_increasing


def test_generator_is_reproducible_with_same_seed(tmp_path):
    first_file = tmp_path / "first.csv"
    second_file = tmp_path / "second.csv"

    generate_dataset(10, first_file, seed=42)
    generate_dataset(10, second_file, seed=42)

    first = pd.read_csv(first_file)
    second = pd.read_csv(second_file)

    pd.testing.assert_frame_equal(first, second)


def test_generator_creates_output_directory(tmp_path):
    output_file = tmp_path / "new_folder" / "events.csv"

    generate_dataset(5, output_file, seed=42)

    assert output_file.exists()


def test_generator_rejects_zero_cases():
    import pytest

    from scripts.generate_data import main

    # The CLI should reject zero cases before generating data.
    import sys

    old_argv = sys.argv
    try:
        sys.argv = [
            "generate_data.py",
            "--cases", "0",
        ]

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 2
    finally:
        sys.argv = old_argv
