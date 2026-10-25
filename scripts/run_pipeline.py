
import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_DATASET = (
    PROJECT_ROOT / "data" / "raw" / "hospital_event_log_full.csv"
)

DEFAULT_REPORT = (
    PROJECT_ROOT / "data" / "processed" / "data_quality_report.json"
)


def run_step(description, command):
    """Run one pipeline step and stop if it fails."""

    print(f"\n{'=' * 60}")
    print(description)
    print("=" * 60)

    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        check=False,
    )

    if result.returncode != 0:
        print(
            f"\nPIPELINE FAILED: {description}",
            file=sys.stderr,
        )
        return False

    print(f"\nSUCCESS: {description}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Run the CareFlow data engineering pipeline."
    )

    parser.add_argument(
        "--cases",
        type=int,
        default=1500,
        help="Number of patient cases to generate (default: 1500).",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible data.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_DATASET,
        help="Path for the generated event-log CSV.",
    )

    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_REPORT,
        help="Path for the JSON quality report.",
    )

    args = parser.parse_args()

    if args.cases < 1:
        parser.error("--cases must be at least 1")

    dataset_path = args.output
    report_path = args.report

    if not dataset_path.is_absolute():
        dataset_path = PROJECT_ROOT / dataset_path

    if not report_path.is_absolute():
        report_path = PROJECT_ROOT / report_path

    python = sys.executable

    # Step 1: Generate the dataset.
    if not run_step(
        "STEP 1: Generate event-log dataset",
        [
            python,
            str(PROJECT_ROOT / "scripts" / "generate_data.py"),
            "--cases",
            str(args.cases),
            "--output",
            str(dataset_path),
            "--seed",
            str(args.seed),
        ],
    ):
        sys.exit(1)

    # Step 2: Validate the generated dataset.
    if not run_step(
        "STEP 2: Validate event-log dataset",
        [
            python,
            str(PROJECT_ROOT / "scripts" / "validate_data.py"),
            str(dataset_path),
        ],
    ):
        sys.exit(1)

    # Step 3: Generate the quality report only after validation passes.
    if not run_step(
        "STEP 3: Generate data-quality report",
        [
            python,
            str(
                PROJECT_ROOT
                / "scripts"
                / "generate_quality_report.py"
            ),
            "--input",
            str(dataset_path),
            "--output",
            str(report_path),
        ],
    ):
        sys.exit(1)

    print("\n" + "=" * 60)
    print("CAREFLOW PIPELINE COMPLETED SUCCESSFULLY")
    print(f"Dataset: {dataset_path}")
    print(f"Quality report: {report_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
