import logging
from typing import Dict

import pandas as pd

from inout import file_reader as f

"""
Indexes metadata about embeddings (book title, author, etc.) into cache for app lookup
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

    def add_key_prefix_to_cache(self, key_prefix) -> Dict[str, str]:
        """Write mapping of index and lookup column to cache"""
        pqt = pd.read_parquet(self.filepath)
        logging.info(f"Getting index data from {pqt}...")
        title_dict = dict(zip(pqt.index, pqt[key_prefix]))
        return title_dict

    def load_docs(self, key_prefix: str):
        r = self.conn
        vector_dict: Dict[str, str] = self.add_key_prefix_to_cache(key_prefix)
        logging.info("Inserting titles into {key_prefix} key prefix")

        for i, (k, v) in enumerate(vector_dict.items()):
            try:
                # write to Redis
                r.set(f"{key_prefix}::{k}", v)
                logging.info(f"Set {i} into {key_prefix}")
            except Exception as e:
                logging.error("An exception occurred: {}".format(e))
