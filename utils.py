#!usr/bin/python3
# encoding: utf-8

# TODO: use Pathlib
# TODO: create venv for test codes
# TODO: write code in clean way
# TODO: familiar with git
import sys
import xml.etree.ElementTree as ET
# import xmltodict

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

    for child in root:
        print(child.tag)
        print(ET.tostring(child, encoding='utf-8', method='text'))


if __name__ == '__main__':
    read_xml(sys.argv[1])



