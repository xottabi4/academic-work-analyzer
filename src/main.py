import os

import PyPDF2
from requests.exceptions import SSLError
from sqlitedict import SqliteDict

import definitions
from crawlers.luDatabase import LuDatabaseCrawler
from pdf_processing.pdfDocumentProcessing import extractAbstract


def crawlForData(mydict):
    crawler = LuDatabaseCrawler()
    # start from 990
    for documentNumber in range(1618, 1619):
        try:
            documentPath = crawler.findAndSaveDocument(documentNumber)
            text = extractAbstract(documentPath)
        except SSLError as err:
            print(err)
            continue
        except ValueError as err:
            print(err)
            continue

        if documentPath in mydict:
            print("Document already in DB!")
            continue

        print(documentPath)
        print(text)
        mydict[documentPath] = text


def reextractAbstracts(academicFiles, mydict):
    for academicFile in academicFiles:
        documentPath = os.path.join(definitions.documentStoragePath, academicFile)
        print(documentPath)
        text = extractAbstract(documentPath)
        print(text)
        mydict[documentPath] = text


def viewFileInfo(academicFiles):
    for academicFile in academicFiles:
        documentPath = os.path.join(definitions.documentStoragePath, academicFile)
        pdfFIle = PyPDF2.PdfFileReader(open(documentPath, "rb"))
        print(pdfFIle.documentInfo)


def main():
    mydict = SqliteDict(os.path.join(definitions.rootDirectory, "academic_work_abstracts.sqlite"), autocommit=True)

    # crawlForData(mydict)

    # academicFiles = os.listdir(definitions.documentStoragePath)
    # reextractAbstracts(academicFiles, mydict)

    printContents(mydict)
    mydict.close()


def printContents(mydict):
    print(len(mydict))
    for key, value in mydict.items():
        print(key)
        print(len(value))
        print(value)


if __name__ == '__main__':
    main()
