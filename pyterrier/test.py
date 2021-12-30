#!usr/bin/python3
# encoding: utf-8

import click
import pyterrier as pt
import pandas as pd
from pathlib import Path


pt.init()

@click.command()
@click.option('--document_dir', '-d', help='path contain all documents')
@click.option('--index_dir', '-i', help='path for saving terrier-index')
@click.option('--rebuild_index', default=True, help='option for if needed to rebuild index from scratch')
@click.option('--query_dir', '-q', help='path contain all queries')
@click.option('--save_idr', default='./terrier-result')
def terrier_search(document_dir, index_dir, rebuild_index, query_dir, save_dir):

    # build index
    if rebuild_index:
        indexer = pt.FilesIndexer(index_dir, overwrite=True, verbose=True)
        indexref = indexer.index(document_dir)

    index = pt.IndexFactory.of(index_dir)

    # read queries
    query_path = Path(query_dir)
    query_df = []
    for child in query_path.iter_dir()
        if child.is_file():
            with child.open() as f:
                text = f.read()
        query_df.append({'qid': child.name, 'query': text})
    query_df = pd.DataFrame(query_df)
    
    # build retrieval model

    # qe = query expansion
    bm25  = pt.BatchRetrieve(index, wmodel='BM25', controls={'qe': 'on', 'qemodel': 'Bo1'}, num_results=50)
    # tfidf = pt.BatchRetrieve(index, wmodel="TF_IDF")
    # pl2   = pt.BatchRetrieve(index, wmodel='PL2')
    
    # for telescoping
    # pipeline = (bm25 % 100) >> other_model


    # run retrieval experiments
    pt.Experiment(
        retr_systems=[bm25],
        topics=query_dir,
        save_dir=save_dir
    )
    
    # retrieve results
    bm25_result = bm25.transform(query_df)

