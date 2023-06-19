from src.logs.viberary_logging import ViberaryLogging

import duckdb
import pandas as pd

"""Generates input data in English for Embeddings
"""

con = duckdb.connect("viberary.duckdb")

## original file is from https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home
## Actual file: https://drive.google.com/uc?id=1LXpK1UfqtP89H1tYy0pBGHjYk8IhigUK


duckdb.sql(
    "select * from read_json_auto('/Users/vicki/viberary/viberary/data/goodreads_books.json',lines='true'"
)
duckdb.sql(
    "CREATE TABLE goodreads_en as select * from goodreads WHERE language_code like 'en%';"
)

sentences = con.sql(
    """select concat_ws(' ' , lower(regexp_replace(title, '[[:^alpha:]]',' ','g')), \
                    lower(regexp_replace(description, '[[:^alpha:]]',' ','g'))) as sentence from goodreads_en;"""
).df()

sentences.to_csv("sentences_en.csv", index=False, header=False)
