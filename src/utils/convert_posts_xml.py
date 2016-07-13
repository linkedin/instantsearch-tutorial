"""
Convert posts xml to json
"""
from __future__ import unicode_literals

import argparse
import json

import xmltodict


def run(input_file, output_file, max_lines):
    with open(input_file, 'rb') as f_input:
        with open(output_file, 'wb') as f_output:
            for line_number, line in enumerate(f_input):
                if line_number < 2:
                    continue
                if max_lines and (line_number >= max_lines):
                    break
                if (line_number % 10000) == 0:
                    print 'Done with line: %d' % line_number
                try:
                    output = xmltodict.parse(line)
                except Exception, e:
                    continue
                json_output = dict()
                json_output['@Title'] = output['row'].get('@Title')
                if not json_output['@Title']:
                    continue
                json_output['@Id'] = output['row']['@Id']
                if not json_output['@Id']:
                    continue
                json_output['@Score'] = output['row']['@Score']
                if not json_output['@Score']:
                    continue
                f_output.write(json.dumps(json_output))
                f_output.write('\n')


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--i', action='store', dest='input',)
    arg_parser.add_argument('--o', action='store', dest='output',)
    arg_parser.add_argument('--m', action='store', dest='max_lines', type=int)
    args = arg_parser.parse_args()
    run(input_file=args.input, output_file=args.output,
        max_lines=args.max_lines)


if __name__ == '__main__':
    main()
