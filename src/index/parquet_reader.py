import logging
import logging.config
from typing import Dict, List

import pandas as pd
import pyarrow.parquet as pq

from inout.file_reader import get_config_file as cf


class ParquetReader:
    def __init__(self, filepath):
        conf = cf()
        logging.config.fileConfig(conf["logging"]["path"])
        self.filepath = filepath

    def file_to_embedding_dict(self, columns: List) -> Dict:
        """
        Reads Parquet file and processes in Pandas
        in chunks

        index: title, author, link, review_count, embeddings
        """

        logging.info(f"Creating dataframe from {self.filepath}...")

        parquet_file = pq.ParquetFile(str(self.filepath))

        final_df = pd.DataFrame()

        for i, batch in enumerate(parquet_file.iter_batches(columns=columns)):
            logging.info(f"Loading RecordBatch {i}")
            df = batch.to_pandas()
            final_df = final_df.append(df, ignore_index=True)

        # Format as dict for read into Redis
        df_dict = final_df.to_dict("split")
        data = df_dict["data"]

        # Data: Index, title, author, Link, embeddings
        embedding_dict = {
            item[1]: (item[0], item[2], item[3], item[4], item[5])
            for item in data
            if len(item) == 6
        }

        return embedding_dict
