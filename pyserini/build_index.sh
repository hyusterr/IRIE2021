python3 -m pyserini.index -collection JsonCollection \
                          -generator DefaultLuceneDocumentGenerator \
                          -threads 8 \
                          -input $1 \
                          -index $2 \
                          -storePositions -storeDocvectors -storeRaw
