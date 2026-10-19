
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
