from src.models.bert.knn_search import KNNSearch
from src.io.redis_conn import RedisConnection

"""Tests retrieval from Redis
"""

retriever = KNNSearch("beauty and the beast", RedisConnection().conn())
results = retriever.top_knn()
print(results)
