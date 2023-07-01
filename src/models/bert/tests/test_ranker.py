import pytest
from fakeredis import FakeRedis

from models.bert.knn_search import KNNSearch


@pytest.fixture
def redis_mock():
    return FakeRedis()


def test_rescore(redis_mock):
    result_list = [
        (1, 0.888, "dogs", "lassie"),
        (2, 0.777, "cats", "hello kitty"),
        (3, 0.666, "birds", "big bird"),
    ]
    expected_list = [("dogs", "lassie", 1), ("cats", "hello kitty", 2), ("birds", "big bird", 3)]

    rescore = KNNSearch(redis_mock).rescore(result_list)

    assert rescore == expected_list
