import os

from gensim.models import Doc2Vec
from sklearn.externals import joblib

from definitions import doc2vecStoragePath
from pdf_processing.doc2vec.Label import Label
from pdf_processing.rule_based.AbstractExtractor import extractAbstract, extractAbstractUsingFile
from pdf_processing.utils.SentenceTokenizer import SENTENCE_SPLITTER
from pdf_processing.utils.WordTokenizer import removeCommonWordsAndTokenize

version = "8"
model = Doc2Vec.load(os.path.join(doc2vecStoragePath, "d2v.model" + version))
logreg = joblib.load(os.path.join(doc2vecStoragePath, "log-reg-params.model" + version))


def processAcademicWork(filePath):
    abstract = extractAbstract(filePath)
    return extractDataFromAbstract(abstract)


def processAcademicWorkFile(file):
    abstract = extractAbstractUsingFile(file)
    return extractDataFromAbstract(abstract)


def extractDataFromAbstract(abstract):
    abstractSentences = SENTENCE_SPLITTER.tokenize(abstract)
    data = dict()
    for idx, sentence in enumerate(abstractSentences):
        sentenceWords = removeCommonWordsAndTokenize(sentence)
        testSentenceVector = model.infer_vector(sentenceWords)
        y_pred = logreg.predict([testSentenceVector])
        if Label.PURPOSE.value == y_pred[0]:
            data.update({Label.PURPOSE.value: sentence})
        elif Label.TASKS.value == y_pred[0]:
            tasks = data.get(Label.TASKS.value)
            if not tasks:
                tasks = list()
            tasks.append(sentence)
            data.update({Label.TASKS.value: tasks})
    return data
