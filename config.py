import os

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KY") or b'\xc3L7\xbe\x12\x8b)\xf0\xf5\x9e\xe3\xd1\x99\xeb\x9d\xad'

    MONGODB_SETTINGS = { 'db' : 'UTA_Enrollment' }