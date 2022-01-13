# IRIE2021
## notebook
contain our experiments related to pyterrier, including our highest leaderboard results
My teammate MY ask me to delete the notebooks cause he doesn't want to make it public, I'll reproduce his result with pyterrier when I have time

## pyserini
adapt code from waterloo's pyserini package for bm25 search, follow these steps:  
- save the docs into JSON format; query to tsv format  
- build index with `build_index.sh`  
```bash
bash pyserini/build_index.sh path/contain/doc/jsons path/for/save/indexes
```  
- search with `search.sh`  
```bash
bash pyserini/search.sh path/to/query.tsv path/to/indexes
```
- post-process to kaggle format  
```bash
python3 pyserini/post-process.py run.sample.txt > submission.csv
```

## pyterrier
adapt pyterrier to build retrival system, only for testing, detailed usage is in .ipynb files
- usage
```bash
python3 pyterrier/test.py -d path/contain/all/documents \
                          -i path/for/saving/terrier-index \
                          --rebuild_index option/for/if/needed/to/rebuild/index/from/scratch true or false
                          -q path/contain/all/queries
                          --save_dir path/for/saving/results
                          --output_csv submission.csv
```

## scispacy
adapt allenai's scispacy to do medical-bio NER  
- build a new directory named NER inside each file directory and save the NER result as new document  
```bash
python3 scispacy/doc2ner.py /path/to/document/directory
```

## SBERT 
use sentence-transformers package to do reranker training  
- finetune BERT checkpoint with siamese network  
```bash
python3 SBERT/train.py -qd path/to/train_query/description/ \
                       -dd path/to/doc/abstract/ \
                       -bs batch size \
                       --model_save_path path/to/saving/diretory \
                       -e number of epochs \
                       -m huggingface/pretrain/model/name
```
- first down load model checkpoint at https://drive.google.com/file/d/16FxQ7yeiB-en4mMPmmkxZDCcDzhzOV-I/view?usp=sharing and unzip
- inference on first-stage retrieval outcome
```bash
python3 SBERT/inference.py -m model/saving/path \
                           -qd test_query/description/ \
                           -dd doc/abstract/ \
                           -fr first/stage/output/csv \  
                           -o submission.csv
```
