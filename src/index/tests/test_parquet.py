from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from src.index.parquet_reader import ParquetReader


def test_convert_dataframe_to_dict(tmpdir):
    pq.write_table(
        pa.table(
            {
                "title": ["Title 1", "Title 2"],
                "index": [1, 2],
                "author": ["Author 1", "Author 2"],
                "link": ["Link 1", "Link 2"],
                "review_count": [1, 2],
                "embeddings": [[0.001, 0.002], [0.001, 0.002]],
            }
        ),
        tmpdir / "file.parquet",
    )

    path = Path(tmpdir / "file.parquet")
    reader = ParquetReader(path)
    result = reader.file_to_embedding_dict(
        columns=["title", "index", "author", "link", "review_count", "embeddings"]
    )

    expected_output = {
        1: ("Title 1", "Author 1", "Link 1", 1, np.array([0.001, 0.002])),
        2: ("Title 2", "Author 2", "Link 2", 2, np.array([0.001, 0.002])),
    }

    assert result.keys() == expected_output.keys()

    # assert that values of the dictionaries are equal unless dict element is np.array
    # then assert specific equality of that array
    assert (
        a == b if not isinstance(a, np.array) else a == b.all()
        for a, b in zip(result.values(), expected_output.values())
    )
