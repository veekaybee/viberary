# Script for reading in original JSON file and processing to feed into word2vec
# ./bin/spark-submit /Users/vicki/viberary/viberary/word2vec/generate_input.py  --master local

from pyspark.sql.functions import (
    col,
    regexp_replace,
    collect_list,
    lit,
    explode,
    concat,
    concat_ws,
    expr,
)
from pyspark.sql import Row, SparkSession
from pyspark.sql.types import IntegerType

spark = SparkSession.builder.master("local").appName("Word2Vec InputData").getOrCreate()

# Read in JSON
df_books = spark.read.json("/Users/vicki/viberary/viberary/data/goodreads_books.json")

# Set limit sample for DF modeling
df = df_books.limit(10000)

# Flatten Nested JSON on popular_shelves
df2 = df.select("book_id", "popular_shelves")
df3 = df2.select("book_id", explode("popular_shelves"))
df4 = df3.select("book_id", "col.count", "col.name")
df4 = df4.withColumnRenamed("count", "num_tags")
df4 = df4.withColumn("count_num", df4.num_tags.cast(IntegerType()))

# Filter noisy tags in exploded popular_shelves
df4 = df4.filter(df4.name != "to-read")
# clean up tag hyphens
df4 = df4.withColumn(("name_norm"), regexp_replace(col("name"), "-", " "))
df4 = df4.withColumn("name_norm_space", concat(lit(" "), col("name_norm")))

# multiply tags times occurrences to reflect accurately in text
# May need to take this out for word2vec
df4 = df4.withColumn("tag_occurrences", expr("repeat(name_norm_space, num_tags)"))
df5 = df4.select("book_id", "tag_occurrences")
df6 = df5.groupBy(["book_id"]).agg(collect_list("tag_occurrences"))
df7 = df6.withColumn(
    "tags_occurrences", concat_ws(" ", col("collect_list(tag_occurrences)"))
).withColumnRenamed("book_id", "id")

# join back to original data to get book_id, title, and description
df8 = df.join(df7, df.book_id == df7.id, "inner").select(
    col("book_id"), col("title"), col("description"), col("tags_occurrences")
)
df9 = df8.withColumn(
    "word2vec_input",
    concat_ws(" ", col("title"), col("description"), col("tags_occurrences")),
)

# Write out to file
df10 = df9.select("word2vec_input")
df10.write.csv("viberary/viberary/data/wor2vec.csv")
