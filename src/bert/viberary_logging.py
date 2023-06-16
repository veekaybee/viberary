from src.io import file_reader as f
import logging
from logging.config import fileConfig
from logging import Logger


class ViberaryLogging:
    def setup_logging(self) -> Logger:
        root = f.get_project_root()
        LOGGING_CONFIG = root / "logging.ini"
        fileConfig(LOGGING_CONFIG)
        logger = logging.getLogger("indexer")
        return logger
