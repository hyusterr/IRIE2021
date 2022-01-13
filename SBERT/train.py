#!usr/bin/python3
# encoding: utf-8

import sys
import click
import random
from pathlib import Path
from sentence_transformers import SentenceTransformer, InputExample, losses, evaluation
from torch.utils.data import DataLoader
from itertools import combinations

def prepare_data(train_csv, doc_dir, query_dir):

    with open(train_csv) as f:
        raw_data = [i.strip().split(',') for i in f.readlines()[1:]]
        raw_data = {i[0]: i[1].split() for i in raw_data}

    all_doc_nos = []
    for child in Path(doc_dir).iterdir():
        if child.is_file():
            all_doc_nos.append(child)

    
    train_examples, rerank_dev_set = [], []
    for qid, doc_ids in raw_data.items():
        
        # process query and doc
        with (Path(query_dir) / Path(qid)).open() as f:
            query_text = f.read()
        
        doc_texts = []
        for doc_id in doc_ids:
            with (Path(doc_dir) / Path(doc_id)).open() as f:
                doc_text = f.read()
                doc_texts.append(doc_texts)
            example = InputExample(texts=[query_text, doc_text])
            train_examples.append(example)
        
        # negative sample for finetune validation
        neg_data = random.choices(all_doc_nos, k=100)
        neg_texts = [d.open().read() for d in neg_data if d.stem not in doc_ids]
        rerank_dev_set.append({'query': query_text, 'positive': doc_texts, 'negative': neg_texts})
        
        '''
        for doc1, doc2 in combinations(doc_texts, 2):
            train_examples.append(InputExample(texts=[doc1, doc2])) # label=0.8))
        '''

    random.shuffle(train_examples)

    print('# of train examples', len(train_examples))
    return train_examples, rerank_dev_set

def callback(score, epoch, steps):
    print(f'score: {score}; epoch: {epoch}; steps: {steps}')


@click.command()
@click.option('--train_ans', default='train_ans.csv')
@click.option('--model_name', '-m', default='allenai/scibert_scivocab_cased')
@click.option('--query_dir', '-qd', help='path contain all query text file and control the grantuality')
@click.option('--doc_dir', '-dd', help='path contain all doc text file and control the grantuality')
@click.option('--model_save_path', default='SBERT/scibert')
@click.option('--batchsize', '-bs', default=16)
@click.option('--learning_rate', '-lr', default=1e-5)
@click.option('--epoch', '-e', default=5)
def train(model_name, query_dir, doc_dir, model_save_path, train_ans, batchsize, learning_rate, epoch):
    
    model = SentenceTransformer(model_name, device='cuda')
    all_examples, rerank_dev_set = prepare_data(train_ans, doc_dir, query_dir)

    train_dataloader = DataLoader(all_examples, shuffle=True, batch_size=batchsize)
    train_loss = losses.MultipleNegativesRankingLoss(model=model)
    evaluator = evaluation.RerankingEvaluator(rerank_dev_set, batch_size=batchsize)

    model.fit(train_objectives=[(train_dataloader, train_loss)], 
              epochs=epoch, 
              output_path=model_save_path, 
              show_progress_bar=True,
              checkpoint_save_total_limit=10,
              evaluator=evaluator,
              callback=callback,
              save_best_model=True)


if __name__ == '__main__':
    train()
