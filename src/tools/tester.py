import subprocess
import sys


class TestResult:

    def __init__(self, passed, output):
        self.passed = passed
        self.output = output
