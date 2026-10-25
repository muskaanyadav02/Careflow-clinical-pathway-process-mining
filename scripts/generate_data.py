import argparse
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = (
    PROJECT_ROOT / "data" / "sample" / "sample_event_log.csv"
)

FIELDNAMES = ["Case_ID", "Activity_Name", "Timestamp"]


def generate_patient_journey(case_number, rng):
    """Generate one simulated hospital patient journey."""

    case_id = f"P{case_number:05d}"

    # Each patient arrives at a different time.
    current_time = datetime(2026, 10, 1, 8, 0)
    current_time += timedelta(minutes=rng.randint(0, 600))

    events = []

    def add_event(activity, wait_min=5, wait_max=30):
        """Add an activity after a simulated waiting/processing time."""
        nonlocal current_time

        current_time += timedelta(
            minutes=rng.randint(wait_min, wait_max)
        )

        events.append({
            "Case_ID": case_id,
            "Activity_Name": activity,
            "Timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        })

    # Registration and triage
    add_event("Patient Registration", 1, 5)
    add_event("Triage", 5, 20)

    # Simulated consultation delays
    if rng.random() < 0.25:
        add_event("Doctor Consultation", 60, 150)
    else:
        add_event("Doctor Consultation", 10, 40)

    # Not every patient needs a lab test
    if rng.random() < 0.75:
        if rng.random() < 0.20:
            add_event("Lab Test", 60, 120)
        else:
            add_event("Lab Test", 10, 35)

        # Occasional repeat lab tests
        if rng.random() < 0.12:
            add_event("Repeat Lab Test", 20, 60)

        add_event("Lab Results Review", 10, 45)

        # Some patients return for another consultation
        if rng.random() < 0.30:
            add_event("Doctor Consultation", 15, 75)

    # Treatment and discharge
    add_event("Treatment", 10, 45)
    add_event("Discharge", 5, 30)

    return events


def generate_dataset(case_count, output_file, seed=42):
    """Generate a reproducible simulated hospital event log."""

    rng = random.Random(seed)
    all_events = []

    for case_number in range(1, case_count + 1):
        all_events.extend(
            generate_patient_journey(case_number, rng)
        )

    # Order events by case and timestamp
    all_events.sort(
        key=lambda event: (event["Case_ID"], event["Timestamp"])
    )

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open(
        "w", newline="", encoding="utf-8"
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file, fieldnames=FIELDNAMES
        )
        writer.writeheader()
        writer.writerows(all_events)

    print("Simulated hospital dataset generated successfully!")
    print(f"Patient cases: {case_count}")
    print(f"Total events: {len(all_events)}")
    print(f"Saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate simulated hospital event-log data."
    )
    parser.add_argument(
        "--cases",
        type=int,
        default=100,
        help="Number of patient cases to generate (default: 100).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output CSV path.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible data (default: 42).",
    )

    args = parser.parse_args()

    if args.cases < 1:
        parser.error("--cases must be at least 1.")

    generate_dataset(args.cases, args.output, args.seed)


if __name__ == "__main__":
    main()