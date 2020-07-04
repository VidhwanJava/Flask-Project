from app import app, db, api
from flask import render_template, request, json, Response, flash, redirect, url_for, session, jsonify
from app.models import User, Course, Enrollment
from app.forms import LoginForm, RegisterForm
from flask_restplus import Resource

# courseData = [{"courseID":"1111","title":"PHP 111",
#     "description":"Intro to PHP","credits":"3","term":"Fall, Spring"},
#     {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming",
#     "credits":"4","term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201",
#     "description":"Advanced PHP Programming","credits":"3","term":"Fall"},
#      {"courseID":"4444","title":"Angular 1","description":"Intro to Angular",
#      "credits":"3","term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2",
#      "description":"Advanced Java Programming","credits":"4","term":"Fall"}]

##############################################
@app.route('/api','/api/')
class GetAndPost(Resource):

    def get(self):
        return jsonify(user.objects.all())


@app.route('/api/<idx>')
class GetUpdateDelete(Resource):

    def get(self, idx):
        return jsonify(user.objects(user_id = idx))

##############################################

@app.route("/")
@app.route("/index")
@app.route("/home")
def home():
    return render_template("index.html", home = 1)

@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term = None):
    if term is None:
        term = "Spring 2020"
    classes = Course.objects.order_by("+courseID")
    return render_template("courses.html", courseData = classes, course = 1, term = term)


@app.route("/register",  methods = ["GET","POST"])
def register():

    if session.get('username'):
        return redirect(url_for('home'))

    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count() + 1
        email =form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(user_id = user_id, email = email, first_name = first_name, last_name= last_name)
        user.set_password(password)
        user.save()
        flash("User registered successfully!", "success")
        return redirect(url_for('home'))
    return render_template("register.html",title = "Sign Up", form = form, register = 1)


@app.route("/login", methods = ["GET","POST"])
def login():

    if session.get('username'):
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():

        email = form.email.data
        password = form.password.data

        user = User.objects(email = email).first()
        if user and user.get_password(password):
            flash(f"Welcome back, {user.first_name}", "success")
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect("/home")
        else:
            flash("Sorry, wrong credentials!", "danger")
    return render_template("login.html",title = "Login", form = form, login = 1)



@app.route("/enrollment", methods = ["GET", "POST"])
def enrollment():

    if not session.get('username'):
        return redirect(url_for('login'))

    courseID = request.form.get('courseID')
    courseTitle = request.form.get('title')
    user_id = session.get('user_id')

    if courseID:
        if Enrollment.objects(user_id = user_id, courseID = courseID):
            flash(f"You had already registered for this course {courseTitle}", "warning")
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id = user_id, courseID = courseID).save()
            flash(f"You have been successfully enrolled for {courseTitle}","success")
    
    classes = list( User.objects.aggregate(*[
                    {
                        '$lookup': {
                            'from': 'enrollment', 
                            'localField': 'user_id', 
                            'foreignField': 'user_id', 
                            'as': 'r1'
                        }
                    }, {
                        '$unwind': {
                            'path': '$r1', 
                            'includeArrayIndex': 'r1_id', 
                            'preserveNullAndEmptyArrays': False
                        }
                    }, {
                        '$lookup': {
                            'from': 'course', 
                            'localField': 'r1.courseID', 
                            'foreignField': 'courseID', 
                            'as': 'r2'
                        }
                    }, {
                        '$unwind': {
                            'path': '$r2', 
                            'preserveNullAndEmptyArrays': False
                        }
                    }, {
                        '$match': {
                            'user_id': user_id
                        }
                    }, {
                        '$sort': {
                            'courseID': 1
                        }
                    }
                ]))
    # term = request.form.get('term')
    return render_template("enrollment.html",title = "Enrollment", enrollment = 1, classes = classes)



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

@app.route("/logout")
def logout():
    session['user_id'] = False
    session.pop('username',None)
    return redirect(url_for('home'))