from .base_agent import BaseAgent


class Architect(BaseAgent):

    def __init__(self):
        super().__init__("Architect")

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