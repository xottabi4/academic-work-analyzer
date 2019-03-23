import shutil
from unittest import TestCase

import nltk

from src.pdf_processing.utils.SentenceTokenizer import SENTENCE_SPLITTER, loadCustomPunkt


class SentenceTokenizerTest(TestCase):
    text = "Akrilamīds – pārtikas u.c. ķīmiskais piesārņojums. " \
           "Švalkovskis G., zinātniskie vadītāji As. prof., Dr. ķīm. Jākobsone I., As. prof., Dr. ķīm. Mekšs P. Bakalaura darbs, 42 lappuses, 14 attēli, 15 tabulas, 25 literatūras avoti, 1 pielikums. " \
           "Latviešu valodā.  " \
           "GĀZU HROMATOGRĀFIJA, ELEKTRONU SATVERES DETEKTORS, MASSPEKTROMETRIJA, AKRILAMĪDA NOTEIKŠANA.  " \
           "2002. gada aprīlī Zviedrijā atklāja toksisku vielu – akrilamīdu, kas ir termiski apstrādātā pārtikā. " \
           "Vēlāk atklājumi tika veikti arī citās pasaules valstīs. " \
           "Mērķis ir analizēt vietējo Latvijas produkciju un izpētīt iespējamos komponentus un apstākļus, kas rada akrilamīdu. " \
           "Rezultāti tika iegūti no produktiem, kas satur kartupeļu cieti un graudaugu cieti. " \
           "Kartupeļu cieti saturoši produkti (čipsi, frī) satur akrilamīdu dažādā koncentrācijā, bet graudaugu cieti saturošie ne vienmēr. " \
           "Šodien piem. ir jauka diena, tas bija rakstīts 5. lpp. vai utt. teikuma beigas."

    textSentenceCount = 10

    def test_english_sentence_splitter(self):
        abstractSentences = SENTENCE_SPLITTER.tokenize(self.text)

        for a in abstractSentences:
            print(a)

        self.assertEqual(self.textSentenceCount, len(abstractSentences))

    def test_clean_english_sentence_splitter(self):
        punktLocation = "./tmp"
        nltk.download('punkt', download_dir=punktLocation, force=True)
        punkt = nltk.data.load('./tmp/tokenizers/punkt/english.pickle')
        shutil.rmtree(punktLocation)

        abstractSentences = punkt.tokenize(self.text)


        for a in abstractSentences:
            print(a)

        self.assertEqual(self.textSentenceCount, len(abstractSentences))

    def test_custom_sentence_splitter(self):
        punkt = loadCustomPunkt("latvianPunkt.pickle")
        abstractSentences = punkt.tokenize(self.text)

        for a in abstractSentences:
            print(a)

        self.assertEqual(self.textSentenceCount, len(abstractSentences))

    def test_custom_sentence_splitter2(self):
        punkt = loadCustomPunkt("latvianPunkt2.pickle")
        abstractSentences = punkt.tokenize(self.text)

        for a in abstractSentences:
            print(a)

        self.assertEqual(self.textSentenceCount, len(abstractSentences))
