from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from sqlalchemy import Table, create_engine
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import os
import pandas as pd
from datetime import datetime




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

class loginForm(FlaskForm):
    uname = StringField("Enter username", validators=[DataRequired()])
    pwd = PasswordField("Enter password", validators=[DataRequired()])
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

#data page
@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    df = pd.read_csv('database.csv')
    userlist = df['User'].unique()
    orglist = []
    for user in userlist:
        for i in range(len(df)):
            if df['User'][i] == user:
                orglist.append(df['Org'][i])
                break
    return render_template('dashboard.html', userlist=userlist, orglist=orglist, df=df)

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
