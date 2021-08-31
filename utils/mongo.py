from pymongo import MongoClient
from utils.log import log

log("Connecting to MongoDB")
mongo = MongoClient()["easygif"]
mongo_users = mongo["users"]