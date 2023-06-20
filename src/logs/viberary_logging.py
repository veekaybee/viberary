import logging
from logging import Logger
from logging.config import fileConfig

from inout.file_reader import get_project_root


class ViberaryLogging:
    def setup_logging(self) -> Logger:
        root = get_project_root()
        LOGGING_CONFIG = root / "logging.ini"
        fileConfig(LOGGING_CONFIG)
        logger = logging.getLogger("indexer")
        return logger
