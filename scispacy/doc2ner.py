#!usr/bin/python3
# encoding: utf-8

import click
import spacy
from scispacy.abbreviation import AbbreviationDetector

spacy.prefer_gpu()

nlp = spacy.load("en_core_sci_sm")
# Add the abbreviation pipe to the spacy pipeline.
nlp.add_pipe("abbreviation_detector")


