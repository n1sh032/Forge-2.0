import json

from .base_agent import BaseAgent
from src.providers.omniroute_provider import OmniRouteProvider


class Architect(BaseAgent):

    def __init__(self, provider=None):
        super().__init__("Architect")
        self.provider = provider or OmniRouteProvider()

    def run(self, task):
        prompt = (
            "You are a  senior software engineering planner. "
            "Break the following task into a short list of clear, "
            "logical implementation steps. "
            "Respond with ONLY a JSON array of strings, no other text.\n\n"
            f"Task: {task}"
        )

        reply = self.provider.ask(prompt)
        steps = json.loads(self._strip_code_fence(reply))

        return {
            "task": task,
            "steps": steps
        }

    def generate_commit_message(self, step):
        prompt = (
            "You are a software engineer writing a git commit message "
            "for a change you just made. "
            "Follow the conventional commits style (e.g. 'feat: ...', "
            "'fix: ...', 'test: ...', 'docs: ...'). "
            "Keep it to a single line, no more than 72 characters. "
            "Respond with ONLY the commit message, no quotes, no other text.\n\n"
            f"The change implemented this step: {step}"
        )

        reply = self.provider.ask(prompt)
        return self._strip_code_fence(reply).strip().strip('"').strip("'")
    
    def _strip_code_fence(self, text):
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines)
        return text.strip()