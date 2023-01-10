# Things I've learned while working on Viberary

## File formats

+ Parquet is likely the [most performant](https://www.robinlinacre.com/parquet_api/) file format for compressing JSON/CSV and reading into Spark and Pandas. Spark has its own utility to process Parquet files, but you first need to create a dataframe to do so. 

+ In order to create Parquet files, you first need to specify a schema, and that's usually done either via the DataFrame's internal representation or by converting your initial input (JSON) file to .avsc, which is just a JSON representation of what's available. The Parquet file is created based on the schema. 


## Statistics 

Ranking: 
+ If you're trying to create a recommendation system, often what you'll want to do is sort by rating (without personalization). However, just sorting by average rating has its own issues depending on how much data you have available. There are several ways to deal with this, including creating a dampened rating, and [Wilson score](https://www.evanmiller.org/how-not-to-sort-by-average-rating.html), which is helpful for small data because it ends up balancing out the uncertainty for a small number of observations. 
  
The goal is [to not have a single item](https://www.reddit.com/r/explainlikeimfive/comments/4oirm9/comment/d4cyyo8) with a super-high rating end up on top of the distribution by estimating the true approval rate of the item based on the number of votes the item got by using confidence intervals: given the number of items you approve, your confidence interval approval rate is between x and y. The lower bound is what's used to sort the items. 

