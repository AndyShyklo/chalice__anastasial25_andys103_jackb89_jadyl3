# Chalice: Anastasia, Andy, Jack, Jady
# SoftDev
# October 2024

import os
import sqlite3
from datetime import datetime
from flask import Flask, session, render_template, request, redirect
from story_database import *

app = Flask(__name__)    #create Flask object

app.secret_key = os.urandom(32)

@app.route("/", methods=['GET', 'POST'])
def home():
    if 'username' in session:
        return render_template( 'response.html', username = session['username'] )
    return render_template('home.html')

@app.route("/register", methods=["POST"])
def register():
    return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    print("hi")
    return render_template("login.html")

@app.route("/registerauth", methods=['GET', 'POST'])
def registerer():
    user_file = "users.db"

    user = sqlite3.connect(user_file)
    cUser = user.cursor() 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cUser.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, access TEXT, viewable TEXT, editable TEXT)")
        fetc = cUser.execute("SELECT username, password, access FROM users")
        print(fetc.fetchall())
        if not (username and password):
            return render_template('register.html', message = "One or more fields empty; please try again.")
        print((cUser.execute("SELECT 1 FROM users WHERE username=?", (username,))).fetchone())
        print((cUser.execute("SELECT 1 FROM users WHERE username=?", (username,))).fetchone() == None)
        if (cUser.execute("SELECT 1 FROM users WHERE username=?", (username,))).fetchone() == None:
            try:
                cUser.execute("INSERT INTO users (username, password, access) VALUES (?, ?, ?)", (username, password, "Normal"))
                user.commit()
                session['username']=username
                session['password']=password
                return redirect("/login")
            except sqlite3.IntegrityError:
                return render_template('register.html', message="Integrity Error")
        user.commit()
        return render_template('register.html', message = "Username taken")
    return render_template('register.html')

@app.route("/loginauth", methods=['GET', 'POST'])
def loginer():
    user_file = "users.db"

    user = sqlite3.connect(user_file)
    cUser = user.cursor() 
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        cUser.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, access TEXT, viewable TEXT, editable TEXT)")
        cUser.execute("SELECT password FROM users WHERE username=?", (request.form['username'],))
        res = cUser.fetchone()
        if res is None:
            session.pop('username', None)
            session.pop('password', None)
            return render_template('login.html', message="Username does not exist; please register before logging in.")
        if 'username' in session and session['password'] == res[0]:
            return redirect("/")
        session.pop('username', None)
        session.pop('password', None)
        return render_template('login.html', message = "Invalid login; please try again.")
    return render_template('login.html')

@app.route("/display", methods=['POST'])
def display():
    user_file = "users.db"

    user = sqlite3.connect(user_file)
    cUser = user.cursor() 
    cUser.execute("SELECT * FROM users")
    res = cUser.fetchall()
    fst = "hiiii"
    for row in res:
        fst = fst + "[" + str(row) + "]"
    return(render_template('login.html', message = fst))

@app.route("/logout", methods=['POST'])
def disp_logout():
    session.pop('username', None)
    session.pop('password', None)
    return render_template( 'logout.html' )

# @app.route("/main", methods=['POST'])
# def main():
#     return render_template("home.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    return render_template( 'create.html' )

@app.route("/creator", methods=["GET", "POST"])
def creator():
    if request.method == 'POST':
        title = request.form['title']
        first = request.form['first']
        if (not (title and first)):
            return render_template( 'create.html', message="please enter a title and a first sentence")
        addStory(title, session['username'], first, datetime.now())
        return redirect("/")
    return render_template( 'create.html' )
    
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
