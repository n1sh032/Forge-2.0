from src.agents.architect import Architect


def test_architect():

    architect = Architect()

    plan = architect.run("Build a calculator")

    assert plan["task"] == "Build a calculator"
    assert len(plan["steps"]) > 0