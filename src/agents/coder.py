import os
import json

from .base_agent import BaseAgent
from src.providers.omniroute_provider import OmniRouteProvider


class Coder(BaseAgent):

    def __init__(self, provider=None, project_root="."):
        super().__init__("Coder")
        self.provider = provider or OmniRouteProvider()
        self.project_root = project_root

    def run(self, step):
        file_list = self._list_project_files()
        relevant_files = self._pick_relevant_files(step, file_list)
        file_contents = self._read_files(relevant_files)
        diff = self._generate_diff(step, file_contents)
        return diff

    def _list_project_files(self):
        ignored_dirs = {".venv", "__pycache__", ".git", ".forge"}
        files = []

        for root, dirs, filenames in os.walk(self.project_root):
            dirs[:] = [d for d in dirs if d not in ignored_dirs]

            for filename in filenames:
                path = os.path.relpath(os.path.join(root, filename), self.project_root)
                files.append(path.replace("\\", "/"))

        return files

    def _pick_relevant_files(self, step, file_list):
        prompt = (
            "You are a software engineer deciding which files a coding step touches.\n"
            "Here is the project's file list:\n"
            f"{json.dumps(file_list, indent=2)}\n\n"
            f"Step to implement: {step}\n\n"
            "Respond with ONLY a JSON array of file paths (relative to the project root) "
            "that need to be created or modified for this step. "
            "Use forward slashes. If a needed file doesn't exist yet, include its path anyway. "
            "No other text."
        )

        reply = self.provider.ask(prompt)
        return json.loads(self._strip_code_fence(reply))
