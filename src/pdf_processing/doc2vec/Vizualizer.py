import os

import lime.lime_text
import numpy
import numpy as np
from gensim.models import Doc2Vec
from sklearn.externals import joblib

from definitions import doc2vecStoragePath
from pdf_processing.utils.FileUtils import saveContentToFile
from pdf_processing.utils.WordTokenizer import tokenize, strip_formatting

version = "11"
model = Doc2Vec.load(os.path.join(doc2vecStoragePath, "d2v.model" + version))
logreg = joblib.load(os.path.join(doc2vecStoragePath, "log-reg-params.model" + version))


def predict(model, logreg, x):
    testSentenceVector = model.infer_vector(tokenize(x))
    probabilities = logreg.predict_proba([testSentenceVector])
    print(x)
    print(probabilities)
    return np.squeeze(np.asarray(numpy.round(probabilities, 3)))


def classify(data):
    result = []
    for i in data:
        result.append(predict(model, logreg, i))

    result2 = np.asarray(result, dtype=np.float32)
    return result2


def createModelExplanation(sentenceToExplain, modelExplanationFilename):
    # Create a LimeTextExplainer. This object knows how to explain a text-based
    # prediction by dropping words randomly.
    explainer = lime.lime_text.LimeTextExplainer(
        verbose=True,
        # We need to tell LIME how to split the string into words. We can do this
        # by giving it a function to call to split a string up the same way FastText does it.
        split_expression=tokenize,
        # Our FastText classifer uses bigrams (two-word pairs) to classify text. Setting
        # bow=False tells LIME to not assume that our classifier is based on single words only.
        bow=False,
        # To make the output pretty, tell LIME what to call each possible prediction from our model.
        class_names=tuple(logreg.classes_)
    )

    # Make a prediction and explain it!
    exp = explainer.explain_instance(
        # The review to explain
        strip_formatting(sentenceToExplain),
        # The wrapper function that returns FastText predictions in scikit-learn format
        classifier_fn=classify,
        # How many labels to explain. We just want to explain the single most likely label.
        top_labels=1,
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
    testSentence = "Mērķis ir izpētīt dažādas metodes teksta temata klasifikācijai, implementēt tās tekstiem latviešu valodā un salīdzināt tās"
    output_filename = os.path.join(doc2vecStoragePath, "model11_explanation.html")
    createModelExplanation(testSentence, output_filename)
