from unittest import TestCase

from src.ui.AcademicWorkProcessor import extractDataFromAbstract


class TestExtractDataFromAbstract(TestCase):

    def test_some_big_text(self):
        text = "Darba mērķis ir pārbaudīt dzīves jēgu. Izpētīt rožu popularitāti. Papriecāties par miljonu. Šodien ir saulaina jauka diena. Šis ir vienkāršs stulbs teikums. Pārliecināties par drošību uz ielām. Apskatīt mašīnu plūsmu upē. Pielietot smadzenes problēmu risināšanā. Dejot uz galda. Piektdiena ir piektā diena. Es varu sarakstīt daudz stulbu teikumu. Piemēram, trīs plus trīs ir seši. Analizēt sūdu plūsmu upē. Griezt vadus datoros un citā elektronikā. Šodien man patīk analizēt cilvēku domas. Vienkāršs parasts teikums kurā ir vārds apskatīt."
        data = extractDataFromAbstract(text)

        for k, v in data.items():
            print(k, v)

    def test_single_negative_sentence(self):
        text = "Kāds šodien ir labs laiks ārā."
        data = extractDataFromAbstract(text)

        for k, v in data.items():
            print(k, v)
            self.assertFalse(v)

    def test_single_negative_sentence2(self):
        text = "Lielas urīna plūsmas."
        data = extractDataFromAbstract(text)

        for k, v in data.items():
            print(k, v)
            self.assertFalse(v)

    def test_single_negative_sentence3(self):
        text = "Kaut kāds bezjēdzīgs teikums"
        data = extractDataFromAbstract(text)

        for k, v in data.items():
            print(k, v)
            self.assertFalse(v)

    def test_single_negative_sentence4(self):
        text = "Atslēgvārdi: naudas plūsmas pārskats, tiešā un netiešā naudas plūsmas pārskata sastādīšanas metode, pamatdarbības, ieguldīšanas darbības, finansēšanas darbības naudas plūsmas."
        data = extractDataFromAbstract(text)

        for k, v in data.items():
            print(k, v)
            self.assertFalse(v)
