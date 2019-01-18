from unittest import TestCase

from pdf_processing.utils.SentenceTokenizer import SENTENCE_SPLITTER, SENTENCE_SPLITTER_CUSTOM


class SentenceTokenizerTest(TestCase):

    def test_sentence_splitter(self):
        text = "Akrilamīds – pārtikas u.c. ķīmiskais " \
               "piesārņojums. Švalkovskis G., zinātniskie vadītāji As. prof., Dr. ķīm. Jākobsone I., As. prof., Dr. ķīm. " \
               "Mekšs P. Bakalaura darbs, 42 lappuses, 14 attēli, 15 tabulas, 25 literatūras avoti, 1 pielikums. Latviešu valodā.  " \
               "GĀZU HROMATOGRĀFIJA, ELEKTRONU SATVERES DETEKTORS, MASSPEKTROMETRIJA, AKRILAMĪDA NOTEIKŠANA.  " \
               "2002. gada aprīlī Zviedrijā atklāja toksisku vielu – akrilamīdu, kas ir termiski apstrādātā pārtikā. " \
               "Vēlāk atklājumi tika veikti arī citās pasaules valstīs. Mērķis ir analizēt vietējo Latvijas produkciju un izpētīt iespējamos komponentus un apstākļus, kas rada akrilamīdu. Rezultāti tika iegūti no produktiem, kas satur kartupeļu cieti un graudaugu cieti. Kartupeļu cieti saturoši produkti (čipsi, frī) satur akrilamīdu dažādā koncentrācijā, bet graudaugu cieti saturošie ne vienmēr."

        abstractSentences = SENTENCE_SPLITTER.tokenize(text)

        for a in abstractSentences:
            print(a)
            
        self.assertEqual(9, len(abstractSentences))

    def test_custom_sentence_splitter(self):
        text = "Akrilamīds – pārtikas u.c. ķīmiskais " \
               "piesārņojums. Švalkovskis G., zinātniskie vadītāji As. prof., Dr. ķīm. Jākobsone I., As. prof., Dr. ķīm. " \
               "Mekšs P. Bakalaura darbs, 42 lappuses, 14 attēli, 15 tabulas, 25 literatūras avoti, 1 pielikums. Latviešu valodā.  " \
               "GĀZU HROMATOGRĀFIJA, ELEKTRONU SATVERES DETEKTORS, MASSPEKTROMETRIJA, AKRILAMĪDA NOTEIKŠANA.  " \
               "2002. gada aprīlī Zviedrijā atklāja toksisku vielu – akrilamīdu, kas ir termiski apstrādātā pārtikā. " \
               "Vēlāk atklājumi tika veikti arī citās pasaules valstīs. Mērķis ir analizēt vietējo Latvijas produkciju un izpētīt iespējamos komponentus un apstākļus, kas rada akrilamīdu. Rezultāti tika iegūti no produktiem, kas satur kartupeļu cieti un graudaugu cieti. Kartupeļu cieti saturoši produkti (čipsi, frī) satur akrilamīdu dažādā koncentrācijā, bet graudaugu cieti saturošie ne vienmēr."

        abstractSentences = SENTENCE_SPLITTER_CUSTOM.tokenize(text)

        for a in abstractSentences:
            print(a)

        self.assertEqual(9, len(abstractSentences))
