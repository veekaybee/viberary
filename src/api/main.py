from flask import Flask, render_template, request

from conf.config_manager import ConfigManager
from conf.redis_conn import RedisConnection
from search.knn_search import KNNSearch

app = Flask(__name__)


retriever = KNNSearch(RedisConnection().conn(), ConfigManager())


def get_model_results(word: str, search_conn) -> str:
    data = search_conn.top_knn(word)
    return render_template("index.html", data=data, query=word)


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


@app.route("/how", methods=["POST", "GET"])
def how():
    return render_template("how.html")


@app.route("/search", methods=["POST", "GET"])
def search() -> str:
    word = None

    if request.method == "POST":
        word = request.form.get("query", "")
    elif request.method == "GET":
        word = request.args.get("query", "")

    return get_model_results(word, retriever)
