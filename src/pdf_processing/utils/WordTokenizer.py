import os
import string

import nltk
from nltk.corpus import stopwords

from definitions import stopwordsStoragePath
from pdf_processing.utils.FileUtils import readTextFileLines

nltk.download('stopwords')

STRING_PUNCTUATION = string.punctuation + "–„”“"

_stopWords = set(stopwords.words('english'))

"""
Latvian stopwords retrieved from https://github.com/stopwords-iso/stopwords-lv
"""
_latvianStopWords = set(readTextFileLines(os.path.join(stopwordsStoragePath, "stopwords-lv.txt")))
_stopWords.update(_latvianStopWords)


def removeCommonWordsAndTokenize(sentence):
    rawSentence = strip_formatting(sentence)
    return tokenize(rawSentence)


def tokenize(rawSentence):
    sentenceWords = list()
    for word in rawSentence.split():
        if word not in _stopWords:
            sentenceWords.append(word)
    return sentenceWords


def strip_formatting(sentence):
    return sentence \
        .translate(str.maketrans('', '', STRING_PUNCTUATION)) \
        .lower()
