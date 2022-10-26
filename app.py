from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from sqlalchemy import Table, create_engine
import os
import pandas as pd
from datetime import datetime




#Create flask instance
app = Flask(__name__)
#Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = os.urandom(12)
#Initialise database
db = SQLAlchemy(app)

#Create user model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    sname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    org = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    uname = db.Column(db.String(50), nullable=False, unique=True)
    pwd = db.Column(db.String(50), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    #Create a string
    def __repr__(self):
        return '<Username %r>' % self.uname

with app.app_context():
    db.create_all()

#Create form class

class registerForm(FlaskForm):
    fname = StringField("Enter first name", validators=[DataRequired()])
    sname = StringField("Enter surname", validators=[DataRequired()])
    uname = StringField("Enter username", validators=[DataRequired()])
    pwd = StringField("Enter password", validators=[DataRequired()])
    repwd = StringField("Re-enter password", validators=[DataRequired()])
    email = StringField("Enter email address", validators=[DataRequired()])
    org = StringField("Select your organisation", validators=[DataRequired()])
    role = StringField("Select your role", validators=[DataRequired()])
    submit = SubmitField("Register")

class loginForm(FlaskForm):
    uname = StringField("Enter username", validators=[DataRequired()])
    pwd = StringField("Enter password", validators=[DataRequired()])
    submit = SubmitField("Login")

#Create routes (pages)
# home page
@app.route('/')
def home():
    return render_template('home.html')

#login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    uname = None
    pwd = None
    form = loginForm()
    #validate form
    if form.validate_on_submit():
        uname=form.uname.data
        pwd=form.pwd.data
        form.uname.data=''
        form.pwd.data=''
        flash("Login successful")
    return render_template('login.html',
                            uname = uname,
                            pwd = pwd,
                            form = form
                           )

#register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    fname = None
    sname = None
    uname = None
    pwd = None
    repwd = None
    email = None
    org = None
    role = None
    form = registerForm
    if form.validate_on_submit():
        user = Users.query.filter_by(uname = form.uname.data).first
        if user is None:
            uemail = Users.query.filter_by(email = form.email.data).first
            if uemail is None:
                user = Users(fname=form.fname.data, sname=form.sname.data,
                             uname=form.uname.data, pwd=form.pwd.data,
                             email=form.email.data, org=form.org.data,
                             role=form.role.data)
                db.session.add(user)
                db.session.commit()
                flash("Account created succesfully")
    return render_template('register.html',
                           fname=fname,
                           sname=sname,
                           uname=uname,
                           pwd=pwd,
                           repwd=repwd,
                           email=email,
                           org=org,
                           role=role,
                           form=form
                           )

#data page
@app.route('/data/<fname>+<sname>')
def data(fname, sname):
    return render_template('data.html', fname=fname, sname=sname)

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Invternal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500




if __name__ == '__main__':
    app.run(debug=True)
