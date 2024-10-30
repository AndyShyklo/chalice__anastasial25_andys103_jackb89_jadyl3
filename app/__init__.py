# Chalice: Anastasia, Andy, Jack, Jady
# SoftDev
# October 2024

import os
from flask import Flask, session, render_template, request, redirect
PASSWORD = "hello"

app = Flask(__name__)    #create Flask object

app.secret_key = os.urandom(32)

@app.route("/", methods=['GET', 'POST'])
def home():
    if 'username' in session:
        return render_template( 'response.html', username = session['username'] )
    # return render_template('home.html')
    return redirect("/login")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not (username and password):
            return render_template('register.html', message = "One or more fields empty; please try again.")
        return redirect("/login")
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        if 'username' in session and session['password'] == PASSWORD:
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
    
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
