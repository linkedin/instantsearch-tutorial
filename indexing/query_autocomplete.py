from __future__ import unicode_literals

import sys
import re
import json
import requests


def create_index():
    url = 'http://localhost:9200/stackoverflowtags'
    requests.delete(url)
    requests.put(url)
    mapping = {
        "tag": {
            "properties": {
                "name": {"type": "string"},
                "suggest": {
                    "type": "completion",
                    "analyzer": "simple",
                    "search_analyzer": "simple"
                }
            }
        }
    }
    url = 'http://localhost:9200/stackoverflowtags/tag/_mapping'
    requests.put(url=url, data=json.dumps(mapping))

def main():
    create_index()
    # Regex for extracting key="value" pairs from XML entries
    rx = re.compile(r'(?P<key>[a-z]+)="(?P<val>[^"]+)"', re.I)
    doc_id = 0
    for line in sys.stdin:
        attrs = dict((m.group('key'), m.group('val')) for m in rx.finditer(line))
        doc_id += 1
        if (doc_id % 100) == 0:
            print 'Done with indexing %d tags' % doc_id
        url = 'http://localhost:9200/stackoverflowtags/tag/' + str(doc_id) + '?refresh=true'
        tag_name = attrs['TagName'].lower()
        weight = int(attrs['Count'])
        data = {
            "name": tag_name,
            "suggest": {
                "input": tag_name,
                "output": tag_name,
                "weight": weight,
            }
        }
        requests.put(url, data=json.dumps(data))

if __name__ == '__main__':
    main()
