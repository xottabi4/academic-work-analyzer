from __future__ import division

import logging
import multiprocessing
import os
import warnings
from enum import Enum

import gensim
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

from definitions import modelStoragePath
from src.db.Database import trainDatabase, testDatabase

app_logger = logging.getLogger("modelTrainTest")
app_logger.setLevel(logging.INFO)
fh = logging.FileHandler(os.path.join(modelStoragePath, 'model_results.log'), mode='a')
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
fh.setFormatter(formatter)
app_logger.addHandler(fh)

cores = multiprocessing.cpu_count()
assert gensim.models.doc2vec.FAST_VERSION > -1, "This will be painfully slow otherwise"


class ModelType(Enum):
    DOC2VEC = "d2v"
    FASTTEXT = "fasttext"


class Model:
    model = None
    logreg = None

    def __init__(self, modelType, modelVersion):
        self.modelType = modelType
        self.modelName = modelType.value
        self.modelVersion = modelVersion

        logRegParamsNameVersion = self.modelName + ".log-reg-params" + modelVersion
        self.logRegParamsFullPath = os.path.join(modelStoragePath, logRegParamsNameVersion)

        try:
            self.logreg = joblib.load(self.logRegParamsFullPath)
        except FileNotFoundError:
            warnings.warn("Havent found pretrained log regression params in {}".format(self.logRegParamsFullPath))

        modelNameVersion = self.modelName + ".model" + modelVersion
        self.modelFullPath = os.path.join(modelStoragePath, modelNameVersion)

    def trainLogisticRegression(self, trainDatabase):
        y_train, X_train = self.get_vectors(trainDatabase)

        # OLD used on all models <19
        # logreg = LogisticRegression(n_jobs=1, C=1e5)

        logreg = LogisticRegression(n_jobs=cores, C=1e5, solver="lbfgs", multi_class="multinomial", max_iter=100000)

        logreg.fit(X_train, y_train)
        joblib.dump(logreg, self.logRegParamsFullPath)
        self.logreg = logreg
        print("Model {} saved!".format(self.logRegParamsFullPath))

    def testLogisticRegression(self, testDatabase):
        y_test, X_test = self.get_vectors(testDatabase)

        y_pred = self.logreg.predict(X_test)
        app_logger.info("LogisticRegression results: ")
        app_logger.info('Testing accuracy %s' % accuracy_score(y_test, y_pred))
        app_logger.info('Testing F1 score: {}'.format(f1_score(y_test, y_pred, average='weighted')))

    def get_vectors(self, database):
        targets, regressors = zip(
            *[(doc["token"][0], self.calculateSentenceVector(doc["sentence"])) for doc in database.find()])
        # *[(doc["token"][0], model.wv[doc["sentence"]]) for doc in database.find()])
        return targets, regressors

    def train(self):
        self.trainModel(trainDatabase)
        self.trainLogisticRegression(trainDatabase)

    def test(self):
        app_logger.info("#" * 60)
        app_logger.info("Evaluating {} model version {}".format(self.modelName, self.modelVersion))
        app_logger.info(self.model)
        self.testModelUsingCosDistance(testDatabase)
        app_logger.info(self.logreg)
        self.testLogisticRegression(testDatabase)

    def trainModel(self, trainDatabase):
        raise NotImplementedError()

    def testModelUsingCosDistance(self, testDatabase):
        raise NotImplementedError()

    def calculateSentenceVector(self, sentences):
        raise NotImplementedError()
