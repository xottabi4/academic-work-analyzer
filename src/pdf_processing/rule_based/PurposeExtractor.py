import re

from src.pdf_processing.utils.SentenceTokenizer import SENTENCE_SPLITTER


def isPurposeSentence(sentence):
    return re.search("mērķis", sentence, re.IGNORECASE)


def extractPurpose(abstract):
    abstractSentences = SENTENCE_SPLITTER.tokenize(abstract)
    for idx, sentence in enumerate(abstractSentences):
        if isPurposeSentence(sentence):
            return idx, sentence.strip()
