#!/usr/bin/env python

from src.api.main import app
from inout.file_reader import get_root_dir,get_config_file as cf
import logging.config

conf = cf()
conf_path = conf["logging"]["path"]
root_dir = get_root_dir()
logging.config.fileConfig(f"{root_dir}/{conf_path}")

if __name__ == "__main__":
    logging.info("Starting Flask")
    app.run(debug=True)