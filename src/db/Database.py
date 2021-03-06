import pymongo

from src.db.db_properties import MONGODB_CONNECTION, DATABASE_NAME, COLLECTION_NAME

database = pymongo.MongoClient(MONGODB_CONNECTION)[DATABASE_NAME]

regexDatabase = database[COLLECTION_NAME]
allDataDatabase = database["all_data"]
trainDatabase = database["train_data"]
testDatabase = database["test_data"]
