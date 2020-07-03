import os

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KY") or "vidhwanjav@123!"

    MONGODB_SETTINGS = { 'db' : 'UTA_Enrollment' }