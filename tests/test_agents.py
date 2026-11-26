from src.agents.architect import Architect


class FakeProvider:
    def ask(self, prompt):
        return '["Understand the requirements", "Design the solution", "Implement the solution", "Test the solution"]'


def test_architect():

    architect = Architect(provider=FakeProvider())

    plan = architect.run("Build a calculator")

    assert plan["task"] == "Build a calculator"
    assert len(plan["steps"]) > 0