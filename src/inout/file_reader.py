from pathlib import Path

import git
import yaml


def get_root_dir()->Path:
    """get root path for project based on git"""
    repo = git.Repo(".", search_parent_directories=True)
    root_dir = repo.working_tree_dir
    return root_dir

def get_config_file() -> dict:
    """Access config options"""
    root_dir = get_root_dir()
    config_path = Path( f"{root_dir}/config.yml")

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
        return config