from pathlib import Path, PureWindowsPath


def project_path(root, value):
    root = Path(root).resolve()
    path = Path(value)
    windows = PureWindowsPath(value)
    if (
        not path.parts or path.anchor or windows.anchor
        or any(part.lower() in {"..", ".git", ".env"} or ":" in part for part in windows.parts)
    ):
        raise ValueError(f"Unsafe project path: {value!r}")
