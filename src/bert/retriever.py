from src.bert.knn_search import KNNSearch
from src.bert.redis_conn import RedisConnection

"""Perform simple KNN search in Redis
"""


retriever = KNNSearch(RedisConnection().conn())

print(retriever.top_knn("dog"))
