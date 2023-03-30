# Viberary

![](https://github.com/veekaybee/viberary/blob/main/docs/assets/img/vibe_book.png)

Viberary is a project that will recommend you books based not on genre or title, but vibe by performing semantic search across a set of learned embeddings. 
The idea is pretty simple: return book recommendations based on the vibe of the book that you put in.
So you don't put in "I want science fiction", you'd but in "atmospheric, female lead, worldbuilding, funny" something like that, like a prompt, and get back a list of books

## Reference implementation: 
![](https://github.com/veekaybee/viberary/blob/main/assets/viberary.png)

## Actual Architecture:
![](https://github.com/veekaybee/viberary/blob/main/assets/actual_architecture.png)

## Blog posts and research artifacts

+ Post 0: [Working with the data in BigQuery](https://vickiboykis.com/2022/12/05/the-cloudy-layers-of-modern-day-programming/)
+ Post 1: [Working with the data in Pandas](https://vickiboykis.com/2023/01/17/welcome-to-the-jungle-we-got-fun-and-frames/)
+ Post 2: [Doing research with ChatGPT](https://vickiboykis.com/2023/02/26/what-should-you-use-chatgpt-for/)
+ [LaTeX Resource](https://vickiboykis.com/latex_resources/)

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


