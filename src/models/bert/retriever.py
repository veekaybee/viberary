from src.models.bert.knn_search import KNNSearch
from src.io.redis_conn import RedisConnection

"""Tests retrieval from Redis
"""

retriever = KNNSearch(RedisConnection().conn())
results = retriever.top_knn("funny")
print(results)
