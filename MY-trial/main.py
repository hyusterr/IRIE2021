#!usr/bin/bash
# encoding: utf-8

import re
import glob
import nltk
import click
import string
import unicodedata
import inflect
import contractions
import pandas as pd
import xml.etree.ElementTree as ET
from pathlib import Path
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from bs4 import BeautifulSoup


def parse_xml_file(file_name: str) -> pd.DataFrame:
    xml_data = open(file_name, 'r').read()
    root = ET.XML(xml_data)
    data = []
    cols = []

    for i, child in enumerate(root):
        data.append(child.text)
        cols.append(child.tag)

    df = pd.DataFrame(data).T
    df.columns = cols
    df["qid"] = file_name.split("/")[-1]

    return df


def dir2df_query(file_path: str) -> pd.DataFrame:
    file_path = Path(file_path)
    output = []
    for child in file_path.iterdir():
        if child.isfile():
            tmp_df = parse_xml_file(child.name)
            output.append(tmp_df)
    return pd.concat(output)

@click.command()
@click.option('--train_query', default='./train_query/')
@click.option('--test_query', default='./test_query/')
def main(train_query, test_query):
    
    train_query_df = dir2df_query(train_query)
    test_query_df  = dir2df_query(test_query)





