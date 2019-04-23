import os

import lime.lime_text
import numpy
import numpy as np

from definitions import modelStoragePath
from src.pdf_processing.utils.FileUtils import saveContentToFile
from src.pdf_processing.utils.WordTokenizer import tokenize, strip_formatting, removeCommonWordsAndTokenize

from src.pdf_processing.vector_based.models.Doc2VecModel import Doc2vecModel
from src.pdf_processing.vector_based.models.FastTextModel import FastTextModel

# model = Doc2vecModel("21")
model = FastTextModel("1")


def predict(x):
    # old style
    # testSentenceVector = model.infer_vector(tokenize(x))
    # probabilities = logreg.predict_proba([testSentenceVector])

    print(x)
    testSentenceVector = model.calculateSentenceVector(removeCommonWordsAndTokenize(x))
    probabilities = model.logreg.predict_proba([testSentenceVector])

    # doc2VecModel.predictClass()
    print(x)
    print(probabilities)
    return np.squeeze(np.asarray(numpy.round(probabilities, 3)))


def classify(data):
    result = []
    for i in data:
        result.append(predict(i))

    result2 = np.asarray(result, dtype=np.float32)
    return result2


def createModelExplanation(sentenceToExplain, modelExplanationFilename):
    # Create a LimeTextExplainer. This object knows how to explain a text-based
    # prediction by dropping words randomly.
    explainer = lime.lime_text.LimeTextExplainer(
        verbose=True,
        # We need to tell LIME how to split the string into words. We can do this
        # by giving it a function to call to split a string up the same way FastText does it.
        split_expression=removeCommonWordsAndTokenize,
        # Our FastText classifer uses bigrams (two-word pairs) to classify text. Setting
        # bow=False tells LIME to not assume that our classifier is based on single words only.
        bow=False,
        # To make the output pretty, tell LIME what to call each possible prediction from our model.
        class_names=tuple(model.logreg.classes_)
    )

    # Make a prediction and explain it!
    exp = explainer.explain_instance(
        # The review to explain
        strip_formatting(sentenceToExplain),
        # The wrapper function that returns FastText predictions in scikit-learn format
        classifier_fn=classify,
        # How many labels to explain. We just want to explain the single most likely label.
        # labels=tuple(logreg.classes_),
        top_labels=2,
        # top_labels=len(model.logreg.classes_),
        # How many words in our sentence to include in the explanation. You can try different values.
        num_features=100,
        num_samples=10000
    )

    # Save the explanation to an HTML file so it's easy to view.
    # You can also get it to other formats: as_list(), as_map(), etc.
    # See https://lime-ml.readthedocs.io/en/latest/lime.html#lime.explanation.Explanation
    saveContentToFile(exp.as_html(), modelExplanationFilename)
    print("done")


if __name__ == '__main__':
    # testSentence = "Vienkāršs parasts teikums kurā ir vārds apskatīt."

    # testSentence = "Mans mērķis ir pārņemt pasauli."

    testSentence = "mērķis ir Izpētīt dažādas metodes teksta temata klasifikācijai, implementēt tās tekstiem latviešu valodā un salīdzināt tās"
    testSentence="analizēt iegūtos rezultātu un veikt secinājumus par ūdens apjomu okeānā."
    # testSentence="Izpētīt biežāk lietotās metodes"
    output_filename = os.path.join(modelStoragePath,
        "model_{}_{}_explanation.html".format(model.modelName, model.modelVersion))
    createModelExplanation(testSentence, output_filename)
