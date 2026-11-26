# Forge 2.0

Forge is an interactive coding workflow prototype. OmniRoute drafts a plan and suggests patches. Forge shows each patch before applying it, runs pytest, and asks you to review the changed files before creating a local commit.

This guide describes the [`nish/forge-safety` branch](https://github.com/n1sh032/Forge-2.0/tree/nish/forge-safety).

## Requirements and setup

- Python 3.10 or later and Git on your PATH.
- For live model calls, a configured OmniRoute server at `http://localhost:20128/v1`, access to the model configured in [omniroute_provider.py](src/providers/omniroute_provider.py), and a valid API key.
- For patch and test runs, a Python target project with pytest and its other test dependencies available to Forge's interpreter.

From the Forge repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Set `OMNIROUTE_API_KEY` in your environment or a private `.env` file in the Forge checkout. Start OmniRoute before requesting a live plan.

## Draft a plan

```powershell
.\.venv\Scripts\python.exe -m src.main "Add a unit test for input validation"
```

The command prints the proposed steps as JSON. Add `--help` to see the available options.

## Apply a plan in a linked worktree

From the **target repository**, create a clean linked worktree on a new branch:

```powershell
git worktree add -b forge-task ../forge-task HEAD
```

Return to the **Forge checkout** and pass the actual path to the linked worktree:

```powershell
.\.venv\Scripts\python.exe -m src.main "Add a unit test for input validation" --project ../forge-task
```

Approve the plan and review each patch before running it. If a patch or test fails, Forge can ask OmniRoute for another patch with the failure details you approve. pytest has a 120-second timeout. After tests pass, inspect the diff and new files before approving the commit. Forge requires an empty staging area and stages only the approved paths. If you stop after applying a patch, its changes stay in the target worktree. Tests run with your local account's permissions.

## Working proof

The suite exercises plan parsing, patch application, test execution, retry accounting and selective staging with temporary repositories and fake providers. A previous run on this branch passed **33 tests with 1 skip**, and the CLI help opened successfully. A complete live OmniRoute run has not been verified.

```powershell
.\.venv\Scripts\python.exe -m src.main --help
.\.venv\Scripts\python.exe -m pytest -q
```
