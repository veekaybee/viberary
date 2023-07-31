
<img src="static/assets/img/learningtired.png" alt="drawing" width="600"/>

*TL;DR*: Viberary helps you find books by __vibe__. I built it to satisfy an itch to do [ML side projects](https://vickiboykis.com/2020/06/09/getting-machine-learning-to-production/)  and navigate the current boundary between search and recommendations. It's a production-grade compliment to [my recent deep dive into embeddings.](http://vickiboykis.com/what_are_embeddings/)

<img src="static/assets/img/viberary_arch.png" alt="drawing" width="600"/>

It's a [two-tower](https://blog.reachsumit.com/posts/2023/03/two-tower-model/) semantic retrieval model that encodes both the query and the corpus using the
[Sentence Transformers pretrained asymmetric MSMarco Model](https://www.sbert.net/docs/pretrained-models/msmarco-v3.html).

<img src="static/assets/img/tactical_app.png" alt="drawing" width="600"/>

+ The training data is generated locally in DuckDB and
+ [corpus embeddings learned on AWS P3 instances](https://github.com/veekaybee/viberary/blob/main/src/model/generate_embeddings.ipynb) against the same model and are stored in Redis
+ the inference model for queries is converted to [ONNX Runtime artifacts](https://onnxruntime.ai/) for quick inference
+ queries encoded as embeddings are retrieved using the [Redis Search](https://redis.io/docs/interact/search-and-query/) module using the [HNSW algorithm](https://arxiv.org/abs/1603.09320) included as part of the Redis search module.
+ Results are served through a Flask API running [Gunicorn](https://gunicorn.org/) and served to a Bootstrap front-end.

<img src="static/assets/img/physical_arch.png" alt="drawing" width="600"/>

It's served from two Digital Ocean droplets behind a [Digital Ocean load balancer](https://www.digitalocean.com/products/load-balancer) and [Nginx](https://vicki.substack.com/p/when-you-write-a-web-server-but-you), as a Dockerized application with networking spun up through Docker compose between a web server and Redis image, with data persisted to [external volumes in DigitalOcean](https://docs.digitalocean.com/products/volumes/),  with AWS Route53 serving as the domain registrar and load balancer router. The artifact is generated through GitHub actions on the main branch of the repo and then I manually refresh the docker image on the droplets through a set of Makefile commands. This all works fairly well at this scale for now.

All of this is [in the repo.](https://github.com/veekaybee/viberary)

# What is semantic search?

Viberary is a semantic search engine for book recommendations.  It finds books based on &#10024;vibe&#10024; rather than exact
keyword matches by genre, author, and title. This is in contrast to traditional search engines, which work by performing lexical keyword
matching - that is if you type in "Nutella" into the search engine, it will try to find all documents that specifically have "Nutella" in the document.

Traditional search engines, including Elasticsearch/OpenSearch do this lookup quickly by building [an inverted
index](https://en.wikipedia.org/wiki/Inverted_index), a data structure that creates a
key/value pair where the key is the term and the value is a collection of all the documents that match the term. Some methods for retrieval from an inverted index include BM25, which calculates a relevance score for each element in an inverted index. The retrieval mechanism first selects all the documents with the keyword from the index, the calculates a relevance score, then ranks the documents based on the relevance score.

<img src="static/assets/img/inverted_index.png" alt="drawing" width="600"/>

Semantic search, in contrast, looks for near-meanings based on, as ["AI-Powered Search"](https://www.manning.com/books/ai-powered-search) calls it, "things, not strings." [In other words,](https://www.manning.com/books/relevant-search)

"Wouldn't it be nice if you could search for a term like "dog" and pull back documents that contain terms like "poodle, terrier, and beagle," even if those document shappen to not use the word "dog?"

<img src="static/assets/img/semantic_search.png" alt="drawing" width="600"/>

Semantic search is a vibe. A vibe can be hard to define, but generally it's more of a feeling of association
than something concrete: a mood, a color, or a phrase. Viberary will not give you exact matches for "Nutella", but if you type in "chocolately hazlenut goodness", the expectation is that you'd get back Nutella, and probably also "cake" and "Ferrerro Rocher". Semantic search methods include and semantic similarity measures, semantic query expansion.

Typically today, search engines will try a number of both keyword-based and semantic approaches in a solution known as hybrid search. Hybrid search includes methods like learning to rank, a blend of several retrieval models, query expansion which looks to enhance search results by adding synonyms to the original query, contextual search based on the user's history and location, and semantic search, which looks to use NLP, particularly vector search strategies, to help cluster and orient the user's query in a vector space.

<img src="static/assets/img/search_tree.png" alt="drawing" width="600"/>


The problem of semantic search is not new. It's one researchers and companies have been grappling with for decades in the field known as information retrieval, which started with roots in library science. [The paper introducing Google in 1998](https://storage.googleapis.com/pub-tools-public-publication-data/pdf/334.pdf) even discusses the problems with keyword-only search,

> People are likely to surf the web using its link graph, often starting with high quality human maintained indices such as Yahoo! or with search engines. Human maintained lists cover popular topics effectively but are subjective, expensive to build and maintain, slow to improve, and cannot cover all esoteric topics. Automated search engines that rely on keyword matching usually return too many low quality matches.

The tension and ability to make search engines work in the space between [query understanding](https://queryunderstanding.com/) through human enrichment and getting machines to better understand user intent has always been present.

Netflix was one of the first companies that started doing vibe-based content exploration when it [came up with a list of over 36, 00
genres](https://www.netflix.com/tudum/articles/netflix-secret-codes-guide) like "Gentle British
Reality TV" and "WitchCraft and the Dark Arts" in the 2010s. They [used large teams of people](https://www.theatlantic.com/technology/archive/2014/01/how-netflix-reverse-engineered-hollywood/282679/) to watch
movies and tag them with metadata. The process was so detailed that taggers received a 36-page document that "taught them how to rate movies on their sexually suggestive content, goriness, romance levels, and even narrative elements like plot conclusiveness."

These labels were then incorporated into Netflix's [recommendation architectures](https://netflixtechblog.com/system-architectures-for-personalization-and-recommendation-e081aa94b5d8) as features for training data.

It can be easier to incorporate these kinds of features into recommendations than search because the process of recommendation is the process of implicitly learning user preferences through data about the user and offering them suggestions of content or items to purchase based on their past history, as well as the history of users across the site, or based on the properties of the content itself. As such, [recommender interfaces often include lists of suggestions](https://www.nngroup.com/articles/recommendation-guidelines/) like "you might like.." or "recommended for you", or "because you interacted with X.."


Search, on the other hand, is an activity where the user expects their query to match exactly, so users have specific expectations of modern search interfaces:

1. They are [extremely responsive and low-latency](http://glinden.blogspot.com/2006/11/marissa-mayer-at-web-20.html)
2. Results are accurate and we get what we need in the first page
3. We use text boxes the same way [we have been conditioned](https://arxiv.org/pdf/2301.08613.pdf) to use Google Search over the past 30 years in the SERP (search engine results page)

So, in some ways , there is a conflict between a traditional search interface and semantic search, because semantic search is in that gray area between search and recommendations and traditional search expects exact results for exact queries.

Many search engines today, Google included, use a blend of traditional keyword search and semantic search to offer both direct results and related content, and with the explosion of generative AI and chat-based search and recommendation interfaces, this [division is becoming even blurrier.](https://docs.google.com/presentation/d/12aoYVaqus600NEuWASw_eF9xSDXGUMzGedAftfqBCCE/edit)


<img src="static/assets/img/searchandrec.png" alt="drawing" width="600"/>


# Why semantically search books?

I love reading, particularly novels. I am always reading something. Check out my past reviews
[2021](https://vickiboykis.com/essays/2022-01-02-favorite-books/),
[2020](https://vickiboykis.com/essays/2021-04-16-favorite-books/), [2019](https://vickiboykis.com/essays/2020-01-01-books/),
and you get the idea. As a reader, I am always looking for something good to read. Often, I'll get
recommendations by browsing sites like [LitHub](https://lithub.com/), but sometimes I'm in the mood for a particular
genre, or, more specifically a feeling that a book can capture. For example, after finishing ["The Overstory" by Richard Powers](https://www.richardpowers.net/the-overstory/), I was in the mood for more sprawling multi-generational epics
on arcane topics (I know so much about trees now!)

But you can't really find collections like this unless a human who
reads a lot puts a list like this together. One of my favorite formats of book recommendations [is
Biblioracle](https://themorningnews.org/article/greetings-from-the-biblioracle), where readers
send John Warner, an extremely well-read novelist, a list of the last five books they've read and he recommends their next read
based on their reading preferences. He is rarely wrong.


Finally, Goodreads native recommendations, even though I am an extremely active site user, are not great. [After Amazon purchased them to remove competition, there is no incentive to tune recommendations or search results](https://countercraft.substack.com/p/goodreads-has-no-incentive-to-be).

Given the recent rise in interest of semantic search based by vector databases, as well as [the paper I just finished on embeddings](http://vickiboykis.com/what_are_embeddings/), and given that my recent work had been in recommendations, I thought it would interesting if I could create a book recommendation engine.

But when I started formulating the machine learning task and doing background research, I reasoned that recommendations can be non-personalized, but most of the effective architectures are personalized, meaning they collect data from users. I have no desire to get deep into user data collection, with the exception of search queries and search query result lists, which I currently do log to see if I can fine-tune the model or offer suggestions at query time.

Recommendation surfaces are also traditionally rows of cards or lists that are loaded when the user is logged in, something that I don't also don't have. I'd like the user to be able to enter their own search query.

What I really had was a non-personalized search engine. When I initially started formulating the problem, I thought I could use a variation of the two-tower model architecture where you have a



This idea eventually evolved into the thinking that, given my project constraints and preferences, what I had was really a semantic search problem aimed specifically at surfacing books.

# Architecting Semantic Search

There are several stages to in building semantic search:

<img src="static/assets/img/modelsteps.png" alt="drawing" width="600"/>


1. Data Collection
2. Modeling and generating embeddings
3. Indexing the embeddings
3. Model Inference and Front end design



Most [search and recommendation architectures](https://eugeneyan.com/writing/system-design-for-discovery/) share a foundational set of commonalities: there is a set of documents that we have, that we'd like to filter through to get to the right documents presented to the user.
We  update those documents, via an indexing function, and we then filter them, either manually or through machine learning, then rank them, also using either algorithms or heuristics, and then present them to the user in a front-end.



# Project Architecture Decisions

I had several requirements for this project given these steps. First, I wanted to a project that was well-scoped so that I wouldn't get tired, and so that I would ship it, because the worst ML project is the one that remains unshipped. [As Mitch writes](https://mitchellh.com/writing/building-large-technical-projects), "give yourself a good demo."

Second, I wanted to explore new technologies while also being careful of not wasting [my innovation tokens](https://mcfunley.com/choose-boring-technology). In other words, I wanted to build something normcore, i.e. using the right tool for the right job, and [not going overboard.](https://vicki.substack.com/p/you-dont-need-kafka)

The third factor was to try to ignore [the noisiness of the current ML ecsystem](https://vickiboykis.com/2022/11/10/how-i-learn-machine-learning/), which comes out with a new model and a new product and a new wrapper for the model for the product every day. I can't say this was easy: it is extremely hard to ignore the noise and just build, particularly given all the discourse around LLMs in the ML community, and now in society at large, but I tried my best to work with tech that had been established for at least a couple years if not more to avoid life on the bleeding edge, particularly given the brittleness of Python's packaging compatibility ecosystem.

I wish I could say that I was able to plan all of this out in advance, and the project that I eventually shipped was exactly what I had envisioned. But, like with any engineering effort, I had a bunch of false starts and dead ends.

I started out [using Big Cloud](https://vickiboykis.com/2022/12/05/the-cloudy-layers-of-modern-day-programming/), a strategic mistake that cost me a lot of time and frustration because I couldn't see inside the cloud components and slowed down development cycles.  I eventually moved to data processing using DuckDB, but [it still look a long time](https://vickiboykis.com/2023/01/17/welcome-to-the-jungle-we-got-fun-and-frames/), as is typically the case in any data-centric project.

Then, I spent a long time [working through creating baseline models in Word2Vec](https://github.com/veekaybee/viberary/releases/tag/v0.0.1) so I could get some context for baseline text retrieval methods in the pre-Transformer era.

I started out trying to implement Word2Vec in PyTorch which gave me a really good understanding of how it worked for my paper, but slowed me down in engineering implementation, since

Finally, in going from local development to production, I hit [a bunch of different snags](https://vickiboykis.com/2023/07/18/what-we-dont-talk-about-when-we-talk-about-building-ai-apps/), most of them related to making Docker images smaller, thinking about the size of the machine I'd need for infrence, Docker networking, load testing traffic, and correctly routing Nginx.



My project tech stack, as it now stands is:
primarily Python with:
+ Original data in JSON files
+ Processed using the Python Client for DuckDB
+ Encoding of documents into model embeddings with SBERT, [specifically the MS-Marco Asymmetric model](https://www.sbert.net/examples/applications/semantic-search/README.html#symmetric-vs-asymmetric-semantic-search)
+ A Redis instance that indexes the embeddings into a special search index for retrieval
+ A Flask API that has a search query route that encodes the query with the same MSMarco model and then runs HNSW lookup in realtime against the Redis search index
+ A Bootstrap UI that returns the top 10 ranked results
+ Redis and Flask encapsulated in a networked docker compose configuration via Dockerfile, depending on the architecture (arm or AMD)
+ a Makefile that does a bunch of routine things around the app like reindexing the embeddigns and bringing up the app
+ Nginx on the hosting server to reverse-proxy requests from the load balancer
+ pre-commit for formatting and linting
+ a logging module for capturing queries and outputs
+ and tests in pytest

Tooling:

+ PyCharm for development, [including in Docker via bind mounts](https://www.jetbrains.com/help/pycharm/docker.html)
+ iterm2
+ VSCode for specifically writing the documentation, it's nicer than PyCharm for this
+ [Whimsical for charts](https://whimsical.com/)
+ Docker Desktop for Mac (considered briefly switching to Podman but haven't yet)


# The Training Data

The book data comes from  [UCSD Book Graph](https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/books).

The data is stored in several gzipped-JSON files,

+ [books](https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/books) -  detailed meta-data about 2.36M books
+ [reviews](https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/reviews?authuser=0) - Complete 15.7m reviews (~5g):15M records with detailed review text

 [Sample row:](https://gist.github.com/veekaybee/e8ea5dcf5632fd6345096023dc18159e)
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

Citation:
```
@inproceedings{DBLP:conf/recsys/WanM18,
  author       = {Mengting Wan and
                  Julian J. McAuley},
  editor       = {Sole Pera and
                  Michael D. Ekstrand and
                  Xavier Amatriain and
                  John O'Donovan},
  title        = {Item recommendation on monotonic behavior chains},
  booktitle    = {Proceedings of the 12th {ACM} Conference on Recommender Systems, RecSys
                  2018, Vancouver, BC, Canada, October 2-7, 2018},
  pages        = {86--94},
  publisher    = {{ACM}},
  year         = {2018},
  url          = {https://doi.org/10.1145/3240323.3240369},
  doi          = {10.1145/3240323.3240369},
  timestamp    = {Mon, 22 Jul 2019 19:11:02 +0200},
  biburl       = {https://dblp.org/rec/conf/recsys/WanM18.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```
From this, I initially [did some data exploration](https://github.com/veekaybee/viberary/blob/main/src/notebooks/03_duckdb_eda.ipynb) to get a feel for the data I had at hand. I wanted to know how full the dataset was, how many missing data I had, what language most of the reviews are in, and other things that will help understand what the model's embedding space looks like.

Then,  I constructed several tables that I'd need to send to the embeddings model to generate embeddings for the text:

```
TABLE goodreads_authors;
TABLE goodreads_auth_ids;
TABLE goodreads_reviews;
TABLE goodreads
```

The final relationships between the tables look like this:

```
SELECT
        review_text,
        goodreads_auth_ids.title,
        link,
        goodreads_auth_ids.description,
        goodreads_auth_ids.average_rating,
        goodreads_authors.name AS author,
        text_reviews_count,
        review_text || goodreads_auth_ids.title || goodreads_auth_ids.description
        || goodreads_authors.name as sentence
        FROM goodreads_auth_ids
        JOIN goodreads_reviews
        ON goodreads_auth_ids.book_id = goodreads_reviews.book_id
        JOIN goodreads_authors
        ON goodreads_auth_ids.author_id = goodreads_authors.author_id
        WHERE goodreads_auth_ids.author_id NOT ILIKE ''
```
The "sentence" column which concatenates ```review_text || goodreads_auth_ids.title || goodreads_auth_ids.description``` is the most important because it's this one that is used as a representation of the document to the embedding model and the one we use to look up similarity between the input vector.

There are a couple of things to note about the data. First, it's from 2019 so the recency on the recommendations from the data won't be great, but it should do fairly well on classical books. Second,  since [Goodreads no longer has an API](https://debugger.medium.com/goodreads-is-retiring-its-current-api-and-book-loving-developers-arent-happy-11ed764dd95), it's impossible to get this updated in any kind of reasonable way.  It's possible that future iterations of Viberary will use something like [Open Library](https://openlibrary.org/), but this will involve a lot of foundational data work.


# The Model

Viberary uses [Sentence Transformers](https://www.sbert.net/), a modified version of [the BERT architecture](https://jalammar.github.io/illustrated-bert/) that reduces computational overhead for deriving embeddings for sentence pairs [in a much more operationally efficient way](https://arxiv.org/pdf/1908.10084.pdf) than the original BERT model, making it easy to generate sentence-level embeddings that can be compared relatively quickly using cosine similarity.

This fits our use case because our input documents are several sentences long, and our query will be a keyword like search of at most 10 or 11 words, also like a sentence.

```
@inproceedings{reimers-2019-sentence-bert,
  title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
  author = "Reimers, Nils and Gurevych, Iryna",
  booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
  month = "11",
  year = "2019",
  publisher = "Association for Computational Linguistics",
  url = "https://arxiv.org/abs/1908.10084",
}
```

Given a sentence, `a``, and a second sentence, `b``, from an input, upstream model with BERT or similar variations as its source data and model weights, we'd like to learn a model whose output is a similarity score for two sentences. In the process of generating that score, the intermediate layers of that model give us embeddings for subsentences and words that we can then use to encode our query and corpus and do semantic similarity matching.

Given two input sentences, we pass them through the sentence transformer network and uses mean-pooling (aka averaging) all the embeddings of words/subwords in the sentence, then compares the final [embedding using cosine similarity, a common distance measure that performs well  for multidimensional vector spaces](https://github.com/UKPLab/sentence-transformers/blob/master/docs/training/overview.md)

<img src="static/assets/img/pooling.png" alt="drawing" width="600"/>

Sentence Transformers has a number of pre-trained variations on this architecutre, the most common of which is `sentence-transformers/all-MiniLM-L6-v2`, which [maps sentences and paragraphs](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) into a 384-dimension vector space. This means that each sentence is encoded in a vector that has 384 values, each with a different magnitude.

The initial results of this model were [just so-so](https://github.com/veekaybee/viberary/releases/tag/v.0.0.4), so I had to decide whether to use a different model or tune this one. The different model I considered was the series of [MSMarco models](https://www.sbert.net/docs/pretrained-models/msmarco-v3.html) , which were trained based on sample Bing searches. This was closer to what I wanted. Additionally, [the search task was asymmetric](https://www.sbert.net/examples/applications/semantic-search/README.html), which meant that the model accounted for the fact that the corpus vector would be longer than the query vector.

I chose `msmarco-distilbert-base-v3`, which is middle of the pack in terms of performance, and critically, is also tuned for cosine similarity lookups, instead of dot product, another similarity measure that takes into account both magnitude and direction, whereas cosine similarity only considers direction rather than size. This makes cosine similarity more suited for information retrieval with text because it's not as affected by text length, and additionally, it's more efficent at handling sparse representations of data.

There was a problem, however, the vectors for this series of models was twice as long, at `768` dimensions per embedding vector.

The longer a vector is, the more computationally intensive it is to work with, increasing,  with the runtime and the memory requirement grows quadratic with the input length. However, the logner it is,  the more information about the original input it compresses, so there is always a fine-lined tradeoff between being able to encode more information and faster inference, which is critical in search applications.

Learning embeddings was tricky not only in selecting the correct model, but also because everyone in the entire universe is using GPUs right now.

I first tried Colab, but soon found that, even at the paid tier, my instances would mysteriously get shut down or downgraded, particularly on Friday nights, when everyone is doing side projects.

<img src="static/assets/img/colab.png" alt="drawing" width="600"/>

I then tried Paperspace but found its UI hard to navigate.

I settled on doing the training on AWS since I already have an account and, in doing PRs for PyTorch, [had already configured EC2 instances for deep learning.](https://vickiboykis.com/2022/07/26/how-to-prepare-an-aws-test-image-for-pytorch/)

The process turned out to be much less painless than I anticipated, with the exception that P3 instances run out very quickly due to everyone training on them. [But it only took about 20 minutes to generate embeddings for my model](https://github.com/veekaybee/viberary/blob/main/src/model/generate_embeddings.ipynb), which is a really fast feedback loop as far as ML is concerned. I then wrote that data out to a snappy-compressed parquet file that I then load manually to the server where inference is performed.

# Redis and Indexing

Once I learned embeddings for the model, I needed to store them somewhere for inference. Here's where Redis comes in. There are about five million options now for storing embeddings for all kinds of operations. Some are better, some are worse. Here were my criteria:

+ an existing technology I'd worked with before
+ something I could change parameters on on my own and host on my own
+ something that provided blazing-fast inference
+ a software package where the documentation tells you O(n) performance time of [all its constitutent data structures](https://redis.io/docs/data-types/hashes/)

I'm just kidding about the last one but it's one of the things I love about the Redis documentation, one of the last pieces of technical documentation that talks to developers like they are competent and capable of higher reasoning.

Since I'd previously worked with Redis, already knew it to be highly reliable and relatively simple to use, as well as plays well with web apps and available packaged in Docker, which I would need for my next step to production, I went with [Redis Search](https://redis.io/docs/interact/search-and-query/), which offers storage and inference out of the box, as well as frequently updated Python modules.

Redis search is an add-on to Redis that you can load as part of the [redis-stack-server Docker image](https://github.com/RediSearch/RediSearch).

 It offers vector similarity search by indexing vectors stored as fields in Redis hash data structures, which are just field-value pairs like you might see in a dictionary or associative array. The common Redis commands for working with hashes are `HSET` and `HGET`, and [we can first HSET our embeddings](https://github.com/veekaybee/viberary/blob/main/src/index/indexer.py) and then create an index on top of them.   An important point is that we only want to [create the index schema after we `HSET` the embeddings](https://github.com/veekaybee/viberary/blob/main/src/index/index_embeddings.py), otherwise performance degrades significantly.

 For our learned embeddings, this process takes about ~1 minute.

 Now that we have the data in Redis, we can perform lookups. Since we'll be doing this in the context of a web app, we write a simple [Flask application](https://github.com/veekaybee/viberary/tree/main/src/api) that has several routes and captures the associated static files of the home page, the search box, and images, and takes a user query, runs it through the created search index object after cleaning the query, and returns a result:

 ```
# this allows us to build a query string as well as use the search box
@app.route("/search", methods=["POST", "GET"])
def search() -> str:
    word = None

    if request.method == "POST":
        word = request.form.get("query", "")
    elif request.method == "GET":
        word = request.args.get("query", "")

    return get_model_results(word, retriever)
 ```

that data gets passed into the model through a KNN Search object which takes a Redis connection and a config helper object:

```
retriever = KNNSearch(RedisConnection().conn(), ConfigManager())

conf = ConfigManager()

def get_model_results(word: str, search_conn) -> str:
    data = search_conn.top_knn(word)
    return render_template("index.html", data=data, query=word)
```

The [search class](https://github.com/veekaybee/viberary/blob/main/src/search/knn_search.py#L13) is where most of the real work happens. First, the user query string is parsed and sanitized, although in theory, in BERT models, you should be able to send the text as-is, since BERT was originally trained on data that does not do text clean-up and parsing, like traditional NLP does.

Then, that data is rewritten into the Python dialect for the Redis query syntax. The search syntax is can be a little hard to work with  originally, both in the Python API and on the Redis CLI, so I spent a lot of time playing aorund with this and figuring out what works best, as well as tuning the hyperparameters passed in [from the config file](https://github.com/veekaybee/viberary/blob/9f55493e0c8f77c0727df9c0e9191033469e468a/config.yml#L24), such as the number of results, the vector size, and the float type (very important to make sure all these hyperparameters are correct given the model and vector inputs, or none of this works correctly.)

```python
q = (
            Query(f"*=>[KNN {top_k} @{self.vector_field} $vec_param AS vector_score]")
            .sort_by("vector_score", asc=False)
            .sort_by(f"{self.review_count_field}", asc=False)
            .paging(0, top_k)
            .return_fields(
                "vector_score",
                self.vector_field,
                self.title_field,
                self.author_field,
                self.link_field,
                self.review_count_field,
            )
            .dialect(2)
        )```

[HNSW is the algorithm, initially written at Twitter,  implemented in Redis](https://github.com/RediSearch/RediSearch) that actually peforms the query based on cosine similarity. In short, [it looks for an approximate solution](https://arxiv.org/abs/1603.09320) to the k-nearest neighbors problem by formulating nearest neighbors as a graph search problem to be able to find nearest neighbors at scale (naive solutions mean that you have to compare each element to each other element, a process which computationally scales linearly with the number of elements we have). HNSW bypasses this problem by using skip list data structures to  create multi-level linked lists to keep track of nearest neighbors. During the navigation process, HNSW traverses through the layers of the graph to find the shortest connections, leading to finding the nearest neighbors of a given point.

It then returns the closest elements, ranked by cosine similarity. In our case, it returns the document whose 768-dimension vector most closely matches the 768-dimension vector generated by our model at query time.

# Getting the UI Right

Once we get the results from the API, all we get back is a list of elements that include the title, author, cosine similarity, and link to the book. It's now our job to present this to the user, and, additionally, to think about the best way to get the user to write a vibe query.

User expectations are really hard

Search UIs can be notoriously hard because they are so open-ended

 # DigitalOcean, Docker, and Production

 Now that this all works in a development environment, it's time to scale it for production. There are many, many considerations. The one I wanted to focus on included:

 + reproducible environments, aka not developing on my laptop
 + very simple manipulation of resources in the cloud
 + The ability to spin up and down resources quickly
 + Fast CI/CD

 For this stack, I started by creating a Dockerfile that encompassed all the pieces of the web app. The redis instance has its own Dockerfile, from Redis, that I don't want to mess with.

 In the app dockerfile, I want to make sure to have the fastest load time possible, so I follow [Docker best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/) of having the layers that change the most last, caching, and mounting files into the Docker image so I'm not constantly copying data.

 ```
 FROM bitnami/pytorch
USER root

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ../../requirements.txt requirements.txt

RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean \
    && apt-get update \
    && apt-get -y --no-install-recommends install \
    -y git

RUN --mount=type=cache,target=~/.cache/pip  pip install -r requirements.txt
RUN pip uninstall dataclasses -y

RUN mkdir /viberary/data; exit 0
RUN chmod 777 /viberary/data; exit 0
ENV TRANSFORMERS_CACHE=/viberary/data
ENV SENTENCE_TRANSFORMERS_HOME=/viberary/data
ENV PYTHONPATH "${PYTHONPATH}:/viberary/src:/opt/bitnami/python/lib/python3.8/site-packages"
ENV WORKDIR=/viberary
WORKDIR $WORKDIR
```

The Docker compose takes this Dockerfile and networks it to the Redis container.

```
version: "3.8"

services:
  redis:
    image: redis/redis-stack-server:latest
    volumes:
      - redis-data:/data
    container_name: redis
    command: redis-server --port 6379 --appendonly yes  --protected-mode no  --loadmodule /opt/redis-stack/lib/redisearch.so --loadmodule /opt/redis-stack/lib/rejson.so
    platform: linux/amd64

  web:
    container_name: viberary
    build:
      context: .
      dockerfile: docker/prod/Dockerfile
    ports:
      - '8000:8000'
    volumes:
      - ./:/viberary
      - ./viberary/src/training_data:/training_data
      - /mnt/viberary:/viberary/logs
    environment:
      - REDIS_HOST=redis
    depends_on:
      - redis
    platform: linux/amd64
    command: gunicorn -b 0.0.0.0:8000 -w 4 src.api.wsgi:app -t 900

volumes:
  redis-data:
```

 finally outputting everything to port 80 via nginx, which I configured on each DigitalOcean droplet that I created.

```
server {
    listen 80;
    server_name ip address;
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
    root /var/www/src/api/static;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/var/www/viberary.sock;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

Digital Ocean is a fantastic resource that provides low-maintenance servers for small projects exactly like this one, and in order to create redundancy, I load balanced two droplets behind a load balancer, pointing to the same web address, a domain I bought from Amazon's route 53.

When I push code, it [first goes through a pre-commit hook](https://github.com/veekaybee/viberary/blob/main/.pre-commit-config.yaml) that lints it and cleans everything up, including black, ruff, and isort.

Then, GitHub actions builds the artifact icnluding running pytest, which it sends to my server using GitHub Secrets config.

```
name: Python package and deploy

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [ "3.9" ]

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - uses: actions/cache@v3
        with:
          path: ${{ env.pythonLocation }}
          key: ${{ env.pythonLocation }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install ruff pytest
      - name: Lint with ruff
        run: |
          # stop the build if there are Python syntax errors or undefined names
          ruff --format=github --select=E9,F63,F7,F82 --target-version=py39 .
          # default set of ruff rules with GitHub Annotations
          ruff --format=github --target-version=py39 .
      - name: Test with pytest
        run: |
          pytest

      - name: install ssh keys
        run: |
          install -m 600 -D /dev/null ~/.ssh/id_rsa
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/id_rsa
          ssh-keyscan -H ${{ secrets.SSH_HOST }} > ~/.ssh/known_hosts
      - name: connect and pull
        run: ssh ${{ secrets.SSH_USER }}@${{ secrets.SSH_HOST }} "cd ${{ secrets.WORK_DIR }} && git checkout ${{ secrets.MAIN_BRANCH }} && git pull origin main && exit"
      - name: cleanup
        run: rm -rf ~/.ssh
```

Once the code is on the server, I tear down, rebuild, and reload the docker image through the makefile, and also add embeddings:

```embed:
	docker exec -it viberary python /viberary/src/index/index_embeddings.py

build:
	docker compose build

up-intel:
	docker compose up -d

up-arm:
	export DOCKER_DEFAULT_PLATFORM=linux/amd64
	docker compose up -d

onnx:
	docker exec -it viberary optimum-cli export onnx --model sentence-transformers/msmarco-distilbert-base-v3 sentence-transformers/msmarco-distilbert-base-v3_onnx/

down:
	docker compose down

logs:
	docker compose logs -f -t
```

Now, we have a working app.

The final part of this was load testing, which I did with [Python's Locust library](https://locust.io/), which provides a nice interface for running any type of code against any endpoint that you specify.

One thing that I realized as I was load testing was that my model was slow, and search expects instant results, so I converted it to an [ONNX artifact](https://onnxruntime.ai/) and had to change the related code, as well.


# Key Takeaways

+ __Getting to a testable prototype is key__. I did all my initial exploratory work locally in Jupyter notebooks, [including working with Redis](https://github.com/veekaybee/viberary/blob/main/src/notebooks/05_duckdb_0.7.1.ipynb), so I could see the data output of each cell. I [strongly believe](https://vickiboykis.com/2021/11/07/the-programmers-brain-in-the-lands-of-exploration-and-production/) working with a REPL will get you the fastest results immediately. Then, when I had a strong enough grasp of all my datatypes and data flow, I immediately moved the code into object-oriented, testable modules. Once you know you need structure, you need it immediately because it will allow you to develop more quickly with reusable, modular components.

+ __Vector sizes and models are important__. If you don't watch your hyperparameters, if you pick the wrong model for your given machine learning task, the results are going to be bad and it won't work at all.

+ __Don't use the cloud if you don't have to__. I'm using DigitalOcean, which is really, really, really nice for medium-sized companies and projects and is often overlooked over AWS and GCP. I'm very versant in cloud, but it's nice to not have to use BigCloud if you don't have to and to be able to do a lot more with your server directly. DigitalOcean has reasonable pricing, reasonable servers, and a few extra features like monitoring, load balancing, and block storage that are nice coming from BigCloud land, but don't overwhlem you with choices. They also recently acquired [Paperspace](https://www.paperspace.com/), which I've used before to train models, so should have GPU integration.

+ __DuckDB__ is becoming a stable tool for work up to 100GB locally. There are a lot of issues that still need to be worked out because it's a growing project. For example, for two months I couldn't use it for my JSON parsing because it didn't have regex features that I was looking for, which were added in 0.7.1, so use with caution. Also, since it's embedded, you can only run one process at a time which means you can't run both command line queries and notebooks.  But it's a really neat tool for quickly munging data.

+ __Docker still takes time__  I spent a great amount of time on Docker. Why is Docker different than my local environment? How do I get the image to build quickly and why is my image now 3 GB? What do people do with CUDA libraries (exclude them if you don't think you need them initially, it turns out). I spent a lot of time making sure this process worked well enough for me to not get frustrated rebuilding hundreds of times. Relatedly,  __Do not switch laptop architectures in the middle of a project__ .


And finally,

+ True semantic search is very hard and involves a lot of algorithmic fine-tuning. People have been fine-tuning Google for years and years. Netflix had thousands of labelers. [Each company has teams of engineers working on search and recommendations](https://vicki.substack.com/p/what-we-talk-about-when-we-talk-about) to steer the algorithms in the right direction. Just take a look at the company formerly known as Twitter's algo stack.  It's fine if the initial results are not that great.

The important thing is to keep benchmarking the current model against previous models and to keep iterating and keep building


# Next Steps

I have a couple things on the roadmap I'd like to accomplish.

1. Include a "I'm Feeling Lucky" type button that generates one good vibe-y recommendation at random.
2. Build out [a feature/model store](https://github.com/veekaybee/viberary/issues/73) for the model and the training data, will likely just be hosted in DigitalOcean as well, nothing super fancy, but right now it's annoying to move these artifacts around, but not annoying enough where I had enough time to build one.
3. If model performance becomes an issue, migrate the API to Java ([Go was my first choice](https://github.com/veekaybee/viberary/issues/15) but it doens't have a very good ONNX story at the moment)
4. Add Prometheus and Grafana. I had these initially but they created too much overhead and Digital Ocean default monitoring is good enough.
5. [Query autocompletion](https://github.com/veekaybee/viberary/issues/70) in the search bar
6. [Chart of most recommended books](https://github.com/veekaybee/viberary/issues/65) based on log data on the site
7. Include a toggle for multi-lingual search. I haven't tried this out well at all, and most of the books are in English, but I'd like to see if it's a possibility, as well as investigate how well this model handles it.

We'll see how many of these I get to - I'd love to do at least the random button.

# Resources

+ [Relevant Search by Turnbull and Berryman](https://www.manning.com/books/relevant-search)
+ [Corise Search Course](https://corise.com/course/search-fundamentals) and Search with Machine Learning - I've taken these, and have nothing to sell except the fact that Grant and Daniel are aweosme. [Code is here.](https://github.com/gsingers/search_fundamentals_course)
+ [What Are Embeddings](https://vickiboykis.com/what_are_embeddings/) - during the process of writing this I came up with a lot of sources included in the site and bibliography
+ [Towards Personalized and Semantic Retrieval: An End-to-End Solution for E-commerce Search via Embedding Learning](https://arxiv.org/abs/2006.02282)
+ [Pretrained Transformers for Text Ranking: BERT and Beyond](https://arxiv.org/pdf/2010.06467.pdf)
+ [Advanced IR Youtube Series](https://www.youtube.com/playlist?list=PLSg1mducmHTPZPDoal4m59pPxxsceXF-y)

