import logging
from typing import Dict

import pandas as pd

from inout import file_reader as f

"""
Indexes embeddings from a file into a Redis instance
"""


class TitleMapper:
    def __init__(
        self,
        redis_conn,
        filepath,
    ) -> None:
        self.conn = redis_conn
        self.filepath = filepath
        logging.config.fileConfig(f.get_project_root() / "logging.conf")

    def index_title_redis(self) -> Dict[str, str]:
        """Write mapping of title to index to Redis"""
        pqt = pd.read_parquet(self.filepath)
        logging.info(f"Getting index data from {pqt}...")
        title_dict = dict(zip(pqt["index"], pqt["sentence"]))
        return title_dict

    def index_title_redis(self) -> Dict[str, str]:
        """Write mapping of title to index to Redis"""
        pqt = pd.read_parquet(self.filepath)
        logging.info(f"Getting index data from {pqt}...")
        title_dict = dict(zip(pqt["index"], pqt["author"]))
        return title_dict

    def load_title_docs(self):
        r = self.conn
        vector_dict: Dict[str, str] = self.index_title_redis()
        logging.info("Inserting titles into the title index")

        # an input dictionary from a dictionary
        for i, (k, v) in enumerate(vector_dict.items()):
            try:
                # write to Redis
                r.set(f"title::{k}", v)
                logging.info(f"Set {i} title into Redis")
            except Exception as e:
                logging.error("An exception occurred: {}".format(e))

    def load_author_docs(self):
        r = self.conn
        vector_dict: Dict[str, str] = self.index_title_redis()
        logging.info("Inserting titles into the title index")

        # an input dictionary from a dictionary
        for i, (k, v) in enumerate(vector_dict.items()):
            try:
                # write to Redis
                r.set(f"author::{k}", v)
                logging.info(f"Set {i} title into Redis")
            except Exception as e:
                logging.error("An exception occurred: {}".format(e))
