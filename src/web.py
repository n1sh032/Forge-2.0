import argparse
import os
import subprocess
from pathlib import Path

from src.web_runtime import serve


def git(root, *args):
    return subprocess.check_output(
        ["git", *args],
        cwd=root,
        text=True,
        encoding="utf-8",
        timeout=15,
    ).strip()


class ForgeApplication:
    actions = {"plan", "patch", "apply", "commit", "next"}

