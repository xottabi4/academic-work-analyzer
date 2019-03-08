import os

rootDirectory = os.path.dirname(os.path.abspath(__file__))
resourcesStoragePath = os.path.join(rootDirectory, "resources")
documentStoragePath = os.path.join(resourcesStoragePath, "academicFiles")
processedDocumentStoragePath = os.path.join(documentStoragePath, "processed")
abbreviationsStoragePath = os.path.join(resourcesStoragePath, "abbreviations")
stopwordsStoragePath = os.path.join(resourcesStoragePath, "stopwords")
doc2vecStoragePath = os.path.join(resourcesStoragePath, "doc2vecModels")
