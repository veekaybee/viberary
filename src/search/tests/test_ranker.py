import pytest
from fakeredis import FakeRedis

from search.knn_search import KNNSearch


@pytest.fixture
def redis_mock():
    return FakeRedis()


def parse_and_sanitize_input():
    input = " dogs cats frogs@"

    sanitized_input = parse_and_sanitize_input()

    assert input == sanitized_input


def test_rescore(redis_mock):
    result_list = [
        (0.888, "dogs", "lassie", "http://", 1, 0),
        (0.777, "cats", "hello kitty", "http://", 2, 1),
        (0.666, "birds", "big bird", "http://", 3, 2),
    ]
    expected_list = [
        (0.888, "dogs", "lassie", "http://", 1, 1),
        (0.777, "cats", "hello kitty", "http://", 2, 2),
        (0.666, "birds", "big bird", "http://", 3, 3),
    ]

    rescore = KNNSearch(redis_mock).rescore(result_list)

    assert rescore == expected_list


def test_dedup(redis_mock):
    result_list = [
        (0.888, "dogs", "lassie", "http://", 10),
        (0.888, "dogs", "lassie", "http://", 20),
        (0.777, "cats", "hello kitty", "http://", 30),
        (0.666, "birds", "big bird", "http://", 40),
    ]
    expected_list = [
        (0.888, "dogs", "lassie", "http://", 20),
        (0.777, "cats", "hello kitty", "http://", 30),
        (0.666, "birds", "big bird", "http://", 40),
    ]

    rescore = KNNSearch(redis_mock).dedup_by_score(result_list)
    assert rescore == expected_list
