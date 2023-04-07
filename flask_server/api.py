import logging
from pathlib import Path

from flask import Flask
from flask import render_template, request, jsonify
from gensim.models import Word2Vec

app = Flask(__name__)

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO
)

current_dir = Path.cwd()

parent_dir = Path('..').resolve()
models_dir = parent_dir / 'models'
ft_file_path = models_dir / 'fasttext.model'
w2v_file_path = models_dir / 'word2vec.model'
ft = str(ft_file_path)
w2v = str(w2v_file_path)

## Load Model
ft_model = Word2Vec.load(ft)
w2v_model = Word2Vec.load(w2v)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/<model>/<word>', methods=['GET', 'POST'])
def search(model, word):
    n = request.args.get('topn')
    search_query = request.args.get('q')

    if not n:
        n = 10
    else:
        n = int(n)

    if model == "fasttext":
        data = jsonify(ft_model.wv.most_similar([word], topn=n))
    elif model == "word2vec":
        data = jsonify(w2v_model.wv.most_similar([word], topn=n))

    return render_template('index.html', search_query=search_query, data=data.json)


if __name__ == '__main__':
    app.run()
