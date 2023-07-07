import logging
import logging.config
from typing import Dict, List

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

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
        title_field,
        author_field,
        index_name,
        link_field,
        nvecs=0,
        dim=0,
        max_edges=0,
        ef=0,
        index_type="HNSW",
        distance_metric="COSINE",
        float_type="FLOAT64",
    ) -> None:
        self.conn = redis_conn
        self.filepath = filepath
        self.dim = dim
        self.nvecs = nvecs
        self.max_edges = max_edges
        self.ef = ef
        self.vector_field_name = vector_field
        self.title_field_name = title_field
        self.author_field_name = author_field
        self.link_field_name = link_field
        self.float_type = float_type
        self.index_name = index_name
        self.distance_metric = distance_metric
        self.index_type = index_type
        logging.config.fileConfig(f.get_project_root() / "logging.conf")

    # TODO: unit test these columns and parquet writes
    def file_to_embedding_dict(self, columns: List) -> Dict:
        """
        Reads Parquet file and processes in Pandas
        in chunks

        index: title, author, link, embeddings
        """

        parquet = self.filepath

        logging.info(f"Creating dataframe from {parquet}...")

        parquet_file = pq.ParquetFile(str(parquet))

        final_df = pd.DataFrame()

        for i, batch in enumerate(parquet_file.iter_batches(columns=columns)):
            logging.info(f"Loading RecordBatch {i}")
            df = batch.to_pandas()
            final_df = final_df.append(df, ignore_index=True)

        # Format as dict for read into Redis
        df_dict = final_df.to_dict("split")
        data = df_dict["data"]
        # Data: Index, title, author, Link, embeddings
        my_dict = {item[1]: (item[0], item[2], item[3], item[4]) for item in data if len(item) == 5}

        return my_dict

    def drop_index(self):
        """Delete Redis index but does not delete underlying data"""
        logging.info(f"Deleting Redis index {self.index_name}...")
        r = self.conn

        if r.exists(self.index_name):
            r.ft(self.index_name).dropindex(delete_documents=True)

    def create_search_index_schema(
        self,
    ) -> None:
        r = self.conn
        """Create Redis index with schema parameters from config"""
        logging.info("Creating redis schema...")

        schema = (
            VectorField(
                self.vector_field_name,
                self.index_type,
                {"TYPE": self.float_type, "DIM": self.dim, "DISTANCE_METRIC": self.distance_metric},
            ),
            TextField(self.title_field_name),
            TextField(self.author_field_name),
            TextField(self.link_field_name),
        )
        logging.info(f"using {self.vector_field_name}, {self.float_type}, {self.dim}")
        logging.info(f"using {schema}")

        r.ft(self.index_name).create_index(
            fields=schema,
            definition=IndexDefinition(prefix=["viberary:"], index_type=IndexType.HASH),
        )
        r.ft(self.index_name).config_set("default_dialect", 2)
        logging.info(f"Creating Redis schema: {schema} in index {self.index_name}")

    def write_embeddings_to_search_index(self, columns):
        r = self.conn
        pipe = r.pipeline(transaction=False)

        vector_dict = self.file_to_embedding_dict(columns)
        logging.info(f"Inserting vector into Redis search index {self.index_name}")

        for k, v in vector_dict.items():
            np_vector = v[2].astype(np.float64)
            pipe.hset(
                f"{self.index_name}:{k}",
                mapping={
                    self.vector_field_name: np_vector.tobytes(),
                    self.title_field_name: v[0],
                    self.author_field_name: v[1],
                    self.link_field_name: v[3],
                },
            )
            if k % 5000 == 0:
                logging.info(f"Inserting {k} vector into Redis index {self.index_name}")
                pipe.execute()

    def get_search_index_metadata(self):
        r = self.conn
        metadata = r.ft(self.index_name).info()
        logging.info(
            f"name: {metadata['index_name']}, "
            f"docs: {metadata['num_records']}, "
            f"time:{metadata['total_indexing_time']} ms"
        )
