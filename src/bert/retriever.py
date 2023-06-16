from src.bert.knn_search import KNNSearch

"""Perform simple KNN search in Redis
"""


retriever = KNNSearch()

retriever.top_knn("dog")
