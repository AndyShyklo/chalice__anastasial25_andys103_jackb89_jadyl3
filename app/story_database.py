# Chalice: Anastasia, Andy, Jack, Jady
# SoftDev
# October 2024

import sqlite3 #enable SQLite operations

DB_FILE="stories.db"
#open db if exists, otherwise create
db = sqlite3.connect(DB_FILE) 
c = db.cursor() #facilitate db ops

# storiesDontExist = (c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stories'").fetchall() == [])
# if storiesDontExist:
#     command = "CREATE TABLE IF NOT EXISTS stories (story_id INT AUTO_INCREMENT PRIMARY KEY, story_name)"
#     c.execute(command)
command = "CREATE TABLE IF NOT EXISTS stories (story_id INT PRIMARY KEY, story_name text NOT NULL)"
c.execute(command)
# """CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, name text NOT NULL, begin_date DATE, end_date DATE);"""

# call whenever user adds a story. 
# story_name, author, first_chapter, and date should all be strings.
def addStory(story_name, author, first_chapter, date):
    # create story table
    command = f"INSERT INTO stories (story_name) VALUES (?)"
    val = (story_name,)
    c.execute(command, val)
    db.commit()
    key = c.lastrowid
    print(key)
    # create table for chapters using story_id
    command = f"CREATE TABLE chapters_for_{key} (id INT PRIMARY KEY, content text NOT NULL, contributor text NOT NULL, date text NOT NULL)"
    c.execute(command)
    command = f"INSERT INTO chapters_for_{key} (content, contributor, date) VALUES (?, ?, ?)"
    val = (first_chapter, author, date)
    c.execute(command, val)
    #create table for authors using story_id
    command = f"CREATE TABLE authors_for_{key} (id INT PRIMARY KEY, author text NOT NULL)"
    c.execute(command)
    command = f"INSERT INTO authors_for_{key} (author) VALUES (?)"
    val = (author,)
    c.execute(command, val)

# def returnStories():
#     c.execute("SELECT story_name FROM stories")
#     rows = c.fetchall()
#     for row in rows:
#         print(row)

def returnChapters():
    c.execute("SELECT story_id FROM stories")
    ids = c.fetchall()
    for id in ids:
        print(id)
#         c.execute("SELECT content FROM chapters_for_"+str(id))
#         texts = c.fetchall()
#         for text in texts:
#             print(text)

db.commit() #save changes
# c.execute("SELECT id, code FROM courses"):

# db.close()