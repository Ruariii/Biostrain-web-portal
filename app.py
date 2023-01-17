from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired
from sqlalchemy import Table, create_engine
import mysql.connector
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import os
import PBI_python_module as pb




#Create flask instance

app = Flask(__name__)

#Add database (local machine database)
# engine = create_engine('mysql+pymysql://root:jqtnnhj2@localhost/userinfo')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:jqtnnhj2@localhost/userinfo'
# #Render MySQL Docker connection
# database = os.environ['MYSQL_DATABASE']
# user = os.environ['MYSQL_USER']
# password = os.environ['MYSQL_PASSWORD']
# root_password = os.environ['MYSQL_ROOT_PASSWORD']
# port = os.environ['MYSQL_PORT']
# engine = create_engine(f'mysql+pymysql://{user}:{password}@{port}/{database}')
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{port}/{database}'


# connect to Render database OR local database
def connectDB():
    try:
        database = os.environ['MYSQL_DATABASE']
        user = os.environ['MYSQL_USER']
        password = os.environ['MYSQL_PASSWORD']
        root_password = os.environ['MYSQL_ROOT_PASSWORD']
        port = os.environ['MYSQL_PORT']
        engine = create_engine(f'mysql+pymysql://{user}:{password}@{port}/{database}')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{port}/{database}'
        # test connection
        connection = mysql.connector.connect(user=user, password=password, host=port, database=database)
    except:
        engine = create_engine('mysql+pymysql://root:jqtnnhj2@localhost/userinfo')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:jqtnnhj2@localhost/userinfo'
    return engine

engine = connectDB()
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
    Gender = db.Column(db.VARCHAR(1))
    Weight = db.Column(db.Float)
    Height = db.Column(db.Float)

    def __repr__(self):
        return '<User Index %r>' % self.Index

#Create data model
class Testdatalog(db.Model, UserMixin):
    Index = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    Org = db.Column(db.Text)
    User = db.Column(db.Text)
    Timestamp = db.Column(db.Date)
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
    org = SelectField("Select squad to view", choices=['Select squad:', 'Senior squad (men)', 'U21 squad (men)'], validators=[DataRequired()])
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
    playerform.name.choices = [player.User for player in Playerprofiles.query.filter_by(Org='Senior squad (men)').all()]

    if request.method == 'POST' and squadform.validate:
        try:
            org = request.form['org']
            pro = request.form['pro']
            squadTestData = Testdatalog.query.filter_by(Org=org, Protocol=pro)
            squadPlayers = Playerprofiles.query.filter_by(Org=org)
            dataArray, dataArrayHead, countExt, timeStr,\
            players, bestPeak, best150, FLpeakAsym, \
            BLpeakAsym, FL150Asym, BL150Asym, = pb.squadPlot(squadTestData, squadPlayers, pro)
            return render_template('squad.html',
                                   pro=pro,
                                   dataArray=dataArray,
                                   dataArrayHead=dataArrayHead,
                                   timeStr=timeStr,
                                   countExt=countExt,
                                   best150=best150,
                                   bestPeak=bestPeak,
                                   players=players,
                                   FL150Asym=FL150Asym,
                                   FLpeakAsym=FLpeakAsym,
                                   BLpeakAsym=BLpeakAsym,
                                   BL150Asym=BL150Asym)
        except:
            name = request.form['name']
            playerTestData = Testdatalog.query.filter_by(User=name)
            user = Playerprofiles.query.filter_by(User=name).first()
            height = user.Height
            weight = user.Weight
            baselineMax, timeStr, countExt, proArray, \
            radarLabels, radarDataL, radarDataR, fPlotDictL, \
            fLabelDictL, fPlotDictR, fLabelDictR, fAsymDict, \
            flAsym, blAsym, dataArrayHead = pb.playerPlot(playerTestData, name)
            results = pb.get_scores(playerTestData)
            report = pb.generate_report(results)

            index = [row[0] for row in baselineMax]
            protocol = [row[1] for row in baselineMax]
            label = [row[2] for row in baselineMax]
            score = [row[3] for row in baselineMax]
            tz = [row[4] for row in baselineMax]
            timestamp = [row[5] for row in baselineMax]
            specificScore = [100 * (force / weight) for force in score]
            specificRadarL = [100 * (force / weight) for force in radarDataL]
            specificRadarR = [100 * (force / weight) for force in radarDataR]

            return render_template('player.html',
                                   name=name,
                                   index=index,
                                   protocol=protocol,
                                   label=label,
                                   score=score,
                                   tz=tz,
                                   timestamp=timestamp,
                                   timeStr=timeStr,
                                   specificScore=specificScore,
                                   radarLabels=radarLabels,
                                   specificRadarL=specificRadarL,
                                   specificRadarR=specificRadarR,
                                   countExt=countExt,
                                   fPlotDictL=fPlotDictL,
                                   fLabelDictL=fLabelDictL,
                                   fPlotDictR=fPlotDictR,
                                   fLabelDictR=fLabelDictR,
                                   fAsymDict=fAsymDict,
                                   flAsym=flAsym,
                                   blAsym=blAsym,
                                   dataArrayHead=dataArrayHead,
                                   report=report
                                   )

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
    players = Playerprofiles.query.filter_by(Org=squad).all()

    playerArray=[]

    for player in players:
        playerObj = {}
        playerObj['id'] = player.Index
        playerObj['name'] = player.User
        playerArray.append(playerObj)


    return jsonify({'players' : playerArray})

@app.route('/pro/<squad>')
@login_required
def squadSelect(squad):
    protocols = Testdatalog.query.filter_by(Org=squad).all()

    proArray=[]

    for protocol in protocols:
        proObj = {}
        proObj['id'] = protocol.Index
        proObj['name'] = protocol.Protocol
        proArray.append(proObj)


    return jsonify({'protocols' : proArray})

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Invternal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500




#if __name__ == '__main__':
    #app.run(debug=True)
