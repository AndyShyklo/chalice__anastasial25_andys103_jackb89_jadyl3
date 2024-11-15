# Chalice: Anastasia, Andy, Jack, Jady
# SoftDev
# October 2024

import sqlite3 #enable SQLite operations

DB_FILE="stories.db"

def createStories():
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()
    command = "CREATE TABLE IF NOT EXISTS stories (story_id INTEGER PRIMARY KEY AUTOINCREMENT, story_name text NOT NULL, chapter_count INT)"
    c.execute(command)
    command = "CREATE TABLE IF NOT EXISTS chapters (story_id INT, chapter_id INT, content text NOT NULL, author)"
    c.execute(command)
# """CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, name text NOT NULL, begin_date DATE, end_date DATE);"""

'''change database---------------------------------------------------------------------------------------------'''
# call whenever user adds a story. 
# story_name, author, first_chapter, and date should all be strings.
def addStory(story_name, author, first_chapter):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()
    # insert story into stories
    command = "INSERT INTO stories (story_name, chapter_count) VALUES (?,?)"
    val = (story_name,1)
    c.execute(command, val)
    db.commit()
    key = c.lastrowid
    # insert chapter into chapters with the story_id
    command = "INSERT INTO chapters (story_id, chapter_id, content, author) VALUES (?,?,?,?)"
    val = (key, 1, first_chapter, author)
    c.execute(command, val)
    db.commit()
    return key

def addChapter(story_id, content, author):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()
    # gets chapter count
    c.execute("SELECT chapter_count FROM stories WHERE story_id=?", (story_id,))
    chapter_count = c.fetchone()[0]
    # add chapter to chapters
    command = "INSERT INTO chapters (story_id, chapter_id, content, author) VALUES (?,?,?,?)"
    val = (story_id, chapter_count+1, content, author)
    c.execute(command, val)
    # update chapter count
    command = "UPDATE stories SET chapter_count = "+ str(chapter_count+1) +" WHERE story_id = "+ str(story_id)
    c.execute(command)
    db.commit()
    return story_id

def deleteChapter(story_id, chapter_id):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()
    # check if either exist
    # TODO
    # delete from chapters
    command = "DELETE FROM chapters WHERE story_id = " + str(story_id) + " AND " + "chapter_id = " + str(chapter_id)
    c.execute(command)
    db.commit()
    # update chaptercount for stories
    c.execute("SELECT chapter_count FROM stories WHERE story_id = "+ str(story_id))
    chapter_count = c.fetchone()[0]
    command = "UPDATE stories SET chapter_count = " + str(chapter_count-1) + "WHERE story_id = "+ str(story_id)
    db.commit()
    return story_id

def deleteStory(story_id):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()
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
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()
    c.execute("SELECT story_name FROM stories")
    rows = c.fetchall()
    resp = []
    for row in rows:
        resp.append(row[0])
    return resp

def returnStoryTitle(story_id):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()
    c.execute("SELECT story_name FROM stories WHERE story_id =" + str(story_id))
    rows = c.fetchall()
    if len(rows) == 0:
        return ""
    resp = rows[0]
    return resp[0]

# returns chapters of an id.
def returnChapters(story_id):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()
    c.execute("SELECT content FROM chapters WHERE story_id =" + str(story_id))
    rows = c.fetchall()
    resp = []
    for row in rows:
        resp.append(row[0])
    return resp

def returnAuthor(story_id):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()
    c.execute("SELECT author FROM chapters WHERE story_id =" + str(story_id))
    rows = c.fetchall()
    resp = rows[0]
    return resp[0]
        
# if used for a table of contents make sure to truncate content!    
def returnChaptersList(story_id):
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()
    c.execute("SELECT content, author FROM chapters WHERE story_id =" + str(story_id))
    rows = c.fetchall()
    return rows
    
'''--------------------------------------------------------------------------------------------------------'''
#for admin stuyff
def deleteStories():
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()
    c.execute("DROP table stories")
    c.execute("DROP table chapters")

