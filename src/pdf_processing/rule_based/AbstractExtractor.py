import io
import os
import re
from string import digits

from pdfminer.converter import TextConverter
from pdfminer.pdfdocument import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.psparser import PSSyntaxError

from src.pdf_processing.rule_based.AbstractDetector import AbstractDetector, ABSTRACT

# otherSymbols = """"#$%&'()*+,-/:<=>@[\]^_`{|}~"""


def preprocessText(pageText):
    text = pageText.strip()
    # TODO create regex that in case when number is surrounded by some symbols delete both number and symbols,
    #  because sometimes page numbers are inlcuding some bullshit symbols like: "- 2 -" example file F81348-Francis_Edgars_Prog020010.pdf
    text = text.strip(digits)
    return text.strip()


def extractRawAbstract(pdf_file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    # with open(pdf_path, 'rb') as fh:
    try:
        pdfPageList = list(PDFPage.get_pages(pdf_file, caching=True, check_extractable=True))
    except (PDFTextExtractionNotAllowed, PSSyntaxError):
        print("Cant extract text from file, it is encrypted or damaged!")
        return None

    validText = ""
    abstractDetector = AbstractDetector()

    for currentPage in pdfPageList[1:]:
        page_interpreter.process_page(currentPage)
        currentPageText = fake_file_handle.getvalue()
        # print(currentPageText)
        # print(len(currentPageText))
        currentPageText = preprocessText(currentPageText)
        if abstractDetector.isFirstAbstractPage(currentPageText):
            validText += " " + currentPageText
            # print(validText)
            if abstractDetector.doesAbstractConsistOfMorePages(validText):
                fake_file_handle.truncate(0)
                fake_file_handle.seek(0)
                continue
            else:
                return validText

        fake_file_handle.truncate(0)
        fake_file_handle.seek(0)

    # close open handles
    converter.close()
    fake_file_handle.close()


def extractAbstract(documentPath, deletePdfIfNoAbstractFound=False):
    with open(documentPath, 'rb') as fh:
        text = extractRawAbstract(fh)
    if not text:
        if deletePdfIfNoAbstractFound:
            os.remove(documentPath)
        print("No latvian abstract found in document!")
        return None
    text = postprocessAbstract(text)
    return text


def extractAbstractUsingFile(file):
    text = extractRawAbstract(file)
    if not text:
        print("No latvian abstract found in document!")
        return None
    text = postprocessAbstract(text)
    return text


def postprocessAbstract(text):
    text = text.strip()
    text = re.sub(ABSTRACT, "", text, count=1, flags=re.IGNORECASE)
    text = text.strip()

    # needs substitution ţ -> ž; Ĝ -> ļ ; Ħ -> ņ; ė -> ķ; ă -> ģ
    text = text.replace("ţ", "ž")
    text = text.replace("Ĝ", "ļ")
    text = text.replace("Ħ", "ņ")
    text = text.replace("ė", "ķ")
    text = text.replace("ă", "ģ")

    # TODO some strange people write both latvian and english anotations in single page, find way to remove english one

    text = text.replace(".", ". ")

    # replace bulletpoint with dot in order to separate sentences
    text = text.replace("•", ". ")

    # in order to separate task, conclusion and result lists.
    text = text.replace(";", ". ")

    # This statement affects all whitespace characters (space, tab, newline, return, formfeed)
    text = " ".join(text.split())
    return text
