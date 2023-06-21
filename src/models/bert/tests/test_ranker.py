import pytest
from fakeredis import FakeRedis

from models.bert.knn_search import KNNSearch


@pytest.fixture
def redis_mock():
    return FakeRedis()


def test_rescore(redis_mock):
    result_list = [(0, 0.888, "dogs"), (1, 0.777, "cats"), (2, 0.666, "birds")]
    expected_list = [("dogs", 0), ("cats", 1), ("birds", 2)]

    rescore = KNNSearch(redis_mock).rescore(result_list)

    assert rescore == expected_list
