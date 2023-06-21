# %%
    """This script needs to be run on a machine with GPU access
    Currently being run on Paperspace
    """

import sys

!{sys.executable} -W ignore:DEPRECATION -m pip install --quiet duckdb==0.7.1 \
duckdb-engine \
watermark \
jupysql \
sqlalchemy \
python-snappy \
pyarrow \
memray \
pandas  \
ipywidgets  \
matplotlib \
gensim \
nltk \
plotly \
redis==4.5.3 \
jupyter-black \
sentence_transformers \
redis \
jupyter_black

# %%
# Autoformat cells on run
import jupyter_black
import pandas as pd

jupyter_black.load()

# %%
# set log level for model training
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(
    format="%(levelname)s - %(asctime)s: %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

# %%
!pwd

# %%
embeddings = pd.read_csv("embedding_data.csv")

# %%
embeddings

# %%
corpus = embeddings["sentence"].tolist()
titles = embeddings["title"].tolist()
indices = embeddings.index.tolist()

# %%
from sentence_transformers import SentenceTransformer, util

#  A common value for BERT & Co. are 512 word pieces, which correspond to about 300-400 words (for English).
# Longer texts than this are truncated to the first x word pieces.
# By default, the provided methods use a limit fo 128 word pieces, longer inputs will be truncated
# the runtime and the memory requirement grows quadratic with the input length - we'll have to play around with this

# Change the length to 200
model = SentenceTransformer("all-MiniLM-L6-v2")
model.max_seq_length = 200


corpus_embeddings = model.encode(
    corpus, show_progress_bar=True, device="cuda", convert_to_numpy=False
)

# %%
embeddings_list = [x.tolist() for x in corpus_embeddings]
embedding_tuple = list(zip(titles, indices, embeddings_list))

# %%
from tqdm import tqdm
import numpy as np
import pyarrow as pa
import pandas as pd

df = pd.DataFrame(embedding_tuple, columns=["sentence", "index", "embeddings"])

# %%
df

# %%
fields = [
    ("sentence", pa.string()),
    ("index", pa.int64(), False),
    ("embeddings", pa.large_list(pa.float64())),
]
schema = pa.schema(fields)

df.to_parquet(
    "learned_embeddings.snappy", engine="pyarrow", compression="snappy", schema=schema
)

# %%
pqt = pd.read_parquet("learned_embeddings.snappy")

# %%



