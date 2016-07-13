"""
Attempt basic xml parsing
"""
from __future__ import unicode_literals

import argparse
from collections import defaultdict
import json
import xmltodict


def run(input_file, output_file):
    questions = dict()
    with open(input_file) as f_input:
        lines = f_input.read()
        output = xmltodict.parse(lines)
        posts = output['posts']['row']
        answers = defaultdict(list)
        for post_number, post in enumerate(posts):
            if (post_number % 1000) == 0:
                print 'Done with post: ', post_number
            if post['@PostTypeId'] == '1':
                post_id = int(post['@Id'])
                questions[post_id] = post
            else:
                if '@ParentId' in post:
                    parent_id = int(post['@ParentId'])
                    answers[parent_id].append(post)

        for post_id, question in questions.iteritems():
            if answers.get(post_id):
                question['answers'] = answers[post_id]

    with open(output_file, 'wb') as f_output:
        for _, question in questions.iteritems():
            f_output.write(json.dumps(question))
            f_output.write('\n')


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--i', action='store', dest='input',)
    arg_parser.add_argument('--o', action='store', dest='output',)
    args = arg_parser.parse_args()
    run(input_file=args.input, output_file=args.output)


if __name__ == '__main__':
    main()
