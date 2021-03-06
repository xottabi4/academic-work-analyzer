from src.pdf_processing.utils.WordTokenizer import removeCommonWordsAndTokenize
from src.pdf_processing.vector_based.models.Doc2VecModel import Doc2vecModel
from src.pdf_processing.vector_based.models.FastTextModel import FastTextModel

from src.db.Database import trainDatabase, testDatabase

if __name__ == '__main__':
    # model = Doc2vecModel("22")
    model = FastTextModel("1")
    # model = FastTextModel("pretrained")

    # model.train(trainDatabase)
    model.test(testDatabase)

    # print(model.model.wv.)
    print(len(model.model.wv.vectors_ngrams))
    print(len(model.model.wv.vocab))

    # print("*"*100)
    # model.findSimilarSentences(removeCommonWordsAndTokenize("SKAITLIS un pieci dzīves gadi"))
    # model.findSimilarSentences(removeCommonWordsAndTokenize("label"))
    # model.findSimilarSentences(["tasks_label"])
    # print(model.model.wv.vocab["tasks_label"])
    #
    # sentenceVector = model.calculateSentenceVector(['tasks_label'])
    # actualSentencevector=model.model.wv.word_vec('tasks_label', use_norm=False)
    # print(sentenceVector)
    # print(actualSentencevector)
    # print(sentenceVector-actualSentencevector)
    # model.findSimilarSentences(removeCommonWordsAndTokenize("Darba mērķis ir pārbaudīt dzīves jēgu."))


    # train("20", vectorModel=Model.DOC2VEC.value)
    # test("20", vectorModel="doc2vec")
    # trainFasttext(trainDatabase)
