import pandas as pd
from pathlib import Path

results_file = Path("data/processed/conformance_results.csv")
summary_file = Path("data/processed/deviation_summary.csv")

# Check whether the required files exist
if not results_file.exists() or not summary_file.exists():
    raise FileNotFoundError("Required analysis output file not found.")

results = pd.read_csv(results_file)
summary = pd.read_csv(summary_file)

print("===== DEVIATION SUMMARY VALIDATION =====")

# 1. Validate the patient-level results
required_result_columns = {
    "Case_ID",
    "Exact_Match",
    "Additional_Activities",
    "Missing_Activities",
    "First_Difference",
}

if not required_result_columns.issubset(results.columns):
    raise ValueError("Required columns are missing from conformance results.")

if results["Case_ID"].isna().any():
    raise ValueError("Missing patient case identifiers found.")

if results["Case_ID"].duplicated().any():
    raise ValueError("Duplicate patient case identifiers found.")

exact_matches = (
    results["Exact_Match"]
    .astype(str)
    .str.lower()
    .eq("true")
    .sum()
)

different_journeys = (
    results["Exact_Match"]
    .astype(str)
    .str.lower()
    .eq("false")
    .sum()
)

assert exact_matches + different_journeys == len(results), (
    "Some journeys have an invalid Exact_Match value."
)

print(f"Patient-level records: {len(results)}")
print(f"Exact matches: {exact_matches}")
print(f"Different journeys: {different_journeys}")

# 2. Validate the summary file structure
required_summary_columns = {"Category", "Finding", "Patient_Count"}

if not required_summary_columns.issubset(summary.columns):
    raise ValueError("Required columns are missing from deviation summary.")

if summary.duplicated(["Category", "Finding"]).any():
    raise ValueError("Duplicate summary findings found.")

# 3. Compare overall summary counts with patient-level results
overall = summary[summary["Category"] == "Overall"]

def get_summary_count(finding):
    matching_rows = overall.loc[
        overall["Finding"] == finding, "Patient_Count"
    ]

    if len(matching_rows) != 1:
        raise ValueError(f"Missing or duplicate summary finding: {finding}")

    return int(matching_rows.iloc[0])

assert get_summary_count("Total patient journeys") == len(results)
assert get_summary_count("Exact pathway matches") == exact_matches
assert get_summary_count(
    "Journeys differing from expected pathway"
) == different_journeys

# 4. Recalculate additional-activity counts from patient-level results
expected_additional = {}

for activities in results["Additional_Activities"].dropna():
    for activity in str(activities).split(","):
        activity = activity.strip()

        if activity:
            expected_additional[activity] = (
                expected_additional.get(activity, 0) + 1
            )

actual_additional = summary[
    summary["Category"] == "Additional Activity"
]

actual_additional = dict(
    zip(actual_additional["Finding"], actual_additional["Patient_Count"])
)

assert actual_additional == expected_additional, (
    "Additional-activity counts do not match the patient-level results."
)

# 5. Validate first-difference counts
first_difference_count = results["First_Difference"].notna().sum()

expected_difference_count = different_journeys

assert first_difference_count == expected_difference_count, (
    "First-difference count does not match different journeys."
)

first_difference_row = summary[
    summary["Category"].astype(str).str.startswith("First Difference")
]

assert len(first_difference_row) == 1, (
    "Missing or duplicate first-difference summary."
)

assert int(first_difference_row["Patient_Count"].iloc[0]) == first_difference_count, (
    "First-difference summary count does not match detailed results."
)
# 6. Confirm all summary counts are valid
if (summary["Patient_Count"] < 0).any():
    raise ValueError("Negative patient counts found.")

print(f"Journeys with a first difference: {first_difference_count}")
print("First-difference validation passed!")