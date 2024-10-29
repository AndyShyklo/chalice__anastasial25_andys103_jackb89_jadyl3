# Chalice: Anastasia, Andy, Jack, Jady
# SoftDev
# October 2024

import os
from flask import Flask, session, render_template, request, url_for, redirect
PASSWORD = "hello"

app = Flask(__name__)    #create Flask object

app.secret_key = os.urandom(32)

@app.route("/", methods=['GET', 'POST'])
def home():
    if 'username' in session:
        if session['password'] == PASSWORD:
            return render_template( 'response.html', username = session['username'] )
        session.pop('username', None)
        session.pop('password', None)
        return render_template( 'login.html', wrong_pass = True )
    return render_template( 'login.html', wrong_pass = False )

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        return redirect(url_for('home'))
    return "Bad request method"

@app.route("/logout", methods=['POST'])
def disp_logout():
    session.pop('username', None)
    session.pop('password', None)
    return render_template( 'logout.html' )
    
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
