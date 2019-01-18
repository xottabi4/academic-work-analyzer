ID_DOCUMENT = "_id"
PURPOSE_DOCUMENT = "purpose"
ABSTRACT_DOCUMENT = "abstract"
PURPOSE_SENTENCE_ID_DOCUMENT = "purpose_sentence_id"


def createRecord(pdfFilePath, abstract=None, purpose=None):
    record = {ID_DOCUMENT: pdfFilePath}
    if abstract:
        record.update(createAbstract(abstract))
    if purpose:
        record.update(createPurpose(purpose))
    return record


def createPurpose(purpose, purposeSentenceId=None):
    record = {PURPOSE_DOCUMENT: purpose}
    if purposeSentenceId:
        record.update({PURPOSE_SENTENCE_ID_DOCUMENT: purposeSentenceId})
    return record


def createAbstract(abstract):
    return {ABSTRACT_DOCUMENT: abstract}
