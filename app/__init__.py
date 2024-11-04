# Chalice: Anastasia, Andy, Jack, Jady
# SoftDev
# October 2024

import os
import sqlite3
from flask import Flask, session, render_template, request, redirect

app = Flask(__name__)    #create Flask object

app.secret_key = os.urandom(32)

@app.route("/", methods=['GET', 'POST'])
def home():
    if 'username' in session:
        return render_template( 'response.html', username = session['username'] )
    # return render_template('home.html')
    return redirect("/login")

@app.route("/registerer", methods=["POST"])
def registerer():
    return redirect("/register")

@app.route("/loginer", methods=["POST"])
def loginer():
    return redirect("/login")

@app.route("/register", methods=['GET', 'POST'])
def register():
    user_file = "users.db"

    user = sqlite3.connect(user_file)
    cUser = user.cursor() 
    if request.method == 'POST':
        print("hi")
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
                session['username']=password
                session['password']=username
                return redirect("/")
            except sqlite3.IntegrityError:
                return render_template('register.html', message="Integrity Error")
        user.commit()
        return render_template('register.html', message = "Username taken")
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
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
            return render_template('login.html', message="Username does not exist; please register before logging in.")
        if 'username' in session and session['password'] == res[0]:
            return redirect("/")
        session.pop('username', None)
        session.pop('password', None)
        return render_template('login.html', message = "Invalid login; please try again.")
    return render_template('login.html')

@app.route("/logout", methods=['POST'])
def disp_logout():
    session.pop('username', None)
    session.pop('password', None)
    return render_template( 'logout.html' )

@app.route("/main", methods=['POST'])
def main():
    return render_template("home.html")
    
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
