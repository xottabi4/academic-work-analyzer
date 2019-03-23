import os
from unittest import TestCase

import numpy
from gensim.models import Doc2Vec
from sklearn.externals import joblib

from definitions import doc2vecStoragePath
from pdf_processing.doc2vec.Label import Label
from pdf_processing.utils.WordTokenizer import removeCommonWordsAndTokenize


class Doc2VecModelTest(TestCase):
    version = "19"
    model = Doc2Vec.load(os.path.join(doc2vecStoragePath, "d2v.model" + version))
    logreg = joblib.load(os.path.join(doc2vecStoragePath, "log-reg-params.model" + version))

    def test_manual_sentence_1(self):
        self.assertSentencePrediction(Label.PURPOSE.value,
            "Mērķis Izpētīt dažādas metodes teksta temata klasifikācijai, implementēt tās tekstiem latviešu valodā un salīdzināt tās")

    def test_manual_sentence_2(self):
        self.assertSentencePrediction(Label.OTHER.value,
            "šis ir vienkārši kaut kāds teikums")

    def test_manual_sentence_3(self):
        self.assertSentencePrediction(Label.OTHER.value,
            "darba mērķis")

    def test_manual_sentence_4(self):
        self.assertSentencePrediction(Label.OTHER.value,
            "darba mērķis dancot uz galda")

    def test_manual_sentence_5(self):
        self.assertSentencePrediction(Label.PURPOSE.value,
            "pētījuma mēķis ir izpētīt pērtiķu popularitāti")

    def test_manual_sentence_6(self):
        self.assertSentencePrediction(Label.PURPOSE.value,
            "pētījuma mēķis ir noskaidrot cilvēku skaitu valstī")

    def test_manual_sentence_7(self):
        self.assertSentencePrediction(Label.OTHER.value,
            "Mans mērķis šodien darbā ir dejot")

    def test_manual_sentence_8(self):
        self.assertSentencePrediction(Label.PURPOSE.value,
            "šī teikuma pētījuma Mērķis ir  rakstīšana uz galda")

    def test_manual_sentence_9(self):
        self.assertSentencePrediction(Label.OTHER.value,
            "Parasts teikums kurā nav nekā īpaša")

    def test_manual_sentence_10(self):
        self.assertSentencePrediction(Label.TASKS.value,
            "Izpētīt biežāk lietotās metodes")

    def assertSentencePrediction(self, expectedOutput, input):
        testSentence = removeCommonWordsAndTokenize(input)
        testSentenceVector = self.model.infer_vector(testSentence)
        y_pred = self.logreg.predict([testSentenceVector])
        self.assertEqual(expectedOutput, y_pred[0])

    def manual_test(self,
            sentence="Mērķis Izpētīt dažādas metodes teksta temata klasifikācijai, implementēt tās tekstiem latviešu valodā un salīdzināt tās"):
        """
        Some useful methods for model valuation
        :param sentence:
        :return:
        """

        testSentence = removeCommonWordsAndTokenize(sentence)

        print(testSentence)

        testSentenceVector = self.model.infer_vector(testSentence)
        # print(testSentenceVector)

        # print("other score: {}".format(1 - spatial.distance.cosine(testSentenceVector, model.docvecs["other"])))
        # print("purpose score: {}".format(1 - spatial.distance.cosine(testSentenceVector, model.docvecs["purpose"])))

        y_pred = self.logreg.predict([testSentenceVector])
        print("y_pred")
        print(y_pred)

        print("labels")
        print(self.logreg.classes_)

        print(numpy.round((self.logreg.predict_proba([testSentenceVector])), 3))

        print(self.model.docvecs.most_similar(positive=[testSentenceVector]))
        print(self.model.docvecs.most_similar(positive=[testSentenceVector], topn=1)[0][0])

        # print(model.wv.vocab)
        # max = len(model.wv.vocab) - 1
        # print(max)
        # word1 = model.wv.index2word[randint(0, max)]
        # word2 = model.wv.index2word[randint(0, max)]
        # print(word1)
        # print(word2)
        # print(model.wv.similarity(word1, word2))
