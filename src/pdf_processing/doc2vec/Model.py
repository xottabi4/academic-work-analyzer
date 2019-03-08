from __future__ import division

import multiprocessing
import time
from random import shuffle

import gensim
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

from db.Database import trainDatabase, testDatabase


def train(trainData, modelName):
    alldocs = []
    for record in trainData.find():
        alldocs.append(TaggedDocument(words=record['sentence'], tags=record['token']))
    cores = multiprocessing.cpu_count()
    assert gensim.models.doc2vec.FAST_VERSION > -1, "This will be painfully slow otherwise"

    model = Doc2Vec(dm=0, vector_size=300, negative=5, hs=0, min_count=5, sample=0, epochs=100, window=15, workers=cores)

    model.build_vocab(alldocs)
    doc_list = alldocs[:]
    shuffle(doc_list)
    print(len(doc_list))

    print("Training %s" % model)

    startTime = time.time()

    model.train(doc_list, total_examples=len(doc_list), epochs=model.epochs)
    # model = Doc2Vec(alpha=0.025, min_alpha=0.025)  # use fixed learning rate
    # model.build_vocab(doc_list)

    # for epoch in range(model.epochs):
    #     print(model.corpus_count, model.iter)
    #     model.train(doc_list,  total_examples=model.corpus_count,                epochs=model.iter)
    #     model.alpha -= 0.002  # decrease the learning rate
    #     model.min_alpha = model.alpha  # fix the learning rate, no decay
    elapsed = time.time() - startTime
    print("Finished training. It took {} seconds".format(elapsed))

    print("\nEvaluating %s" % model)

    model.save(modelName)
    print("Model {} saved!".format(modelName))


def testModelUsingCosDistance(testDatabase, modelName, printWrongSentences=False):
    model = Doc2Vec.load(modelName)

    totalTestSentenceCount = testDatabase.count_documents({})
    wrongSentences = list()
    for testSentence in testDatabase.find():
        testSentenceVector = model.infer_vector(testSentence["sentence"])
        testSentenceToken = model.docvecs.most_similar(positive=[testSentenceVector], topn=1)[0][0]
        if testSentence["token"][0] != testSentenceToken:
            wrongSentences.append(testSentence)

    wrongSentenceAmount = len(wrongSentences)
    print("CosDistance results: ")
    print(totalTestSentenceCount)
    print("Total wrong sentences clasified: {}".format(wrongSentenceAmount))
    error = wrongSentenceAmount / totalTestSentenceCount
    print("Error (%): {}".format(error * 100))
    print("Correct : {}".format(1 - error))

    if printWrongSentences:
        for sentence in wrongSentences:
            print(sentence)


def get_vectors(model, database):
    targets, regressors = zip(
        *[(doc["token"][0], model.infer_vector(doc["sentence"], steps=20)) for doc in database.find()])
    return targets, regressors


def trainLogisticRegression(trainDatabase, modelName, logRegParamsName):
    model = Doc2Vec.load(modelName)

    y_train, X_train = get_vectors(model, trainDatabase)

    logreg = LogisticRegression(n_jobs=1, C=1e5)
    logreg.fit(X_train, y_train)
    joblib.dump(logreg, logRegParamsName)


def testLogisticRegression(testDatabase, modelName, logRegParamsName):
    model = Doc2Vec.load(modelName)

    y_test, X_test = get_vectors(model, testDatabase)

    logreg = joblib.load(logRegParamsName)
    y_pred = logreg.predict(X_test)
    print("LogisticRegression results: ")
    print('Testing accuracy %s' % accuracy_score(y_test, y_pred))
    print('Testing F1 score: {}'.format(f1_score(y_test, y_pred, average='weighted')))


def main(version, trainModel=True):
    modelName = "d2v.model" + version
    if trainModel:
        train(trainDatabase, modelName)
    testModelUsingCosDistance(testDatabase, modelName)

    logRegParamsName = "log-reg-params.model" + version
    if trainModel:
        trainLogisticRegression(trainDatabase, modelName, logRegParamsName)
    testLogisticRegression(testDatabase, modelName, logRegParamsName)


if __name__ == '__main__':
    main("11", False)
