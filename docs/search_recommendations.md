Is this a recommendations or search project? What does it mean for something to be a recommendations or search project? 

Here are some intro notes:

How are search and recommendations the same, and how are they different? 
--

+ [Question on Mastodon](https://jawns.club/@vicki/109621807848237349)
+ [Question on Twitter](https://twitter.com/vboykis/status/1610031965410926597)

TL;DR: 
 - The design of both search and recommendations is to find and filter information
 - Search is a "recommendation with a null query"
 - Search is "I want this", recommendations is "you might like this"
 - In recommendations, man "is this search query", from [Computing Taste by Nick Seaver](https://press.uchicago.edu/ucp/books/book/chicago/C/bo183892298.html)
 - Search and recommendations are at opposite ends of an extreme spectrum
 - Search is more about retrieving information versus filtering for preferences, and in search the user has more agency versus recommendations where the recommender system has more agency
 

[Marcia Bates on Search Systems](https://theinformed.life/2023/01/01/episode-104-marcia-bates-on-search-systems/):

 - People like to see where topics are embedded in the contextual landscape because effective searching is not intuitive and there is no explicit index for search strategies

[Michael Ekstrand on search vs recsys](https://md.ekstrandom.net/blog/2015/10/search-and-recsys)

+ Search is directed information-seeking and we care about
 - Item properties
 - User properties (preferences and interaction history)
 - Query
 - Context
 
 In general, these things make up the following formulation: 
 
<img width="351" alt="Screen Shot 2023-01-07 at 10 15 24 AM" src="https://user-images.githubusercontent.com/3837836/211157746-eb24aa27-a7a7-4e9c-a510-c555541b6478.png">

+ Item + User context: Traditional recommendations: 
+ Item + Query context: Non-personalized search
+ Context + user: context-aware recommender
+ item, query, query, context: Context-aware personalized search 

## Resources

### Books
+ [Computing Taste](https://press.uchicago.edu/ucp/books/book/chicago/C/bo183892298.html) by Nick Seaver, on music recommendation
+ [The Revolt of the Public](https://press.stripe.com/the-revolt-of-the-public), about the collapse of top-down information sources

### Papers

+ [A Survey of Diversification Techniques in Search and Recommendation](https://arxiv.org/abs/2212.14464)
+ [Recommender Systems Notation](https://md.ekstrandom.net/pubs/notation)
+ [Wide and Deep Learning for Recommender Systems](https://arxiv.org/abs/1606.07792)
+ [The design of browsing and berrypicking techniques for the online search interface](https://pages.gseis.ucla.edu/faculty/bates/berrypicking.html)

### Sites/Talks/Posts
+ James Kirk on [lessons from industrial recommender systems](https://www.youtube.com/watch?v=Zoq0oHrGabc)
+ [Marcia Bates interview on search systems](https://theinformed.life/2023/01/01/episode-104-marcia-bates-on-search-systems/)
+ [Michael Ekstrand on the difference](https://md.ekstrandom.net/blog/2015/10/search-and-recsys) between search and recommendations
and on [recsys notation](https://md.ekstrandom.net/pubs/notation)
+ [Eugene Yan on system design](https://eugeneyan.com/writing/system-design-for-discovery/) for search and recommendations
+ [New Search system based on Stable diffusion](https://metaphor.systems/)
+ [Expanding AI Dark Forest](https://maggieappleton.com/ai-dark-forest) by Maggie Appleton 

![IMG_2941](https://user-images.githubusercontent.com/3837836/211155553-3040bda6-846f-43f9-b7bd-b328abc9cd85.jpg)

