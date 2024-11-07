# Chalice: Anastasia, Andy, Jack, Jady
# SoftDev
# October 2024

import os
import sqlite3
from flask import Flask, session, render_template, request, redirect
from story_database import *

app = Flask(__name__)    #create Flask object

app.secret_key = os.urandom(32)

@app.route("/", methods=['GET', 'POST'])
def home():
    # def test():
    #     return render_template('story.html')

    db = sqlite3.connect("stories.db") 
    c = db.cursor()
    command = "CREATE TABLE IF NOT EXISTS stories (story_id INTEGER PRIMARY KEY AUTOINCREMENT, story_name text NOT NULL, chapter_count INT)"
    c.execute(command)
    command = "CREATE TABLE IF NOT EXISTS chapters (story_id INT, chapter_id INT, content text NOT NULL, author, date)"
    c.execute(command)
    user_file = "users.db"

    user = sqlite3.connect(user_file)
    cUser = user.cursor() 
    cUser.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, access TEXT, viewable INTEGER[], editable INTEGER[])")
    user.commit()
    db.commit()
    if 'username' not in session:
        return render_template('home.html')
  
    cUser.execute("SELECT viewable FROM users WHERE username = ?", (session['username'],))
    row=cUser.fetchone()

    if row and row[0]:
        listD = []
        if (type(row) == tuple):
            for i in row:
                dar = []
                dar.append(int(i))
                dar.append(returnStoryTitle(int(i)))
                dar.append(returnChapters(int(i)))
                dar.append(returnAuthor(int(i)))
                listD.append(dar)
        else:
            d = row.split(',')
            for i in d:
                dar = []
                dar.append(int(i))
                dar.append(returnStoryTitle(int(i)))
                dar.append(returnChapters(int(i)))
                dar.append(returnAuthor(int(i)))
                listD.append(dar)
        user.commit()
        db.commit()
        return render_template("response.html", username = session['username'], message="", rows = listD)
    
    else:
        d = "No viewable stories"
        user.commit()
        db.commit()
        return render_template("response.html", username = session['username'], message=d)
    

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
    user_file = "users.db"

    user = sqlite3.connect(user_file)
    cUser = user.cursor() 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cUser.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, access TEXT, viewable INTEGER[], editable INTEGER[])")
        if not (username and password):
            user.commit()
            return redirect("/register?message=One+or+more+fields+empty;+please+try+again.")
        print((cUser.execute("SELECT 1 FROM users WHERE username=?", (username,))).fetchone())
        print((cUser.execute("SELECT 1 FROM users WHERE username=?", (username,))).fetchone() == None)
        if (cUser.execute("SELECT 1 FROM users WHERE username=?", (username,))).fetchone() == None:
            try:
                cUser.execute("INSERT INTO users (username, password, access) VALUES (?, ?, ?)", (username, password, "Normal"))
                user.commit()
                session['username']=username
                session['password']=password
                db = sqlite3.connect("stories.db")
                c = db.cursor()
                c.execute("SELECT story_id FROM stories")
                rows = c.fetchall()

                editList = [str(row[0]) for row in rows]
                if editList:
                    editStr = ",".join(editList)
                else:
                    editStr = ""
                
                cUser.execute("UPDATE users SET editable = ? WHERE username = ?", (editStr, username))
                user.commit()
                return redirect("/login")
            except sqlite3.IntegrityError:
                register("Integrity Error")
                return redirect("/register?message=Integrity+Error")
        user.commit()
        return redirect("/register?message=Username+taken")
    return redirect("/register")

