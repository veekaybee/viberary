from conf.config_manager import ConfigManager
from conf.redis_conn import RedisConnection
from search.knn_search import KNNSearch

retriever = KNNSearch(RedisConnection().conn())
conf = ConfigManager()


def get_model_results(word: str, search_conn: KNNSearch) -> dict:
    """
    Stores query and top 10 results in a dict
    Args:
        word: stri
        search_conn:

    Returns: Dictionary of query/results

    """
    eval_dict = {}
    data = search_conn.top_knn(word)
    eval_dict[word] = data

    print(eval_dict)
