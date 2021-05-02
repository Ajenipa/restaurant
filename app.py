from flask import Flask,render_template,request,url_for,redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import datetime
import validators
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,validators
from wtforms.validators import InputRequired,Email,Length,EqualTo
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from send_mail import send_mail
app =  Flask(__name__)

ENV = "dev"
if ENV == "dev":
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:ajenipa1@localhost/contactme"
    app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:ajenipa1@localhost/Users"
else:
    app.debug = False
    app.config["SQLALCHEMY_DATABASE_URI"]=""
    app.config["SQLALCHEMY_TRACK_MODIFICATION"]= False
db = SQLAlchemy(app)
Bootstrap(app)
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
app.config["SECRET_KEY"]="1234"
class Users(UserMixin, db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(222), unique=True)
    email = db.Column(db.String(222))
    password = db.Column(db.String(222))
    def __init__(self,username,email,password):
        self.username=username
        self.email = email
        self.password = password
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=2, max=100)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=2, max=80)])
    remember = BooleanField('remember me')
class SignupForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=2, max=100)])
    email = StringField('email', validators=[InputRequired(),Email(message="invalid email"), Length(max=100)])
    password = PasswordField('password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
class contactme(db.Model):
    __tablename__="contactme"
    id = db.Column(db.Integer,primary_key=True)
    name =db.Column(db.String(22))
    email =db.Column(db.String(225))
    subject =db.Column(db.String(225))
    message =db.Column(db.Text())
    namet = db.Column(db.String(255))
    emailt = db.Column(db.String(255))
    phonet = db.Column(db.Text())
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    peoplet = db.Column(db.Integer)
    messaget = db.Column(db.String(255))
    def __init__(self,name,email,subject,message,namet,emailt,phonet,date,time,peoplet,messaget):
        self.name = name
        self.email = email
        self.subject = subject
        self.message = message
        self.namet = namet
        self.emailt = emailt
        self.phonet = phonet
        self.date = date
        self.time = time
        self.peoplet = peoplet
        self.messaget = messaget
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]
        namet="*"
        emailt="*"
        phonet=0
        date= datetime.datetime.utcnow()
        time=datetime.datetime.utcnow()
        peoplet=0
        messaget="*"
        new_message=contactme(name,email,subject,message,namet="*",emailt="*",phonet=0,date=date,time=time,peoplet=0,messaget="*")
        db.session.add(new_message)
        db.session.commit()
        send_mail(name,email,subject,message,namet,emailt,phonet,date,time,peoplet,messaget)

        return render_template("index.html", message="message Sent")
    return render_template("index.html")
@app.route("/booktable", methods=["POST","GET"])
def booktable():
    if request.method == "POST":
        name = "*"
        email = "*"
        subject = "*"
        message = "*"
        namet=request.form["namet"]
        emailt=request.form["emailt"]
        phonet= request.form["phonet"]
        date= datetime.datetime.utcnow()
        time=datetime.datetime.utcnow()
        peoplet= request.form["peoplet"]
        messaget=request.form["messaget"]
        new_message=contactme(name=name,email=email,subject=subject,message=message,namet=namet,emailt=emailt,phonet=phonet,date=date,time=time,peoplet=peoplet,messaget=messaget)
        db.session.add(new_message)
        db.session.commit()
        send_mail(name,email,subject,message,namet,emailt,phonet,date,time,peoplet,messaget)
     
        return render_template("book.html", messsage="table has been booked successfully")

    return render_template("book.html" )
@app.route('/about')
def about():
    return render_template("about.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        new_user = Users.query.filter_by(username=form.username.data).first()#check if user exists
        if new_user:#if it exists
            if check_password_hash(new_user.password,form.password.data): #comparing the stored password and the inputed password
                login_user(new_user,remember=form.remember.data)
                return render_template("index.html")

        return render_template("login.html", form = form, message="Invalid Password/Username ")
    return render_template("login.html", form=form)
@app.route("/signup", methods=["POST","GET"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.password.data, method="sha256")
        newx=Users.query.filter_by(username=form.username.data).first()# check if username already exist
        if newx: #if it exists, redirect to the register form, if it does not exist, go ahead and register user0
            return render_template("register.html", form=form, message="username is taken!, Choose another")
        new=Users(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(new)
        db.session.commit()
        return hashed_password
    return render_template("register.html", form=form)
@app.route("/rice")
def rice():
    return render_template('rice.html')
@app.route("/snacks")
def snacks():
    return render_template('snacks.html')
@app.route("/drinkz")
def drinkz():
    return render_template('drinkz.html')
@app.route("/swallow")
def swallow():
    return render_template('swallows.html')
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
if __name__ == "__main__":
    app.run(debug=True)