from src.tools.tester import run_tests


def test_run_tests_passes(tmp_path):
    test_file = tmp_path / "test_sample.py"
    test_file.write_text("def test_ok():\n    assert True\n")

    result = run_tests(project_root=str(tmp_path))

    assert result.passed is True


def test_run_tests_fails(tmp_path):
    test_file = tmp_path / "test_sample.py"
    test_file.write_text("def test_broken():\n    assert False\n")

    result = run_tests(project_root=str(tmp_path))

    assert result.passed is False
    assert "test_broken" in result.output