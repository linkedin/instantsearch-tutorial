import json
import web
import requests

urls = ('/search', 'Search')
LOCAL_HOST = 'http://localhost:9200'
INDEX_NAME = 'stackoverflow'
FIELD_NAME = 'posts'
NUM_TO_RETRIEVE = 100
NUM_TO_CUSTOM_SCORE = 10


def construct_custom_scoring_query(raw_query):
    """
    TODO: this doesn't work and not sure why
    currently overfetch and score later
    """
    query = {
        "query": {
            "function_score": {
                "boost_mode": "replace",
                "query": {
                    "match": {
                        "name": {"query": raw_query, "operator": "and"}
                    }
                },
                "script_score": {
                    "script": "doc[\"popularity\"].value"
                }
            }
        }
    }
    return query


def construct_simple_query(raw_query, num_docs):
    """docstring for fname"""
    query = {
        "query": {
            "match": {
                "name": {"query": raw_query, "operator": "and"}
            }
        },
        "size": num_docs,
    }
    return query


class Search:
    def _makeSuggestion(self, tag):
        return {"text": tag,
                "type": "suggestion",
                "href": "http://stackoverflow.com/questions/tagged/" + tag.lower()
               }

    def getQuerySuggestions(self, query):
        # TODO implement me
        return [
                self._makeSuggestion("java"),
                self._makeSuggestion("javascript"),
                self._makeSuggestion("jquery")
               ]

    def getInstantResults(self, query):
        url = LOCAL_HOST + '/' + INDEX_NAME + '/' + FIELD_NAME + '/_search'
        query = construct_simple_query(raw_query=query,
                                       num_docs=NUM_TO_RETRIEVE)
        response = requests.get(url=url, data=json.dumps(query))
        output = response.json()
        hits = output.get('hits')
        response = []
        if hits:
            hits = hits.get('hits')
            for hit in hits:
                source = hit['_source']
                post_id = hit['_id']
                if source:
                    text = source.get('name')
                    score = source.get('popularity')
                    if text:
                        response.append({'text': text,
                                         'post_id': post_id,
                                         'score': score,
                                         'type': 'instant',
                                         'href': 'http://stackoverflow.com/questions/' + post_id
                                        })
            # sort the output by score, this is custom ranking
            response.sort(key=lambda x: x['score'], reverse=True)
        return response[:NUM_TO_CUSTOM_SCORE]

    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        params = web.input()
        query = params['q']
        query_suggestions = self.getQuerySuggestions(query)
        instant_results = self.getInstantResults(query)
        final_results = query_suggestions + instant_results
        return json.dumps(final_results)


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
