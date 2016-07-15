from __future__ import division

import json
import web
import requests

urls = ('/search', 'Search')
LOCAL_HOST = 'http://localhost:9200'
INDEX_NAME = 'stackoverflow'
FIELD_NAME = 'posts'
NUM_TO_RETRIEVE = 100
NUM_TO_CUSTOM_SCORE = 10
MAX_QUERY_AUTOCOMPLETE_RESULTS = 3


def construct_simple_query(raw_query, num_docs):
    """Simple query construction to retrieve results with an and operator"""
    query = {
        "query": {
            "match": {
                "name": {"query": raw_query, "operator": "and"}
            }
        },
        "size": num_docs,
    }
    return query


def get_instant_results(query):
    url = LOCAL_HOST + '/' + INDEX_NAME + '/' + FIELD_NAME + '/_search'
    # TODO: Modify the query here to support fuzzy matching of documents
    query = construct_simple_query(raw_query=query,
                                   num_docs=NUM_TO_RETRIEVE)
    response = requests.get(url=url, data=json.dumps(query))
    time_taken = response.elapsed.microseconds / 1000.0
    print 'Time taken for query: %s : %4.2fms' % (query, time_taken)
    output = response.json()
    hits = output.get('hits')
    response = []
    # TODO: Go through the hits to find out the related tags
    if hits:
        hits = hits.get('hits')
        for hit in hits:
            source = hit['_source']
            post_id = hit['_id']
            if source:
                text = source.get('name')
                score = source.get('popularity')
                if text:
                    href = 'http://stackoverflow.com/questions/' + post_id
                    response.append(
                        {'text': text,
                         'post_id': post_id,
                         'score': score,
                         'type': 'instant',
                         'href': href,
                         })
        # sort the output by score, this is custom ranking
        # TODO: Modify the score here to take into account popularity, tf-idf etc.
        response.sort(key=lambda x: x['score'], reverse=True)
    return response[:NUM_TO_CUSTOM_SCORE]


def make_suggestion(tag):
    return {"text": tag,
            "type": "suggestion",
            "href": "http://stackoverflow.com/questions/tagged/" + tag.lower()
            }


def get_query_suggestions(query):
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
    output = response.json()
    results = output['tag-suggest'][0]['options']
    # arbitrary cut-off for number of results
    max_results = min(MAX_QUERY_AUTOCOMPLETE_RESULTS, len(results))
    text_results = [r['text'] for r in results[:max_results]]
    return [make_suggestion(r) for r in text_results]


class Search:
    def __init__(self):
        pass

    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        params = web.input()
        query = params['q']
        query_suggestions = get_query_suggestions(query)
        instant_results = get_instant_results(query)
        final_results = query_suggestions + instant_results
        return json.dumps(final_results)


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
