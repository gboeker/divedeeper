from flask import render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user
from db import *
from pymongo import *
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    data = db['users'].find_one({"user_id": user_id})
    if (data):
        return User(data['user_id'], data['password'])
    else:
        return None

class User(UserMixin):
    def __init__(self, user_id, password):
        self.id = user_id 
        self.password = password 

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

'''
NOTE: 
To get the active user from anywhere else or a different file 
you need to import flask_login first then you can retrieve the active user with current_user
Example:
    from flask_login import current_user
    user = current_user
'''

def auth_login():
    collections = db.list_collection_names()
    if request.method == 'POST':
        # TODO: Log the user in
        # TODO: Redirect to the appropriate page for the logged in user
        return redirect('/')
    else:
        return render_template('login.html')


def auth_signup():
    if request.method == 'POST':
        user_id = request.form["username"]
        password = request.form["password"]
        confirm_password =  request.form["confirm-password"]
        if (load_user(user_id)):
            return render_template('signup.html', username_taken=True, passwords_dont_match=False)
        elif(password != confirm_password):
            return render_template('signup.html', username_taken=False, passwords_dont_match=True)
        else:
            user = User(user_id, generate_password_hash(password))
            db['users'].insert_one({"user_id": user.id, "password": user.password})
            login_user(user)
            # TODO: Redirect to the appropriate page for the logged in user
            return redirect('/')

    else:
        return render_template('signup.html', username_taken=False, passwords_dont_match=False)



