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
    target = root / path
    resolved = target.resolve()
    if not resolved.is_relative_to(root) or resolved == root:
        raise ValueError(f"Path escapes project: {value!r}")
    if target.is_symlink() or any(parent.is_symlink() for parent in target.parents if parent != root):
        raise ValueError(f"Symbolic links are not supported: {value!r}")
