import argparse
import json
import subprocess
from pathlib import Path

from src.agents.architect import Architect
from src.manager.manager import Manager
from src.manager.state_machine import ForgeState

