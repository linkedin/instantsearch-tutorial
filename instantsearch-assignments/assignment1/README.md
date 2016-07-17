# Assignment 1
In this assignment we will be aiming for accomplishing setting up a search index for instant search results and query autocomplete. We will be using the elasticsearch instance that we started in Assignment 0 for holding our search index. The assignment is divided into two parts which are presented below.

### End Result
At the end of this assignment you should have two indicies one for instant results and one for query autocomplete setup and verified.

### Dataset
The dataset that we will be working today has been taken from the stackoverflow data dump. The dataset has been simiplified for readability and to allow users to focus on retrieval and ranking aspects. The dataset is divided into two files:
* **Tags_small.xml** - This file contains the information of the tags, tag post id and count of posts associated with the tag.
```xml
<?xml version="1.0" encoding="utf-8"?>
<tags>
  <row Id="1" TagName=".net" Count="233796" ExcerptPostId="3624959" WikiPostId="3607476" />
</tags>  
```

* **posts_small.json** - This file contains one post per line along with the id, title and a [score](http://meta.stackexchange.com/questions/229255/what-is-the-score-of-a-post) as voted by the users.
```json
{"@Score": "358", "@Id": "4", "@Title": "When setting a form's opacity should I use a decimal or double?"}
```
### Elastic Search Basics

1. **Index Settings** - As a first step we will be setting up our search index to hold the stackoverflow dataset. You will need to set the following settings when building the index. [Configure Analyzers](https://www.elastic.co/guide/en/elasticsearch/guide/current/configuring-analyzers.html) and [Index Settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-update-settings.html)
    * **Number of Shards** - This control how distributed you want your index, the primary reason to this is to limit number of documents on a single host. Given our small dataset a *single* sharded index should suffice.
    * **Analysis** - This is crucial step that determines how string tokens are represented and stored in the inverted index. In this part you need to determine which analyzer suits the best needs for our usecase. You can read about analysis process here [Elasticsearch Analysis](https://www.elastic.co/blog/found-text-analysis-part-1). Given our usercase we recommend use of [edge n-grams analyzer](https://www.elastic.co/blog/found-text-analysis-part-1#using-ngrams-for-advanced-token-searches).

2. **Suggestors** - As a part of building query autocomplete we require indexing tokens into a Finite State Transducer (FST) for finding similar terms. We recommend using the [Completion Suggestor](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters-completion.html) provided by elasticsearch for this usecase. 
    
3. **Index Mapping** - To help elasticsearch index fields with the correct analyzers and understand the data in the field we need to help make it aware of a schema. In this part we utilize our understanding of the fields to specify how we want them to be represented in the index and be searched. Read [here](https://www.elastic.co/blog/found-elasticsearch-mapping-introduction) to see how to create an index mapping in elasticsearch       

4. **Indexing** - With the index setup you will read the json stackoverflow posts and send it to elasticsearch for indexing. Utilize [this](https://www.elastic.co/guide/en/elasticsearch/guide/current/index-doc.html) elasticsearch documentation to understand how to index a document.

### Task I
Using the basics of elasticsearch to create an index to store stackoverflow posts. 

### Task II
Similar to Task I create a separate index to store stackoverflow tags.

### Verification
Once you have the tasks ready we provide tests to verify if the data has been indexed correctly. 
