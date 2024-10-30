# Chalice: Anastasia, Andy, Jack, Jady
# SoftDev
# October 2024

import sqlite3 #enable SQLite operations

DB_FILE="stories.db"
#open db if exists, otherwise create
db = sqlite3.connect(DB_FILE) 
c = db.cursor() #facilitate db ops

storiesDontExist = (c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='courses'").fetchall() == [])
if storiesDontExist:
    command = "CREATE TABLE stories (story_id INT AUTO_INCREMENT PRIMARY KEY, story_name)"
    c.execute(command)

# call whenever user adds a story. 
# story_name, author, first_chapter, and date should all be strings.
def addStory(story_name, author, first_chapter, date):
    # create story table
    command = f"INSERT INTO stories (story_name) VALUES (?)"
    val = (story_name)
    c.execute(command, val)
    db.commit()
    key = c.lastrowid
    # create table for chapters using story_id
    command = f"CREATE TABLE chapters_for_{key} (id INT AUTO_INCREMENT PRIMARY KEY, content, contributor, date)"
    c.execute(command)
    command = f"INSERT INTO chapters_for_{key} (content, contributor, date) VALUES (?, ?, ?)"
    val = (first_chapter, author, date)
    c.execute(command, val)
    #create table for authors using storu_id
    command = f"CREATE TABLE authors_for_{key} (order INT AUTO_INCREMENT PRIMARY KEY, author)"
    c.execute(command)
    command = f"INSERT INTO authors_for_{key} (author) VALUES (?)"
    val = (author)
    c.execute(command, val)



db.commit() #save changes
# c.execute("SELECT id, code FROM courses"):

db.close()