import argparse
import json
import subprocess
from pathlib import Path

from src.agents.architect import Architect
from src.manager.manager import Manager
from src.manager.state_machine import ForgeState


def git_output(project, *args):
    return subprocess.check_output(["git", *args], cwd=project, text=True, encoding="utf-8")
