from random import choice

from db.DbUtils import ABSTRACT_DOCUMENT, PURPOSE_DOCUMENT
from db.Database import regexDatabase, allDataDatabase, trainDatabase, testDatabase
from pdf_processing.doc2vec.Label import Label
from pdf_processing.utils.SentenceTokenizer import SENTENCE_SPLITTER
from pdf_processing.utils.WordTokenizer import removeCommonWordsAndTokenize


def prepareDatasets(database):
    createAllValidData(regexDatabase, allDataDatabase)
    createTrainTestData(allDataDatabase, trainDatabase, testDatabase)


def createAllValidData(regexDatabase, allDataDatabase):
    allData = regexDatabase.find({ABSTRACT_DOCUMENT: {"$ne": None}})
    createDataSet(allData, allDataDatabase)


def createTrainTestData(allDataDatabase, trainDatabase, testDatabase):
    trainData, testData = trainTestSplit(allDataDatabase)

    for data in trainData:
        trainDatabase.save(data)
    print(trainDatabase.count_documents({}))
    for data in testData:
        testDatabase.save(data)
    print(testDatabase.count_documents({}))


def trainTestSplit(allDataDatabase, testPercent=0.25):
    howManyNumbers = int(round(testPercent * allDataDatabase.count_documents({})))
    return allDataDatabase.find()[howManyNumbers:], allDataDatabase.find()[:howManyNumbers]


def createDataSet(trainData, trainDatabase):
    for record in trainData:
        abstractSentences = SENTENCE_SPLITTER.tokenize(record[ABSTRACT_DOCUMENT])

        if PURPOSE_DOCUMENT in record:
            sentenceId = record[PURPOSE_DOCUMENT][0]
            del abstractSentences[sentenceId]
            sentence = record[PURPOSE_DOCUMENT][1]
            sentenceSplitted = removeCommonWordsAndTokenize(sentence)
            trainDatabase.save({"token": [Label.PURPOSE.value], "sentence": sentenceSplitted})

        try:
            _, abstractSentence = choice(list(enumerate(abstractSentences)))
            print(abstractSentence)
            trainDatabase.save(
                {"token": [Label.OTHER.value], "sentence": removeCommonWordsAndTokenize(abstractSentence)})
        except:
            print("Empty list")


if __name__ == '__main__':
    prepareDatasets()
