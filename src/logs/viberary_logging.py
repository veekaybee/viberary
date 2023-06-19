import logging
from logging import Logger
from logging.config import fileConfig

from src.io import file_reader as f


class ViberaryLogging:
    def setup_logging(self) -> Logger:
        root = f.get_project_root()
        LOGGING_CONFIG = root / "logging.ini"
        fileConfig(LOGGING_CONFIG)
        logger = logging.getLogger("indexer")
        return logger
