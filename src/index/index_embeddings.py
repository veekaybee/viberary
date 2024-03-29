from pathlib import Path

from conf.config_manager import ConfigManager
from conf.redis_conn import RedisConnection
from index.index_fields import IndexFields
from index.indexer import Indexer

# Load Embeddings Data
conf = ConfigManager().get_config_file()
filepath = Path(f"{conf['embeddings_data']['path']}{conf['embeddings_data']['file']}")
index_name = conf["search"]["index_name"]
nvecs = conf["search"]["nvecs"]
dim = conf["search"]["dim"]
max_edges = conf["search"]["max_edges"]
ef = conf["search"]["ef"]
distance_metric = conf["search"]["distance_metric"]
float_type = conf["search"]["float_type"]
index_type = conf["search"]["index_type"]

# # Instantiate indexer
indexer = Indexer(
    RedisConnection().conn(),
    filepath=filepath,
    index_name=index_name,
    index_type=index_type,
    distance_metric=distance_metric,
    float_type=float_type,
    nvecs=nvecs,
    dim=dim,
    max_edges=max_edges,
    ef=ef,
)

fields = IndexFields()

# Delete existing index
indexer.drop_index()

# Load Embeddings
indexer.write_embeddings_to_search_index(
    columns=[
        fields.title_field,
        fields.index_field,
        fields.author_field,
        fields.link_field,
        fields.review_count_field,
        fields.embeddings_field,
    ]
)

# Recreate schema based on Indexer
# This step has to happen after the hset, otherwise it will be slow
indexer.create_search_index_schema()

# Check Search Index Metadata
indexer.get_search_index_metadata()
