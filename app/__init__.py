# Chalice: Anastasia, Andy, Jack, Jady
# SoftDev
# October 2024

import os
from flask import Flask, session, render_template, request, redirect
from story_database import *
from user_database import *

app = Flask(__name__)    #create Flask object

app.secret_key = os.urandom(32)

@app.route("/", methods=['GET', 'POST'])
def home():
    createStories()
    createUsers()
    if 'username' not in session:
        return render_template('home.html')
    viewList = makeViewList(session['username'])
    if viewList:
        return render_template("response.html", username = session['username'], rows = viewList)
    return render_template("response.html", username = session['username'], message = "None yet!")
    
@app.route("/register", methods=['GET', "POST"])
def register():
    message=request.args.get('message', "")
    return render_template("register.html", message=message)

@app.route("/login", methods=['GET', 'POST'])
def login():
    message=request.args.get('message', "")
    return render_template("login.html", message=message)

@app.route("/registerauth", methods=['GET', 'POST'])
def registerer():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not (username and password):
            return render_template("register.html", message = "One or more fields empty; please try again.")
        message = addUser(username, password)
        if (message):
            return render_template('register.html', message = message)
        session['username'] = username
        session['password'] = password
        return redirect("/")
    return redirect("/register")

@app.route("/loginauth", methods=['GET', 'POST'])
def loginer():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not (username and password):
            return render_template("login.html", message = "One or more fields empty; please try again.")
        message = checkLogin(username, password)
        if (message):
            return render_template("login.html", message = message)
        session['username'] = username
        session['password'] = password
        return redirect("/")
    return redirect("/login")

@app.route("/logout", methods=['GET', 'POST'])
def disp_logout():
    session.pop('username', None)
    session.pop('password', None)
    return render_template( 'logout.html' )

@app.route("/create", methods=["GET", "POST"])
def create():
    if 'username' not in session:
        return redirect('/login')
    return render_template( 'create.html' )

@app.route("/creator", methods=["GET", "POST"])
def creator():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        title = request.form['title']
        first = request.form['first']
        if not (title and first):
            return render_template( 'create.html', message="One or more fields empty; please try again.")
        id = addStory(title, session['username'], first)
        newStory(session['username'], id)
        return redirect("/")
    return redirect("/create")
    
@app.route("/editable", methods = ["GET", "POST"])
def editable():     
    if 'username' not in session:
        return redirect('/login')
    
    editList = makeEditList(session['username'])
    if editList:
        return render_template("editable.html", rows = editList)
    return render_template("editable.html", message = "No editable stories...yet!")
    
@app.route("/edit", methods=["GET", "POST"])
def edit():
    if 'username' not in session:
        return redirect('/login')
    
    story_id = request.args.get('story_id')
    if not story_id:
        return redirect("/editable")
    
    story = [story_id, returnStoryTitle(story_id), returnChapters(story_id), returnAuthor(story_id)]
    return render_template("edit.html", story = story)

@app.route("/editcomplete", methods=["GET", "POST"])
def editcomplete():
    if 'username' not in session:
        return redirect('/login')
    
    id = request.args.get('story')
    if request.method == 'GET':
        content = request.args.get("new_chapter")
        if not content:
            story = [id, returnStoryTitle(id), returnChapters(id), returnAuthor(id)]
            return render_template("edit.html", story=story, message="Please enter content for the new chapter.")
        editStory(id, content, session['username'])
        return redirect("/editable")
    return redirect("/edit")
        

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
