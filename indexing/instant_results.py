"""
Very simple reproduction of code here:
https://www.elastic.co/guide/en/elasticsearch/guide/current/_index_time_search_as_you_type.html
"""
from __future__ import unicode_literals

import sys
import json
import requests

LOCAL_HOST = 'http://localhost:9200'
TITLE_KEY = '@Title'
INDEX_NAME = 'stackoverflow'
FIELD_NAME = 'posts'


def create_index():
    # Delete the index if it exists
    url = LOCAL_HOST + '/' + INDEX_NAME
    requests.delete(url)

    # Recreate the index with our choice of analyzer
    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "analysis": {
                "filter": {
                    "autocomplete_filter": {
                        "type": "edge_ngram",
                        "min_gram": 1,
                        "max_gram": 20
                    }
                },
                "analyzer": {
                    "autocomplete": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "autocomplete_filter"
                        ]
                    }
                }
            }
        }
    }
    url = LOCAL_HOST + '/' + INDEX_NAME
    requests.put(url=url, data=json.dumps(index_settings))

    # Set up field mappings
    index_mapping = {
        FIELD_NAME: {
            "properties": {
                "name": {
                    "type": "string",
                    "analyzer": "autocomplete",
                    "search_analyzer": "standard",
                },
                "popularity": {
                    "type": "float",
                    "index": "no"
                }
            }
        }
    }
    url = LOCAL_HOST + '/' + INDEX_NAME + '/' + FIELD_NAME + '/_mapping'
    requests.put(url=url, data=json.dumps(index_mapping))


def main():
    create_index()
    url = LOCAL_HOST + '/' + INDEX_NAME + '/' + FIELD_NAME
    line_number = 0
    for line in sys.stdin:
        line_number += 1
        if (line_number % 1000) == 0:
            print 'Done with indexing %d posts' % line_number
        current_entry = json.loads(line)
        current_title = current_entry.get(TITLE_KEY)
        if not current_title:
            continue
        post_id = current_entry.get('@Id', -1)
        new_url = url + '/' + post_id
        popularity = current_entry.get('@Score', 0)
        data = {
            'name': current_title,
            'popularity': float(popularity),
        }
        requests.put(url=new_url, data=json.dumps(data))
    print 'INDEXED: %d documents' % line_number

if __name__ == '__main__':
    main()
