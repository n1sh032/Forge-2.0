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

    def _read_files(self, file_paths):
        contents = {}

        for path in file_paths:
            full_path = os.path.join(self.project_root, path)
            if os.path.exists(full_path):
                with open(full_path, "r", encoding="utf-8") as f:
                    contents[path] = f.read()
            else:
                contents[path] = None

        return contents

    def _generate_diff(self, step, file_contents):
        files_section = ""
        for path, content in file_contents.items():
            if content is None:
                files_section += f"\n--- {path} (does not exist yet) ---\n(new file)\n"
            else:
                files_section += f"\n--- {path} (current content) ---\n{content}\n"

        prompt = (
            "You are a software engineer implementing ONE small coding step.\n"
            f"Step: {step}\n\n"
            "Here are the current contents of the relevant files:\n"
            f"{files_section}\n\n"
            "Produce a unified diff (git diff format) that implements this step. "
            "For new files, write a diff that creates them from scratch. "
            "Respond with ONLY the diff, no other text or explanation."
        )

        return self.provider.ask(prompt)

    def _strip_code_fence(self, text):
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines)
        return text.strip()