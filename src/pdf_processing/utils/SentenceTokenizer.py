import pickle

import nltk

from definitions import abbreviationsStoragePath
from src.pdf_processing.utils.FileUtils import readTextFileLines

nltk.download('punkt')

import os


def loadLatvianAbbreviations():
    """
    Abbreviation taken from below sources:

    http://publications.europa.eu/code/lv/lv-5000300.htm
    http://www.neslimo.lv/client/pme_saisinajumi_list.php?id=saisinajumi
    https://www.letonika.lv/article.aspx?id=abbrME
    """

    latvianAbbreviations = set()

    latvianAbbreviations.update(readTextFileLines(os.path.join(abbreviationsStoragePath, "latvian_abbreviations.txt")))
    latvianAbbreviations.update(readTextFileLines(os.path.join(abbreviationsStoragePath, "europa.txt")))
    latvianAbbreviations.update(readTextFileLines(os.path.join(abbreviationsStoragePath, "neslimo.txt")))

    latvianAbbreviations = [x.lower().strip() for x in latvianAbbreviations]
    return set(latvianAbbreviations)


def createPunktPatameters():
    extra_abbreviations = loadLatvianAbbreviations()
    sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentence_tokenizer._params.abbrev_types.update(extra_abbreviations)
    # •
    # print(sentence_tokenizer._params.abbrev_types)
    return sentence_tokenizer


SENTENCE_SPLITTER = createPunktPatameters()


def loadCustomPunkt(punkt_pickle):
    with open(os.path.dirname(os.path.abspath(__file__)) + "/" + punkt_pickle, mode='rb') as fin:
        return pickle.load(fin)


SENTENCE_SPLITTER_CUSTOM = loadCustomPunkt("latvianPunkt.pickle")
