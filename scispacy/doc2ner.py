#!usr/bin/python3
# encoding: utf-8

import sys
import click
import spacy
from scispacy.abbreviation import AbbreviationDetector

spacy.prefer_gpu()

# en_core_sci_sm performs already well
nlp = spacy.load(sys.argv[2])
# Add the abbreviation pipe to the spacy pipeline.
nlp.add_pipe("abbreviation_detector")

def doc2ner(text: str) -> str:
    doc = nlp(text)
    print(" ".join([ent.text for ent in doc.ents]))

with open(sys.argv[1], 'r') as f:
    text = f.read()
doc2ner(text)
