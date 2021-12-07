#!usr/bin/python3
# encoding: utf-8

# TODO: use Pathlib
# TODO: create venv for test codes
# TODO: write code in clean way
# TODO: familiar with git
import sys
import xml.etree.ElementTree as ET
from pprint import pprint
from pathlib import Path

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


def chunk_into_pieces(directory):
    '''
    chunk files from doc/train_query/test_query into pieces and save into assigned directory
    input:
    - directory: str

    output:
    - None
    - saving logistic:
        - e.g. doc/3052048 contains file with abstract and body
          save each part to
          doc/abstract/3052048
          doc/body/3052048
    * train_query/11 has xml format problem
    '''
    
    parent_path = Path(directory)
    for child in parent_path.iterdir():
        if child.is_file():
            content_dict = read_xml(child)
            for name, content in content_dict.items():
                save_dir = parent_path / name
                if not save_dir.exists():
                    save_dir.mkdir()
                filename = child.name
                save_path = save_dir / filename
                save_path.write_text(content.strip(), encoding='utf-8')


def calculate_map(answer_csv, prediction_csv):
    '''
    calculate MAP from 2 csv file:
    query_id,doc_id1 doc_id2
    input:
    - answer_csv: str
    - prediction_csv: str

    output:
    - a score between 0 and 1, float
    '''
    with open(answer_csv, 'r') as f:
        answers = [i.strip().split(',') for i in f.readlines()]
        answers = {ans[0]: ans[1].split() for ans in answers}
    with open(prediction_csv, 'r') as f:
        predictions = [i.strip().split(',') for i in f.readlines()]
        predictions = {pred[0]: pred[1].split() for pred in predictions}

    assert len(answers) == len(predictions)

    average_precisions = []
    for key in answers.keys():
        y_true = answers[key]
        y_pred = predictions[key]

        



def build_query_pyserini(directory):
    '''
    transform query into pyserini's format, 
    '''




if __name__ == '__main__':
    calculate_map(sys.argv[1], sys.argv[2])



