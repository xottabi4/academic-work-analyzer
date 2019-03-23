import os

import PyPDF2
from requests.exceptions import SSLError

import definitions
from src.crawlers.LuDatabase import LuDatabaseCrawler
from src.db.Database import regexDatabase
from src.db.DbUtils import createRecord, ABSTRACT_DOCUMENT, createPurpose, ID_DOCUMENT
from src.pdf_processing.rule_based.AbstractExtractor import extractAbstract
from src.pdf_processing.rule_based.PurposeExtractor import extractPurpose


def crawlForData(collection):
    crawler = LuDatabaseCrawler()
    # start from 990
    for documentNumber in range(2500, 2510):
        try:
            documentFilename = crawler.findAndSaveDocument(documentNumber)
        except SSLError as err:
            print(err)
            continue
        except ValueError as err:
            print(err)
            continue

        if collection.find_one(documentFilename):
            print("Document already in DB!")
            continue

        print(documentFilename)
        collection.save(createRecord(documentFilename))


def viewFileInfo(academicFiles):
    for academicFile in academicFiles:
        documentPath = os.path.join(definitions.documentStoragePath, academicFile)
        pdfFile = PyPDF2.PdfFileReader(open(documentPath, "rb"))
        print(pdfFile.documentInfo)


def reextractAbstracts(academicFiles, collection):
    for academicFile in academicFiles:
        print(academicFile)
        documentPath = os.path.join(definitions.documentStoragePath, academicFile)
        abstract = extractAbstract(documentPath)
        print(abstract)
        collection.save(createRecord(academicFile, abstract))
        newDocumentPath = os.path.join(definitions.processedDocumentStoragePath, academicFile)
        os.rename(documentPath, newDocumentPath)


def reextractPurposes(collection):
    for record in collection.find({ABSTRACT_DOCUMENT: {"$ne": None}}):
        purpose = extractPurpose(record[ABSTRACT_DOCUMENT])
        if not purpose:
            print("Couldn't find purpose in abstract of document: {}".format(record[ID_DOCUMENT]))
            continue
        print(purpose)
        record.update(createPurpose(purpose))
        collection.save(record)


def main():
    collection = regexDatabase
    # collection.drop()

    # crawlForData(collection)

    # moveProcessedFilesBack()

    academicFiles = get_directory_files(definitions.documentStoragePath)
    reextractAbstracts(academicFiles, collection)
    reextractPurposes(collection)



    # for x in collection.find():
    #     print(x)
    #
    # abstract = collection.find_one(
    #     "/home/xottabi4/Documents/augstskola/magistratura/magistra_darbs/academic-work-analyzer/resources/F91698-Mertena_Laura_Ekon010293.pdf")


def moveProcessedFilesBack():
    processedAcademicFiles = get_directory_files(definitions.processedDocumentStoragePath)
    for processedFile in processedAcademicFiles:
        documentPath = os.path.join(definitions.processedDocumentStoragePath, processedFile)
        newDocumentPath = os.path.join(definitions.documentStoragePath, processedFile)
        os.rename(documentPath, newDocumentPath)


def get_directory_files(directory):
    return [f for f in os.listdir(directory) if
        os.path.isfile(os.path.join(directory, f))]


if __name__ == '__main__':
    main()
