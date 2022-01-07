#!usr/bin/python3
# encoding: utf-8

import nltk
import contractions
import inflect
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from bs4 import BeautifulSoup
import re, string, unicodedata


class Preprocessing():
    def __init__(self, data: str):
        self.data = data

    def html_remover
