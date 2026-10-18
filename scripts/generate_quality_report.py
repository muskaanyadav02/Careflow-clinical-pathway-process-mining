
import argparse
import json
import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_FILE = (
    PROJECT_ROOT / "data" / "raw" / "hospital_event_log_full.csv"
)

DEFAULT_OUTPUT = (
    PROJECT_ROOT / "data" / "processed" / "data_quality_report.json"
)

REQUIRED_COLUMNS = ["Case_ID", "Activity_Name", "Timestamp"]


def generate_quality_report(input_file):
    """Generate a quality report for a hospital event-log CSV."""

    input_file = Path(input_file)
    data = pd.read_csv(input_file)

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    parsed_timestamps = pd.to_datetime(
        data["Timestamp"],
        errors="coerce",
    )

    # Count events that are out of chronological order within each case.
    chronological_violations = 0

    valid_rows = data.loc[
        data["Case_ID"].notna() & parsed_timestamps.notna()
    ].copy()

    valid_rows["Parsed_Timestamp"] = (
        parsed_timestamps.loc[valid_rows.index]
    )

    for _, group in valid_rows.groupby("Case_ID", sort=False):
        timestamps = group["Parsed_Timestamp"]

        chronological_violations += int(
            (timestamps.diff().dropna() < pd.Timedelta(0)).sum()
        )

    # Count both null and blank values in required columns.
    missing_values = {}

    for column in REQUIRED_COLUMNS:
        null_count = int(data[column].isna().sum())

        blank_count = int(
            data[column]
            .astype("string")
            .str.strip()
            .eq("")
            .fillna(False)
            .sum()
        )

        missing_values[column] = null_count + blank_count

    report = {
        "input_file": str(input_file),
        "total_events": int(len(data)),
        "unique_cases": int(data["Case_ID"].nunique()),
        "unique_activities": int(data["Activity_Name"].nunique()),
        "activity_counts": {
            str(activity): int(count)
            for activity, count in (
                data["Activity_Name"].value_counts().items()
            )
        },
        "missing_values": missing_values,
        "duplicate_events": int(
            data.duplicated(subset=REQUIRED_COLUMNS).sum()
        ),
        "invalid_timestamps": int(
            parsed_timestamps.isna().sum()
        ),
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
    """Parse arguments, generate the report, and handle input errors."""

    parser = argparse.ArgumentParser(
        description="Generate a CareFlow data-quality report."
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_FILE,
        help="Input event-log CSV file.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output JSON report path.",
    )

    args = parser.parse_args()

    try:
        report = generate_quality_report(args.input)

    except FileNotFoundError:
        print(
            f"ERROR: Input file not found: {args.input}",
            file=sys.stderr,
        )
        sys.exit(1)

    except pd.errors.EmptyDataError:
        print(
            f"ERROR: Input CSV is empty: {args.input}",
            file=sys.stderr,
        )
        sys.exit(1)

    except pd.errors.ParserError as error:
        print(
            f"ERROR: Unable to parse input CSV: {error}",
            file=sys.stderr,
        )
        sys.exit(1)

    except ValueError as error:
        print(
            f"ERROR: {error}",
            file=sys.stderr,
        )
        sys.exit(1)

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    args.output.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=2))
    print(f"\nReport saved to: {args.output}")


if __name__ == "__main__":
    main()
