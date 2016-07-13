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
    # TODO: Write the index settings json. This will include number
    # of shards and field analysis strategy
    index_settings = {}

    url = LOCAL_HOST + '/' + INDEX_NAME
    requests.put(url=url, data=json.dumps(index_settings))

    # TODO: Setup the index mappings by specifying field properties,
    # analyzers and type
    index_mapping = {}

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
