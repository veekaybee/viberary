import logging.config
from pathlib import Path

import duckdb

from inout import file_reader as f

"""Generates training dataset for converting to SBERT
Source data https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home
"""


class TrainingDataGenerator:
    root_path = Path("viberary" / f.get_project_root())

    books = Path(root_path / "data" / "goodreads_books.json")
    authors = Path(root_path / "data" / "goodreads_book_authors.json")
    reviews = Path(root_path / "data" / "goodreads_reviews_dedup.json")

    def __init__(self):
        logging.config.fileConfig(f.get_project_root() / "logging.conf")

    def _create_tables(self):
        duckdb.connect("")
        duckdb.sql(
            "CREATE TABLE goodreads_reviews AS "
            "SELECT * FROM read_json_auto(reviews,ignore_errors='true',lines='true') ;"
        )
        duckdb.sql(
            "CREATE TABLE goodreads AS "
            "SELECT * FROM read_json_auto(books,ignore_errors='true',lines='true') ;"
        )
        duckdb.sql(
            "CREATE TABLE goodreads_authors AS "
            "SELECT REGEXP_EXTRACT(authors, '[0-9]+') AS"
            "author_id, title, description, average_rating, book_id FROM goodreads);"
        )

    def generate(self, con):
        self._create_tables()

        duckdb.sql("COPY (query ) TO '20230701_training.parquet' (FORMAT PARQUET);")
