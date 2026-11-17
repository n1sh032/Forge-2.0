# Forge 2.0

Forge is a prototype for planning a coding task with OmniRoute, generating a
patch, applying it to a Git worktree and checking it with pytest. The manager
exposes individual steps for a caller to run.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
```

For model calls, set `OMNIROUTE_API_KEY` and run a configured OmniRoute server.
The default endpoint is `http://localhost:20128/v1`.
Draft a plan with `python -m src.main "Add a unit test for input validation"`.
The command prints the plan for review.

Use a clean disposable branch or worktree for the target project. Tests execute
the target's code with your local permissions. Review the generated diff before
running tests. After tests pass, review the result and pass the individual file
paths to `Manager.commit(approved_paths=[...])`. Forge refuses to commit when
the index already contains staged changes.

The repair state supports a caller requesting another coding attempt. This
branch has no automatic repair driver or feedback prompt. A failed test can
leave changes in the target worktree for review.
