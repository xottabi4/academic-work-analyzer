import re

from db.DbUtils import createPurpose, ABSTRACT_DOCUMENT, ID_DOCUMENT
from pdf_processing.utils.SentenceTokenizer import SENTENCE_SPLITTER


def isPurposeSentence(sentence):
    return re.search("mērķis", sentence, re.IGNORECASE)


def extractPurpose(abstract):
    abstractSentences = SENTENCE_SPLITTER.tokenize(abstract)
    for idx, sentence in enumerate(abstractSentences):
        if isPurposeSentence(sentence):
            return idx, sentence.strip()


def reextractPurposes(collection):
    for record in collection.find({ABSTRACT_DOCUMENT: {"$ne": None}}):
        purpose = extractPurpose(record[ABSTRACT_DOCUMENT])
        if not purpose:
            print("Couldn't find purpose in abstract of document: {}".format(record[ID_DOCUMENT]))
            continue
        print(purpose)
        record.update(createPurpose(purpose))
        collection.save(record)
