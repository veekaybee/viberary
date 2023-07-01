from src.io.redis_conn import RedisConnection
from src.search.knn_search import KNNSearch

"""Tests retrieval from Redis
"""

retriever = KNNSearch(RedisConnection().conn())
results = retriever.top_knn("funny")
print(results)
