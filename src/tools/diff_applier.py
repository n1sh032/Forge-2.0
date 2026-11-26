import subprocess
import tempfile
import os


class DiffResult:

    def __init__(self, success, message):
        self.success = success
        self.message = message


