import logging
import logging.config
from typing import Dict, List

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
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

    def file_to_embedding_dict(self, columns: List) -> Dict[str, List[float]]:
        """Reads Parquet file and processes in Pandas, returning zipped dict of input index and column"""
        parquet = self.filepath

        logging.info(f"Creating dataframe from {parquet}...")

        parquet_file = pq.ParquetFile(str(parquet))

        final_df = pd.DataFrame()

        for batch in parquet_file.iter_batches(columns=columns):
            logging.info(f"RecordBatch {batch}")
            df = batch.to_pandas()
            final_df = final_df.append(df, ignore_index=True)

        df_dict = final_df.to_dict("split")
        data = df_dict["data"]
        my_dict = {item[0]: item[1] for item in data}

        return my_dict

    def drop_index(self):
        """Delete Redis index but does not delete underlying data"""
        logging.info(f"Deleting Redis index {self.index_name}...")
        r = self.conn

        if r.exists(self.index_name):
            r.ft(self.index_name).dropindex()

    def create_search_index_schema(self) -> None:
        """Create Redis index with schema parameters from config"""
        logging.info("Creating redis schema...")
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
        logging.info(f"using {self.vector_field}, {self.float_type}, {self.dim}")
        logging.info(f"using {schema}")

        r.ft(self.index_name).create_index(schema)
        r.ft(self.index_name).config_set("default_dialect", 2)
        logging.info(f"Creating Redis schema: {schema} in index {self.index_name}")

    def write_embeddings_to_search_index(self, columns):
        r = self.conn
        pipe = r.pipeline()

        vector_dict: Dict[str, List[float]] = self.file_to_embedding_dict(columns)
        logging.info(f"Inserting vector into Redis search index {self.index_name}")

        # an input dictionary from a dictionary
        for i, (k, v) in enumerate(vector_dict.items()):
            data = np.array(v, dtype=np.float64)
            np_vector = data.astype(np.float64)

            try:
                # write to index using pipeline
                pipe.hset(f"vector::{k}", mapping={self.vector_field: np_vector.tobytes()})
                if i % 2000 == 0:
                    logging.info(f"Set vector {i}  into {self.index_name} as {self.vector_field}")
                    pipe.execute()
            except Exception as e:
                logging.error("An exception occurred: {}".format(e))

    def write_keys_to_cache(self, columns, key_prefix):
        """
        Writing title, author, and link and other string metadata for lookups in search
        """
        r = self.conn
        pipe = r.pipeline()

        vector_dict: Dict[str, str] = self.file_to_embedding_dict(columns)
        logging.info(f"Inserting keys into Redis keyspace {key_prefix}")

        for i, (k, v) in enumerate(vector_dict.items()):
            try:
                # write to Redis
                pipe.set(f"{key_prefix}::{k}", v)
                if i % 1000 == 0:
                    logging.info(f"Set {i} into {key_prefix}")
                    pipe.execute()
            except Exception as e:
                logging.error("An exception occurred: {}".format(e))

    def get_search_index_metadata(self):
        r = self.conn
        metadata = r.ft(self.index_name).info()
        logging.info(
            f"name: {metadata['index_name']}, "
            f"docs: {metadata['max_doc_id']}, "
            f"time:{metadata['total_indexing_time']} seconds"
        )
