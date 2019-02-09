import pickle

import nltk
import pymongo
from nltk.tokenize.punkt import PunktTrainer

from db.DbUtils import ABSTRACT_DOCUMENT
from definitions import abbreviationsStoragePath
from pdf_processing.utils.FileUtils import readTextFileLines
from properties import DATABASE_NAME, MONGODB_CONNECTION

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
    # print(sentence_tokenizer._params.abbrev_types)
    return sentence_tokenizer


SENTENCE_SPLITTER = createPunktPatameters()


def trainSentenceTokenizer():
    """
    Method trains custom sentence tokenizer using punk.
    At the moment it preforms worse then plain englihs one (most likely due to not that much data)
    """
    database = pymongo.MongoClient(MONGODB_CONNECTION)[DATABASE_NAME]
    collection = database["crawled-data"]

    text = ""
    for record in collection.find({ABSTRACT_DOCUMENT: {"$ne": None}}):
        text += record[ABSTRACT_DOCUMENT] + " "
    # print(text[0:100])
    # text =

    punkt = PunktTrainer()
    punkt.train(text)

    model = nltk.PunktSentenceTokenizer(punkt.get_params())
    with open("latvianPunkt.pickle", mode='wb') as fout:
        pickle.dump(model, fout, protocol=pickle.HIGHEST_PROTOCOL)


def loadCustomPunkt():
    with open(os.path.dirname(os.path.abspath(__file__)) + "/latvianPunkt.pickle", mode='rb') as fin:
        return pickle.load(fin)


SENTENCE_SPLITTER_CUSTOM = loadCustomPunkt()

if __name__ == '__main__':
    trainSentenceTokenizer()
