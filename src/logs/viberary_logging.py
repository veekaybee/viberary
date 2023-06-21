import logging
from logging import Logger
from logging.config import fileConfig

from inout.file_reader import get_project_root


class ViberaryLogging:
    def setup_logging(self) -> Logger:
        logger = logging.getLogger("indexer")
        return logger
