# Training data generation

Training data generation happens manually. The first step is generating a training data set against the original JSON
file using DuckDB using `generate_training_data`

The second step, `model/generate_embeddings.py`, runs on a Paperspace instance.

To run on Paperspace, run the following in Jupyterlab:

1. `pip install virtualenv`
2. `virtualenv embed`
3. `embed source/bin/activate`
4. `pip install -r requirements.txt` from the datagen requirements file
5. `python embedding_generator.py`
