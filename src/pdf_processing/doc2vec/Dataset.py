from random import choice

from db.DbUtils import ABSTRACT_DOCUMENT, PURPOSE_DOCUMENT, TASKS_DOCUMENT
from db.Database import regexDatabase, allDataDatabase, trainDatabase, testDatabase, database
from pdf_processing.doc2vec.Label import Label
from pdf_processing.utils.SentenceTokenizer import SENTENCE_SPLITTER
from pdf_processing.utils.WordTokenizer import removeCommonWordsAndTokenize, processWords


def prepareDatasets():
    createAllValidData(regexDatabase, allDataDatabase)
    createTrainTestData(allDataDatabase, trainDatabase, testDatabase)


def createAllValidData(regexDatabase, allDataDatabase):
    allData = regexDatabase.find({ABSTRACT_DOCUMENT: {"$ne": None}})
    createDataSet(allData, allDataDatabase)


def createTrainTestData(allDataDatabase, trainDatabase, testDatabase):
    print(trainDatabase.count_documents({}))
    print(testDatabase.count_documents({}))

    labels = [e.value for e in Label]
    for label in labels:
        trainData, testData = trainTestSplit(allDataDatabase, label)
        # print("Train size: {}, test size: {}".format(len(list(trainData)),len(list(testData))))
        for data in trainData:
            trainDatabase.save(data)
        print(trainDatabase.count_documents({}))
        for data in testData:
            testDatabase.save(data)
        print(testDatabase.count_documents({}))


def trainTestSplit(allDataDatabase, label, testPercent=0.25):
    howManyNumbers = int(round(testPercent * allDataDatabase.count_documents({"token": label})))
    print("Label: {}, total count: {}".format(label, howManyNumbers))
    return allDataDatabase.find({"token": label})[howManyNumbers:], allDataDatabase.find({"token": label})[
    :howManyNumbers]


def createDataSet(trainData, trainDatabase, useOtherLabel=True):
    for record in trainData:
        abstractSentences = SENTENCE_SPLITTER.tokenize(record[ABSTRACT_DOCUMENT])
        abstractSentenceIndicesToDelete = list()
        if PURPOSE_DOCUMENT in record:
            purposes = [record[PURPOSE_DOCUMENT]]
            for purpose in purposes:
                sentenceId = purpose[0]
                abstractSentenceIndicesToDelete.append(sentenceId)
                sentence = purpose[1]
                sentenceSplitted = removeCommonWordsAndTokenize(sentence)
                trainDatabase.save({"token": [Label.PURPOSE.value], "sentence": sentenceSplitted})

        if TASKS_DOCUMENT in record:
            tasks = record[TASKS_DOCUMENT]
            for task in tasks:
                sentenceId = task[0]
                abstractSentenceIndicesToDelete.append(sentenceId)
                sentence = task[1]
                sentenceSplitted = removeCommonWordsAndTokenize(sentence)
                trainDatabase.save({"token": [Label.TASKS.value], "sentence": sentenceSplitted})
        if useOtherLabel:
            abstractSentenceIndicesToDelete.sort(reverse=True)
            for indice in abstractSentenceIndicesToDelete:
                del abstractSentences[indice]
            try:
                _, abstractSentence = choice(list(enumerate(abstractSentences)))
                print(abstractSentence)
                trainDatabase.save(
                    {"token": [Label.OTHER.value], "sentence": removeCommonWordsAndTokenize(abstractSentence)})
            except:
                print("Empty list")


def updateDataset():
    for record in allDataDatabase.find():
        processedWords = processWords(record["sentence"])
        record.update({"sentence": processedWords})
        print(record)
        database["all_data2"].save(record)


if __name__ == '__main__':
    prepareDatasets()

    # updateDataset()
    # createTrainTestData(allDataDatabase, trainDatabase, testDatabase)

# check contents in mongoDB
#     {sentence: {$in: ["1"]}}
