from __future__ import division

import logging
import multiprocessing
import os
import time
from random import shuffle

import gensim
from gensim.models import FastText
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

from src.db.Database import trainDatabase, testDatabase
from definitions import doc2vecStoragePath

app_logger = logging.getLogger("modelTrainTest")
app_logger.setLevel(logging.INFO)
fh = logging.FileHandler(os.path.join(doc2vecStoragePath, 'model_results.log'), mode='a')
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
fh.setFormatter(formatter)
app_logger.addHandler(fh)

cores = multiprocessing.cpu_count()
assert gensim.models.doc2vec.FAST_VERSION > -1, "This will be painfully slow otherwise"


def trainFasttext(trainData, modelName="fasttext.model"):
    alldocs = []
    for record in trainData.find():
        alldocs.append(TaggedDocument(words=record['sentence'], tags=record['token']))
    cores = multiprocessing.cpu_count()
    assert gensim.models.doc2vec.FAST_VERSION > -1, "This will be painfully slow otherwise"

    model = FastText(workers=cores)
    print(alldocs)
    model.build_vocab(alldocs)
    doc_list = alldocs[:]
    shuffle(doc_list)

    print("Training %s" % model)

    startTime = time.time()
    model.train(doc_list, total_examples=len(doc_list), epochs=model.epochs)
    elapsed = time.time() - startTime

    print("Finished training. It took {} seconds".format(elapsed))

    print("\nEvaluating %s" % model)
    model.save(modelName)
    print("Model {} saved!".format(modelName))


def trainDoc2vec(trainData, modelName):
    alldocs = []
    for record in trainData.find():
        alldocs.append(TaggedDocument(words=record['sentence'], tags=record['token']))

    model = Doc2Vec(dm=0, vector_size=300, negative=5, hs=0, min_count=2, sample=0, epochs=100, window=15,
        workers=cores)

    model.build_vocab(alldocs)
    doc_list = alldocs[:]
    shuffle(doc_list)

    print("Training %s" % model)
    app_logger.info("Training %s" % model)
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

    model.save(modelName)
    print("Model {} saved!".format(modelName))


def testModelUsingCosDistance(testDatabase, modelName, printWrongSentences=False):
    model = Doc2Vec.load(modelName)
    app_logger.info(model)

    totalTestSentenceCount = testDatabase.count_documents({})
    wrongSentences = list()
    for testSentence in testDatabase.find():
        testSentenceVector = model.infer_vector(testSentence["sentence"])
        # print(model.docvecs.most_similar(positive=[testSentenceVector], topn=10))
        testSentenceToken = model.docvecs.most_similar(positive=[testSentenceVector], topn=1)[0][0]
        # print("found token: {}, real token: {}".format(testSentence["token"][0], testSentenceToken))
        if testSentence["token"][0] != testSentenceToken:
            wrongSentences.append(testSentence)

    wrongSentenceAmount = len(wrongSentences)
    app_logger.info("CosDistance results: ")
    app_logger.info("Total sentences count: {}".format(totalTestSentenceCount))
    app_logger.info("Total wrong sentences classified: {}".format(wrongSentenceAmount))
    error = wrongSentenceAmount / totalTestSentenceCount
    app_logger.info("Error (%): {}".format(error * 100))
    app_logger.info("Correct : {}".format(1 - error))

    if printWrongSentences:
        for sentence in wrongSentences:
            print(sentence)


def trainLogisticRegression(trainDatabase, modelName, logRegParamsName):
    model = Doc2Vec.load(modelName)

    y_train, X_train = get_vectors(model, trainDatabase)

    # OLD used on all models <19
    # logreg = LogisticRegression(n_jobs=1, C=1e5)

    logreg = LogisticRegression(n_jobs=cores, C=1e5, solver="lbfgs", multi_class="multinomial", max_iter=1000)

    logreg.fit(X_train, y_train)
    joblib.dump(logreg, logRegParamsName)


def testLogisticRegression(testDatabase, modelName, logRegParamsName):
    model = Doc2Vec.load(modelName)

    y_test, X_test = get_vectors(model, testDatabase)

    logreg = joblib.load(logRegParamsName)
    app_logger.info(logreg)

    y_pred = logreg.predict(X_test)
    app_logger.info("LogisticRegression results: ")
    app_logger.info('Testing accuracy %s' % accuracy_score(y_test, y_pred))
    app_logger.info('Testing F1 score: {}'.format(f1_score(y_test, y_pred, average='weighted')))


def get_vectors(model, database):
    targets, regressors = zip(
        *[(doc["token"][0], model.infer_vector(doc["sentence"], steps=20)) for doc in database.find()])
    return targets, regressors


def train(version, vectorModel=""):
    modelFullPath = createFullModelPath(version)
    trainDoc2vec(trainDatabase, modelFullPath)

    logRegParamsFullPath = createFullLogRegPath(version)
    trainLogisticRegression(trainDatabase, modelFullPath, logRegParamsFullPath)


def test(version, vectorModel=""):
    app_logger.info("#" * 60)
    app_logger.info("Evaluating {} model version {}".format(vectorModel, version))

    modelFullPath = createFullModelPath(version)
    testModelUsingCosDistance(testDatabase, modelFullPath)

    logRegParamsFullPath = createFullLogRegPath(version)
    testLogisticRegression(testDatabase, modelFullPath, logRegParamsFullPath)


def createFullLogRegPath(version):
    logRegParamsName = "log-reg-params.model" + version
    logRegParamsFullPath = os.path.join(doc2vecStoragePath, logRegParamsName)
    return logRegParamsFullPath


def createFullModelPath(version):
    modelName = "d2v.model" + version
    modelFullPath = os.path.join(doc2vecStoragePath, modelName)
    return modelFullPath


if __name__ == '__main__':
    # train("20", vectorModel="doc2vec")
    test("20", vectorModel="doc2vec")
    # trainFasttext(trainDatabase)
