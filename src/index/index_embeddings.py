from pathlib import Path

from index.indexer import Indexer
from inout.file_reader import get_config_file as config
from inout.redis_conn import RedisConnection

# Load Embeddings Data
conf = config()
embedding_data = Path(conf["training_data"]["path"]) / Path(conf["training_data"]["file"])

# Instantiate indexer
indexer = Indexer(
    RedisConnection().conn(),
    embedding_data,
    vector_field="vector",
    author_field="author",
    title_field="title",
    link_field="link",
    review_count_field="review_count",
    index_name="viberary",
    nvecs=800000,
    dim=768,
    max_edges=40,  # maximum allowed outgoing edges for each node in the graph in each layer.
    ef=200,  # maximum allowed potential outgoing edges candidates for each node in the graph
    distance_metric="COSINE",
    float_type="FLOAT64",
    index_type="HNSW",
)

# Create search index
# Delete existing index
indexer.drop_index()

# Load Embeddings
indexer.write_embeddings_to_search_index(
    columns=["title", "index", "author", "link", "review_count", "embeddings"]
)

# Recreate schema based on Indexer
indexer.create_search_index_schema()


# Check Search Index Metadata
indexer.get_search_index_metadata()
