# python -m -> calling package.subpackage.__main__.py from commandline
python3 -m pyserini.search --topics $1 \
                           --index $2 \
                           --output run.sample.txt \
                           --output-format msmarco \
                           --hits 50 \
                           --bm25 \
                           --b 0.75 \
                           --k1 1.2 
