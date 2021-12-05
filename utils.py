#!usr/bin/python3
# encoding: utf-8

# TODO: use Pathlib
# TODO: create venv for test codes
# TODO: write code in clean way
# TODO: familiar with git
import sys
import xmltodict

def read_xml(filename):
    '''
    input:
    - filename: str

    output:
    - ouptut: dict
          if the file is query, the keys will be note, description, summary
          if the file is doc, the keys will be abstract and body
    '''
    with open(filename, 'r') as f:
        data = f.read()

    output = xmltodict.parse(data, item_depth=, item_callback=)
    print(output)

if __name__ == '__main__':
    read_xml(sys.argv[1])



