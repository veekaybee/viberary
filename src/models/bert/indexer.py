import logging
import logging.config
from itertools import islice
from typing import Dict, List

import numpy as np
import pandas as pd
from redis.commands.search.field import TextField, VectorField

from inout import file_reader as f

"""
Indexes embeddings from a file into a Redis instance
"""


class Indexer:
    def __init__(
        self,
        redis_conn,
        filepath,
        vector_field,
        index_name,
        nvecs=0,
        dim=0,
        max_edges=0,
        ef=0,
        distance_metric="COSINE",
        token_field_name="token",
        float_type="FLOAT64",
    ) -> None:
        self.conn = redis_conn
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
        logging.config.fileConfig(f.get_project_root() / "logging.conf")

    def file_to_embedding_dict(self) -> Dict[str, List[float]]:
        """Reads Parquet file and process in Pandas, returning zipped dict of index and embeddings

        Returns:
            Dict[str, List[float]]: _description_
        """
        parquet = self.filepath

        logging.info(f"Creating dataframe from {parquet}...")
        pqt = pd.read_parquet(parquet)

        embedding_dict = dict(zip(pqt["index"], pqt["embeddings"]))

        return embedding_dict

    def drop_index(self):
        """Delete Redis index, will need to do to recreate"""
        logging.info(f"Deleting Redis index {self.index_name}...")
        r = self.conn

        r.ft(self.index_name).dropindex()

    def create_index_schema(self) -> None:
        """Create Redis index with schema parameters from config"""
        logging.info(f"Creating redis schema...")
        r = self.conn

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
        logging.info(f"Creating Redis schema: {schema} in index {self.index_name}")

    def take(self, n, iterable):
        return list(islice(iterable, n))

    def load_docs(self):
        r = self.conn

        vector_dict: Dict[str, List[float]] = self.file_to_embedding_dict()
        logging.info(f"Inserting vector into Redis index {self.index_name}")

        sample_dict = self.take(10, vector_dict.items())

        # an input dictionary from a dictionary
        for i, (k, v) in enumerate(sample_dict):
            data = np.array(v, dtype=np.float64)
            np_vector = data.astype(np.float64)

            try:
                # write to Redis
                r.hset(f"vector::{k}", mapping={self.vector_field: np_vector.tobytes()})
                logging.info(
                    f"Set vector {i}  into {self.index_name} as {self.vector_field}"
                )
            except Exception as e:
                logging.error("An exception occurred: {}".format(e))

    def get_index_metadata(self):
        r = self.conn
        metadata = r.ft(self.index_name).info()
        logging.info(
            f"name: {metadata['index_name']}, docs: {metadata['max_doc_id']}, time:{metadata['total_indexing_time']} seconds"
        )
