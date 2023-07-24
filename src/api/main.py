import logging.config

from pydantic import BaseModel, Json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from inout.file_reader import get_root_dir, get_config_file as cf
from inout.redis_conn import RedisConnection
from search.knn_search import KNNSearch

conf = cf()
logging.config.fileConfig(conf["logging"]["path"])
root = get_root_dir()

app = FastAPI(title="Viberary")
templates = Jinja2Templates(directory= Path( f"{root}/src/api/templates"))
app.mount("/static", StaticFiles(directory=f"{root}/src/api/static"), name="static")


@app.post("/search")
async def search(request: Request):
    retriever = KNNSearch(RedisConnection().conn())
    data = retriever.top_knn(request.query)
    return templates.TemplateResponse("search.html", {"data": data, "query": request.query})

@app.get("/",response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", context= {"request": request})


@app.get("/how",response_class=HTMLResponse)
async def how(request: Request):
    return templates.TemplateResponse("how.html", context={"request": request})

@app.get("/ping")
async def root():
    return {"message": "pong"}
