"""
Very simple reproduction of code here:
https://www.elastic.co/guide/en/elasticsearch/guide/current/_index_time_search_as_you_type.html
"""
from __future__ import unicode_literals

import argparse
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


def run(input_file, max_lines):
    create_index()
    # samples
    url = LOCAL_HOST + '/' + INDEX_NAME + '/' + FIELD_NAME
    with open(input_file, 'rb') as f_input:
        for line_number, line in enumerate(f_input):
            if (line_number % 1000) == 0:
                print 'Done with indexing: %d posts' % line_number
            if max_lines and (line_number >= max_lines):
                break
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


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--i', action='store', dest='input', )
    arg_parser.add_argument('--m', action='store', dest='max_lines', type=int)
    args = arg_parser.parse_args()
    run(input_file=args.input, max_lines=args.max_lines)


if __name__ == '__main__':
    main()
