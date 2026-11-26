import json

from .base_agent import BaseAgent
from src.providers.omniroute_provider import OmniRouteProvider


class Architect(BaseAgent):

    def __init__(self, provider=None):
        super().__init__("Architect")
        self.provider = provider or OmniRouteProvider()

    def run(self, task):
        return {
            "task": task,
            "steps": [
                "Understand the requirements",
                "Design the solution",
                "Implement the solution",
                "Test the solution"
            ]
        }