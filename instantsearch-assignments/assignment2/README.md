# Assignment 2
In this assignment we will be working on the midtier of our application. The midtier will hold all our query building, ranking and scoring logic. This will also serve as the place to plugin any custom blending logic and business rules if any.

### End Result
At the end of this assignment you should be able to query autocomplete and instant search results index and blend the results together with a custom logic.

### Dataset
The dataset that we will be working today has been taken from the stackoverflow data dump. The dataset has been simiplified for readability and to allow users to focus on retrieval and ranking aspects. The dataset is divided into two files:
* **Tags.xml** - This file contains the information of the tags, tag post id and count of posts associated with the tag.
```xml
<?xml version="1.0" encoding="utf-8"?>
<tags>
  <row Id="1" TagName=".net" Count="233796" ExcerptPostId="3624959" WikiPostId="3607476" />
</tags>  
```

* **posts_10K.json** - This file contains one post per line along with the id, title and a [score](http://meta.stackexchange.com/questions/229255/what-is-the-score-of-a-post) as voted by the users.
```json
{"@Score": "358", "@Id": "4", "@Title": "When setting a form's opacity should I use a decimal or double?"}
```
### Elastic Search Basics

1. **Query Building** - The way you rewrite the query greatly influences the quality of the results that are retrieved. The search query can be rewritten as entered by the user or augmented with metadata, normalized (analyzed, tokenized, phrase extraction etc.) to be a more targeted and meaningful query. Elasticsearch utilizes the lucene api for querying the index and provides a plethora of query building options. We present some below and recommend you explore others to see what suits best. 
    * [Match Query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html)
    * [Term Query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html)
    * [Compound Queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/compound-queries.html)
 
    We recommend you start off by utilizing the Match Query and then move on to exploring different Compound Queries.

2. **Query Autocomplete** - We utilize the Elasticsearch suggest module to build queries for the query autocomplete results. To build the query for autocomplete refer to documentation [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters.html).     


### Task I
Using the query building techniques discussed above query the search index for instant search results and autocomplete suggestions. 

### Task II
Using the two resultsets from instant search results and autocomplete return a blended result set to be shown in the typeahead interface.

### Verification
Once you have the tasks ready we provide tests to verify if the result set has blended results for known queries.
