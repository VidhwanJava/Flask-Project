from app import app, db
from flask import render_template, request, json, Response
from app.models import User, Course, Enrollment

courseData = [{"courseID":"1111","title":"PHP 111",
    "description":"Intro to PHP","credits":"3","term":"Fall, Spring"},
    {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming",
    "credits":"4","term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201",
    "description":"Advanced PHP Programming","credits":"3","term":"Fall"},
     {"courseID":"4444","title":"Angular 1","description":"Intro to Angular",
     "credits":"3","term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2",
     "description":"Advanced Java Programming","credits":"4","term":"Fall"}]

@app.route("/")
@app.route("/index")
@app.route("/home")
def home():
    return render_template("index.html", home = 1)

@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term = "Fall 2020"):
    return render_template("courses.html", courseData = courseData, course = 1, term = term)


@app.route("/register")
def register():
    return render_template("register.html", register = 1)


@app.route("/login")
def login():
    return render_template("login.html", login = 1)


@app.route("/enrollment", methods = ["GET", "POST"])
def enrollment():
    id = request.form.get('courseID')
    title = request.form.get('title')
    term = request.form['term']
    return render_template("enrollment.html", enrollment = 1, data = {"id":id,"title":title,"term":term})

@app.route("/api/")
@app.route("/api/<idx>")
def api(idx = None):
    if(idx == None):
        jdata = courseData
    else:
        jdata = courseData[int(idx)]
    return Response(json.dumps(jdata), mimetype = "application/json")


@app.route('/user')
def user():
    # User(user_id = 1, first_name = "Athul", last_name = "Krishnan P U", email = "muthu@pandiz.com", password = "muthu123").save()
    # User(user_id = 2, first_name = "Arun", last_name = "Shaju", email = "wlvrn@0011.com", password = "0011").save()
    users = User.objects.all()
    
    return render_template("user.html", users = users)

