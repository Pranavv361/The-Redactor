#Libraries Used
import argparse
import os
import glob
import spacy
import re

#Loading spacy model
nlp = spacy.load('en_core_web_sm')

#Redact names
def redact_names(text):
    doc = nlp(text)
    redacted_names = []
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            redacted_text = Redactcharacter * len(ent.text)
            text = text.replace(ent.text, redacted_text)
            redacted_names.append((ent.text, ent.start_char, ent.end_char))
    return text, redacted_names


def main(fileExtension, output_folder, stats, redactnames, redactdates, redactphones, redactgenders, redactaddress):
    filename = []
    text = ""
    #Reading multiple files with same File Extension
    for pattern in fileExtension:
        for file_name in glob.glob(pattern):
            filename.append(file_name)
            redacted_terms = []
            with open(file_name,'r') as f:
                text = f.read()
                if redactnames:
                        text, redacted_names = redact_names(text)
                        if redacted_names:
                                redacted_names.append(('names', len(redacted_names)))
                                redacted_terms.extend(redacted_names)