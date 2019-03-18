from unittest import TestCase

from pdf_processing.utils.WordTokenizer import removeCommonWordsAndTokenize


class WordTokenizeTest(TestCase):

    def test_english_sentence_splitter(self):
        sentence = "9 šis teikums saSTāv no burtiem a b c 33333333 "
        words = removeCommonWordsAndTokenize(sentence)

        for a in words:
            print(a)

        correctWords = ['SKAITLIS', 'šis', 'teikums', 'sastāv', 'burtiem', 'SKAITLIS']
        self.assertTrue(words == correctWords)
