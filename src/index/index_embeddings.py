from pathlib import Path

from index.indexer import Indexer
from index.title_mapper import TitleMapper
from inout import file_reader as f
from inout.redis_conn import RedisConnection

training_data: Path = f.get_project_root() / "src" / "training_data" / "20230701_training.parquet"
embedding_data: Path = (
    f.get_project_root() / "src" / "training_data" / "20230701_learned_embeddings.snappy"
)

# Load Embeddings Data

# Instantiate indexer
indexer = Indexer(
    RedisConnection().conn(),
    embedding_data,
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


# Load plain keys/values that map to title and author
title_mapper.load_docs("title")
title_mapper.load_docs("author")
title_mapper.load_docs("link")
