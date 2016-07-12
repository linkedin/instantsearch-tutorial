from __future__ import unicode_literals

import argparse
import json
import requests
import xmltodict


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


def run(input_file):
    create_index()
    with open(input_file, 'rb') as f_input:
        doc = xmltodict.parse(f_input.read())
        rows = doc['tags']['row']
        for row_number, row in enumerate(rows):
            if (row_number % 1000) == 0:
                print 'Done with indexing: %d posts' % row_number
            url = 'http://localhost:9200/stackoverflowtags/tag/' + \
                  str(row_number+1) + '?refresh=true'
            tag_name = row['@TagName'].lower()
            weight = int(row['@Count'])
            data = {
                "name": tag_name,
                "suggest": {
                    "input": tag_name,
                    "output": tag_name,
                    "weight": weight,
                }
            }
            requests.put(url, data=json.dumps(data))


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--i', action='store', dest='input', )
    args = arg_parser.parse_args()
    run(input_file=args.input)


if __name__ == '__main__':
    main()
