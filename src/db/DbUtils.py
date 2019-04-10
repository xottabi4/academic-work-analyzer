ID_DOCUMENT = "_id"
TASKS_DOCUMENT = "tasks"
PURPOSE_DOCUMENT = "purpose"
ABSTRACT_DOCUMENT = "abstract"
CONCLUSIONS_DOCUMENT = 'conclusions'
RESULTS_DOCUMENT = 'ŗesults'


def createRecord(pdfFilePath, abstract=None, purpose=None, tasks=None):
    record = {ID_DOCUMENT: pdfFilePath}
    if abstract:
        record.update(createAbstract(abstract))
    if purpose:
        record.update(createPurpose(purpose))
    if tasks:
        record.update(createTasks(tasks))
    return record


def createTasks(tasks, sentenceId=None):
    record = {TASKS_DOCUMENT: tasks}
    # if sentenceId:
    #     record.update({PURPOSE_SENTENCE_ID_DOCUMENT: sentenceId})
    return record


def createPurpose(purpose, purposeSentenceId=None):
    record = {PURPOSE_DOCUMENT: purpose}
    # if purposeSentenceId:
    #     record.update({PURPOSE_SENTENCE_ID_DOCUMENT: purposeSentenceId})
    return record


def createAbstract(abstract):
    return {ABSTRACT_DOCUMENT: abstract}


def createRecord(recordType, tasks):
    record = {recordType: tasks}
    return record
