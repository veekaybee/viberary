# Viberary

![]()

<p align="center"><img src="https://github.com/veekaybee/viberary/blob/main/docs/assets/img/vibe_book.png" width="400" height="400" /></p>

Viberary is a project that will eventually recommend you books based not on genre or title, but vibe by performing semantic search across a set of learned embeddings on a dataset of books from Goodreads and their metadata. 

The idea is simple: return book recommendations based on the vibe of the book that you put in.
So you don't put in "I want science fiction", you'd but in "atmospheric, female lead, worldbuilding, funny" as a prompt, and get back a list of books.


## Reference implementation: 
![](https://github.com/veekaybee/viberary/blob/main/assets/viberary.png)

## Actual Architecture:
![](https://github.com/veekaybee/viberary/blob/main/assets/actual_architecture.png)

My approach is: 

- [X] Explore the data 
  + Post 0: [Working with the data in BigQuery](https://vickiboykis.com/2022/12/05/the-cloudy-layers-of-modern-day-programming/)
  + Post 1: [Working with the data in Pandas](https://vickiboykis.com/2023/01/17/welcome-to-the-jungle-we-got-fun-and-frames/)
  + Post 2: [Doing research with ChatGPT](https://vickiboykis.com/2023/02/26/what-should-you-use-chatgpt-for/)
- [X] Build a baseline model in Word2Vec. [Done]
   - Built and implemented in the [word2vec_demo](https://github.com/veekaybee/viberary/tree/word2vec_demo) branch
- [X] Doing a [deep dive on embeddings](https://vickiboykis.com/what_are_embeddings/) and [LaTeX Resource](https://vickiboykis.com/latex_resources/)
- [x] Deploy the baseline model to "prod" (aka a single server) and test it out. Word2Vec Demo: 

https://user-images.githubusercontent.com/3837836/230725711-62d7b203-e4c3-4188-a9fd-14ea74db876e.mov

- [ ] Build a model [using BERT](https://github.com/veekaybee/viberary/tree/bert) and also deploy that and evaluate them against each other. In progress [on this branch](https://github.com/veekaybee/viberary/tree/bert)

https://github-production-user-asset-6210df.s3.amazonaws.com/3837836/246661581-5afb9972-bef1-4481-81c6-489a2a8cc861.MOV


  

# Repo Structure

Since the project is actively in exploration and development, there are a lot of winding codepaths, experiments, and dead ends in the codebase. It is not production-grade for ANY definition of production. I'll let you know when it's ready. 

+ `src` - where all the code is
  + `api` - Flask sever that calls the model, includes a search endpoint. Eventually will be rewritten in Go (for performance reasons)
  + `datagen` includes data generated for feeding into Word2Vec and for generating embeddings and also the code used to generate the embeddings, done on a Paperspace GPU instance. 
  + `models` - The actual models including Word2Vec and BERT. 
    + `bert` - Right now in production only BERT gets called from the API. the `bert` directory includes an indexer which indexes embeddings generated in `datagen` into a Redis instance. Redis and the Flask app talk to each other through an app running via `docker-compose` and the `Dockerfile` for the main app instance. 
     + `word2vec` - Word2Vec implemented in PyTorch. I did this before I implemented Word2Vec in Gensim to learn about PyTorch idioms and paradigms. [Annotated output is here.](https://colab.research.google.com/gist/veekaybee/a40d8f37dd99eda2e6d03f4c10671674/cbow.ipynb)
  + There are some utilities such as data directory access, io operations and a separate indexer that indexes titles into Redis for easy retrieval by the application
  + `notebooks` - Exploration and development of the input data, various concepts, algorithms, etc. The best resource there [is this notebook](https://github.com/veekaybee/viberary/blob/main/notebooks/05_duckdb_0.7.1.ipynb), which covers the end-to-end workflow of starting with raw data, processing in DuckDB, learning a Word2Vec embeddings model, and storing and querying those embeddings in Redis Search. This is the solution I eventually turned into the application directory structure. 
+ `docs` - This serves and rebuilds viberary.pizza



## Relevant Literature and Bibliography

+ ["Towards Personalized and Semantic Retrieval: An End-to-End Solution for E-commerce Search via Embedding Learning"](https://arxiv.org/abs/2006.02282)
+ ["PinnerSage"](https://arxiv.org/abs/2007.03634)
+ ["My Research Rabbit Collection"](https://www.researchrabbitapp.com/collection/public/R6DO98QNZP)
+ My [paper on embeddings and its bibliography](https://vickiboykis.com/what_are_embeddings/index.html) 

## Input Data Sample

UCSD Book Graph, with the critical part being the [user-generated shelf labels.](https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/books). [Sample row:](https://gist.github.com/veekaybee/e8ea5dcf5632fd6345096023dc18159e) Note these are all encoded as strings!

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

## Embeddings Sample

<img width="648" alt="Screen Shot 2023-02-18 at 2 10 15 PM" src="https://user-images.githubusercontent.com/3837836/219883909-cb615361-9356-4b62-936f-4ea7c6719296.png">


