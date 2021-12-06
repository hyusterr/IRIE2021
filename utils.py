#!usr/bin/python3
# encoding: utf-8

# TODO: use Pathlib
# TODO: create venv for test codes
# TODO: write code in clean way
# TODO: familiar with git
import sys
import xml.etree.ElementTree as ET
from pprint import pprint

# think point: XML information may highlight something, e.g. bold means important
def read_xml(filename):
    '''
    input:
    - filename: str

    output:
    - ouptut: dict
          if the file is query, the keys will be note, description, summary
          if the file is doc, the keys will be abstract and body
    '''

    tree = ET.parse(filename)
    root = tree.getroot()
    output = {child.tag: ET.tostring(child, encoding='utf-8', method='text').decode("utf-8") for child in root}

    return output


if __name__ == '__main__':
    pprint(read_xml(sys.argv[1]))



