
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FILE = PROJECT_ROOT / "data" / "sample" / "sample_event_log.csv"

REQUIRED_COLUMNS = ["Case_ID", "Activity_Name", "Timestamp"]

EXPECTED_ACTIVITIES = {
    "Patient Registration",
    "Triage",
    "Doctor Consultation",
    "Lab Test",
    "Repeat Lab Test",
    "Lab Results Review",
    "Treatment",
    "Discharge",
}


def validate_event_log(file_path):
    """Validate the structure and quality of a hospital event log."""

    errors = []
    warnings = []

    if not file_path.exists():
        return ["File not found: {}".format(file_path)], warnings

    try:
        data = pd.read_csv(file_path)
    except (OSError, pd.errors.ParserError, UnicodeDecodeError) as exc:
        return [f"Could not read CSV: {exc}"], warnings

    # 1. Check required columns
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        errors.append(f"Missing required columns: {missing_columns}")
        return errors, warnings

    # 2. Check for an empty dataset
    if data.empty:
        errors.append("Dataset contains no event records.")
        return errors, warnings

    # 3. Check missing and blank values
    for column in REQUIRED_COLUMNS:
        missing = data[column].isna() | (
            data[column].astype("string").str.strip().eq("").fillna(False)
        )

        if missing.any():
            errors.append(
                f"{column}: {int(missing.sum())} missing or blank values."
            )

    # Stop checks that depend on valid identifiers or activities
    if data["Case_ID"].isna().any() or data["Activity_Name"].isna().any():
        return errors, warnings

    if (
        data["Case_ID"].astype("string").str.strip().eq("").any()
        or data["Activity_Name"].astype("string").str.strip().eq("").any()
    ):
        return errors, warnings

    # 4. Check duplicate event records
    duplicates = data.duplicated(subset=REQUIRED_COLUMNS)

    if duplicates.any():
        errors.append(f"Found {int(duplicates.sum())} duplicate events.")

    # 5. Parse and validate timestamps
    parsed_timestamps = pd.to_datetime(
        data["Timestamp"], errors="coerce"
    )

    invalid_timestamps = int(parsed_timestamps.isna().sum())

    if invalid_timestamps:
        errors.append(
            f"Found {invalid_timestamps} invalid timestamps."
        )
    else:
        data["Timestamp"] = parsed_timestamps

        # 6. Check chronological order within each patient case
        for case_id, group in data.groupby("Case_ID", sort=False):
            if not group["Timestamp"].is_monotonic_increasing:
                errors.append(
                    f"Events are not chronologically ordered for {case_id}."
                )

    # 7. Check unexpected activity names
    actual_activities = set(data["Activity_Name"].dropna().astype(str))
    unexpected = actual_activities - EXPECTED_ACTIVITIES

    if unexpected:
        warnings.append(f"Unexpected activity names: {sorted(unexpected)}")

    # 8. Check whether cases have start and end activities
    for case_id, group in data.groupby("Case_ID", sort=False):
        activities = group["Activity_Name"].tolist()

        if activities[0] != "Patient Registration":
            warnings.append(
                f"{case_id}: first event is not Patient Registration."
            )

        if activities[-1] != "Discharge":
            warnings.append(f"{case_id}: last event is not Discharge.")

    return errors, warnings


def main():
    file_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_FILE

    if not file_path.is_absolute():
        file_path = Path.cwd() / file_path

    print(f"Validating: {file_path}")

    errors, warnings = validate_event_log(file_path)

    print("\nValidation summary")
    print("------------------")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    for error in errors:
        print(f"ERROR: {error}")

    for warning in warnings:
        print(f"WARNING: {warning}")

    if errors:
        print("\nValidation FAILED.")
        sys.exit(1)

    print("\nValidation PASSED.")


if __name__ == "__main__":
    main()
