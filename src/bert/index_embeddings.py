exit;
from src.bert.indexer import Indexer
from importlib import resources
from pathlib import Path

training_data:Path = Path("data/sentence_embeddings.csv")

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


indexer.file_to_embedding_dict()
indexer.delete_index()
indexer.create_index_schema()
indexer.load_docs()
indexer.check_load()