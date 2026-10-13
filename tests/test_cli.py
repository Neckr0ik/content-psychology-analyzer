import main


def test_batch_run(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main.main([]) == 0
    assert (tmp_path / "output" / "analysis_report.md").exists()
    assert (tmp_path / "output" / "engagement_ranking.png").exists()


def test_single_text(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main.main(["--text", "What really happened? Exclusive premiere.", "--no-charts"]) == 0


def test_compare_writes_report(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main.main(["--compare", "A drama.", "Award-winning exclusive premiere."]) == 0
    report = (tmp_path / "output" / "framing_report.md").read_text(encoding="utf-8")
    assert "Chong" in report and "does not measure" in report
    assert (tmp_path / "output" / "framing_comparison.png").exists()
    assert "differs" in capsys.readouterr().out
