
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Reproducible simulated data
random.seed(42)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / "data" / "sample" / "sample_event_log.csv"

FIELDNAMES = ["Case_ID", "Activity_Name", "Timestamp"]


def generate_patient_journey(case_number):
    """Generate one simulated hospital patient journey."""

    case_id = f"P{case_number:03d}"

    # Each patient arrives at a different time
    current_time = datetime(2026, 10, 1, 8, 0)
    current_time += timedelta(minutes=random.randint(0, 600))

    events = []

    def add_event(activity, wait_min=5, wait_max=30):
        """Add an activity after a simulated waiting/processing time."""
        nonlocal current_time

        current_time += timedelta(
            minutes=random.randint(wait_min, wait_max)
        )

        events.append({
            "Case_ID": case_id,
            "Activity_Name": activity,
            "Timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        })

    # Every patient begins with registration and triage
    add_event("Patient Registration", 1, 5)
    add_event("Triage", 5, 20)

    # Some patients experience a long wait for consultation
    if random.random() < 0.25:
        add_event("Doctor Consultation", 60, 150)
    else:
        add_event("Doctor Consultation", 10, 40)

    # Some patients do not require laboratory testing
    needs_lab_test = random.random() < 0.75

    if needs_lab_test:
        # Some patients experience delays before the lab test
        if random.random() < 0.20:
            add_event("Lab Test", 60, 120)
        else:
            add_event("Lab Test", 10, 35)

        # Some tests need to be repeated
        if random.random() < 0.12:
            add_event("Repeat Lab Test", 20, 60)

        add_event("Lab Results Review", 10, 45)

        # Some patients return for another consultation
        if random.random() < 0.30:
            add_event("Doctor Consultation", 15, 75)

    # All patients proceed to treatment and discharge
    add_event("Treatment", 10, 45)
    add_event("Discharge", 5, 30)

    return events


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    all_events = []

    for case_number in range(1, 101):
        all_events.extend(generate_patient_journey(case_number))

    # Ensure events are ordered by patient and timestamp
    all_events.sort(
        key=lambda event: (event["Case_ID"], event["Timestamp"])
    )

    with OUTPUT_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file, fieldnames=FIELDNAMES
        )
        writer.writeheader()
        writer.writerows(all_events)

    print("Sample dataset generated successfully!")
    print(f"Patient cases: {len(set(e['Case_ID'] for e in all_events))}")
    print(f"Total events: {len(all_events)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
