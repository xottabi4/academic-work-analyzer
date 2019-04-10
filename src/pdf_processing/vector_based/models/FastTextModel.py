from __future__ import division

import multiprocessing
import os
import time
import warnings
from random import shuffle

import gensim
import numpy as np
from gensim.models import FastText

from definitions import modelStoragePath
from src.pdf_processing.vector_based.Label import Label
from src.pdf_processing.vector_based.models.Model import Model, ModelType, app_logger
from gensim.test.utils import datapath

cores = multiprocessing.cpu_count()
assert gensim.models.doc2vec.FAST_VERSION > -1, "This will be painfully slow otherwise"


class FastTextModel(Model):

    def __init__(self, modelVersion):
        super().__init__(ModelType.FASTTEXT, modelVersion)
        try:
            self.model = FastText.load(self.modelFullPath)
        except FileNotFoundError:
            warnings.warn("Havent found pretreined model in {}".format(self.modelFullPath))
            if "pretrained" == modelVersion:
                cap_path = os.path.join(modelStoragePath, "pretrained/cc.lv.300")
                print("Loading original pretrained vectors")
                self.model = FastText.load_fasttext_format(cap_path, full_model=False)

    def trainModel(self, trainData, addLabelsToVocabulary=False):
        if "pretrained" == self.modelVersion:
            self.model.save(self.modelFullPath)
            return
        alldocs = []
        for record in trainData.find():
            sentenceAndLabed = record['sentence']
            if addLabelsToVocabulary:
                sentenceAndLabed.append(record['token'][0])
                print(sentenceAndLabed)
            alldocs.append(sentenceAndLabed)

        epochs = 50
        model = FastText(workers=cores, size=100, window=15, min_count=1, sg=0, word_ngrams=1)
        model.build_vocab(alldocs)

        if addLabelsToVocabulary:
            labels = [e.value for e in Label]
            print(labels)
            model.build_vocab(labels, update=True)

        doc_list = alldocs[:]
        shuffle(doc_list)

        print("Training %s" % model)
        startTime = time.time()
        model.train(doc_list, total_examples=len(doc_list), epochs=epochs)
        elapsed = time.time() - startTime

        print("Finished training. It took {} seconds".format(elapsed))

        print("\nEvaluating %s" % model)
        model.save(self.modelFullPath)
        self.model = model
        print("Model {} saved!".format(self.modelFullPath))

    def testModelUsingCosDistance(self, testDatabase, printWrongSentences=False):
        # self.testModelUsingCosDistanceImpl(testDatabase)
        pass

    def testModelUsingCosDistanceImpl(self, testDatabase, printWrongSentences=False):
        totalTestSentenceCount = testDatabase.count_documents({})
        wrongSentences = list()
        for testSentence in testDatabase.find():
            testSentenceToken = self.findSimilarSentences(testSentence["sentence"])

            # testSentenceVector = self.model.infer_vector(testSentence["sentence"])
            # # print(model.docvecs.most_similar(positive=[testSentenceVector], topn=10))
            # testSentenceToken = self.model.docvecs.most_similar(positive=[testSentenceVector], topn=1)[0][0]
            # # print("found token: {}, real token: {}".format(testSentence["token"][0], testSentenceToken))
            # if testSentence["token"][0] != testSentenceToken:
            #     wrongSentences.append(testSentence)

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

    # possible to use only if you add labels to vocabulary
    def findSimilarSentences(self, testSentence):
        sentenceVector = self.calculateSentenceVector(testSentence)
        print(sentenceVector)

        # this finds most similar word from entire vocabulary
        testSentenceToken = self.model.wv.most_similar(positive=[sentenceVector])
        testSentenceToken = testSentenceToken[0][0]

        # this finds most similar word from labels
        labels = [e.value for e in Label]

        # doesnt work as ahvent found method that supports vectors as params
        # labelVectors = [self.model.wv.word_vec(l, use_norm=False) for l in labels]
        # testSentenceToken= self.model.wv.n_similarity(sentenceVector, labelVectors[0])

        # this works but you have to pass actula words instead of vectors
        # testSentenceToken = self.model.wv.most_similar_to_given(testSentence, labels)
        print(testSentenceToken)
        return testSentenceToken

    def calculateSentenceVector(self, words):
        if len(words) < 1:
            print(words)
            raise ValueError("Word count in sentence is less then 1")

        sentenceVector = np.zeros(self.model.vector_size)
        for sentence in words:
            try:
                sentenceVector += self.model.wv[sentence]
            except KeyError:
                continue

        sentenceVector = sentenceVector / len(words)
        return sentenceVector
