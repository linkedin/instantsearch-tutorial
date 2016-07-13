"""
Test instant search indexing
"""
import json
import requests

LOCAL_HOST = 'http://localhost:9200'
INDEX_NAME = 'stackoverflow'
FIELD_NAME = 'posts'
NUM_TO_RETRIEVE = 100
NUM_TO_CUSTOM_SCORE = 10
MAX_QUERY_AUTOCOMPLETE_RESULTS = 3


def construct_simple_query(raw_query, num_docs):
    query = {
        "query": {
            "match": {
                "name": {"query": raw_query, "operator": "and"}
            }
        },
        "size": num_docs,
    }
    return query


def test_indexing(query):
    url = LOCAL_HOST + '/' + INDEX_NAME + '/' + FIELD_NAME + '/_search'
    query = construct_simple_query(raw_query=query,
                                   num_docs=NUM_TO_RETRIEVE)
    response = requests.get(url=url, data=json.dumps(query))
    output = response.json()
    hits = output.get('hits')
    if hits is None:
        print 'INDEXING test failed, no hits returned'
        return
    total = hits.get('total', 0)
    if total < 1:
        print 'INDEXING test failed, no hits returned'
        return
    print 'INDEXING TEST PASSED'


def test_query_autocomplete(query):
    url = 'http://localhost:9200/stackoverflowtags/_suggest'
    data = {
        "tag-suggest": {
            "text": query,
            "completion": {
                "field": "suggest"
            }
        }
    }
    response = requests.get(url=url, data=json.dumps(data))
    if response.status_code != 200:
        print 'Did not get response from elasticsearch, TEST FAILED'
        return
    output = response.json()
    try:
        results = output['tag-suggest'][0]['options']
    except Exception, _:
        print 'Response seems off, did you set the right ' \
              'index name?, TEST FAILED'
        return
    if len(results) < 1:
        print 'Response seems off, did you set the right ' \
              'index name?, TEST FAILED'
        return
    text = results[0]['text']
    if text != query:
        print 'Response seems off, did you set the right ' \
              'index name?, TEST FAILED'
        return
    print 'QUERY AUTOCOMPLETE TEST PASSED'


def main():
    test_query_autocomplete(query='.net')
    test_indexing(query='how do i calculate some')


if __name__ == '__main__':
    main()
