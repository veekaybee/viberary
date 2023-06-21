import logging
from pathlib import Path
import os

from models.bert.knn_search import KNNSearch
from logs.viberary_logging import ViberaryLogging
from inout.redis_conn import RedisConnection

from flask import Flask
from flask import render_template, jsonify, request

app = Flask(__name__)

logger = ViberaryLogging().setup_logging()


def return_model_results(word: str) -> str:
    retriever = KNNSearch(RedisConnection().conn())
    data = jsonify(retriever.top_knn(word))
    return render_template("index.html", data=data.json, query=word)


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    word = request.form["query"]
    return return_model_results(word)


# Local testing model only
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
