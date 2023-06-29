from pathlib import Path


def get_project_root() -> Path:
    """Sets the project root to Viberary for any resources

    Returns:
        Path: Wraps filepath in correct relative reference to project root
    """
    return Path(__file__).parent.parent.parent
