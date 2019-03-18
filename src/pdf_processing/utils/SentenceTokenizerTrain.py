import pickle

import nltk
import pymongo
from nltk.tokenize.punkt import PunktTrainer

from db.DbUtils import ABSTRACT_DOCUMENT


def trainSentenceTokenizer():
    """
    Method trains custom sentence tokenizer using punk.
    At the moment it preforms worse then plain english one (most likely due to not that much data)
    """
    from properties import DATABASE_NAME, MONGODB_CONNECTION

    database = pymongo.MongoClient(MONGODB_CONNECTION)[DATABASE_NAME]
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
