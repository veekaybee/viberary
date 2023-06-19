import pprint
from pprint import pformat
from typing import List

import numpy as np
import torch
from redis import Redis
from redis.commands.search.query import Query
from sentence_transformers import SentenceTransformer, util
from torch import Tensor

from redis.commands.search import result

from src.logs.viberary_logging import ViberaryLogging


class KNNSearch:
    def __init__(self, query_string, redis_conn, vector_field="vector") -> None:
        self.conn = redis_conn
        self.index = "viberary"
        self.vector_field = vector_field
        self.logger = ViberaryLogging().setup_logging()
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.query_string = query_string

    # TODO: character escaping, etc, etc for query sanitation input
    def vectorize_query(self) -> np.ndarray:
        query_embedding = self.embedder.encode(self.query_string, convert_to_tensor=False)
        return query_embedding

    def top_knn(self, top_k=10) -> List:
        """Return top 10 vector results from model using HNSW search

        Args:
            top_k (int, optional): _description_. Defaults to 10.

        Returns:
            List: Returns list of tuple that includes the index, cosine similarity, and book title
        """
        query_vector = self.vectorize_query().astype(np.float64).tobytes()

        q = (
            Query(f"*=>[KNN {top_k} @{self.vector_field} $vec_param AS vector_score]")
            .sort_by("vector_score", asc=False)
            .paging(0, top_k)
            .return_fields("token", "vector_score")
            .dialect(2)
        )

        params_dict = {"vec_param": query_vector}

        results = self.conn.ft(self.index).search(q, query_params=params_dict)
        results_docs = results.docs
        self.logger.info(pformat(results))

        index_vector = []

        for i in results_docs:
            id = i["id"]  # bookid
            id_int = id.lstrip("vector::")
            title = self.conn.get(f"title::{id_int}")
            index_vector.append((i["id"], i["vector_score"], title))

        self.logger.info(pformat(index_vector))

        scored_results = self.rescore(index_vector)

        return scored_results

    def rescore(self, result_list: List) -> List:
        """Takes a ranked list and returns ordinal scores for each
        cosine similarity for UI legibility
        """
        ranked_list = []

        for index, val in enumerate(result_list):
            ranked_list.append((val[2], index))

        return ranked_list
