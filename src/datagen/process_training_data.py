import duckdb

"""Generates input data in English for Embeddings
Source data https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home
"""

con = duckdb.connect("viberary.duckdb")

goodreads = "/Users/vicki/viberary/viberary/data/goodreads_books.json"

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
