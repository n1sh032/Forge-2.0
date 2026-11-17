import subprocess
import sys
from tempfile import TemporaryFile


class TestResult:

    def __init__(self, passed, output):
        self.passed = passed
        self.output = output


def run_tests(project_root=".", timeout=120):
    """
    Runs the test suite in project_root using pytest.

    Deterministic - no LLM involved. Returns a TestResult describing
    whether tests passed and the end of the output, so a failure can be
    inspected or shown to the user.
    """

    with TemporaryFile() as log:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest"],
                cwd=project_root,
                stdout=log,
                stderr=subprocess.STDOUT,
                timeout=timeout,
            )
            passed = result.returncode == 0
            prefix = ""
        except subprocess.TimeoutExpired:
            passed = False
            prefix = f"pytest timed out after {timeout} seconds\n"
        start = max(0, log.seek(0, 2) - 64 * 1024)
        log.seek(start)
        if start:
            prefix += "[Showing the last 64 KiB of pytest output]\n"
        return TestResult(passed, prefix + log.read().decode("utf-8", errors="replace"))
