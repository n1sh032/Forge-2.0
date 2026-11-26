import subprocess
import sys


class TestResult:

    def __init__(self, passed, output):
        self.passed = passed
        self.output = output


def run_tests(project_root="."):
    """
    Runs the test suite in project_root using pytest.

    Deterministic - no LLM involved. Returns a TestResult describing
    whether tests passed and the raw output, so a failure can be
    inspected or shown to the user.
    """

    result = subprocess.run(
        [sys.executable, "-m", "pytest"],
        cwd=project_root,
        capture_output=True,
        text=True
    )

    passed = result.returncode == 0
    output = result.stdout + result.stderr

    return TestResult(passed=passed, output=output)