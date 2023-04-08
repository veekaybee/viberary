# Viberary

![]()

<p align="center"><img src="https://github.com/veekaybee/viberary/blob/main/docs/assets/img/vibe_book.png" width="400" height="400" /></p>

Viberary is a project that will recommend you books based not on genre or title, but vibe by performing semantic search across a set of learned embeddings on a dataset of books from Goodreads and their metadata. 

The idea is pretty simple: return book recommendations based on the vibe of the book that you put in.
So you don't put in "I want science fiction", you'd but in "atmospheric, female lead, worldbuilding, funny" as a prompt, and get back a list of books

## Reference implementation: 
![](https://github.com/veekaybee/viberary/blob/main/assets/viberary.png)

## Actual Architecture:
![](https://github.com/veekaybee/viberary/blob/main/assets/actual_architecture.png)

My approach is: 

1. Explore the data [Done]
  + Post 0: [Working with the data in BigQuery](https://vickiboykis.com/2022/12/05/the-cloudy-layers-of-modern-day-programming/)
  + Post 1: [Working with the data in Pandas](https://vickiboykis.com/2023/01/17/welcome-to-the-jungle-we-got-fun-and-frames/)
  + Post 2: [Doing research with ChatGPT](https://vickiboykis.com/2023/02/26/what-should-you-use-chatgpt-for/)
2. Build a baseline model in Word2Vec [In progress]
3. Deploy the baseline model to "prod" (aka a single server) and test it out [In progress]
4. Build a model using base BERT (or DistilBERT, etc.) and also deploy that and evaluate them against each other. 
5. At the same time, write a document about what embeddings are and how they fit into modern machine learning workflows
  + [LaTeX Resource](https://vickiboykis.com/latex_resources/)

# Repo Structure

Since the project is actively in exploration and development, there are a lot of winding codepaths, experiments, and dead ends in the codebase. It is not production-grade for ANY definition of production. I'll let you know when it's ready. 

For now, there are a couple key directories: 

+ `notebooks` - Exploration and development of the input data, various concepts, algorithms, etc. The best resource there [is this notebook](https://github.com/veekaybee/viberary/blob/main/notebooks/05_duckdb_0.7.1.ipynb), which covers the end-to-end workflow of starting with raw data, processing in DuckDB, learning a Word2Vec embeddings model, and storing and querying those embeddings in Redis Search. This is the solution I'm working towards for the first baseline production model. 
+ `flask_server` - A model learned in Word2Vec AND Fasttext from the code here (https://github.com/veekaybee/viberary/blob/main/notebooks/05_duckdb_0.7.1.ipynb) and deployed on a tiny Flask server on a GitHub droplet. This is not production-grade, but allows for model serving and evaluation. 

Demo here: 

https://user-images.githubusercontent.com/3837836/230725711-62d7b203-e4c3-4188-a9fd-14ea74db876e.mov

+ `word2vec` - Word2Vec implemented in PyTorch. I did this before I implemented Word2Vec in Gensim to learn about PyTorch idioms and paradigms. [Annotated output is here.](https://colab.research.google.com/gist/veekaybee/a40d8f37dd99eda2e6d03f4c10671674/cbow.ipynb)

+ `docs` - This serves and rebuilds viberary.pizza

+ `api` - Me starting to learn Go for what will eventually be the production-grade server (ported from Flask

## Relevant Literature and Bibliography

+ ["Towards Personalized and Semantic Retrieval: An End-to-End Solution for E-commerce Search via Embedding Learning"](https://arxiv.org/abs/2006.02282)
+ ["PinnerSage"](https://arxiv.org/abs/2007.03634)
+ ["Making Machine Learning Easy with Embeddings"](https://mlsys.org/Conferences/doc/2018/115.pdf)
+ ["Research Rabbit Collection"](https://www.researchrabbitapp.com/collection/public/R6DO98QNZP)

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


