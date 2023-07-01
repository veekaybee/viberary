"""This script needs to be run on a machine with GPU access
Currently being run on Paperspace
Trains embedding data
"""

import logging
import time

import pandas as pd
import pyarrow as pa
from sentence_transformers import SentenceTransformer

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(
    format="%(levelname)s - %(asctime)s: %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

fields = [
    ("sentence", pa.string()),
    ("index", pa.int64(), False),
    ("embeddings", pa.large_list(pa.float64())),
]
schema = pa.schema(fields)

dt = time.strftime("%Y%m%d%H%M")

# Read local data from paperspace
# Generated from training_data_generator
logger.info("Reading in datafile")
embeddings = pd.read_parquet("/notebooks/20230701_training.parquet")

# Format for learning embeddings
logger.info("Converting to embeddings format")
corpus = embeddings["sentence"].tolist()
titles = embeddings["title"].tolist()
author = embeddings["author"].tolist()
indices = embeddings.index.tolist()

# A common value for BERT & Co. are 512 word pieces,
# which correspond to about 300-400 words (for English).
# Longer texts than this are truncated to the first x word pieces.
# By default, the provided methods use a limit fo 128 word pieces,
# the runtime and the memory requirement grows quadratic with the input length

# Change the length to 200
logger.info("Running embeddings")
model = SentenceTransformer("all-MiniLM-L6-v2")
model.max_seq_length = 200

# Load MiniLM model and generate embeddings
model = SentenceTransformer("sentence-transformers/msmarco-distilbert-base-v3")
model.max_seq_length = 200


corpus_embeddings = model.encode(
    corpus, show_progress_bar=True, device="cuda", convert_to_numpy=False
)

torch.save(corpus_embeddings.state_dict(), "/notebooks/")

# To dataframe for write in Parquet
embeddings_list = [x.tolist() for x in corpus_embeddings]
embedding_tuple = list(zip(titles, indices, author, embeddings_list))

fields = [
    ("sentence", pa.string()),
    ("index", pa.int64(), False),
    ("author", pa.string()),
    ("embeddings", pa.large_list(pa.float64())),
]
schema = pa.schema(fields)

# TODO: change the name of the file to machine generated
df = pd.DataFrame(embedding_tuple, columns=["title", "index", "author", "embeddings"])
df.to_parquet(
    "20230701_learned_embeddings.snappy",
    engine="pyarrow",
    compression="snappy",
    schema=schema,
)

# write results to parquet for ingestion in Redis
logger.info("Writing to parquet")
df.to_parquet(f"{time}embeddings.snappy", engine="pyarrow", compression="snappy", schema=schema)
