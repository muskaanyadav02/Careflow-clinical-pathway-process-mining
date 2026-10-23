from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def test_bottleneck_summary():
    path = PROCESSED / "bottleneck_summary.csv"
    assert path.exists(), "Bottleneck summary was not generated"

    df = pd.read_csv(path)
    assert not df.empty
    assert {"Transition", "Occurrences", "Average_Minutes", "Maximum_Minutes"}.issubset(df.columns)
    assert (df["Occurrences"] > 0).all()
    assert (df["Average_Minutes"] >= 0).all()
    assert (df["Maximum_Minutes"] >= df["Average_Minutes"]).all()


def test_conformance_results():
    path = PROCESSED / "conformance_results.csv"
    assert path.exists(), "Conformance results were not generated"

    df = pd.read_csv(path)
    assert not df.empty
    assert {"Case_ID", "Exact_Match", "Missing_Activities", "Additional_Activities"}.issubset(df.columns)
    assert df["Case_ID"].notna().all()
    assert df["Case_ID"].is_unique


def test_deviation_summary():
    path = PROCESSED / "deviation_summary.csv"
    assert path.exists(), "Deviation summary was not generated"

    df = pd.read_csv(path)
    assert not df.empty
    assert {"Category", "Finding", "Patient_Count"}.issubset(df.columns)
    assert pd.to_numeric(df["Patient_Count"], errors="coerce").notna().all()
    assert (df["Patient_Count"] >= 0).all()


def test_process_tree_visualization():
    path = PROCESSED / "discovered_process_tree.png"
    assert path.exists(), "Process tree visualization was not generated"
    assert path.stat().st_size > 0
