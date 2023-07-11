from pathlib import Path

import yaml


def get_project_root() -> Path:
    """Sets the project root to /viberary for any resources

    Returns:
        Path: Wraps filepath in correct relative reference to project root
    """
    return Path(__file__).parent.parent.parent


def get_config_file() -> dict:
    """Access config options"""
    config_path = get_project_root() / "config.yml"
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
        return config
