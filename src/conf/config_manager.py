from pathlib import Path

import git
import yaml


class ConfigManager:
    """
    Gets root path of dir and logger config
    """

    def __init__(self):
        self.config_path = None

    def get_root_dir(self) -> Path:
        """get root path for project based on git"""
        repo = git.Repo(".", search_parent_directories=True)
        root_dir = repo.working_tree_dir
        return root_dir

    def get_config_path(self) -> Path:
        root_dir = self.get_root_dir()
        self.config_path = Path(f"{root_dir}/config.yml")
        return self.config_path

    def get_config_file(self) -> dict:
        """Access config options"""
        self.get_config_path()

        with open(self.config_path, "r") as file:
            config = yaml.safe_load(file)
            return config

    def get_logger_path(self) -> Path:
        conf = self.get_config_file()
        path = conf["logging"]["path"]
        return path
