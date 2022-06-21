import sys

ITEMS_PER_PAGE = 10
MONGODB_HOST = 'mongo'
MONGODB_PORT = 27017
MONGODB_NAME = 'qlda'

if 'local' in sys.argv:
    MONGODB_HOST = '127.0.0.1'