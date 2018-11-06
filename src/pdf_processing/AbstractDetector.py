import re

TABLE_OF_CONTENTS = "Saturs|Satura rādītājs"
ABSTRACT = "Anotācija"
MAX_ACCEPTABLE_NUMBER_COUNT = 50


class AbstractDetector:
    hasFoundAbstract = False

    def doesAbstractConsistOfMorePages(self, validText):
        # about 2506 chars is full page
        #  sometimes people insert this as last statemet (no dot at the end)
        # Atslēgvārdi: nanokompozīts, mehāniskā uzvedība, mitruma ietekme, starpfāžu slānis

        sentenceEndWithDot = "." == validText[-1]
        pageIsFullOfText = len(validText) >= 2500
        isKeywordsSectionLast = re.search("Atslēgvārdi:", validText[-100:], re.IGNORECASE)
        return not sentenceEndWithDot and pageIsFullOfText and not isKeywordsSectionLast

    def isFirstAbstractPage(self, currentPageText):
        possibleReturnValue = self._isFirstAbstractPageLogic(currentPageText)
        if not self.hasFoundAbstract and possibleReturnValue:
            self.hasFoundAbstract = True
            return possibleReturnValue
        elif self.hasFoundAbstract:
            return True
        else:
            return False

    def _isFirstAbstractPageLogic(self, currentPageText):
        return re.search(ABSTRACT, currentPageText, re.IGNORECASE) and \
               not re.search(TABLE_OF_CONTENTS, currentPageText[:15], re.IGNORECASE) and \
               self._validateNumberCount(currentPageText, MAX_ACCEPTABLE_NUMBER_COUNT)

    def _validateNumberCount(self, pageText, maxAcceptableNumberCount):
        numberCount = sum(c.isdigit() for c in pageText)
        return numberCount <= maxAcceptableNumberCount
