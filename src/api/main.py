import logging.config

from flask import Flask, render_template, request

from inout.file_reader import get_root_dir,get_config_file as cf
from inout.redis_conn import RedisConnection
from search.knn_search import KNNSearch

app = Flask(__name__)

conf = cf()
conf_path = conf["logging"]["path"]
root_dir = get_root_dir()
logging.config.fileConfig(f"{root_dir}/{conf_path}")


def return_model_results(word: str) -> str:
    retriever = KNNSearch(RedisConnection().conn())
    data = retriever.top_knn(word)
    return render_template("index.html", data=data, query=word)


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


@app.route("/how", methods=["POST", "GET"])
def how():
    return render_template("how.html")


@app.route("/search", methods=["POST"])
def search():
    word = request.form["query"]
    return return_model_results(word)
