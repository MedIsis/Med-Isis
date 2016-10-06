import bcrypt
from flask import Flask, render_template, session, g, abort, request, url_for,flash,redirect
from flask_login import login_user, logout_user, LoginManager
from pymongo import MongoClient
import pymongo
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
                session['username'] = request.form['email']
                print session['username']
                return redirect(url_for('profile'))
        return 'Invalid username/password combination'
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users =db.users
        existing_user = users.find_one({'username' : request.form['email']})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode(), salt)
            users.insert({'username' : request.form['email'], 'password' : hashpass})
            session['username'] = request.form['email']
            db.profile.insert({'ref_id':session['username']})
            # print 'hi user entered'

            return redirect(url_for('profile'))

        return 'That username already exists!'
    print session['username']
    return render_template('index.html')

@app.route('/profile',methods=['GET', 'POST'])
def profile():
    if   request.method=='POST':
        db.profile.insert({'first_name':request.form['first_name'],'phno':request.form['phno'],'allergies':request.form['allergies'],'diabeties':request.form['diabeties'],'heart':request.form['heart'],'dob':request.form['dob'],'last_name':request.form['last_name'],'email':request.form['email'],'gender':request.form['gender'],'panno':request.form['panno'],'m1':request.form['m1'],'t1':request.form['t1'],'blood_group':request.form['blood_group'],'emrcntct':request.form['emrcntct'],'bp':request.form['bp']})
        print 'everything inserted'
        # render_template('profile.html',)
    if request.method=='POST':
        if 'username' in session:

            # print session['username']
            curuser=db.profile.find_one({'ref_id':session['username']})
            db.profile.update_one({'ref_id':session['username']},{'$set':{'first_name':request.form['first_name'],'phno':request.form['phno'],'allergies':request.form['allergies'],'diabeties':request.form['diabeties'],'heart':request.form['heart'],'dob':request.form['dob'],'last_name':request.form['last_name'],'email':request.form['email'],'gender':request.form['gender'],'blood_group':request.form['blood_group'],'emrcntct':request.form['emrcntct'],'bp':request.form['bp']}},upsert=False)

            print 'everything inserted'

            return redirect(url_for('profile'))
        return redirect(url_for('home'))
    return render_template('profile.html')


@app.route('/displayprofile',methods=['GET','POST'])
def displayprofile():
    curuser=db.profile.find_one({'ref_id':session['username']})
    print session['username']
    return render_template('profile.html',curuser=curuser)




if __name__ == '__main__':
    app.run(host='localhost',port=1010)
