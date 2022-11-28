# Viberary

![](viberary-logo.png)

Viberary is a project that will eventually recommend you books based not on genre or title, but vibe. 
The idea is pretty simple: return book recommendations based on the vibe of the book that you put in.
So you don't put in "I want science fiction", you'd but in "atmospheric, female lead, worldbuilding, funny" something like that, like a prompt, and get back a list of books

Reference implementation: 
![](viberary.png)

Right now it's just all BigQuery and vibes.

## Lit Review

+ ["Towards Personalized and Semantic Retrieval: An End-to-End Solution for E-commerce Search via Embedding Learning"](https://arxiv.org/abs/2006.02282)
+ ["PinnerSage"](https://arxiv.org/abs/2007.03634)


## Input Data

UCSD Book Graph, with the critical part being the [user-generated shelf labels.](https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/books). [Sample row:](https://gist.github.com/veekaybee/e8ea5dcf5632fd6345096023dc18159e)

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
    },
    {
      "count": "69",
      "name": "favorites"
    },
    {
      "count": "48",
      "name": "spiritual"
    },
    {
      "count": "45",
      "name": "owned"
    },
    {
      "count": "43",
      "name": "books-i-own"
    },
    {
      "count": "33",
      "name": "fiction"
    },
    {
      "count": "30",
      "name": "taoism"
    },
    {
      "count": "27",
      "name": "self-help"
    },
    {
      "count": "22",
      "name": "inspirational"
    },
    {
      "count": "20",
      "name": "currently-reading"
    },
    {
      "count": "19",
      "name": "humor"
    },
    {
      "count": "18",
      "name": "my-library"
    },
    {
      "count": "17",
      "name": "eastern-philosophy"
    },
    {
      "count": "15",
      "name": "philosophy-religion"
    },
    {
      "count": "15",
      "name": "buddhism"
    },
    {
      "count": "14",
      "name": "owned-books"
    },
    {
      "count": "12",
      "name": "default"
    },
    {
      "count": "12",
      "name": "religious"
    },
    {
      "count": "12",
      "name": "psychology"
    },
    {
      "count": "12",
      "name": "library"
    },
    {
      "count": "11",
      "name": "my-books"
    },
    {
      "count": "10",
      "name": "religion-philosophy"
    },
    {
      "count": "9",
      "name": "tao"
    },
    {
      "count": "9",
      "name": "religion-spirituality"
    },
    {
      "count": "9",
      "name": "religion-and-spirituality"
    },
    {
      "count": "9",
      "name": "philosophical"
    },
    {
      "count": "9",
      "name": "i-own"
    },
    {
      "count": "8",
      "name": "other"
    },
    {
      "count": "7",
      "name": "wish-list"
    },
    {
      "count": "7",
      "name": "to-buy"
    },
    {
      "count": "7",
      "name": "self-improvement"
    },
    {
      "count": "7",
      "name": "humour"
    },
    {
      "count": "7",
      "name": "classics"
    },
    {
      "count": "6",
      "name": "shelfari-favorites"
    },
    {
      "count": "6",
      "name": "zen"
    },
    {
      "count": "6",
      "name": "pooh"
    },
    {
      "count": "6",
      "name": "literature"
    },
    {
      "count": "5",
      "name": "to-read-again"
    },
    {
      "count": "5",
      "name": "series"
    },
    {
      "count": "5",
      "name": "re-read"
    },
    {
      "count": "5",
      "name": "personal-growth"
    },
    {
      "count": "5",
      "name": "own-it"
    },
    {
      "count": "5",
      "name": "life"
    },
    {
      "count": "5",
      "name": "eastern-thought"
    },
    {
      "count": "5",
      "name": "abandoned"
    },
    {
      "count": "5",
      "name": "20th-century"
    },
    {
      "count": "4",
      "name": "read-2016"
    },
    {
      "count": "4",
      "name": "winnie-the-pooh"
    },
    {
      "count": "4",
      "name": "religion-and-philosophy"
    },
    {
      "count": "4",
      "name": "reference"
    },
    {
      "count": "4",
      "name": "piglet"
    },
    {
      "count": "4",
      "name": "philosophy-and-religion"
    },
    {
      "count": "4",
      "name": "non-fic"
    },
    {
      "count": "4",
      "name": "life-lessons"
    },
    {
      "count": "4",
      "name": "have"
    },
    {
      "count": "4",
      "name": "didnt-finish"
    },
    {
      "count": "4",
      "name": "china"
    },
    {
      "count": "4",
      "name": "books"
    },
    {
      "count": "4",
      "name": "benjamin-hoff"
    },
    {
      "count": "3",
      "name": "did-not-finish"
    },
    {
      "count": "3",
      "name": "unread"
    },
    {
      "count": "3",
      "name": "books-owned"
    },
    {
      "count": "3",
      "name": "home"
    },
    {
      "count": "3",
      "name": "psychology-philosophy"
    },
    {
      "count": "3",
      "name": "bought"
    },
    {
      "count": "3",
      "name": "young-adult"
    },
    {
      "count": "3",
      "name": "want"
    },
    {
      "count": "3",
      "name": "unsorted"
    },
    {
      "count": "3",
      "name": "theology"
    },
    {
      "count": "3",
      "name": "spirituality-religion"
    },
    {
      "count": "3",
      "name": "poetry"
    },
    {
      "count": "3",
      "name": "philosophy-eastern"
    },
    {
      "count": "3",
      "name": "personal"
    },
    {
      "count": "3",
      "name": "peace-corps"
    },
    {
      "count": "3",
      "name": "nonfiction-other"
    },
    {
      "count": "3",
      "name": "new-age"
    },
    {
      "count": "3",
      "name": "must-reads"
    },
    {
      "count": "3",
      "name": "motivational"
    },
    {
      "count": "3",
      "name": "library1"
    },
    {
      "count": "3",
      "name": "inspirational-spiritual"
    },
    {
      "count": "3",
      "name": "home-shelf"
    },
    {
      "count": "3",
      "name": "fun"
    },
    {
      "count": "3",
      "name": "essays"
    },
    {
      "count": "3",
      "name": "daoism"
    },
    {
      "count": "3",
      "name": "children"
    },
    {
      "count": "3",
      "name": "american"
    },
    {
      "count": "3",
      "name": "adult"
    },
    {
      "count": "2",
      "name": "brooklyn"
    },
    {
      "count": "2",
      "name": "male-author"
    },
    {
      "count": "2",
      "name": "humorous"
    },
    {
      "count": "2",
      "name": "a-own"
    },
    {
      "count": "2",
      "name": "on-the-shelf"
    },
    {
      "count": "2",
      "name": "unfinished"
    },
    {
      "count": "2",
      "name": "small-black-bookcase"
    },
    {
      "count": "2",
      "name": "spiritualism"
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

## Processing

Read into BigQuery with notebooks to profile. 
