from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
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


#Create routes (pages)
# home page
@app.route('/')
def home():
    return render_template('home.html')

#register account page
@app.route('/register')
def register():
    return render_template('register.html')

#login page
@app.route('/login')
def login():
    return render_template('login.html')

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
