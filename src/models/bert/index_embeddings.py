import time
from importlib import resources
from pathlib import Path

from redis.exceptions import ConnectionError

from inout import file_reader as f
from inout.redis_conn import RedisConnection
from models.bert.indexer import Indexer
from models.bert.title_mapper import TitleMapper

training_data: Path = f.get_project_root() / "src" / "data" / "learned_embeddings.snappy"


def connect_to_redis_with_retries():
    max_retries = 5  # Maximum number of connection retries
    retry_delay = 2  # Delay between retries in seconds

    for attempt in range(max_retries):
        try:
            return RedisConnection().conn()
        except ConnectionError:
            print(
                f"Connection to Redis failed (attempt {attempt + 1}/{max_retries}). Retrying in {retry_delay} seconds..."
            )
            time.sleep(retry_delay)

    raise ConnectionError(f"Failed to connect to Redis after {max_retries} attempts.")


redis_conn = connect_to_redis_with_retries()

# Instantiate indexer
indexer = Indexer(
    redis_conn,
    training_data,
    nvecs=1000,
    dim=384,
    max_edges=40,  # Optional Number of maximum allowed outgoing edges for each node in the graph in each layer.
    ef=200,  # Number of maximum allowed potential outgoing edges candidates for each node in the graph
    vector_field="vector",
    token_field_name="token",
    index_name="viberary",
    distance_metric="COSINE",
    float_type="FLOAT64",
)

# Delete existing index
indexer.delete_index()

# Load embeddings from parquet file
indexer.file_to_embedding_dict()

# Recreate schema based on Indexer
indexer.create_index_schema()

# Load Embeddings
indexer.load_docs()

# Check Index Metadata
indexer.get_index_metadata()

# Write index mapping title to index
title_mapper = TitleMapper(
    RedisConnection().conn(),
    training_data,
)

title_mapper.load_docs()
