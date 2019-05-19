import numpy as np

from src.pdf_processing.rule_based.AbstractExtractor import extractAbstract, extractAbstractUsingFile
from src.pdf_processing.utils.SentenceTokenizer import SENTENCE_SPLITTER
from src.pdf_processing.utils.WordTokenizer import removeCommonWordsAndTokenize
from src.pdf_processing.vector_based.Label import Label
from src.pdf_processing.vector_based.models.Doc2VecModel import Doc2vecModel
from src.pdf_processing.vector_based.models.FastTextModel import FastTextModel

# model = Doc2vecModel("21")
model = FastTextModel("1")


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
    rowMaximum = findMaxAcceptableValueInRow(matrix)

    result = dict()
    if purpoiseSentenceIndex is None:
        purposeSentence = ""
    else:
        purposeSentence = abstractSentences[purpoiseSentenceIndex]
    result.update({Label.PURPOSE.value: purposeSentence})

    labels = [e.value for e in Label]
    labels.remove(Label.PURPOSE.value)
    labels.remove(Label.OTHER.value)

    for label in labels:
        tasksSentenceIndices = findSentenceIndeces(rowMaximum, label)
        tasks = list()
        for taskSentenceId in tasksSentenceIndices:
            tasks.append(abstractSentences[taskSentenceId])
        record = {label: tasks}
        result.update(record)
    return result


def findSentenceIndeces(rowMaximum, label):
    labels = model.logreg.classes_
    tasksLocation = np.where(labels == label)
    tasksSentenceIndices = np.where(rowMaximum == tasksLocation[0])[0]
    return tasksSentenceIndices


def findPurposeSentenceIndex(matrix):
    labels = model.logreg.classes_
    purposeLocation = np.where(labels == Label.PURPOSE.value)

    rowMaximum = findMaxAcceptableValueInRow(matrix)
    if purposeLocation not in rowMaximum:
        return None

    columnMaximum = np.argmax(matrix, axis=0)
    purpoiseSentenceIndex = columnMaximum[purposeLocation]

    matrix[purpoiseSentenceIndex, :] = 0
    matrix[:, purposeLocation] = 0
    matrix[purpoiseSentenceIndex, purposeLocation] = 1
    return purpoiseSentenceIndex[0]


def findMaxAcceptableValueInRow(matrix):
    maxValuePositionInRow = np.argmax(matrix, axis=1)
    maxValueInRow = np.amax(matrix, axis=1)

    acceptableValuePositioninRow = maxValuePositionInRow.copy()
    maskIndices = np.where(maxValueInRow <= 0.5)[0]

    acceptableValuePositioninRow[maskIndices] = -1
    return acceptableValuePositioninRow


def populatePredictionMatrix(abstractSentences):
    data = list()
    for idx, sentence in enumerate(abstractSentences):
        sentenceWords = removeCommonWordsAndTokenize(sentence)
        print(sentenceWords)
        if len(sentenceWords) == 1 and sentenceWords[0] == "SKAITLIS":
            data.append(np.zeros(len(model.logreg.classes_)))
            continue
        try:
            testSentenceVector = model.calculateSentenceVector(sentenceWords)
        except ValueError:
            data.append(np.zeros(len(model.logreg.classes_)))
            continue
        proba = model.logreg.predict_proba([testSentenceVector])
        data.append(proba[0])
    matrix = np.array(data)
    return matrix
