# IRIE2021
## pyserini
adapt code from waterloo's pyserini package for bm25 search, follow these steps:  
- save the docs into JSON format; query to tsv format  
- build index with `build_index.sh`  
`bash build_index.sh path/contain/doc/jsons path/for/save/indexes`  
- search with `search.sh`  
`bash search.sh path/to/query.tsv path/to/indexes`  
- post-process to kaggle format  
`python3 run.sample.txt > submission.csv`

## scispacy
adapt allenai's scispacy to do medical-bio NER
- build a new directory named NER inside each file directory and save the NER result as new document 
`python3 scispacy/doc2ner.py /path/to/document/directory`

## SBERT 
use sentence-transformers package to do reranker training 
- finetune BERT checkpoint with siamese network
`python3 SBERT/train.py -qd path/to/train_query/description/ \
                        -dd path/to/doc/abstract/ \
                        -bs batch size \
                        --model_save_path path/to/saving/diretory \
                        -e number of epochs \
                        -m huggingface/pretrain/model/name` \
- inference on first-stage retrieval outcome
`python3 SBERT/inference.py -m model/saving/path \
                            -qd test_query/description/ \
                            -dd doc/abstract/ \
                            -fr first/stage/output/csv \
                            -o submission.csv` 
