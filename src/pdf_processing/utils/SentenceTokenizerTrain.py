import pickle

import nltk
from nltk.tokenize.punkt import PunktTrainer

from src.db.Database import database
from src.db.DbUtils import ABSTRACT_DOCUMENT


def trainSentenceTokenizer():
    """
    Method trains custom sentence tokenizer using punk.
    At the moment it preforms worse then plain english one (most likely due to not that much data)
    """
    collection = database["crawled-data"]

    text = ""
    for record in collection.find({ABSTRACT_DOCUMENT: {"$ne": None}}):
        text += record[ABSTRACT_DOCUMENT] + " "

    trainer = PunktTrainer()
    trainer.INCLUDE_ALL_COLLOCS = True
    trainer.INCLUDE_ABBREV_COLLOCS = True
    trainer.train(text)

    model = nltk.PunktSentenceTokenizer(trainer.get_params())
    with open("latvianPunkt2.pickle", mode='wb') as fout:
        pickle.dump(model, fout, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    trainSentenceTokenizer()
