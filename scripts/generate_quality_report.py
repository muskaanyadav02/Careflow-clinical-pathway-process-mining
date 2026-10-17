
import argparse
import json
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FILE = PROJECT_ROOT / "data" / "raw" / "hospital_event_log_full.csv"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "processed" / "data_quality_report.json"

REQUIRED_COLUMNS = ["Case_ID", "Activity_Name", "Timestamp"]


def generate_quality_report(input_file):
    data = pd.read_csv(input_file)

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    parsed_timestamps = pd.to_datetime(data["Timestamp"], errors="coerce")

    chronological_violations = 0
    valid_rows = data.loc[
        data["Case_ID"].notna() & parsed_timestamps.notna()
    ].copy()
    valid_rows["Parsed_Timestamp"] = parsed_timestamps.loc[valid_rows.index]

    for _, group in valid_rows.groupby("Case_ID", sort=False):
        ordered = group["Parsed_Timestamp"]
        chronological_violations += int((ordered.diff().dropna() < pd.Timedelta(0)).sum())

    missing_values = {
        column: int(
            data[column].isna().sum()
            + (
                data[column].astype("string").str.strip().eq("").fillna(False)
            ).sum()
        )
        for column in REQUIRED_COLUMNS
    }

    report = {
        "input_file": str(input_file),
        "total_events": int(len(data)),
        "unique_cases": int(data["Case_ID"].nunique()),
        "unique_activities": int(data["Activity_Name"].nunique()),
        "activity_counts": {
            str(activity): int(count)
            for activity, count in data["Activity_Name"].value_counts().items()
        },
        "missing_values": missing_values,
        "duplicate_events": int(data.duplicated(
            subset=REQUIRED_COLUMNS
        ).sum()),
        "invalid_timestamps": int(parsed_timestamps.isna().sum()),
        "chronological_violations": chronological_violations,
    }

    report["status"] = (
        "PASSED"
        if (
            not any(missing_values.values())
            and report["duplicate_events"] == 0
            and report["invalid_timestamps"] == 0
            and chronological_violations == 0
        )
        else "FAILED"
    )

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Generate a CareFlow data-quality report."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_FILE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    report = generate_quality_report(args.input)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=2))
    print(f"\nReport saved to: {args.output}")


if __name__ == "__main__":
    main()
