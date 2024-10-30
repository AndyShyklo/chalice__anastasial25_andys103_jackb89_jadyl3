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

def addStory(story_name, author, first_chapter):
    command = f"INSERT INTO stories (story_name) VALUES (?)"
    val = (story_name)
    c.execute(command, val)
    command = f"CREATE TABLE chapters_for_{c.lastrowid} (story_id INT AUTO_INCREMENT PRIMARY KEY, story_name, authors_id, chapters)"
    command = f"CREATE TABLE authors_for_{c.lastrowid} (story_id INT AUTO_INCREMENT PRIMARY KEY, story_name, authors_id, chapters)"



db.commit() #save changes
# c.execute("SELECT id, code FROM courses"):

db.close()