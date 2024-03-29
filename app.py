from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired
from sqlalchemy import Table, create_engine, MetaData
import mysql.connector
import sqlite3
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import os
import PBI_python_module as pb
import requests
from sqlalchemy import create_engine

#Create flask instance

app = Flask(__name__)

# connect to Render database OR local database
def connectDB():
    try:
        engine = create_engine('sqlite:////Users/ruarihodgin/Desktop/Lucid/Biostrain/Biostrain-web-portal-main/biostrain.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/ruarihodgin/Desktop/Lucid/Biostrain/Biostrain-web-portal-main/biostrain.db'
        debugStatus = True

    except:
        engine = create_engine('sqlite:////home/biostrain/Biostrain-web-portal/biostrain.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/biostrain/Biostrain-web-portal/biostrain.db'
        debugStatus = False

    return engine, debugStatus

engine, debugStatus = connectDB()
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

    __tablename__ = 'Login'

    def __repr__(self):
        return '<User ID %r>' % self.id

class PlayerProfiles(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    Org = db.Column(db.VARCHAR(45))
    User = db.Column(db.VARCHAR(45))
    Gender = db.Column(db.VARCHAR(1))
    Weight = db.Column(db.Float)
    Height = db.Column(db.Float)
    loginID = db.Column(db.Integer, nullable=False)

    __tablename__ = 'Playerprofiles'

    def __repr__(self):
        return '<User Index %r>' % self.Index


#Create data model
class PlayerData(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    Org = db.Column(db.Text)
    User = db.Column(db.Text)
    Timestamp = db.Column(db.Integer)
    Protocol = db.Column(db.Text)
    Phase = db.Column(db.Integer)
    Strategy = db.Column(db.Text)
    Matchday = db.Column(db.Text)
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
    loginID = db.Column(db.Integer, nullable=False)

    __tablename__ = 'Playerdata'

    def __repr__(self):
        return '<User Index %r>' % self.Index



class loginForm(FlaskForm):
    uname = StringField("Enter username", validators=[DataRequired()])
    pwd = PasswordField("Enter password", validators=[DataRequired()])
    submit = SubmitField("Login")

class playerForm(FlaskForm):
    squad = SelectField("Select squad", choices=[], validators=[DataRequired()])
    name = SelectField("Select player", choices=[], validators=[DataRequired()])
    submit = SubmitField("Take me there")

class squadForm(FlaskForm):
    org = SelectField("Select squad to view", choices=[], validators=[DataRequired()])
    pro = SelectField("Select protocol", choices=[], validators=[DataRequired()])
    submit = SubmitField("Take me there")

#Create routes (pages)

#login page
@app.route('/', methods=['GET', 'POST'])
def login():
    uname = None
    pwd = None
    form = loginForm()
    #validate form
    if form.validate_on_submit():
        user = Login.query.filter_by(username=form.uname.data).first()
        ID = user.id
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
    return redirect(url_for('login'))

#user hub page
@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    squadform = squadForm(request.form)
    playerform = playerForm(request.form)
    form = {
            'squad':squadform,
            'player':playerform
            }
    uname = current_user.username
    user = Login.query.filter_by(username=uname).first()
    player_profiles = PlayerProfiles.query.filter_by(loginID=current_user.id).all()
    squads = list(set([player.Org for player in player_profiles]))
    squads.sort()
    try:
        player_data = PlayerData.query.filter_by(Org=squads[0], loginID=current_user.id).all()
        pros = list(set([player.Protocol for player in player_data]))
        squadform.org.choices = [squad for squad in squads]
        squadform.pro.choices = [pro for pro in pros]
        playerform.squad.choices = squads
        playerform.name.choices = [player.User for player in PlayerProfiles.query.filter_by(Org=squads[0], loginID=current_user.id).all()]
    except:
        squadform.org.choices = ['No squad data - create user profiles on your Biostrain app!']
        squadform.pro.choices = []
        playerform.squad.choices = ['No squad data - create user profiles on your Biostrain app!']
        playerform.name.choices = []

    if request.method == 'POST' and squadform.validate:
        try:
            org = request.form['org']
            pro = request.form['pro']
            squadTestData = PlayerData.query.filter_by(loginID=current_user.id, Org=org, Protocol=pro)
            squadProData, squadProDateData, allTests, allDates, testDates, squadData = pb.getSquadDict(squadTestData, pro)
            return render_template('squad.html',
                                   squadData=squadData,
                                   pro=pro,
                                   squadProData=squadProData,
                                   squadProDateData=squadProDateData,
                                   allDates=allDates,
                                   allTests=allTests,
                                   testDates=testDates
                                   )
        except:
            org = request.form['squad']
            name = request.form['name']
            playerTestData = PlayerData.query.filter_by(User=name, Org=org, loginID=current_user.id)
            sessions, lastBaseline, baselineList, baselineProtocolList, \
            lastFatigue, fatigueList, fatigueProtocolList, dates, numTests = pb.getPlayerDict(playerTestData)
            playerSessions = pb.getSessions(sessions)
            tableList = pb.getSessionTables(playerSessions)
            playerTags = pb.getPlayerTags(playerSessions)
            sessionList = list(playerSessions)
            selectedSession = request.args.get('tabular-session-select')
            playerinfo_content = render_template('playerinfo.html',
                                                 name=name,
                                                 org=org,
                                                 playerSessions=playerSessions,
                                                 sessionList=sessionList,
                                                 dates=dates,
                                                 numTests=numTests
                                                 )
            sessionselector_content = render_template('sessionselector.html',
                                                      playerSessions=playerSessions,
                                                      sessionList=sessionList[::-1],
                                                      sessions=sessions,
                                                      tableList=tableList[::-1],
                                                      selectedSession=selectedSession
                                                      )
            progresstracker_content = render_template('progresstracker.html',
                                                      playerSessions=playerSessions,
                                                      playerTags=playerTags,
                                                      sessionList=sessionList)
            return render_template('playernew.html',
                                   playerinfo_content=playerinfo_content,
                                   sessionselector_content=sessionselector_content,
                                   progresstracker_content=progresstracker_content)

    return render_template('dashboard.html', form=form)

@app.route('/squad', methods=["GET", "POST"])
@login_required
def squadPage():

    return render_template('squad.html')


@app.route('/ifu', methods=["GET", "POST"])
@login_required
def ifu():

    return render_template('ifu.html')

@app.route('/device', methods=["GET", "POST"])
@login_required
def device():

    return render_template('device.html')


@app.route('/player/<squad>')
@login_required
def playerSelect(squad):
    uname = current_user.username
    players = PlayerProfiles    .query.filter_by(loginID=current_user.id, Org=squad).all()

    playerArray=[]

    for player in players:
        playerObj = {}
        playerObj['id'] = player.id
        playerObj['name'] = player.User
        playerArray.append(playerObj)


    return jsonify({'players' : playerArray})

@app.route('/pro/<squad>')
@login_required
def squadSelect(squad):
    uname = current_user.username
    protocols = PlayerData.query.filter_by(loginID=current_user.id, Org=squad).all()

    proArray=[]

    for protocol in protocols:
        proObj = {}
        proObj['id'] = protocol.id
        proObj['name'] = protocol.Protocol
        proArray.append(proObj)


    return jsonify({'protocols' : proArray})

@app.route('/playernew')
@login_required
def playernew():

    return render_template('playernew.html')



#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Invternal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=debugStatus)