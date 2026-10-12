import pandas as pd

# Step 1: Load patient event data
file_path = "data/sample/sample_event_log.csv"
df = pd.read_csv(file_path)

# Step 2: Convert timestamps
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Step 3: Sort activities by patient and time
df = df.sort_values(["Case_ID", "Timestamp"])

# Step 4: Build each patient's actual journey
patient_journeys = (
    df.groupby("Case_ID")["Activity_Name"]
    .apply(list)
)

# Step 5: Define a sample expected pathway
expected_pathway = [
    "Patient Registration",
    "Triage",
    "Doctor Consultation",
    "Treatment",
    "Discharge"
]

# Step 6: Compare actual journeys with the expected pathway
print("\n===== CAREFLOW CONFORMANCE CHECK =====")

print("Expected pathway:")
print(" -> ".join(expected_pathway))

matching_patients = 0
different_patients = 0

for case_id, journey in patient_journeys.items():
    if journey == expected_pathway:
        matching_patients += 1
    else:
        different_patients += 1

print("\nTotal patients:", len(patient_journeys))
print("Exact pathway matches:", matching_patients)
print("Different from expected pathway:", different_patients)

print("\n===== CHECK COMPLETED =====")