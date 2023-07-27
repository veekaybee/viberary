#!/usr/bin/env python

import logging.config

from conf.config_manager import ConfigManager
from src.api.main import app

conf = ConfigManager()
conf.set_logger_config()

if __name__ == "__main__":
    logging.info("Starting Flask")
    app.run(debug=True)
