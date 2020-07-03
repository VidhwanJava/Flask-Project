from flask import Flask
from app import db

class User(db.Document):
    user_id = db.IntField( unique = True)
    first_name = db.StringField( max_length = 25)
    last_name = db.StringField( max_length = 25)
    email = db.StringField( max_length = 25)
    password = db.StringField( max_length = 20)

class Course(db.Document):
    course_id = db.StringField( max_length = 20, unique = True)
    title = db.StringField( max_length = 30)
    description = db.StringField( max_length = 200)
    credits = db.IntField()
    term = db.StringField( max_length = 20)

class Enrollment(db.Document):
    user_id = db.IntField()
    course_id = db.StringField( max_length = 20)