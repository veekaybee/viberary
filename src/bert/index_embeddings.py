from src.bert.indexer import Indexer
from importlib import resources
from pathlib import Path
from src.io import file_reader as f

training_data: Path = f.get_project_root() / "data" / "embeddings.snappy"

# Instantiate indexer
indexer = Indexer(
    training_data,
    nvecs=10,
    dim=384,
    max_edges=40,  # Optional Number of maximum allowed outgoing edges for each node in the graph in each layer.
    ef=200,  # Number of maximum allowed potential outgoing edges candidates for each node in the graph
    vector_field="vector",
    token_field_name="token",
    index_name="viberary",
    distance_metric="COSINE",
    float_type="FLOAT64",
)

# Load embeddings from parquet file
indexer.file_to_embedding_dict()

# Delete existing index
indexer.delete_index()

# Recreate schema based on Indexer
indexer.create_index_schema()

# Load Embeddings
indexer.load_docs()

# Check Index Metadata
indexer.get_index_metadata()
