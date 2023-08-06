import markdown2
from flask import Flask, redirect, render_template, request, url_for

from conf.config_manager import ConfigManager
from conf.redis_conn import RedisConnection
from search.knn_search import KNNSearch

app = Flask(__name__)


retriever = KNNSearch(RedisConnection().conn())
conf = ConfigManager()


def get_model_results(word: str, search_conn) -> str:
    data = search_conn.top_knn(word)
    return render_template("index.html", data=data, query=word)


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


@app.route("/how", methods=["POST", "GET"])
def render_template_from_markdown():
    root = conf.get_root_dir()
    with open(f"{root}/src/api/templates/readme.md", "r") as f:
        markdown_content = f.read()
    html_content = markdown2.markdown(markdown_content)

    return render_template("how_markdown.html", markdown_content=html_content)


@app.route("/search", methods=["GET", "POST"])
def search() -> str:
    if request.method == "POST":
        query = request.form.get("query")
        # Redirect to the URL with the query parameter in the response
        return redirect(url_for("search_results", query=query))
    else:
        query = request.args.get("query")
        return get_model_results(query, retriever)


@app.route("/search/results")
def search_results():
    query = request.args.get("query")
    return get_model_results(query, retriever)
