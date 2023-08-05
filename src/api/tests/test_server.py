from unittest.mock import patch

import pytest
from fakeredis import FakeRedis

from api.main import app
from search.knn_search import KNNSearch


@pytest.fixture
def test_client():
    app.testing = True
    return app.test_client()


@pytest.fixture
def redis_mock():
    return FakeRedis()


def knn_search_mock(redis_mock):
    pass


@patch.object(KNNSearch, "__init__", knn_search_mock)
def test_search_with_post_request(test_client):
    response = test_client.post("/search", data={"query": "test_query"})
    assert response.status_code == 302
    assert "/search/results?query=test_query" in response.headers["Location"]
