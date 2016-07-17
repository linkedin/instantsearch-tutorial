"""
Test instant search indexing
"""
import requests


def test_backend(query):
    url = 'http://localhost:8080/search?q=' + query
    response = requests.get(url)
    if response.status_code != 200:
        print 'Did not get response from elasticsearch, TEST FAILED'
        return
    json_results = response.json()
    if len(json_results) < 2:
        print 'Did not get adequate response from elasticsearch, TEST FAILED'
        return
    found_suggestion = False
    found_instant_result = False
    for result in json_results:
        result_type = result.get('type')
        if result_type == 'suggestion':
            found_suggestion = True
        if result_type == 'instant':
            found_instant_result = True
        if found_suggestion and found_instant_result:
            break

    if found_instant_result and found_suggestion:
        print 'TEST PASSED'
    else:
        print 'Did not get adequate response from elasticsearch, TEST FAILED'


if __name__ == '__main__':
    test_backend("python")
