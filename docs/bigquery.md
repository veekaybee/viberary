# Working with BigQuery

BigQuery is [Dremel, Google's version of read-only analytics](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36632.pdf) on large datasets.  Dremel builds on ideas from web search and parallel DBMSs. Its architecture borrows the concept of a serving tree used in
distributed search engines. [You can ingest in multiple formats](https://cloud.google.com/blog/products/data-analytics/new-blog-series-bigquery-explained-overview), including inferred from schemaless zipped json files, which is what's available in the UCSD graph. 

Something to watch out for on ingest is that BigQuery actually just splits JSON output into two "rows" which are just one ROW at the [query level.](https://www.cloudskillsboost.google/focuses/3696?parent=catalog)

You can also, as of recently, explore your query results with a Colab Notebook, [either via a cell magic](https://github.com/googleapis/python-bigquery/blob/5d3e5d36d6ff492ba6b76018a4d832e67a2c46a6/google/cloud/bigquery/magics/magics.py) which wraps the bigquery client and hides authentication or direct bigquery client, which gives you more control over performance and execution. 

## Colab Notebooks 

Colab notebooks are Google's answer to Jupyter and have most of the same functionality. They obscure a bit more than they should, particularly when it comes to pulling data in from BigQuery, but you can do some quick memory profiling. 

```bash
!grep MemTotal /proc/meminfo
MemTotal:       26690640 kB
```
Will give you the total RAM. For a default notebook, it's 13, for Colab Pro it's 26. 

```
!df -H
```

You can confirm these by mousing over the runtime. (close enough)

![](memory.png)

```
Filesystem      Size  Used Avail Use% Mounted on
overlay         243G   25G  219G  10% /
tmpfs            68M     0   68M   0% /dev
shm              13G     0   13G   0% /dev/shm
/dev/root       2.1G  1.1G  955M  54% /sbin/docker-init
tmpfs            14G   41k   14G   1% /var/colab
/dev/sda1       250G   43G  207G  18% /etc/hosts
tmpfs            14G     0   14G   0% /proc/acpi
tmpfs            14G     0   14G   0% /proc/scsi
tmpfs            14G     0   14G   0% /sys/firmware
```

You can start indexing into your dataframe for memory usage using:

```
dataframe.info(memory_usage="deep")
```

## BigQuery into Pandas DataFrames: 

You can load it [in this way](https://cloud.google.com/bigquery/docs/samples/bigquery-query-results-dataframe)


```
from google.colab import auth
from google.cloud import bigquery
from google.colab import data_table

import google.auth
from google.cloud import bigquery
from google.cloud import bigquery_storage

location = 'US' # Location inserted based on the query results selected to explore
client = bigquery.Client(project=project, location=location)
data_table.enable_dataframe_formatter()

# Make clients
bqclient = bigquery.Client(credentials=auth.authenticate_user(), project=project,)
bqstorageclient = bigquery_storage.BigQueryReadClient(credentials=auth.authenticate_user())

# define your query
your_query = """SELECT * FROM `{project}.viberary.goodreads_books` LIMIT 1000"""

dataframe = (
    bqclient.query(your_query)
            .result()
            .to_dataframe(
                bqstorage_client=bqstorageclient,
                progress_bar_type='tqdm_notebook',)
)
```

The to_dataframe method is actually a [to_arrow](https://github.com/googleapis/python-bigquery/blob/0f08e9a8ff638e78006d71acd974de2dff89b5d9/google/cloud/bigquery/table.py#L2182) and to_pandas call under the covers. 

## TODO

[memory profiling](https://pythonspeed.com/articles/estimating-memory-usage/)
[fil for pandas dataframes](https://pythonspeed.com/articles/pandas-dataframe-series-memory-usage/)