#!usr/bin/python3
# encoding: utf-8

import re
import click
import pyterrier as pt
import pandas as pd
from pathlib import Path
from typing import List, Dict


pt.init()

def dataframe_to_submission_csv(df: pd.DataFrame, out_name: str) -> Dict[str, List]:
    
    output_dict = dict()
    for name, group in df.groupby('qid'):
        result = group['docno'].tolist()
        output_dict[name] = result

    with open(out_name, 'w') as f:
        f.write('topic,doc\n')
        for qid, docnos in output_dict.items():
            f.write(f'{qid},{" ".join([str(i) for i in docnos])}\n')

    return result


def prepare_doc_to_df(document_dir: str) -> pd.DataFrame:
    document_dir = Path(document_dir)
    output = []
    for child in document_dir.iterdir():
        if child.is_file():
            with child.open() as f:
                output.append({'docno': child.stem, 'text': f.read()})
    return pd.DataFrame(output)
                

@click.command()
@click.option('--document_dir', '-d', help='path contain all documents')
@click.option('--index_dir', '-i', help='path for saving terrier-index')
@click.option('--rebuild_index', default=True, type=bool, help='option for if needed to rebuild index from scratch')
@click.option('--query_dir', '-q', help='path contain all queries')
@click.option('--save_dir', default='./terrier-result')
@click.option('--output_csv', default='submission.csv')
def terrier_search(document_dir, index_dir, rebuild_index, query_dir, save_dir, output_csv):

    # build index
    if rebuild_index:
        doc_df = prepare_doc_to_df(document_dir)
        indexer = pt.DFIndexer(index_dir, overwrite=True, verbose=True)
        indexref = indexer.index(doc_df['text'], doc_df['docno'])

    index = pt.IndexFactory.of(index_dir)

    # read queries
    query_path = Path(query_dir)
    query_df = []
    for child in query_path.iterdir():
        if child.is_file():
            with child.open() as f:
                text = f.read()
                text = re.sub(r'[^\w]', ' ', text) # pyterrier do not stand special symbols in query
            query_df.append({'qid': child.name, 'query': text})
    query_df = pd.DataFrame(query_df)
    
    # build retrieval model

    # qe = query expansion
    # bm25  = pt.BatchRetrieve(index, wmodel='BM25', controls={'qe': 'on', 'qemodel': 'Bo1'}, num_results=50)
    # tfidf = pt.BatchRetrieve(index, wmodel="TF_IDF")
    pl2   = pt.BatchRetrieve(index, wmodel='PL2', controls={'qe': 'on', 'qemodel': 'Bo1'}, num_results=50)
    
    # for telescoping
    # pipeline = (bm25 % 100) >> other_model


    # run retrieval experiments
    '''
    pt.Experiment(
        retr_systems=[bm25],
        topics=query_dir,
        save_dir=save_dir
    )
    '''
    
    # retrieve results
    result = pl2.transform(query_df)
    dataframe_to_submission_csv(result, output_csv)


if __name__ == '__main__':
    terrier_search()
