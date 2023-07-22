import logging.config
from datetime import datetime
from pathlib import Path

import duckdb

from inout.file_reader import get_config_file as config

"""Generates training dataset for converting to SBERT
Source data https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home
"""


class TrainingDataGenerator:
    def __init__(self):
        conf = config()
        logging.config.fileConfig(Path(conf["logging"]["path"]))
        self.con = duckdb.connect("viberary.db")

        self.books = Path(conf["data"]["books"])
        self.authors = Path(conf["data"]["authors"])
        self.reviews = Path(conf["data"]["reviews"])

    def _get_date_and_hour(self) -> str:
        current_date = datetime.now()
        formatted_date: str = current_date.strftime("%Y%m%d%H")

        return formatted_date

    def _create_tables(self, duckdb_conn):
        reviews_query = f"""CREATE TABLE IF NOT EXISTS goodreads_reviews
        AS SELECT *
        FROM read_json_auto("{self.reviews}",ignore_errors='true',lines='true') ;"""

        books_query = f"""CREATE TABLE IF NOT EXISTS goodreads
        AS SELECT *
        FROM read_json_auto("{self.books}",ignore_errors='true',lines='true') ;"""

        authors_query = f"""CREATE TABLE IF NOT EXISTS goodreads_authors
        AS SELECT author_id, name
        FROM read_json_auto("{self.authors}",lines='true');"""

        author_ids_query = """CREATE TABLE IF NOT EXISTS goodreads_auth_ids
        AS SELECT REGEXP_EXTRACT(authors, '[0-9]+') as author_id, title, description,link,
        average_rating, book_id, text_reviews_count
        FROM goodreads;"""

        # Drop and recreate new tables
        logging.info("Dropping old tables")
        duckdb_conn.sql(
            """DROP TABLE goodreads_authors;
            DROP TABLE goodreads_auth_ids;
            DROP TABLE goodreads_reviews;
            DROP TABLE goodreads;"""
        )
        logging.info("Creating reviews..")
        duckdb_conn.sql(reviews_query)

        logging.info("Creating books..")
        duckdb_conn.sql(books_query)

        logging.info("Creating authors..")
        duckdb_conn.sql(authors_query)

        logging.info("Creating author_ids..")
        duckdb_conn.sql(author_ids_query)

    def _get_join_tables_query(self, duckdb_conn):
        date = self._get_date_and_hour()

        output_path: Path = self.conf["training_data"]["path"] / f"{date}_training.parquet"

        query = """SELECT
        review_text,
        goodreads_auth_ids.title,
        link,
        goodreads_auth_ids.description,
        goodreads_auth_ids.average_rating,
        goodreads_authors.name AS author,
        text_reviews_count,
        review_text || goodreads_auth_ids.title || goodreads_auth_ids.description 
        || goodreads_authors.name as sentence
        FROM goodreads_auth_ids
        JOIN goodreads_reviews
        ON goodreads_auth_ids.book_id = goodreads_reviews.book_id
        JOIN goodreads_authors
        ON goodreads_auth_ids.author_id = goodreads_authors.author_id
        WHERE goodreads_auth_ids.author_id NOT ILIKE '' """

        duckdb_conn.sql(f"COPY ({query} ) TO '{output_path}' (FORMAT PARQUET);")

    def generate(self):
        date = self._get_date_and_hour()
        logging.info("Creating tables from JSON...")
        self._create_tables(duckdb_conn=self.con)
        logging.info(f"Writing parquet file {date}_training.parquet")
        self._get_join_tables_query(duckdb_conn=self.con)


if __name__ == "__main__":
    TrainingDataGenerator().generate()
