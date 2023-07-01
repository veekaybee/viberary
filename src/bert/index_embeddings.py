from pathlib import Path

from models.bert.indexer import Indexer
from models.bert.title_mapper import TitleMapper

from inout import file_reader as f
from inout.redis_conn import RedisConnection

training_data: Path = f.get_project_root() / "src" / "training_data" / "20230701_training.parquet"

# Instantiate indexer
indexer = Indexer(
    RedisConnection().conn(),
    training_data,
    "vector",
    "viberary",
    nvecs=1000,
    dim=384,
    max_edges=40,  # maximum allowed outgoing edges for each node in the graph in each layer.
    ef=200,  # maximum allowed potential outgoing edges candidates for each node in the graph
    token_field_name="token",
    distance_metric="COSINE",
    float_type="FLOAT64",
)

# Delete existing index
indexer.drop_index()

# Load embeddings from parquet file
indexer.file_to_embedding_dict()

# Recreate schema based on Indexer
indexer.create_index_schema()

# Load Embeddings
indexer.load_docs()

# # Check Index Metadata
indexer.get_index_metadata()

# Write index mapping title to index
title_mapper = TitleMapper(
    RedisConnection().conn(),
    training_data,
)

title_mapper.load_title_docs()
title_mapper.load_author_docs()
