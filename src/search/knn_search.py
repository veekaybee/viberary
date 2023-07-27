import logging.config
import re
from collections import namedtuple
from typing import List, Tuple

import numpy as np
from redis.commands.search.query import Query

from index.index_fields import IndexFields
from model.onnx_embedding_generator import ONNXEmbeddingGenerator


class KNNSearch:
    fields = ["score", "title", "author", "link", "review_count"]
    BookEntries = namedtuple("BookEntries", fields)

    def __init__(self, redis_conn, conf) -> None:
        self.conf = conf.get_config_file()
        self.conn = redis_conn
        self.index = self.conf["search"]["index_name"]
        self.fields = IndexFields()
        self.vector_field = self.fields.vector_field
        self.title_field = self.fields.title_field
        self.author_field = self.fields.author_field
        self.link_field = self.fields.link_field
        self.review_count_field = self.fields.review_count_field
        self.model = ONNXEmbeddingGenerator(conf)

    def vectorize_query(self, query_string) -> np.ndarray:
        query_embedding = self.model.generate_embeddings(query_string)
        numpy_embedding = query_embedding.numpy()
        return numpy_embedding

    def parse_and_sanitize_input(self, input_string: str) -> str:
        input_string = input_string.strip()
        input_string = re.sub(r"[^\w\s]", "", input_string)
        input_string = re.sub(r"\s+", " ", input_string)

        return input_string

    def top_knn(
        self,
        query: str,
    ) -> List[Tuple[float, str, str, str, int]]:
        """Return top k vector results from model

        Args:
            top_k (int, optional): Defaults to 50.
            query str: query string

        Returns:
            List: Returns [(score, title, author, link, review_count)]
        """
        r = self.conn
        top_k = self.conf["search"]["top_k"]

        sanitized_query = self.parse_and_sanitize_input(query)
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

        index_vector = [
            self.BookEntries(
                i["vector_score"], i["title"], i["author"], i["link"], i["review_count"]
            )
            for i in results_docs
        ]

        log_data = {"query": query, "results": results.docs}
        logging.info(log_data)

        deduped_results = self.dedup_by_number_of_reviews(index_vector)

        return deduped_results

    def dedup_by_number_of_reviews(self, result_list: BookEntries) -> BookEntries:
        """
        Dedup ranked list of 50 elements
        Args:
            result_list ():

        Returns: Deduped list by title
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
