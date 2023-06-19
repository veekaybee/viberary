import csv
import importlib.resources
import sys
from io import TextIOWrapper
from pathlib import Path
from typing import IO, Dict, List, TypedDict
import pyarrow as pa

import numpy as np
import pandas as pd
from pandas import DataFrame
from redis import Redis
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.query import Query
from tqdm import tqdm

from src.logs.viberary_logging import ViberaryLogging
from src.io import file_reader as f

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
        self.logger = ViberaryLogging().setup_logging()

    def index_title_redis(self) -> Dict[str, str]:
        """Write mapping of title to index to Redis"""
        r = self.conn
        pqt = pd.read_parquet(self.filepath)
        self.logger.info(f"Getting index data from {pqt}...")
        title_dict = dict(zip(pqt["index"], pqt["sentence"]))
        print(title_dict)
        return title_dict

    def load_docs(self):
        r = self.conn
        vector_dict: Dict[str, str] = self.index_title_redis()
        self.logger.info(f"Inserting k,v")

        # an input dictionary from a dictionary
        for i, (k, v) in enumerate(vector_dict.items()):
            try:
                # write to Redis
                r.set(f"title::{k}", v)
                self.logger.info(f"Set {i} vector into Redis index")
            except Exception as e:
                self.logger.error("An exception occurred: {}".format(e))
