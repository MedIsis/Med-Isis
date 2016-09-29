import bcrypt
from flask import Flask, render_template, session, g, abort, request, url_for,flash,redirect
from flask_login import login_user, logout_user, LoginManager
from pymongo import MongoClient
from flask_pymongo import PyMongo

from werkzeug.security import generate_password_hash

import os
salt=bcrypt.gensalt()
connection=MongoClient('localhost',27017)
db=connection.Users

app=Flask(__name__)

@app.route('/')
def indexpage():
    return render_template('index.html')
@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        login_user = db.users.find_one({'username' : request.form['email']})
        print login_user['password'],login_user['username'],bcrypt.hashpw(request.form['password'].encode(),salt)
        if login_user:
            if bcrypt.hashpw(request.form['password'].encode(),login_user['password'].encode()) == login_user['password']:
                # session['username'] = request.form['username']
                return "yo success"
        return 'Invalid username/password combination'
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users =db.users
        existing_user = users.find_one({'username' : request.form['email']})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode(), salt)
            print hashpass
            users.insert({'username' : request.form['email'], 'password' : hashpass})
            print 'hi user entered'
            # session['username'] = request.form['email']
            return 'hello namaste'

        return 'That username already exists!'
    return render_template(('index.html'))


if __name__ == '__main__':
    app.run(host='localhost',port=1010)
