from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired
from sqlalchemy import Table, create_engine
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import os
import pandas as pd
import PBI_python_module as pb
import numpy as np
from datetime import datetime
import flask.json
import json




#Create flask instance
def init_app():
    app = Flask(__name__)
    with app.app_context():
        from plotlydash.dashboard import init_dashboard, init_callbacks
        app = init_dashboard(app)
        with app.app_context():
            init_callbacks(app)
    return app
app = init_app()
#Add database
engine = create_engine('mysql+pymysql://root:jqtnnhj2@localhost/userinfo')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:jqtnnhj2@localhost/userinfo'
app.config['SECRET_KEY'] = os.urandom(12)
#Initialise database
with app.app_context():
    db = SQLAlchemy(app)
#Flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Login.query.get(int(user_id))


#Create user model
class Login(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<User ID %r>' % self.id

class Playerprofiles(db.Model, UserMixin):
    Index = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    Org = db.Column(db.VARCHAR(45))
    User = db.Column(db.VARCHAR(45))

    def __repr__(self):
        return '<User Index %r>' % self.Index

#Create data model
class Testdatalog(db.Model, UserMixin):
    Index = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    Org = db.Column(db.Text)
    User = db.Column(db.Text)
    Timestamp = db.Column(db.DateTime)
    Protocol = db.Column(db.Text)
    TZ = db.Column(db.Text)
    Left0ms = db.Column(db.Float)
    Left50ms = db.Column(db.Float)
    Left100ms = db.Column(db.Float)
    Left150ms = db.Column(db.Float)
    Left200ms = db.Column(db.Float)
    Left250ms = db.Column(db.Float)
    Left300ms = db.Column(db.Float)
    Leftpeak = db.Column(db.Float)
    Right0ms = db.Column(db.Float)
    Right50ms = db.Column(db.Float)
    Right100ms = db.Column(db.Float)
    Right150ms = db.Column(db.Float)
    Right200ms = db.Column(db.Float)
    Right250ms = db.Column(db.Float)
    Right300ms = db.Column(db.Float)
    Rightpeak = db.Column(db.Float)
    Combined0ms = db.Column(db.Float)
    Combined50ms = db.Column(db.Float)
    Combined100ms = db.Column(db.Float)
    Combined150ms = db.Column(db.Float)
    Combined200ms = db.Column(db.Float)
    Combined250ms = db.Column(db.Float)
    Combined300ms = db.Column(db.Float)
    Combinedpeak = db.Column(db.Float)

    def __repr__(self):
        return '<User Index %r>' % self.Index

class loginForm(FlaskForm):
    uname = StringField("Enter username", validators=[DataRequired()])
    pwd = PasswordField("Enter password", validators=[DataRequired()])
    submit = SubmitField("Login")

class playerForm(FlaskForm):
    squad = SelectField("Select squad", choices=['Senior squad (men)', 'U21 squad (men)'], validators=[DataRequired()])
    name = SelectField("Select player", choices=[], validators=[DataRequired()])
    submit = SubmitField("Take me there")

class squadForm(FlaskForm):
    squad = SelectField("Select squad to view", choices=['Senior squad (men)', 'U21 squad (men)'], validators=[DataRequired()])
    pro = SelectField("Select protocol", choices=[], validators=[DataRequired()])
    submit = SubmitField("Update figures")

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
        user = Login.query.filter_by(username=form.uname.data).first()
        if user is None:
            flash("Username incorrect, please try again.")
        else:
            if check_password_hash(user.password,form.pwd.data):
                flash("Login Successful!")
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect password, please try again.")
    return render_template('login.html',
                            uname = uname,
                            pwd = pwd,
                            form = form
                           )

#Logout functionality
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('home'))

#user hub page
@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    form = playerForm()
    form.name.choices = [player.User for player in Playerprofiles.query.filter_by(Org='Senior squad (men)').all()]

    if request.method == "POST":
        name = request.form['name']
        playerTestData = Testdatalog.query.filter_by(User=name)
        baselineMax, fatigueMax = pb.playerPlot(playerTestData)
        index = [row[0] for row in baselineMax]
        protocol = [row[1] for row in baselineMax]
        label = [row[2] for row in baselineMax]
        score = [row[3] for row in baselineMax]
        tz = [row[4] for row in baselineMax]
        timestamp = [row[5] for row in baselineMax]

        barDict = {}
        for pro in protocol:
            barDict[pro]={}
        for pro in barDict:
            for type in label:
                barDict[pro][type]=[]

        for i in range(len(score)):
            for pro in barDict:
                for type in barDict[pro]:
                    if protocol[i] == pro:
                        if label[i] == type:
                            barDict[pro][type].append(score[i])

        return render_template('player.html',
                               name=name,
                               index=index,
                               protocol=protocol,
                               label=label,
                               score=score,
                               tz=tz,
                               timestamp=timestamp,
                               barDict = barDict)

    return render_template('dashboard.html', form=form)

@app.route('/squad', methods=["GET", "POST"])
@login_required
def squad():
    df = pd.read_csv('database.csv')
    userlist = df['User'].unique()
    orglist = df['Org'].unique()
    prolist = df['Protocol'].unique()
    return render_template('squad.html', userlist=userlist, orglist=orglist, df=df, prolist=prolist)

@app.route('/player', methods=["GET", "POST"])
@login_required
def player():
    user = request.playerForm['name']


    return render_template('player.html')


@app.route('/player/<squad>')
@login_required
def playerSelect(squad):
    players = Playerprofiles.query.filter_by(Org=squad).all()

    playerArray=[]

    for player in players:
        playerObj = {}
        playerObj['id'] = player.Index
        playerObj['name'] = player.User
        playerArray.append(playerObj)


    return jsonify({'players' : playerArray})

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
