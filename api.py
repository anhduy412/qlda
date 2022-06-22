import datetime
from mongo_connect import mongo_create
from bson.objectid import ObjectId
from passlib.context import CryptContext
mydb = mongo_create()
user = mydb.user
project = mydb.project
work = mydb.work

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_info(user_id):
    if not isinstance(user_id, ObjectId):
        user_id = ObjectId(user_id)
    return mydb.user.find_one({'_id': user_id})

def getNOW():
    return datetime.now().timestamp()

def convert_utc_7(value):
    if len(str(value)) == 13:
        value = value / 1000
    return datetime.fromtimestamp(int(value)+25200).strftime("%Y/%m/%d %H:%M:%S")

def get_string_now():
    return datetime.fromtimestamp(datetime.now().timestamp()+25200).strftime("%Y/%m/%d %H:%M:%S")