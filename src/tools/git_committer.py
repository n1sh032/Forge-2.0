import subprocess


class CommitResult:

    def __init__(self, success, message):
        self.success = success
        self.message = message


def commit_changes(project_root, commit_message):
    """
    Stages all changes and commits them with the given message.

    Deterministic - no LLM involved here, just running git. The
    message itself is expected to already be generated elsewhere.
    """

