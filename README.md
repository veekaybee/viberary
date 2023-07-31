# Viberary

![]()


🚧 <img src="https://img.shields.io/badge/under%20construction-FF8C00" /> -in Beta release</a>
🚧

<p align="center"><img src="https://github.com/veekaybee/viberary/blob/main/docs/assets/img/vibe_book.png" width="400" height="400" /></p>

Viberary is a search engine that recommends you books based not on genre or title, but vibe by
performing [semantic search](https://en.wikipedia.org/wiki/Semantic_search)
across [a set of learned embeddings](https://vickiboykis.com/what_are_embeddings/index.html) on a dataset of books from
Goodreads and their metadata.

It returns a list of book recommendations based on the vibe of the book that you put in.
So you don't put in "I want science fiction", you'd but in "atmospheric, female lead, worldbuilding, funny" as a prompt,
and get back a list of books. This project came out of experiences I had where recommendations for movies, TV, and music
have fairly been good, but book recommendations are always a problem.

For much, much more detail see the how page on the project website.

## App Architecture

<img src="static/assets/img/tactical_app.png" alt="drawing" width="600"/>

It's a [two-tower](https://blog.reachsumit.com/posts/2023/03/two-tower-model/) semantic retrieval model that encodes both the query and the corpus using the
[Sentence Transformers pretrained asymmetric MSMarco Model](https://www.sbert.net/docs/pretrained-models/msmarco-v3.html).

<img src="static/assets/img/tactical_app.png" alt="drawing" width="600"/>

The training data is generated locally in DuckDB and the model is converted to ONNX for low-latency inference, with [corpus embeddings learned on AWS P3 instances](https://github.com/veekaybee/viberary/blob/main/src/model/generate_embeddings.ipynb) against the same model and stored in Redis and retrieved using the [Redis Search](https://redis.io/docs/interact/search-and-query/) module using the [HNSW algorithm](https://arxiv.org/abs/1603.09320) included as part of the Redis search module. Results are served through a Flask API running [Gunicorn](https://gunicorn.org/) and served to a Bootstrap front-end.

<img src="static/assets/img/physical_arch.png" alt="drawing" width="600"/>

It's served from two Digital Ocean droplets behind a [Digital Ocean load balancer](https://www.digitalocean.com/products/load-balancer) and [Nginx](https://vicki.substack.com/p/when-you-write-a-web-server-but-you), as a Dockerized application with networking spun up through Docker compose between a web server and Redis image, with data persisted to [external volumes in DigitalOcean](https://docs.digitalocean.com/products/volumes/),  with AWS Route53 serving as the domain registrar and load balancer router.

The artifact is generated through GitHub actions on the main branch of the repo and then I manually refresh the docker image on the droplets through a set of Makefile commands.

# Running the project

1. Fork/clone the repo
2. Go to the project root (`viberary`)
3. Donwload the [corpus embeddings file](https://github.com/veekaybee/viberary/releases/tag/v0.0.2) to
`/viberary/src/training_data`.
4. Go to the root of the repo and run `make onnx` to generate the runnable model artifact.
5. `make build-arm (or make build-intel)` - Builds the docker image depending on your architecture
4. `make up` - Docker compose running in background
5. `make embed` - indexes the embeddings once the web server is running
7. `localhost:8000` - Loads the web server

# Monitoring the project

1. `make logs` for logs


# Repo Structure

+ `src` - where all the code is
    + `api` - Flask sever that calls the model, includes a search endpoint. Eventually will be rewritten in Go (for
      performance reasons)
    + `training_data` - generated training data
    + `model` - The actual BERT model. Includes data generated for generating embeddings and also the code used to generate the embeddings, on an EC2 instance.
    + `index` includes an indexer which indexes embeddings generated in `model` into a Redis instance. Redis and the Flask app talk to each
          other through an app running via `docker-compose` and the `Dockerfile` for the main app instance.
    + `search` - performs the search calls from api
    + `conf` - There are some utilities such as data directory access, io operations and a separate indexer that indexes titles
      into Redis for easy retrieval by the application
    + `notebooks` - Exploration and development of the input data, various concepts, algorithms, etc. The best resource
      there [is this notebook](https://github.com/veekaybee/viberary/blob/main/notebooks/05_duckdb_0.7.1.ipynb), which
      covers the end-to-end workflow of starting with raw data, processing in DuckDB, learning a Word2Vec embeddings
      model, ([Annotated output is here.](https://colab.research.google.com/gist/veekaybee/a40d8f37dd99eda2e6d03f4c10671674/cbow.ipynb)) and storing and querying those embeddings in Redis Search. This is the solution I eventually turned into
      the application directory structure.
+ `docs` - This serves and rebuilds `viberary.pizza`

# CONTRIBUTING

Happy to take contributions, please follow instructions above for building and testing locally, make sure all unit tests pass and your branch passes locally before issuing a PR.

## Relevant Literature and Bibliography

+ My [paper on embeddings and its bibliography](https://vickiboykis.com/what_are_embeddings/index.html)
+ [Towards Personalized and Semantic Retrieval: An End-to-End Solution for E-commerce Search via Embedding Learning](https://arxiv.org/abs/2006.02282)
+ [PinnerSage](https://arxiv.org/abs/2007.03634)
+ [My Research Rabbit Collection](https://www.researchrabbitapp.com/collection/public/R6DO98QNZP)

## Input Data

UCSD Book Graph, with the critical part being
the [user-generated shelf labels.](https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/books). [Sample row:](https://gist.github.com/veekaybee/e8ea5dcf5632fd6345096023dc18159e)
Note these are all encoded as strings!

```json
{
  "isbn": "0413675106",
  "text_reviews_count": "2",
  "series": [
    "1070125"
  ],
  "country_code": "US",
  "language_code": "",
  "popular_shelves": [
    {
      "count": "2979",
      "name": "to-read"
    },
    {
      "count": "291",
      "name": "philosophy"
    },
    {
      "count": "187",
      "name": "non-fiction"
    },
    {
      "count": "80",
      "name": "religion"
    },
    {
      "count": "76",
      "name": "spirituality"
    },
    {
      "count": "76",
      "name": "nonfiction"
    }
  ],
  "asin": "",
  "is_ebook": "false",
  "average_rating": "3.81",
  "kindle_asin": "",
  "similar_books": [
    "888460",
    "734023",
    "147311",
    "219106",
    "313972",
    "238866",
    "196325",
    "200137",
    "588008",
    "112774",
    "2355135",
    "336248",
    "520437",
    "421044",
    "870160",
    "534289",
    "64794",
    "276697"
  ],
  "description": "Taoist philosophy explained using examples from A A Milne's Winnie-the-Pooh.",
  "format": "",
  "link": "https://www.goodreads.com/book/show/89371.The_Te_Of_Piglet",
  "authors": [
    {
      "author_id": "27397",
      "role": ""
    }
  ],
  "publisher": "",
  "num_pages": "",
  "publication_day": "",
  "isbn13": "9780413675101",
  "publication_month": "",
  "edition_information": "",
  "publication_year": "",
  "url": "https://www.goodreads.com/book/show/89371.The_Te_Of_Piglet",
  "image_url": "https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png",
  "book_id": "89371",
  "ratings_count": "11",
  "work_id": "41333541",
  "title": "The Te Of Piglet",
  "title_without_series": "The Te Of Piglet"
}
```

## Roadmap

Here's a list of refinements I'd like to make to this project:

1. Include a "I'm Feeling Lucky" type button that generates one good vibe-y recommendation at random.
2. Build out [a feature/model store](https://github.com/veekaybee/viberary/issues/73) for the model and the training data, will likely just be hosted in DigitalOcean as well, nothing super fancy, but right now it's annoying to move these artifacts around, but not annoying enough where I had enough time to build one.
3. If model performance becomes an issue, migrate the API to Java ([Go was my first choice](https://github.com/veekaybee/viberary/issues/15) but it doens't have a very good ONNX story at the moment)
4. Add Prometheus and Grafana. I had these initially but they created too much overhead and Digital Ocean default monitoring is good enough.
5. [Query autocompletion](https://github.com/veekaybee/viberary/issues/70) in the search bar
6. [Chart of most recommended books](https://github.com/veekaybee/viberary/issues/65) based on log data on the site
7. Include a toggle for multi-lingual search. I haven't tried this out well at all, and most of the books are in English, but I'd like to see if it's a possibility, as well as investigate how well this model handles it.
