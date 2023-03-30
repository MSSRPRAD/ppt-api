import string
import sys

from flask import Flask, render_template, redirect, url_for, flash, session, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required, login_user, LoginManager, current_user, logout_user
import os
from flask_bcrypt import Bcrypt

import chat
import ppt

app = Flask(__name__)

bcrypt = Bcrypt(app)

basedir = os.path.abspath(os.path.dirname(__file__))

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

app.config['SECRET_KEY'] = "secretkey"

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Error:
    message = string

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable = False)
    password = db.Column(db.String(100), nullable = False)
    requests = db.relationship('Request', backref = 'user')

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(5000), nullable = True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user:
        session.clear()
        flash("If you try to open this page after logging in you will be logged out automatically!")
        logout_user()
        redirect(url_for('login'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                flash("")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password. Please Try Again!")
        else:
            flash("Invalid Credentials. Please Try Again!")
    return render_template('login.html')

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard', methods = ['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password)
        new_user = User(username=username, password = hashed_password)
        existing_user = User.query.filter_by(username=username).first()
        if (existing_user):
            # print('\nAlready Exists Error!\n', file=sys.stderr)
            flash("That name is already taken, please choose another")
            return render_template('register.html')
        else:
            db.session.add(new_user)
            db.session.commit()
            flash("")
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/delete/user')
@login_required
def deleteUser():
    user = current_user
    if user:
        User.query.filter_by(id=user.id).delete()
        logout_user()
        db.session.commit()
        return redirect(url_for('home'))

@app.route('/dashboard/create', methods=['POST','GET'])
@login_required
def create():
    if request.method == 'POST':
        req = Request()
        req.user=current_user
        content=request.form['content']
        content = chat.chat(content, current_user.username)
        req.content=content
        db.session.add(req)
        db.session.commit()
        ppt.ppt(current_user.username)
        path = current_user.username+".pptx"
        return send_file(path, as_attachment=True)
    return "THERE WAS AN ERROR WHILE ADDING THE TASK!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
