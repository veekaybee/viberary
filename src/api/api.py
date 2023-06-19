import logging
from pathlib import Path

from src.models.bert.knn_search import KNNSearch
from src.logs.viberary_logging import ViberaryLogging
from src.io.redis_conn import RedisConnection

from flask import Flask
from flask import render_template, jsonify, request

app = Flask(__name__)

logger = ViberaryLogging().setup_logging()


def return_model_results(word: str, n: int = 10) -> str:
    retriever = KNNSearch(word, RedisConnection().conn())
    data = jsonify(retriever.top_knn())
    return render_template("index.html", data=data.json, query=word)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    word = request.form["query"]
    return return_model_results(word)


# Local testing model only
if __name__ == "__main__":
    app.run()