def addFrankenstien():
    if returnStoryTitle(1) != "Frankenstein":
        sentence1 = "You will rejoice to hear that no disaster has accompanied the commencement of an enterprise which you have regarded with such evil forebodings. I arrived here yesterday, and my first task is to assure my dear sister of my welfare and increasing confidence in the success of my undertaking."
        storyid = addStory("Frankenstein", "Mary Shelley", sentence1)
        sentence2 = "I am already far north of London, and as I walk in the streets of Petersburgh, I feel a cold northern breeze play upon my cheeks, which braces my nerves and fills me with delight."
        sentence3 = "Do you understand this feeling? This breeze, which has travelled from the regions towards which I am advancing, gives me a foretaste of those icy climes."
        sentence4 = "Inspirited by this wind of promise, my daydreams become more fervent and vivid. I try in vain to be persuaded that the pole is the seat of frost and desolation; it ever presents itself to my imagination as the region of beauty and delight."
        sentence5 = "There, Margaret, the sun is for ever visible, its broad disk just skirting the horizon and diffusing a perpetual splendour. There—for with your leave, my sister, I will put some trust in preceding navigators—there snow and frost are banished; and, sailing over a calm sea, we may be wafted to a land surpassing in wonders and in beauty every region hitherto discovered on the habitable globe."
        sentence6 = "Its productions and features may be without example, as the phenomena of the heavenly bodies undoubtedly are in those undiscovered solitudes. What may not be expected in a country of eternal light? I may there discover the wondrous power which attracts the needle and may regulate a thousand celestial observations that require only this voyage to render their seeming eccentricities consistent for ever. "
        sentence7 = "I shall satiate my ardent curiosity with the sight of a part of the world never before visited, and may tread a land never before imprinted by the foot of man. These are my enticements, and they are sufficient to conquer all fear of danger or death and to induce me to commence this laborious voyage with the joy a child feels when he embarks in a little boat, with his holiday mates, on an expedition of discovery up his native river." 
        sentence8 = "But supposing all these conjectures to be false, you cannot contest the inestimable benefit which I shall confer on all mankind, to the last generation, by discovering a passage near the pole to those countries, to reach which at present so many months are requisite; or by ascertaining the secret of the magnet, which, if at all possible, can only be effected by an undertaking such as mine."
        s9 = "These reflections have dispelled the agitation with which I began my letter, and I feel my heart glow with an enthusiasm which elevates me to heaven, for nothing contributes so much to tranquillise the mind as a steady purpose—a point on which the soul may fix its intellectual eye."
        s10 = "This expedition has been the favourite dream of my early years. I have read with ardour the accounts of the various voyages which have been made in the prospect of arriving at the North Pacific Ocean through the seas which surround the pole."
        s11 = "You may remember that a history of all the voyages made for purposes of discovery composed the whole of our good Uncle Thomas’ library. My education was neglected, yet I was passionately fond of reading. These volumes were my study day and night, and my familiarity with them increased that regret which I had felt, as a child, on learning that my father’s dying injunction had forbidden my uncle to allow me to embark in a seafaring life."
        s12 = "These visions faded when I perused, for the first time, those poets whose effusions entranced my soul and lifted it to heaven. I also became a poet and for one year lived in a paradise of my own creation; I imagined that I also might obtain a niche in the temple where the names of Homer and Shakespeare are consecrated. You are well acquainted with my failure and how heavily I bore the disappointment. But just at that time I inherited the fortune of my cousin, and my thoughts were turned into the channel of their earlier bent."
        s13 = "Six years have passed since I resolved on my present undertaking. I can, even now, remember the hour from which I dedicated myself to this great enterprise. I commenced by inuring my body to hardship. I accompanied the whale-fishers on several expeditions to the North Sea; I voluntarily endured cold, famine, thirst, and want of sleep; I often worked harder than the common sailors during the day and devoted my nights to the study of mathematics, the theory of medicine, and those branches of physical science from which a naval adventurer might derive the greatest practical advantage. Twice I actually hired myself as an under-mate in a Greenland whaler, and acquitted myself to admiration. I must own I felt a little proud when my captain offered me the second dignity in the vessel and entreated me to remain with the greatest earnestness, so valuable did he consider my services."
        s14 = "And now, dear Margaret, do I not deserve to accomplish some great purpose? My life might have been passed in ease and luxury, but I preferred glory to every enticement that wealth placed in my path. Oh, that some encouraging voice would answer in the affirmative! My courage and my resolution is firm; but my hopes fluctuate, and my spirits are often depressed. I am about to proceed on a long and difficult voyage, the emergencies of which will demand all my fortitude: I am required not only to raise the spirits of others, but sometimes to sustain my own, when theirs are failing."
        s15 = "This is the most favourable period for travelling in Russia. They fly quickly over the snow in their sledges; the motion is pleasant, and, in my opinion, far more agreeable than that of an English stagecoach. The cold is not excessive, if you are wrapped in furs—a dress which I have already adopted, for there is a great difference between walking the deck and remaining seated motionless for hours, when no exercise prevents the blood from actually freezing in your veins. I have no ambition to lose my life on the post-road between St. Petersburgh and Archangel."
        s16 = "I shall depart for the latter town in a fortnight or three weeks; and my intention is to hire a ship there, which can easily be done by paying the insurance for the owner, and to engage as many sailors as I think necessary among those who are accustomed to the whale-fishing. I do not intend to sail until the month of June; and when shall I return? Ah, dear sister, how can I answer this question? If I succeed, many, many months, perhaps years, will pass before you and I may meet. If I fail, you will see me again soon, or never."
        s17 = "Farewell, my dear, excellent Margaret. Heaven shower down blessings on you, and save me, that I may again and again testify my gratitude for all your love and kindness. Your affectionate brother, R. Walton"
        paragraph = [sentence2, sentence3, sentence4, sentence5, sentence6, sentence7, sentence8, s9, s10, s11, s12, s13, s14, s15, s16, s17]
        for sentence in paragraph:
            addChapter(storyid, sentence, "Mary Shelly")

# db.commit() #save changes

# db.close()