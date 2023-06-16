import pprint
from redis import Redis
from redis.commands.search.query import Query

from sentence_transformers import SentenceTransformer, util
import torch
from torch import Tensor

from typing import List

import numpy as np
from pprint import pformat


class KNNSearch:
    def __init__(self, redis_conn, vector_field="vector") -> None:
        self.conn = redis_conn
        self.query_string = ""
        self.index = "viberary"
        self.vector_field = vector_field

    def vectorize_query(self, query_string) -> np.ndarray:
        embedder = SentenceTransformer("all-MiniLM-L6-v2")
        query_embedding = embedder.encode(self.query_string, convert_to_tensor=False)

        return query_embedding

    def top_knn(self, query_string, top_k=10):
        query_vector = self.vectorize_query(query_string).astype(np.float64).tobytes()

        q = (
            Query(f"*=>[KNN {top_k} @{self.vector_field} $vec_param AS vector_score]")
            .sort_by("vector_score")
            .paging(0, top_k)
            .return_fields("token", "vector_score")
            .dialect(2)
        )

        params_dict = {"vec_param": query_vector}

        # TODO: log and pretty return results
        results = self.conn.ft(self.index).search(q, query_params=params_dict)
        logging.info(pformat(results))
        return results
