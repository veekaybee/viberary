{% extends "how.html" %}

{% block content %}
# What is it????
Viberary is a semantic search engine. It finds books based on vibe rather than exact
keyword matches by genre, author, and title. Traditional search engines work by doing lexical
matching - that is if you type in "Nutella into the search engine, it will try to find all
documents where "Nutella" occurs.

It can do this lookup quickly by building [an inverted
index](https://en.wikipedia.org/wiki/Inverted_index), which is a data structure that creates a
key/value pair where the key is the term and the value is a collection
of all the documents that match the term.

What's a vibe? A vibe can be hard to define, but generally it's more of a feeling of association
than something concrete: a mood, a color, or a phrase. Viberary will not give you exact matches for "Nutella", but if you type in "chocolately hazlenut goodness", the expectation is that you'd get back Nutella.

# Why semantically search books?

I love reading, particularly fiction. I am always reading something. Check out my past reviews
[2021](https://vickiboykis.com/essays/2022-01-02-favorite-books/),
[2020](https://vickiboykis.com/essays/2021-04-16-favorite-books/),[2019](https://vickiboykis.com/essays/2020-01-01-books/),
and you get the idea. And, as a reader, I am always looking for something good to read. Often, I'll get
recommendations by browsing [LitHub](https://lithub.com/) or [BookBub](https://www.bookbub.com/), but sometimes I'm in the mood for a particular
genre, or, more specifically a feeling that a book can capture. For example, after finishing ["The Overstory" by Richard Powers](https://www.richardpowers.net/the-overstory/), I was in the mood for more sprawling multi-generational epics
on arcane topics (I know so much about trees now.) But you can't really find collections like this unless a human who
reads a lot puts a list like this together.

One of my favorite formats of book recommendations [is
Biblioracle](https://themorningnews.org/article/greetings-from-the-biblioracle), where readers
send John Warner, an extremely well-read novelist, a list of the last five books they've read and he recommends their next read
based on their reading preferences. He is rarely wrong.

Armed with this business case (my very important pleasure reading needs), and [a desire to do another end-to-end
machine learning side project](https://vickiboykis.com/2020/06/09/getting-machine-learning-to-production/)
I started exploring ways that I could do a side project around book recommendations by [doing a literature review](https://vickiboykis.com/2022/11/10/how-i-learn-machine-learning/) and thinking about different ways
I could formulate this as a machine learning problem in the information retrieval space.

# The Two Towers

Typically, a common feature of modern recommendation systems is the two tower model

I started reading more about how I could use this here.

In order to do next-book recommendations well, I'd need a large set of user data in order to formualte the data
as a collaborative filtering problem, so that was out. But

# Components of Semantic Search

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

Netflix was one of the first companies that started doing vibe-based search when it [came up with a list of over 36,00
genres](https://www.netflix.com/tudum/articles/netflix-secret-codes-guide) like "Gentle British
Reality TV" and "WitchCraft and the Dark Arts" in the 2010s. They [used large teams of people](https://www.theatlantic.com/technology/archive/2014/01/how-netflix-reverse-engineered-hollywood/282679/) to watch
movies and tag them with metadata. The process was so detailed that taggers received a 36-page document that "taught
them how to rate movies on their sexually suggestive content, goriness, romance
levels, and even narrative elements like plot conclusiveness."

These labels were then incorporated into Netflix's [recommendation architectures](https://netflixtechblog.com/system-architectures-for-personalization-and-recommendation-e081aa94b5d8) as features for training data. However, it's easier to incorporate these kinds of features into recommendations than search because recommendations are all about implicitly learning user
preferences based on their activity and offering them suggestions for content. Search is an activity
where the user expects their query to match exactly, so users have specific expectations of search interfaces:

1. They are extremely responsive

But in order to really do <b>vibe search</b> right and not involve as much manual labelling, we
need to build a semantic search engine.

    {{ markdown_content|safe }}
{% endblock %}
