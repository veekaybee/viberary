import logging
from pathlib import Path

from flask import Flask
from flask import render_template, jsonify, request
from gensim.models import Word2Vec

app = Flask(__name__)

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO
)

# Model object set up and processing
# Hideous
current_dir = Path.cwd()
parent_dir = Path('..').resolve()
models_dir = current_dir / 'models'
ft_file_path = models_dir / 'fasttext.model'
w2v_file_path = models_dir / 'word2vec.model'
ft = str(ft_file_path)
w2v = str(w2v_file_path)

## Load Model - only for local testing
ft_model = Word2Vec.load(ft)
w2v_model = Word2Vec.load(w2v)


def return_model_results(model: str, word: str, n: int = 10) -> str:
    if model == "fasttext":
        model_object = ft_model
    elif model == "word2vec":
        model_object = w2v_model
    else:
        raise Exception(f"Undefined model {model}")

    data = jsonify(model_object.wv.most_similar([word], topn=n))
    return render_template('index.html', model=model, data=data.json, query=word)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    # Model metadata management

    model = request.form['model']
    word = request.form['query']

    return return_model_results(model, word)


# Local testing model only
if __name__ == '__main__':
    app.run()
