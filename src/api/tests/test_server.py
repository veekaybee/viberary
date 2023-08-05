from unittest.mock import Mock, patch

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


@pytest.fixture
def mock_knn_search():
    # Create a mock for the KNNSearch class
    return Mock(spec=KNNSearch)


def test_search_endpoint(test_client, mock_knn_search):
    with patch("search.knn_search.KNNSearch", return_value=mock_knn_search):
        response = test_client.post("/search", data={"query": "test_query"})

    # Assertions on the redirect and the KNNSearch mock
    assert response.status_code == 302
    assert "/search/results?query=test_query" in response.headers["Location"]
