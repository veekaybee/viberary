# Training data generation

Training data generation happens manually. The first step is generating a training data set agains the original JSON
file using DuckDB.

The second step, `generate_embeddings.py`, runs on a Paperspace instance. To run on Paperspace, activate Jupyterlab and:

1. `pip install virtualenv`
2. `virtualenv embed`
3. `embed source/bin/activate`
4. `pip install -r requirements.txt` from the datagen requirements file
5. `python embedding_generator.py`

