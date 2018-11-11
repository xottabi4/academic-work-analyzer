import re

from db.dbUtils import createPurpose, ABSTRACT_DOCUMENT, ID_DOCUMENT


def isPurposeSentence(sentence):
    return re.search("mērķis", sentence, re.IGNORECASE)


def extractPurpose(abstract):
    abstractSentences = abstract.split(".")
    for sentence in abstractSentences:
        if isPurposeSentence(sentence):
            return sentence.strip()


def reextractPurposes(collection):
    for record in collection.find({ABSTRACT_DOCUMENT: {"$ne": None}}):
        purpose = extractPurpose(record[ABSTRACT_DOCUMENT])
        if not purpose:
            print("Couldn't find purpose in abstract of document: {}".format(record[ID_DOCUMENT]))
            continue
        print(purpose)
        record.update(createPurpose(purpose))
        collection.save(record)
