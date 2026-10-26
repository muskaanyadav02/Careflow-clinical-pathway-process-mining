import pandas as pd
from pathlib import Path

# Step 1: Load and validate patient event data
file_path = Path("data/sample/sample_event_log.csv")

if not file_path.exists():
    raise FileNotFoundError(
        f"Event log file not found: {file_path}"
    )

df = pd.read_csv(file_path)

if df.empty:
    raise ValueError("The event log is empty.")

# Step 2: Validate required columns
required_columns = {"Case_ID", "Activity_Name", "Timestamp"}

missing_columns = required_columns - set(df.columns)

if missing_columns:
    raise ValueError(
        f"Missing required columns: {sorted(missing_columns)}"
    )

# Step 3: Validate and prepare the data
for column in ["Case_ID", "Activity_Name", "Timestamp"]:
    df[column] = df[column].replace(r"^\s*$", pd.NA, regex=True)

if df[["Case_ID", "Activity_Name", "Timestamp"]].isna().any().any():
    raise ValueError(
        "Event log contains missing or blank case IDs, "
        "activity names, or timestamps."
    )

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)

if df["Timestamp"].isna().any():
    raise ValueError(
        "Event log contains invalid timestamps. "
        "Please correct them before running conformance analysis."
    )

df = df.sort_values(["Case_ID", "Timestamp"])

# Step 4: Build each patient's actual journey
patient_journeys = df.groupby("Case_ID")["Activity_Name"].apply(list)

# Step 5: Define an illustrative expected pathway
# This is for demonstration and is not a clinically approved standard.
expected_pathway = [
    "Patient Registration",
    "Triage",
    "Doctor Consultation",
    "Treatment",
    "Discharge"
]

# Step 6: Compare actual journeys with the expected pathway
results = []

for case_id, journey in patient_journeys.items():

    missing_activities = [
        activity
        for activity in expected_pathway
        if activity not in journey
    ]

    additional_activities = [
        activity
        for activity in journey
        if activity not in expected_pathway
    ]

    matching_positions = min(
        len(journey),
        len(expected_pathway)
    )

    first_difference = "None"

    for index in range(matching_positions):
        if journey[index] != expected_pathway[index]:
            first_difference = (
                f"Position {index + 1}: expected "
                f"'{expected_pathway[index]}', found "
                f"'{journey[index]}'"
            )
            break

    if (
        first_difference == "None"
        and len(journey) != len(expected_pathway)
    ):
        first_difference = (
            f"Journey lengths differ "
            f"(expected {len(expected_pathway)}, "
            f"found {len(journey)})"
        )

    exact_match = journey == expected_pathway

    results.append({
        "Case_ID": case_id,
        "Actual_Journey": " -> ".join(journey),
        "Exact_Match": exact_match,
        "Missing_Activities": ", ".join(missing_activities) or "None",
        "Additional_Activities": ", ".join(additional_activities) or "None",
        "First_Difference": first_difference
    })

# Step 7: Display summary
results_df = pd.DataFrame(results)

matching_patients = int(results_df["Exact_Match"].sum())
total_patients = len(results_df)
different_patients = total_patients - matching_patients

print("\n===== CAREFLOW CONFORMANCE CHECK =====")

print("\nIllustrative expected pathway:")
print(" -> ".join(expected_pathway))

print("\nTotal patients analyzed:", total_patients)
print("Exact pathway matches:", matching_patients)
print("Different from expected pathway:", different_patients)

if total_patients > 0:
    match_percentage = matching_patients / total_patients * 100
    print(f"Exact match percentage: {match_percentage:.2f}%")

# Step 8: Save patient-level results
output_path = Path("data/processed/conformance_results.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

results_df.to_csv(output_path, index=False)

print("\nDetailed results saved to:", output_path)
print("\n===== CHECK COMPLETED =====")
