import logging.config
from typing import List, Tuple

import numpy as np
from redis.commands.search.query import Query
from sentence_transformers import SentenceTransformer

from inout import file_reader as f
from search.sanitize_input import InputSanitizer


class KNNSearch:
    def __init__(
        self,
        redis_conn,
    ) -> None:
        self.conn = redis_conn
        self.index = "viberary"
        self.vector_field = "vector"
        self.title_field = "title"
        self.author_field = "author"
        self.link_field = "link"
        self.review_count_field = "review_count"
        logging.config.fileConfig(f.get_project_root() / "logging.conf")
        self.sanitizer = InputSanitizer()
        self.embedder = SentenceTransformer("sentence-transformers/msmarco-distilbert-base-v3")

    def vectorize_query(self, query_string) -> np.ndarray:
        query_embedding = self.embedder.encode(query_string, convert_to_tensor=False)
        return query_embedding

    def top_knn(
        self,
        query,
        top_k=50,
    ) -> List[Tuple[float, str, str, str, int]]:
        """Return top k vector results from model

        Args:
            top_k (int, optional): Defaults to 50.
            query str: query string

        Returns:
            List: Returns [(score, title, author, link, review_count)]
        """
        r = self.conn
        sanitized_query = self.sanitizer.parse_and_sanitize_input(query)

        query_vector = self.vectorize_query(sanitized_query).astype(np.float64).tobytes()

        q = (
            Query(f"*=>[KNN {top_k} @{self.vector_field} $vec_param AS vector_score]")
            .sort_by("vector_score", asc=False)
            .sort_by(f"{self.review_count_field}", asc=False)
            .paging(0, top_k)
            .return_fields(
                "vector_score",
                self.vector_field,
                self.title_field,
                self.author_field,
                self.link_field,
                self.review_count_field,
            )
            .dialect(2)
        )

        params_dict = {"vec_param": query_vector}

        results = r.ft(self.index).search(q, query_params=params_dict)
        results_docs = results.docs

        index_vector = []

        for i in results_docs:
            score = i["vector_score"]
            title = i["title"]
            author = i["author"]
            link = i["link"]
            review_count = i["review_count"]
            index_vector.append((score, title, author, link, review_count))

        logging.info(f"query:{query}, results:{[[i[1], i[2], i[3], i[4]] for i in index_vector]}")

        deduped_results = self.dedup_by_score(index_vector)
        scored_results = self.rescore(deduped_results)

        return scored_results

    def rescore(self, result_list: List[Tuple[float, str, str, str, int]]) -> List:
        """Takes a ranked list of tuples
        Each tuple contains [(score, title, author, link, review_count)]
        and returns ordinal scores for each starting at 1
        """
        return [
            (val[0], val[1], val[2], val[3], val[4], index)
            for index, val in enumerate(result_list, 1)
        ]

    def dedup_by_score(
        self, result_list: List[Tuple[float, str, str, str, int]]
    ) -> List[Tuple[float, str, str, str, int]]:
        """
        Dedup ranked list of 50 elements by title by number of reviews and returns subest of top elements
        Args:
            result_list ():

        Returns: Deduped list by nubmer of reviews

        """

        deduped_list = []

        for l1, l2 in zip(result_list, result_list[1:]):
            if l1[1] == l2[1]:
                if l1[4] > l2[4]:
                    deduped_list.append(l1)
                elif l1[4] == l2[4]:
                    deduped_list.append(l2)
                else:
                    deduped_list.append(l2)
            else:
                deduped_list.append(l2)

        return deduped_list[0:10]
