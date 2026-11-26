import argparse
import json
import subprocess
from pathlib import Path

from src.agents.architect import Architect
from src.manager.manager import Manager
from src.manager.state_machine import ForgeState


def git_output(project, *args):
    return subprocess.check_output(["git", *args], cwd=project, text=True, encoding="utf-8")


def approve(prompt):
    return input(f"{prompt} [y/N] ").strip().lower() == "y"


def review_patch(diff):
    print(diff)
    return approve("Apply this patch and run the project's pytest suite?")
