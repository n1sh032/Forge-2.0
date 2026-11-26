import json

from .base_agent import BaseAgent
from src.providers.omniroute_provider import OmniRouteProvider


class Architect(BaseAgent):

    def __init__(self, provider=None):
        super().__init__("Architect")
        self.provider = provider or OmniRouteProvider()

    def run(self, task):
        prompt = (
            "You are a software engineering planner. "
            "Break the following task into a short list of clear, "
            "logical implementation steps. "
            "Respond with ONLY a JSON array of strings, no other text.\n\n"
            f"Task: {task}"
        )

        reply = self.provider.ask(prompt)
        steps = json.loads(self._strip_code_fence(reply))

        return {
            "task": task,
            "steps": [
                "Understand the requirements",
                "Design the solution",
                "Implement the solution",
                "Test the solution"
            ]
        }