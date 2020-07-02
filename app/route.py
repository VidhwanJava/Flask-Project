from app import app
from flask import render_template

@app.route("/")
@app.route("/home")
@app.route("/index")

def home():
    return render_template("index.html", login=0)

@app.route("/courses")
def courses():
    return render_template("courses.html", login=0)

@app.route("/register")
def register():
    return render_template("register.html", login=0)

@app.route("/login")
def login():
    return render_template("login.html", login=0)