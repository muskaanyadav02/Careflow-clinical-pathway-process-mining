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
# Validate exact-match journey consistency
exact_match_flags = (
    results["Exact_Match"]
    .astype(str)
    .str.strip()
    .str.lower()
)

invalid_flags = ~exact_match_flags.isin(["true", "false"])

if invalid_flags.any():
    raise ValueError("Invalid Exact_Match values found.")

exact_match_rows = exact_match_flags.eq("true")

inconsistent_exact_matches = results.loc[
    exact_match_rows
    & (
        results["Additional_Activities"].fillna("").astype(str).str.strip().ne("")
        | results["Missing_Activities"].fillna("").astype(str).str.strip().ne("")
    )
]

if not inconsistent_exact_matches.empty:
    raise ValueError(
        "Exact-match journeys contain missing or additional activities."
    )

print("Exact-match consistency validation passed!")

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
summary_counts = pd.to_numeric(
    summary["Patient_Count"],
    errors="coerce"
)

if summary_counts.isna().any():
    raise ValueError("Missing or invalid patient counts found.")

if (summary_counts < 0).any():
    raise ValueError("Negative patient counts found.")

if (summary_counts % 1 != 0).any():
    raise ValueError("Fractional patient counts found.")

print("Summary count validation passed!")

print(f"Journeys with a first difference: {first_difference_count}")
print("First-difference validation passed!")
# 7. Validate missing-activity counts
missing_activity_count = (
    results["Missing_Activities"]
    .fillna("")
    .astype(str)
    .str.strip()
    .ne("")
    .sum()
)

missing_summary = summary[
    summary["Category"] == "Missing Activity"
]

if missing_summary.empty:
    assert missing_activity_count == 0, (
        "Patient-level missing activities exist, "
        "but the summary has no missing-activity rows."
    )
else:
    assert int(missing_summary["Patient_Count"].sum()) == missing_activity_count, (
        "Missing-activity counts do not match the summary."
    )

print(f"Journeys with missing activities: {missing_activity_count}")
print("Missing-activity validation passed!")