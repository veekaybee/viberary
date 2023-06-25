from pathlib import Path

from inout import file_reader as f
from inout.redis_conn import RedisConnection
from models.bert.indexer import Indexer
from models.bert.title_mapper import TitleMapper

training_data: Path = f.get_project_root() / "src" / "data" / "learned_embeddings.snappy"

# Instantiate indexer
indexer = Indexer(
    RedisConnection().conn(),
    training_data,
    "vector",
    "viberary",
    nvecs=1000,
    dim=384,
    max_edges=40,  # Optional Number of maximum allowed outgoing edges for each node in the graph in each layer.
    ef=200,  # Number of maximum allowed potential outgoing edges candidates for each node in the graph
    token_field_name="token",
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

# # Check Index Metadata
# indexer.get_index_metadata()

# Write index mapping title to index
title_mapper = TitleMapper(
    RedisConnection().conn(),
    training_data,
)

title_mapper.load_docs()
