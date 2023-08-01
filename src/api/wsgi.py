#!/usr/bin/env python

import logging.config

from conf.config_manager import ConfigManager
from src.api.main import app

if __name__ == "__main__":
    cm = ConfigManager()
    logger_path = cm.get_logger_path()
    logging.config.fileConfig(logger_path)
    logging.info("Starting Flask")
    app.run(debug=True)
