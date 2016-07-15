"""
Very simple reproduction of code here:
https://www.elastic.co/guide/en/elasticsearch/guide/current/_index_time_search_as_you_type.html
"""
from __future__ import unicode_literals

import argparse
from elasticsearch import Elasticsearch
import json
import requests
import time

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


def run_bulk_request(input_file, max_lines):
    """
    ATM, this is under test, so do not use
    use bulk api from elasticsearch. This would be much faster,
    but needs tuning
    :param input_file: input json file
    :param max_lines: maximum lines to process
    :return: none
    """
    start_time = time.clock()
    create_index()
    es_host = {"host": "localhost", "port": 9200}
    es = Elasticsearch(hosts=[es_host], timeout=30)
    bulk_data = list()
    max_record_per_request = 500000
    current_total_records = 0
    with open(input_file, 'rb') as f_input:
        for line_number, line in enumerate(f_input):
            if max_lines and (line_number >= max_lines):
                break
            current_entry = json.loads(line)
            current_title = current_entry.get(TITLE_KEY)
            if not current_title:
                continue
            post_id = current_entry.get('@Id', -1)
            popularity = current_entry.get('@Score', 0)
            data = {
                'name': current_title,
                'popularity': float(popularity),
            }
            op_data = {
                "index": {
                    "_index": INDEX_NAME,
                    "_id": post_id,
                    "_type": FIELD_NAME,
                }
            }
            bulk_data.append(op_data)
            bulk_data.append(data)
            current_total_records += 1
            if current_total_records >= max_record_per_request:
                end_time = time.clock()
                elapsed = end_time - start_time
                es.bulk(index=INDEX_NAME, body=bulk_data)
                bulk_data = list()
                current_total_records = 0
                print 'INDEXED: %d documents elapsed ' \
                      '%2.2f seconds' % (line_number, elapsed)

        if current_total_records > 0:
            es.bulk(index=INDEX_NAME, body=bulk_data)
        end_time = time.clock()
        elapsed = end_time - start_time
        print 'INDEXED: %d documents elapsed ' \
              '%2.2f seconds' % (line_number, elapsed)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--i', action='store', dest='input', )
    arg_parser.add_argument('--m', action='store', dest='max_lines', type=int)
    args = arg_parser.parse_args()
    run_bulk_request(input_file=args.input, max_lines=args.max_lines)


if __name__ == '__main__':
    main()
