import importlib.resources
import logging
from io import TextIOWrapper
from logging.config import fileConfig
from pathlib import Path
from typing import IO, Dict, List, TypedDict

import sys

import numpy as np
from pandas import DataFrame
from redis import Redis
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.query import Query
from tqdm import tqdm
import pandas as pd

from src.io import file_reader as f
from src.bert import tqdm_logger 

"""
Indexes embeddings from a file into a Redis instance
"""


class Indexer():
    
        
    def __init__(
        self,
        filepath,
        nvecs=0,
        dim=0,
        max_edges=0,
        ef=0,
        vector_field="",
        index_name="",
        distance_metric="COSINE",
        token_field_name="token",
        float_type="FLOAT64",
    ) -> None:
        self.filepath = filepath
        self.dim = dim
        self.nvecs = nvecs
        self.max_edges = max_edges
        self.ef = ef
        self.vector_field = vector_field
        self.token_field_name = token_field_name
        self.float_type = float_type
        self.index_name = index_name
        self.distance_metric = distance_metric
        root = f.get_project_root()
        LOGGING_CONFIG =  root / 'logging.ini'
        fileConfig(LOGGING_CONFIG)
        self.logger = logging.getLogger('indexer')
        
        

    def read_file(self) -> IO:
        self.logger.info(f"Opening {self.filepath}...")
        return f.get_resource(self.filepath)


    def file_to_embedding_dict(self) -> Dict[str, List[float]]:
        """
        Returns k,v dictionary
        k is the index of the embedding and v is a vector of embeddings
        """
        csv = f.get_project_root() / "data" / "embeddings_sample.csv"
        
        self.logger.info(f"Reading in CSV { csv}...")
        
        tqdm_out = tqdm_logger.TqdmToStdout(self.logger,level=logging.INFO)
        with tqdm(total=len(open(csv, 'r').readlines())) as pbar:
            df = pd.read_csv(csv, chunksize=1000, low_memory=False)
            df = pd.concat(df)
            self.logger.info(f"Creating dataframe from {csv}...")
            embedding_dict = dict(zip(df["idx"], df["embeddings"]))
            print(embedding_dict)
            return embedding_dict

    def redis_connection(self) -> Redis:
        host = "localhost"
        port = 6379
        redis_conn = Redis(host=host, port=port)
        return redis_conn

    def delete_index(self):
        """Delete Redis index, will need to do to recreate"""
        r = self.redis_connection()
        r.flushall()

    def create_index_schema(self) -> None:
        """Create Redis index with schema parameters from config"""

        r = self.redis_connection()

        schema = (
            VectorField(
                self.vector_field,
                "HNSW",
                {
                    "TYPE": self.float_type,
                    "DIM": self.dim,
                    "DISTANCE_METRIC": self.distance_metric,
                },
            ),
            TextField(self.token_field_name),
        )

        r.ft(self.index_name).create_index(schema)
        r.ft(self.index_name).config_set("default_dialect", 2)

    def load_docs(self):

        r = self.redis_connection()

        vector_dict: Dict[str, List[float]] = self.file_to_embedding_dict()

        # an input dictionary from a dictionary
        for i, (k, v) in enumerate(vector_dict.items()):
            logging.info(f"Inserting {i} vector into Redis index {self.index_name}")
            data = np.array(v, dtype=np.float64)
            np_vector = data.astype(np.float64)

            try:
                # try storing vector, log exceptions if fails to map
                r.hset(k, mapping={self.vector_field: np_vector.tobytes()})
                logging.info(f"Set {k} vector into Redis index as {self.vector_field}")
            except Exception as e:
                logging.error("An exception occurred: {}".format(e))

    def check_load(self):
        r = self.redis_connection()
        logging.info("index meta: ", r.ft(self.index_name).info())
