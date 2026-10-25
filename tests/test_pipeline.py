
import subprocess

from scripts import run_pipeline


def test_pipeline_stops_when_validation_fails(monkeypatch, tmp_path):
    calls = []

    def fake_run(command, cwd, check):
        calls.append(command)

        # Simulate successful generation, followed by failed validation.
        if len(calls) == 1:
            return subprocess.CompletedProcess(command, 0)

        return subprocess.CompletedProcess(command, 1)

    monkeypatch.setattr(run_pipeline.subprocess, "run", fake_run)
    monkeypatch.setattr(
        "sys.argv",
        [
            "run_pipeline.py",
            "--cases",
            "10",
            "--output",
            str(tmp_path / "events.csv"),
            "--report",
            str(tmp_path / "report.json"),
        ],
    )

    try:
        run_pipeline.main()
    except SystemExit as exc:
        assert exc.code == 1
    else:
        raise AssertionError("Pipeline should fail when validation fails")

    assert len(calls) == 2
    assert "validate_data.py" in calls[1][1]
    assert all("generate_quality_report.py" not in part for part in calls[1])


def test_pipeline_runs_all_three_steps(monkeypatch, tmp_path):
    calls = []

    def fake_run(command, cwd, check):
        calls.append(command)
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(run_pipeline.subprocess, "run", fake_run)
    monkeypatch.setattr(
        "sys.argv",
        [
            "run_pipeline.py",
            "--cases",
            "10",
            "--output",
            str(tmp_path / "events.csv"),
            "--report",
            str(tmp_path / "report.json"),
        ],
    )

    run_pipeline.main()

    assert len(calls) == 3
    assert "generate_data.py" in calls[0][1]
    assert "validate_data.py" in calls[1][1]
    assert "generate_quality_report.py" in calls[2][1]


def test_pipeline_runs_end_to_end(tmp_path):
    import json
    import sys

    from pathlib import Path

    project_root = Path(run_pipeline.__file__).resolve().parent.parent
    dataset = tmp_path / "events.csv"
    report = tmp_path / "report.json"

    result = subprocess.run(
        [
            sys.executable,
            str(project_root / "scripts" / "run_pipeline.py"),
            "--cases",
            "10",
            "--output",
            str(dataset),
            "--report",
            str(report),
        ],
        cwd=project_root,
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert dataset.exists(), "Generated dataset was not created"
    assert report.exists(), "Quality report was not created"

    with report.open(encoding="utf-8") as file:
        quality_report = json.load(file)

    assert quality_report["total_events"] > 0
    assert quality_report["unique_cases"] == 10

def test_pipeline_rejects_zero_cases(monkeypatch):
    import sys

    monkeypatch.setattr(
        sys,
        "argv",
        ["run_pipeline.py", "--cases", "0"],
    )

    def unexpected_run(*args, **kwargs):
        raise AssertionError("Pipeline should not run with zero cases")

    monkeypatch.setattr(run_pipeline.subprocess, "run", unexpected_run)

    try:
        run_pipeline.main()
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("Pipeline should reject zero cases")
