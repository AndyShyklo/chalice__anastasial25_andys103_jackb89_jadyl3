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
def createStories():
    command = "CREATE TABLE IF NOT EXISTS stories (story_id INTEGER PRIMARY KEY AUTOINCREMENT, story_name text NOT NULL, chapter_count INT)"
    c.execute(command)
    command = "CREATE TABLE IF NOT EXISTS chapters (story_id INT, chapter_id INT, content text NOT NULL, author, date)"
    c.execute(command)
# """CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, name text NOT NULL, begin_date DATE, end_date DATE);"""

'''change database---------------------------------------------------------------------------------------------'''
# call whenever user adds a story. 
# story_name, author, first_chapter, and date should all be strings.
def addStory(story_name, author, first_chapter, date):
    # insert story into stories
    command = "INSERT INTO stories (story_name, chapter_count) VALUES (?,?)"
    val = (story_name,1)
    c.execute(command, val)
    db.commit()
    key = c.lastrowid
    # insert chapter into chapters with the story_id
    command = "INSERT INTO chapters (story_id, chapter_id, content, author, date) VALUES (?,?,?,?,?)"
    val = (key, 1, first_chapter, author, date)
    c.execute(command, val)
    db.commit()
    return key

def addChapter(story_id, content, author, date):
    # gets chapter count
#     command = "SELECT chapter_count FROM stories WHERE story_id = "+ str(story_id)
    command = "SELECT * FROM stories "
    print(command)
    c.execute(command)
    chapter_count = c.fetchall()
    print(chapter_count)
    # add chapter to chapters
    command = "INSERT INTO chapters (story_id, chapter_id, content, author, date) VALUES (?,?,?,?,?)"
    val = (story_id, chapter_count+1, content, author, date)
    c.execute(command, val)
    # update chapter count
    command = "UPDATE stories SET chapter_count = "+ str(chapter_count+1) +" WHERE story_id = "+ str(story_id)
    c.execute(command)
    db.commit()
    return story_id

def deleteChapter(story_id, chapter_id):
    # check if either exist
    # TODO
    # delete from chapters
    command = "DELETE FROM chapters WHERE story_id = " + str(story_id) + "AND" + "chapter_id = " + str(chapter_id)
    c.execute(command)
    db.commit()
    # update chaptercount for stories
    c.execute("SELECT chapter_count FROM stories WHERE story_id = "+ str(story_id))
    chapter_count = c.fetchone()
    command = "UPDATE stories SET chapter_count = " + str(chapter_count-1) + "WHERE story_id = "+ str(story_id)
    return story_id

def deleteStory(story_id):
    # check if story exists
    # TODO
    # delete from stories
    command = "DELETE FROM stories WHERE story_id = " + str(story_id)
    c.execute(command)
    # delete from chapters
    c.execute("DELETE FROM chapters WHERE story_id = "+ str(story_id))
    db.commit()
    return story_id

'''access database-----------------------------------------------------------------------------------------'''
# return story titles
def returnStories():
    c.execute("SELECT story_name FROM stories")
    rows = c.fetchall()
    resp = []
    for row in rows:
        resp.append(row[0])
    return resp

# returns chapters of an id.
def returnChapters(story_id):
    c.execute("SELECT content FROM chapters WHERE story_id =" + str(story_id))
    rows = c.fetchall()
    resp = []
    for row in rows:
        resp.append(row[0])
    return resp
        
# if used for a table of contents make sure to truncate content!    
def returnChaptersList(story_id):
    c.execute("SELECT content, author, date FROM chapters WHERE story_id =" + str(story_id))
    rows = c.fetchall()
    return rows
    
'''--------------------------------------------------------------------------------------------------------'''
#for admin stuyff
def deleteStories():
    c.execute("DROP table stories")
    c.execute("DROP table chapters")

db.commit() #save changes
# c.execute("SELECT id, code FROM courses"):

# db.close()