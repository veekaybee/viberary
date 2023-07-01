CREATE TABLE goodreads_reviews AS SELECT * FROM read_json_auto('/Users/vicki/viberary/data/goodreads_reviews_dedup.json',ignore_errors='true',lines='true') ;

CREATE TABLE goodreads AS SELECT * FROM read_json_auto('/Users/vicki/viberary/data/goodreads_books.json',lines='true');

CREATE TABLE goodreads_authors AS SELECT * FROM read_json_auto('/Users/vicki/viberary/data/goodreads_book_authors.json',lines='true');

CREATE table authorid as select REGEXP_EXTRACT(authors, '[0-9]+') as author_id, title, description, average_rating, book_id FROM goodreads;

COPY (SELECT review_text,title,description,authorid.average_rating, goodreads_authors.name as author FROM authorid  JOIN goodreads_reviews  ON authorid.book_id = goodreads_reviews.book_id JOIN goodreads_authors ON authorid.author_id = goodreads_authors.author_id where authorid.author_id NOT ILIKE '' ) TO '20230630_training.parquet' (FORMAT PARQUET);


import duckdb
from inout import filereader as reader

"""Generates input data in English for Embeddings
Source data https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home
"""



root_path  = Path("viberary" / get_project_root())
con = duckdb.connect("")

books = Path ("/Users/vicki/viberary/viberary/data/goodreads_books.json"
authors =
reviews

duckdb.sql("select * from read_json_auto(,lines='true'")

duckdb.sql(
    """CREATE TABLE goodreads_en AS
    SELECT * FROM goodreads
    WHERE language_code like 'en%';"""
)

sentences = con.sql(
    """SELECT concat_ws(' ' , lower(regexp_replace(title, '[[:^alpha:]]',' ','g')), \
                    lower(regexp_replace(description, '[[:^alpha:]]',' ','g'))) as sentence \
                    FROM goodreads_en;"""
).df()

sentences.to_csv("sentences_en.csv", index=False, header=False)
