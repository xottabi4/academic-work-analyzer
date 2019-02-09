import os

import PyPDF2
from requests.exceptions import SSLError

import definitions
from crawlers.LuDatabase import LuDatabaseCrawler
from db.Database import regexDatabase
from db.DbUtils import createRecord
from pdf_processing.rule_based.AbstractExtractor import reextractAbstracts
from pdf_processing.rule_based.PurposeExtractor import reextractPurposes


def crawlForData(collection):
    crawler = LuDatabaseCrawler()
    # start from 990
    for documentNumber in range(1650, 1700):
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


def main():
    collection = regexDatabase
    # collection.drop()

    # crawlForData(collection)

    academicFiles = os.listdir(definitions.documentStoragePath)
    reextractAbstracts(academicFiles, collection)
    reextractPurposes(collection)
    # for x in collection.find():
    #     print(x)
    #
    # abstract = collection.find_one(
    #     "/home/xottabi4/Documents/augstskola/magistratura/magistra_darbs/academic-work-analyzer/resources/F91698-Mertena_Laura_Ekon010293.pdf")


if __name__ == '__main__':
    main()
