import pytest
from fakeredis import FakeRedis

from ..knn_search import KNNSearch


@pytest.fixture
def redis_mock():
    return FakeRedis()


def test_rescore(redis_mock):
    result_list = [(1, 0.888, "dogs"), (2, 0.777, "cats"), (3, 0.666, "birds")]
    expected_list = [("dogs", 1), ("cats", 2), ("birds", 3)]

    rescore = KNNSearch(redis_mock).rescore(result_list)

    assert rescore == expected_list
