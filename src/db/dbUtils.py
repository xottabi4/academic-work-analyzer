ID_DOCUMENT = "_id"
PURPOSE_DOCUMENT = "purpose"
ABSTRACT_DOCUMENT = "abstract"


def createRecord(pdfFilePath, abstract=None, purpose=None):
    record = {ID_DOCUMENT: pdfFilePath}
    if abstract:
        record.update(createAbstract(abstract))
    if purpose:
        record.update(createPurpose(purpose))
    return record


def createPurpose(purpose):
    return {PURPOSE_DOCUMENT: purpose}


def createAbstract(abstract):
    return {ABSTRACT_DOCUMENT: abstract}
