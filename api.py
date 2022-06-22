from email import header
from mongo_connect import mongo_create
from bson.objectid import ObjectId
mydb = mongo_create()
user = mydb.user
project = mydb.project
work = mydb.work
