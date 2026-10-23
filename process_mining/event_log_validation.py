from pathlib import Path
import pandas as pd


REQUIRED_COLUMNS = {
    "Case_ID",
    "Activity_Name",
    "Timestamp",
}


def load_and_validate_event_log(input_file):
    """Load an event log, validate its data, and sort its events."""

    input_file = Path(input_file)

    # Check whether the input file exists
    if not input_file.exists():
        raise FileNotFoundError(
            f"Event log not found: {input_file}"
        )

    # Load the CSV file
    df = pd.read_csv(input_file)

    # Check for an empty event log
    if df.empty:
        raise ValueError("The event log contains no records.")

    # Check required columns
    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    required_columns = [
        "Case_ID",
        "Activity_Name",
        "Timestamp",
    ]

    # Check for missing values
    if df[required_columns].isna().any().any():
        raise ValueError(
            "The event log contains missing required values."
        )

    # Check for blank values
    for column in required_columns:
        df[column] = df[column].replace(
            r"^\s*$",
            pd.NA,
            regex=True,
        )

    if df[required_columns].isna().any().any():
        raise ValueError(
            "The event log contains blank required values."
        )

    # Validate timestamps
    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        errors="raise",
    )

    # Sort events by patient and timestamp
    df = df.sort_values(
        ["Case_ID", "Timestamp"]
    ).reset_index(drop=True)

    return df