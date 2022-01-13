#!usr/bin/python3
# encoding: utf-8

import click
from pathlib import Path
from typing import List, Dict
from tqdm.auto import tqdm
from sentence_transformers import SentenceTransformer, util


def prepare_data(csv_file: str) -> Dict[str, List[str]]:

    with open(csv_file) as f:
        data = [i.strip().split(',') for i in f.readlines()]
    data = {i[0]: i[1].split()[:100] for i in data[1:]}

    return data


def get_docs(model: SentenceTransformer, 
             doc_dir: str, doc_lst: List[str], 
             query_dir: str, query_no: str) -> str:
    '''
    lst: file contain list of file no, but not file path
    
    return: string to write in submission.csv (top50)
    qid,docid docid docid ..
    '''
    doc_dir = Path(doc_dir)
    docs = []
    for doc in doc_lst:
        doc = doc_dir / Path(doc)
        with open(doc, 'r') as f:
            docs.append(f.read())
    corpus_embeddings = model.encode(docs)

    query_filename = Path(query_dir) / Path(query_no)
    with query_filename.open() as f:
        query_embedding = model.encode(f.read())
    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=50)[0]
    result = f"{query_no},{' '.join([doc_lst[hit['corpus_id']] for hit in hits])}\n"

    return result


@click.command()
@click.option('--model_name', '-m', default='allenai/scibert_scivocab_cased')
@click.option('--query_dir', '-qd', help='path contain all query text file and control the grantuality')
@click.option('--doc_dir', '-dd', help='path contain all doc text file and control the grantuality')
@click.option('--first_result', '-fr', help='csv file for first-stage retrieval')
@click.option('--output_csv', '-o', default='submission.csv')
def inference(model_name, query_dir, doc_dir, first_result, output_csv):
    
    model = SentenceTransformer(model_name, device='cuda')
    data = prepare_data(first_result)
    query_dir = Path(query_dir)
    
    output = open(output_csv, 'w')
    output.write('topic,doc\n')
    for qid, doc_list in tqdm(data.items()):
        result = get_docs(model, doc_dir, doc_list, query_dir, qid)
        output.write(result)
    output.close()


if __name__ == '__main__':
    inference()
