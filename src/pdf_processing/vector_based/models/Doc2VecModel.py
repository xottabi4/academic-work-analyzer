from __future__ import division

import multiprocessing
import time
import warnings
from random import shuffle

import gensim
from gensim.models.doc2vec import TaggedDocument, Doc2Vec

from src.pdf_processing.vector_based.models.Model import Model, app_logger, ModelType

cores = multiprocessing.cpu_count()
assert gensim.models.doc2vec.FAST_VERSION > -1, "This will be painfully slow otherwise"


class Doc2vecModel(Model):

    def __init__(self, modelVersion):
        super().__init__(ModelType.DOC2VEC, modelVersion)
        try:
            self.model = Doc2Vec.load(self.modelFullPath)
        except FileNotFoundError:
            warnings.warn("Havent found pretreined model in {}".format(self.modelFullPath))

    def trainModel(self, trainData):
        alldocs = []
        for record in trainData.find():
            alldocs.append(TaggedDocument(words=record['sentence'], tags=record['token']))

        model = Doc2Vec(dm=0, vector_size=300, negative=5, hs=0, min_count=2, sample=1e-5, epochs=100, window=15,
            workers=cores)

        # model = Doc2Vec(dm=1, dm_concat=1, vector_size=300, negative=5, hs=0, min_count=1, sample=1e-5, epochs=100,
        #     window=15, workers=cores)

        model.build_vocab(alldocs)
        doc_list = alldocs[:]
        shuffle(doc_list)

        print("Training %s" % model)
        startTime = time.time()
        model.train(doc_list, total_examples=len(doc_list), epochs=model.epochs)
        elapsed = time.time() - startTime
        print("Finished training. It took {} seconds".format(elapsed))

        model.save(self.modelFullPath)
        self.model = model
        print("Model {} saved!".format(self.modelFullPath))

    def testModelUsingCosDistance(self, testDatabase, printWrongSentences=False):
        totalTestSentenceCount = testDatabase.count_documents({})
        wrongSentences = list()
        for testSentence in testDatabase.find():
            testSentenceToken = self.findSimilarSentences(testSentence["sentence"])
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

    def findSimilarSentences(self, testSentence):
        testSentenceVector = self.calculateSentenceVector(testSentence)
        testSentenceToken = self.model.docvecs.most_similar(positive=[testSentenceVector], topn=10)[0][0]
        return testSentenceToken

    def calculateSentenceVector(self, sentences):
        sentenceVector = self.model.infer_vector(sentences, steps=20)
        return sentenceVector
