import os
import random
import re
from urllib.parse import urlparse, parse_qs

import PyPDF2
import requests
from PyPDF2.utils import PdfReadError
from bs4 import BeautifulSoup

import definitions
from src.crawlers import properties


class LuDatabaseCrawler:

    def __init__(self):
        self.USER_PATH_ID = self.findUserIdPath()

    def findAllLinks(self, soup):
        return soup.findAll('a', attrs={'href': re.compile("^https://")})

    def extractParticularLink(self, soup, index):
        linkLocation = self.findAllLinks(soup)[index]
        return linkLocation.get('href')

    def findUserIdPath(self):
        link = "http://libra.lanet.lv/F?RN=" + str(random.randint(1, 50))
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        link = self.extractParticularLink(soup, 0)

        documentUrl = urlparse(link)
        return documentUrl.path

    def getDocumentFromDataBase(self, documentNumber):
        documentNumber = "%09d" % documentNumber
        url = "https://kopkatalogs.lv" + self.USER_PATH_ID + "?func=service&doc_library=LUA02&doc_number=" \
              + documentNumber + "&line_number=0001&func_code=WEB-BRIEF&service_type=MEDIA"
        print(url)
        response = requests.get(url)

        if response.text.__contains__("The Object doesn't exist."):
            raise ValueError("Invalid document number provided: " + documentNumber)

        soup = BeautifulSoup(response.text, 'html.parser')
        link = self.extractParticularLink(soup, 0)

        documentGetForm = requests.get(link)

        soup = BeautifulSoup(documentGetForm.text, 'html.parser')
        documentLink = soup.find("body").get("onload").split("=\"")[1].strip("\"")

        documentUrl = urlparse(documentLink)

        query = parse_qs(documentUrl.query)

        documentUrlPath = documentUrl
        documentUrlPath = documentUrlPath._replace(query='')

        r = requests.post(documentUrlPath.geturl(),
            data={'FN': query.get("fn")[0], 'L': query.get("l")[0], 'USR': properties.laisUsername,
                "PWD": properties.laisPassword})

        documentFilename = query.get("fn")[0]
        documentFilename = documentFilename.replace("/", "-")
        return [r.content, documentFilename]

    def findAndSaveDocument(self, documentNumber):
        document, documentFilename = self.getDocumentFromDataBase(documentNumber)
        documentPath = os.path.join(definitions.documentStoragePath, documentFilename)
        self.saveAndValidatePDF(document, documentPath)

        return documentFilename

    def saveAndValidatePDF(self, document, documentPath):
        with open(documentPath, 'wb') as f:
            f.write(document)
        try:
            PyPDF2.PdfFileReader(open(documentPath, "rb"))
        except PdfReadError:
            os.remove(documentPath)
            raise ValueError("Invalid PDF file:\n{}".format(documentPath))
        except OSError:
            os.remove(documentPath)
            raise ValueError(
                "Invalid file (most likely it is empty file or invalid encoding):\n{}".format(documentPath))
