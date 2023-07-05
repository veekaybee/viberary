from inout.redis_conn import RedisConnection
from search.knn_search import KNNSearch

retriever = KNNSearch(RedisConnection().conn())

result = retriever.top_knn("dog")
print(result)
