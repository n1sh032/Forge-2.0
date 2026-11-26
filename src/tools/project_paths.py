from pathlib import Path, PureWindowsPath


def project_path(root, value):
    root = Path(root).resolve()
    path = Path(value)
