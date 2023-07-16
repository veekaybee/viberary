from dataclasses import dataclass


@dataclass(frozen=True)
class IndexFields:
    vector_field: str = "vector"
    index_field: str = "index"
    title_field: str = "title"
    author_field: str = "author"
    link_field: str = "link"
    review_count_field: int = "review_count"
    embeddings_field: str = "embeddings"
