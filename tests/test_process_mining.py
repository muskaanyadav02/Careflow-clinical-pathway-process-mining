from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def test_bottleneck_summary():
    path = PROCESSED / "bottleneck_summary.csv"
    assert path.exists(), "Bottleneck summary was not generated"

    df = pd.read_csv(path)
    assert not df.empty

    # Support both integration and Role 4 CSV formats
    if {"from_activity", "to_activity", "transition_count",
        "average_time_minutes", "maximum_time_minutes"}.issubset(df.columns):
        assert (df["transition_count"] > 0).all()
        assert (df["average_time_minutes"] >= 0).all()
        assert (df["maximum_time_minutes"] >= df["average_time_minutes"]).all()

    elif {"Transition", "Occurrences", "Average_Minutes",
          "Maximum_Minutes"}.issubset(df.columns):
        assert (df["Occurrences"] > 0).all()
        assert (df["Average_Minutes"] >= 0).all()
        assert (df["Maximum_Minutes"] >= df["Average_Minutes"]).all()

    else:
        raise AssertionError(
            f"Unexpected bottleneck CSV columns: {list(df.columns)}"
        )