@app.route("/loginauth", methods=['GET', 'POST'])
def loginer():
    user_file = "users.db"

    user = sqlite3.connect(user_file)
    cUser = user.cursor() 

    db = sqlite3.connect("stories.db") 
    c = db.cursor()

    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        cUser.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, access TEXT, viewable INTEGER[], editable INTEGER[])")
        cUser.execute("SELECT password FROM users WHERE username=?", (request.form['username'],))
        res = cUser.fetchone()
        if res is None:
            session.pop('username', None)
            session.pop('password', None)
            return redirect("/login?message=Username+does+not+exist;+please+register+before+logging+in.")
        if 'username' in session and session['password'] == res[0]:
            cUser.execute("SELECT editable, viewable FROM users WHERE username=?", (session['username'],))
            user_data = cUser.fetchone()

            editable_str = user_data[0] if user_data[0] else ""
            viewable_str = user_data[1] if user_data[1] else ""

            editable_list = editable_str.split(',') if editable_str else []
            viewable_list = viewable_str.split(',') if viewable_str else []

            # Fetch all stories from the database
            c.execute("SELECT story_id FROM stories")
            all_stories = [str(story[0]) for story in c.fetchall()]

            # Identify new stories that are not in either editable or viewable
            new_stories = [story_id for story_id in all_stories if story_id not in editable_list and story_id not in viewable_list]

            # Update editable list with new stories
            if new_stories:
                editable_list.extend(new_stories)
                updated_editable_str = ",".join(editable_list)
                cUser.execute("UPDATE users SET editable=? WHERE username=?", (updated_editable_str, session['username']))
            
            user.commit()
            return redirect("/")
        session.pop('username', None)
        session.pop('password', None)
        return redirect("/login?message=Invalid+login;+please+try+again.")
    user.commit()
    login()
    return redirect("/login")

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
    user.commit()
    return(render_template('/', message = fst))

@app.route("/logout", methods=['GET', 'POST'])
def disp_logout():
    session.pop('username', None)
    session.pop('password', None)
    return render_template( 'logout.html' )

# @app.route("/main", methods=['POST'])
# def main():
#     return render_template("home.html")

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
        if (not (title and first)):
            return render_template( 'create.html', message="please enter a title and a first sentence")
        addStory(title, session['username'], first)
        return redirect("/")
    create()
    return redirect("/create")
    
@app.route("/editable", methods = ["GET", "POST"])
def editable():     
    if 'username' not in session:
        return redirect('/login')

    user_file = "users.db"

    user = sqlite3.connect(user_file)
    cUser = user.cursor()    
    cUser.execute("SELECT editable FROM users WHERE username = ?", (session['username'],))
    row=cUser.fetchone()

    if row and row[0]:
        listD = []
        if (type(row) == tuple):
            for i in row[0]:
                if type(i) == int:
                    dar = []
                    dar.append(int(i))
                    dar.append(returnStoryTitle(int(i)))
                    dar.append(returnChapters(int(i)))
                    dar.append(returnAuthor(int(i)))
                    listD.append(dar)
        else:
            d = row.split(',')
            for i in d:
                dar = []
                dar.append(int(i))
                dar.append(returnStoryTitle(int(i)))
                dar.append(returnChapters(int(i)))
                dar.append(returnAuthor(int(i)))
                listD.append(dar)
        user.commit()
        return render_template("editable.html", username = session['username'], message="", rows = listD)
    
    else:
        d = "No editable stories"
        user.commit()
        return render_template("editable.html", username = session['username'], message=d)
    
@app.route("/edit", methods=["GET", "POST"])
def edit():
    if 'username' not in session:
        return redirect('/login')
    
    story_id = request.args.get('story_id')
    if not story_id:
        return redirect("/editable")
    
    dar = []
    dar.append(int(story_id))
    dar.append(returnStoryTitle(int(story_id)))
    dar.append(returnChapters(int(story_id)))
    dar.append(returnAuthor(int(story_id)))
    return render_template("edit.html", story = dar)

@app.route("/editcomplete", methods=["GET", "POST"])
def editcomplete():
    user_file = "users.db"
    user = sqlite3.connect(user_file)
    cUser = user.cursor()

    if 'username' not in session:
        return redirect('/login')
    
    story = request.args.get('story')

    if request.method == 'POST':
        content = request.args.get("new_chapter")

        if not content:
            return render_template("edit.html", story=story, message="Please enter content for the new chapter.")
        
        addChapter(story, content, session['username'])

        cUser.execute("SELECT editable FROM users WHERE username = ?", (session['username'],))
        editStr = cUser.fetchone()[0]
        editList = editStr.split(',')

        if (int(story) in editList):
            editList.remove(int(story))
            updList = ','.join(str(h) for h in editList)
            cUser.execute("UPDATE users SET editable = ? WHERE username = ?", (updList, session['username']))

        cUser.execute("SELECT viewable FROM users WHERE username = ?", (session['username'],))
        view = cUser.fetchone()[0]
        if view:
            nview = f"{view},{story}"
        else:
            nview = str(story)
            
        cUser.execute("UPDATE users SET viewable = ? WHERE username = ?", (nview, session['username']))
        user.commit()

        return redirect("/editable")
    
    return render_template("edit.html")

        

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
