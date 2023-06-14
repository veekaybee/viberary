from src.io import file_reader as f
from typing import IO, TypedDict, List, Dict

import numpy as np

import pandas as pd
from pandas import DataFrame


from redis import Redis
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.query import Query

import logging

"""
Indexes embeddings from a file into a Redis instance
"""


class Indexer:
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

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.basicConfig(
        format="%(levelname)s - %(asctime)s: %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )

    def read_file(self) -> IO:
        return f.get_resource(self.filepath)

    def file_to_embedding_dict(self) -> Dict[str, List[float]]:
        """
        Returns k,v dictionary
        k is the index of the embedding and v is a vector of embeddings
        """

        csv = self.read_file()
        df: DataFrame = pd.read_csv(csv)
        embedding_dict = dict(zip(df["idx"], df["embeddings"]))
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

    def load_docs(self, client: Redis):

        r = self.redis_connection()

        vector_dict: Dict[str, List[float]] = self.file_to_embedding_dict()

        # an input dictionary from a dictionary
        for i, (k, v) in enumerate(vector_dict.items()):
            logging.info(f"Inserting {i} vector into Redis index {self.index_name}")
            data = np.array(v, dtype=np.float64)
            np_vector = data.astype(np.float64)

            try:
                # try storing vector, log exceptions if fails to map
                client.hset(k, mapping={self.vector_field: np_vector.tobytes()})
                logging.info(f"Set {k} vector into Redis index as {self.vector_field}")
            except Exception as e:
                logging.error("An exception occurred: {}".format(e))

    def check_load(self, client: Redis):
        r = self.redis_connection()
        logging.info("index meta: ", r.ft(self.index_name).info())
