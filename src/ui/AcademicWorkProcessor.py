import os

import numpy as np
from gensim.models import Doc2Vec
from sklearn.externals import joblib

from definitions import modelStoragePath
from src.pdf_processing.vector_based.Label import Label
from src.pdf_processing.rule_based.AbstractExtractor import extractAbstract, extractAbstractUsingFile
from src.pdf_processing.utils.SentenceTokenizer import SENTENCE_SPLITTER
from src.pdf_processing.utils.WordTokenizer import removeCommonWordsAndTokenize

version = "20"
model = Doc2Vec.load(os.path.join(modelStoragePath, "d2v.model" + version))
logreg = joblib.load(os.path.join(modelStoragePath, "log-reg-params.model" + version))


def processAcademicWork(filePath):
    abstract = extractAbstract(filePath)
    return extractDataFromAbstract(abstract)


def processAcademicWorkFile(file):
    abstract = extractAbstractUsingFile(file)
    return extractDataFromAbstract(abstract)


def extractDataFromAbstract(abstract):
    abstractSentences = SENTENCE_SPLITTER.tokenize(abstract)
    matrix = populatePredictionMatrix(abstractSentences)

    purpoiseSentenceIndex = findPurposeSentenceIndex(matrix)

    rowMaximum = np.argmax(matrix, axis=1)
    tasksSentenceIndices = findTaskSentenceIndex(rowMaximum)

    result = dict()
    if purpoiseSentenceIndex is None:
        purposeSentence = ""
    else:
        purposeSentence = abstractSentences[purpoiseSentenceIndex]
    result.update({Label.PURPOSE.value: purposeSentence})

    tasks = list()
    for taskSentenceId in tasksSentenceIndices:
        tasks.append(abstractSentences[taskSentenceId])
    result.update({Label.TASKS.value: tasks})

    return result


def findTaskSentenceIndex(rowMaximum):
    labels = logreg.classes_
    tasksLocation = np.where(labels == Label.TASKS.value)
    tasksSentenceIndices = np.where(rowMaximum == tasksLocation[0])[0]
    return tasksSentenceIndices


def findPurposeSentenceIndex(matrix):
    labels = logreg.classes_
    purposeLocation = np.where(labels == Label.PURPOSE.value)

    rowMaximum = np.argmax(matrix, axis=1)
    if purposeLocation not in rowMaximum:
        return None

    columnMaximum = np.argmax(matrix, axis=0)
    purpoiseSentenceIndex = columnMaximum[purposeLocation]

    matrix[purpoiseSentenceIndex, :] = 0
    matrix[:, purposeLocation] = 0
    return purpoiseSentenceIndex[0]


def populatePredictionMatrix(abstractSentences):
    data = list()
    for idx, sentence in enumerate(abstractSentences):
        sentenceWords = removeCommonWordsAndTokenize(sentence)
        print(sentenceWords)
        testSentenceVector = model.infer_vector(sentenceWords)
        proba = logreg.predict_proba([testSentenceVector])
        data.append(proba[0])
    matrix = np.array(data)
    return matrix
