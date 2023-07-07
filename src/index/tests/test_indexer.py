from pathlib import Path

import pandas as pd
import pytest
from fakeredis import FakeRedis

from src.index.indexer import Indexer
from src.inout import file_reader as f
from src.inout.redis_conn import RedisConnection


@pytest.fixture
def redis_mock():
    return FakeRedis()


@pytest.fixture
def sample_dataframe():
    data = {
        "title": ["Title 1", "Title 2"],
        "index": [1, 2],
        "author": ["Author 1", "Author 2"],
        "link": ["Link 1", "Link 2"],
        "embeddings": [0.001, 0.0002],
    }
    return pd.DataFrame(data)


# TODO : mock Parquet file and fix test
@pytest.mark.skip(reason="need to mock out Parquet file")
def test_convert_dataframe_to_dict(redis_mock, sample_dataframe):
    embedding_data: Path = (
        f.get_project_root() / "src" / "training_data" / "20230710_learned_embeddings.snappy"
    )

    indexer = Indexer(
        RedisConnection().conn(),
        embedding_data,
        vector_field="vector",
        author_field="author",
        title_field="title",
        link_field="link",
        index_name="viberary",
        nvecs=800000,
        dim=768,
        max_edges=40,  # maximum allowed outgoing edges for each node in the graph in each layer.
        ef=200,  # maximum allowed potential outgoing edges candidates for each node in the graph
        distance_metric="COSINE",
        float_type="FLOAT64",
        index_type="HNSW",
    )

    expected_output = {
        1: ("Title 1", "Author 1", "Link 1", "Embeddings 1"),
        2: ("Title 2", "Author 2", "Link 2", "Embeddings 2"),
    }
    result = indexer.file_to_embedding_dict(sample_dataframe)
    assert result == expected_output
