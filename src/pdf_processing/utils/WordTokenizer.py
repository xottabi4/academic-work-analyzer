import os
import string

import nltk
from nltk.corpus import stopwords

from definitions import stopwordsStoragePath
from pdf_processing.utils.FileUtils import readTextFileLines

SKAITLIS = "SKAITLIS"

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
    words = tokenize(rawSentence)
    return processWords(words)


def processWords(words):
    words = substituteNumbers(words)
    words = removeWordsWithLessThenTwoChars(words)
    return list(words)


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


def substituteNumbers(words):
    for word in words:
        if isNumber(word):
            yield SKAITLIS
        else:
            yield word


def removeWordsWithLessThenTwoChars(words):
    for word in words:
        if len(word) > 1:
            yield word


def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
