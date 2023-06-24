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
        r = self.conn
        pqt = pd.read_parquet(self.filepath)
        logging.info(f"Getting index data from {pqt}...")
        title_dict = dict(zip(pqt["index"], pqt["sentence"]))
        return title_dict

    def load_docs(self):
        r = self.conn
        vector_dict: Dict[str, str] = self.index_title_redis()
        logging.info(f"Inserting k,v")

        # an input dictionary from a dictionary
        for i, (k, v) in enumerate(vector_dict.items()):
            try:
                # write to Redis
                r.set(f"title::{k}", v)
                logging.info(f"Set {i} vector into Redis index")
            except Exception as e:
                self.logger.error("An exception occurred: {}".format(e))
