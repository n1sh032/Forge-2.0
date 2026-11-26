from src.web import ForgeApplication


def test_browser_requires_plan_before_worktree_mutations():
    application = ForgeApplication()
    for action in ("patch", "apply", "commit", "next"):
        assert application.execute(action, {}) == {"error": "Create a plan first."}


def test_browser_plan_requires_absolute_worktree_path():
    app = ForgeApplication()
    assert "absolute" in app.execute("plan", {"task": "Add tests", "project": "relative"})["error"]
