import json
import logging.config
from typing import List, Tuple

import numpy as np
from redis.commands.search.query import Query

from index.index_fields import IndexFields
from inout.file_reader import get_config_file as config
from model.onnx_embedding_generator import ONNXEmbeddingGenerator
from search.sanitize_input import InputSanitizer


class KNNSearch:
    def __init__(
        self,
        redis_conn,
    ) -> None:
        self.conf = config()
        logging.config.fileConfig(self.conf["logging"]["path"])
        self.conn = redis_conn
        self.index = self.conf["search"]["index_name"]
        self.fields = IndexFields()
        self.vector_field = self.fields.vector_field
        self.title_field = self.fields.title_field
        self.author_field = self.fields.author_field
        self.link_field = self.fields.link_field
        self.review_count_field = self.fields.review_count_field
        self.sanitizer = InputSanitizer()
        self.model = ONNXEmbeddingGenerator()

    def vectorize_query(self, query_string) -> np.ndarray:
        query_embedding = self.model.generate_embeddings(query_string)
        numpy_embedding = query_embedding.numpy()
        return numpy_embedding

    def top_knn(
        self,
        query:str,
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
        top_k = self.conf["search"]["top_k"]

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

        log_data = {"query": query, "results": [[i[1], i[2], i[3], i[4]] for i in index_vector]}

        log_message = json.dumps(log_data)

        logging.info(log_message)

        deduped_results = self.dedup_by_number_of_reviews(index_vector)
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

    def dedup_by_number_of_reviews(
        self, result_list: List[Tuple[float, str, str, str, int]]
    ) -> List[Tuple[float, str, str, str, int]]:
        """
        Dedup ranked list of 50 elements by title by number of reviews
        and returns subest of top elements
        Args:
            result_list ():

        Returns: Deduped list by title and number of reviews
        """

        deduped_list = []

        titles = set()

        for element in result_list:
            if element[1] not in titles:
                deduped_list.append(element)
                titles.add(element[1])
            else:
                pass

        return deduped_list[0:10]
