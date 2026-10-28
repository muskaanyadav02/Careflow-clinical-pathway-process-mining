from pathlib import Path
import pandas as pd

# Step 1: Base paths set up by Member 2
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "hospital_event_log_full.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "conformance_results.csv"

print("Conformance path setup completed successfully.")
