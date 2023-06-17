import logging
from pathlib import Path

from src.bert.knn_search import KNNSearch
from src.bert.viberary_logging import ViberaryLogging
from src.bert.redis_conn import RedisConnection

from flask import Flask
from flask import render_template, jsonify, request

app = Flask(__name__)

logger = ViberaryLogging().setup_logging()
retriever = KNNSearch(RedisConnection().conn())


def return_model_results(word: str, n: int = 10) -> str:
    data = jsonify(retriever.top_knn(word))
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
