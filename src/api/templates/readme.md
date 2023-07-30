*TL;DR*: Viberary helps you find books by __vibe__. I built it to satisfy an itch to do [ML side projects](https://vickiboykis.com/2020/06/09/getting-machine-learning-to-production/)  and navigate the current boundary between search and recommendations. It's a production-grade compliment to [my recent deep dive into embeddings.](http://vickiboykis.com/what_are_embeddings/)

<img src="static/assets/img/viberary_arch.png" alt="drawing" width="600"/>

It's a [two-tower](https://blog.reachsumit.com/posts/2023/03/two-tower-model/) semantic retrieval model that encodes both the query and the corpus using the
[Sentence Transformers pretrained asymmetric MSMarco Model](https://www.sbert.net/docs/pretrained-models/msmarco-v3.html).

<img src="static/assets/img/tactical_app.png" alt="drawing" width="600"/>

The training data is generated locally in DuckDB and the model is converted to ONNX for quick inference, with [corpus embeddings learned on AWS P3 instances](https://github.com/veekaybee/viberary/blob/main/src/model/generate_embeddings.ipynb) against the same model and stored in Redis and retrieved using the [Redis Search](https://redis.io/docs/interact/search-and-query/) module using the [HNSW algorithm](https://arxiv.org/abs/1603.09320) included as part of the Redis search module. Results are served through a Flask API running [Gunicorn](https://gunicorn.org/) and served to a Bootstrap front-end.

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


The problem of semantic search is not new and is one researchers and companies have been grappling with for decades in the field known as information retrieval, which started with roots in library science. [The paper introducing Google in 1998](https://storage.googleapis.com/pub-tools-public-publication-data/pdf/334.pdf) even discusses the problems with keyword-only search,

> People are likely to surf the web using its link graph, often starting with high quality human maintained indices such as Yahoo! or with search engines. Human maintained lists cover popular topics effectively but are subjective, expensive to build and maintain, slow to improve, and cannot cover all esoteric topics. Automated search engines that rely on keyword matching usually return too many low quality matches.

The tension and ability to make search engines work in the space between [query understanding](https://queryunderstanding.com/) through human enrichment and getting machines to better understand user intent has always been present.

Netflix was one of the first companies that started doing vibe-based content exploration when it [came up with a list of over 36, 00
genres](https://www.netflix.com/tudum/articles/netflix-secret-codes-guide) like "Gentle British
Reality TV" and "WitchCraft and the Dark Arts" in the 2010s. They [used large teams of people](https://www.theatlantic.com/technology/archive/2014/01/how-netflix-reverse-engineered-hollywood/282679/) to watch
movies and tag them with metadata. The process was so detailed that taggers received a 36-page document that "taught them how to rate movies on their sexually suggestive content, goriness, romance levels, and even narrative elements like plot conclusiveness."

These labels were then incorporated into Netflix's [recommendation architectures](https://netflixtechblog.com/system-architectures-for-personalization-and-recommendation-e081aa94b5d8) as features for training data.

It can be easier to incorporate these kinds of features into recommendations than search because the process of recommendation is the process of implicitly learning user preferences through data about the user and offering them suggestions of content or items to purchase based on their past history, as well as the history of users across the site, or based on the properties of the content itself. As such, [recommender interfaces often include lists of suggestions](https://www.nngroup.com/articles/recommendation-guidelines/) like "you might like.." or "recommended for you", or "because you interacted with X.."

Search, on the other hand, is an activity where the user expects their query to match exactly, so users have specific expectations of search interfaces:

1. They are extremely responsive
2. Results are accurate
3. We use text boxes the same way we have been conditioned to use Google Search over the past 30 years

So, in some senses , there is a direct conflict between a traditional search interface and semantic search, because semantic search is in that gray area between search and recommendations. Many search engines today, Google included, use a blend of traditional keyword search and semantic search to offer both direct results and related content, and with the explosion of generative AI and chat-based search and recommendation interfaces, this [division is becoming even blurrier.](https://docs.google.com/presentation/d/12aoYVaqus600NEuWASw_eF9xSDXGUMzGedAftfqBCCE/edit)

<img src="static/assets/img/searchandrec.png" alt="drawing" width="600"/>


# Why semantically search books?

I love reading, particularly fiction. I am always reading something. Check out my past reviews
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

Given the recent rise in interest of semantic search based by vector databases, as well as [the paper I just finished on embeddings](http://vickiboykis.com/what_are_embeddings/), I thought it would interesting if I could create a book recommendation engine. This idea eventually evolved into the thinking that, given my project constraints and preferences, what I had was really a semantic search problem aimed specifically at surfacing books.

# Architecting Semantic Search

There are several parts making up semantic search :

1. Data Collection
2. Modeling and understanding the approach
3. Engineering and Ops
4. UI Design

Most [search and recommendation architectures](https://eugeneyan.com/writing/system-design-for-discovery/) share a foundational set of commonalities: there is a set of documents that we have, that we'd like to filter through to get to the right documents presented to the user. We have to somehow update those documents, via an indexing function, and we then have to filter them, either manually or through machine learning, then rank them, also using either algorithms or heuristics, and then present them to some user front-end.



# Project Architecture Decisions

I had several requirements for this project. First, I wanted to a project that was well-scoped so that I wouldn't get tired, and so that I would ship it, because the worst ML project is the one that remains unshipped. [As Mitch writes](https://mitchellh.com/writing/building-large-technical-projects), "give yourself a good demo."

Second, I wanted to explore new technologies while also being careful of not wasting [my innovation tokens](https://mcfunley.com/choose-boring-technology). In other words, I wanted to build something normcore, i.e. using the right tool for the right job, and [not going overboard.](https://vicki.substack.com/p/you-dont-need-kafka)

The third factor was to try to ignore [the noisiness of the current ML ecsystem](https://vickiboykis.com/2022/11/10/how-i-learn-machine-learning/), which comes out with a new model and a new product and a new wrapper for the model for the product every day. I can't say this was easy: it is extremely hard to ignore the noise and just build, particularly given all the discourse around LLMs in the ML community, and now in society at large, but I tried my best to work with tech that had been established for at least a couple years if not more to avoid life on the bleeding edge, particularly given the brittleness of Python's packaging compatibility ecosystem.

I wish I could say that I was able to plan all of this out in advance, and the project that I eventually shipped was exactly what I had envisioned. But, like with any engineering effort, I had a bunch of false starts and dead ends. I started out [using Big Cloud](https://vickiboykis.com/2022/12/05/the-cloudy-layers-of-modern-day-programming/), a strategic mistake that cost me a lot of time and frustration because I couldn't see inside the cloud components and slowed down development cycles.  I eventually moved to data processing using DuckDB, but [it still look a long time](https://vickiboykis.com/2023/01/17/welcome-to-the-jungle-we-got-fun-and-frames/), as is typically the case in any data-centric project. Then, I spent a long time [working through creating models in Word2Vec](https://github.com/veekaybee/viberary/releases/tag/v0.0.1) so I could get some context for baseline text retrieval methods in the pre-Transformer era. Word2Vec was harder to  implement in PyTorch than using Gensim, and I took a long time before I got there.

My project tech stack, as it now stands is:

+ Original data in JSON files
+ Processed using the Python Client for DuckDB







# The Two Towers

Semantic search straddles the space between search and recommendations, which, thanks to

To understand the context of information retrieval

Typically, a common feature of modern recommendation and ranking systems is the two tower model. We have an item we'd like to recommend.

I started reading more about how I could use this here.

In order to do next-book recommendations well, I'd need a large set of user data in order to formualte the data
as a collaborative filtering problem, so that was out. But

# The training data

I'm using a

# The Mixture of Experts




Since I'd previously worked on

To do this well , you'd need a collaborative filtering algorithm trained on reading data

In the world of
recommendations, at scale, this is known as collaborative filtering, and I
initially wanted to

I wanted to do a personal project that picked up some of my work [updating post
categorization](https://engineering.tumblr.com/post/148350944656/categorizing-posts-on-tumblr)
when I [previously worked at
Tumblr](https://vickiboykis.com/2022/07/25/looking-back-at-two-years-at-automattic-and-tumblr/)
and  serving them [through
Streambuilder](https://engineering.tumblr.com/post/722102563011493888/streambuilder-our-open-source-framework-for)
and combine it with my love for building [end-to-end ML
applications](https://vickiboykis.com/2020/06/09/getting-machine-learning-to-production/) - last
time I built one I used GPT-2(!), and I am also currently extremely interested
in the intersection between recommendations and search. Finally, I recently finished writing a
paper on embeddings, so I knew I wanted to do a project
that had all of these elements.

We can try to approximate this with
traditional search in a number of ways.



# The Architecture

# Getting the UI Right


# Key Learnings

Don't use the cloud if you don't have to

ML apps have a ton of considerations that are not directly related to robots killing people.

Vector sizes and models are important.

Unsupervised learning is still hard.

Nginx and Redis are rock-solid tools. Don't index before xyz

Inference time

Load testing.

There are no guidelines.

DuckDB is slowly becoming a stable tool for work up to 100GB locally.

All you need is one big machine (Josh wills talk)

Docker image sizes are important.

Quick iteration and llocal development is important

The two environments will never match.

https://blog.reachsumit.com/posts/2023/03/two-tower-model/

True semantic search is very hard and involves a lot of algorithmic fine-tuning. People have been fine-tuning Google for years and years. Netflix had thousands of labelers.


# Resources

+ Relevant Search by Turnbull and Berryman
+ Introduction to Information Retrieval
+ Search Course
+ What Are Embeddings
+ Papers: Ecommerce and this one If you are interested in much, much more detail, I recommend Grant and Daniel's course on Search Fundamentals and Search with Machine Learning, which I've taken and can recommend strongly as a way to understand all these concepts. I am not affiliated with the program or with them, but I liked the class.
https://corise.com/course/search-fundamentals
