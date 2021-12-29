#!usr/bin/python3
# encoding: utf-8

import sys
import click
import spacy
from pathlib import Path
from tqdm.auto import tqdm
from scispacy.abbreviation import AbbreviationDetector

spacy.prefer_gpu()

# en_core_sci_sm performs already well
nlp = spacy.load("en_core_sci_sm")
# Add the abbreviation pipe to the spacy pipeline.
# nlp.add_pipe("abbreviation_detector")

def doc2ner(text: str, nlp=nlp) -> str:
    doc = nlp(text)
    ners = " ".join([ent.text for ent in doc.ents])
    # print(" ".join([abrv._.long_form for abrv in doc._.abbreviations]))
    return ners


def main(directory):
    parent_path = Path(directory)
    for child in tqdm(parent_path.iterdir()):
        if child.is_file():
            with child.open() as f: text = f.read()
            ner_text = doc2ner(text)
            save_dir = parent_path / 'NER'
            if not save_dir.exists():
                save_dir.mkdir()
            filename = child.name
            save_path = save_dir / filename
            save_path.write_text(ner_text.strip(), encoding='utf-8')


if __name__ == '__main__':
    main(sys.argv[1])
