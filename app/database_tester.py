from story_database import *

title1 = "Frankenstein"
sentence1 = "You will rejoice to hear that no disaster has accompanied the commencement of an enterprise which you have regarded with such evil forebodings."
author = "Admin"
# use military time?
date = "10:23 October 30, 2024"

print("-------------------Creating Story--------------------------")
createStories()
deleteStories()
createStories()
story_id = addStory(title1, author, sentence1, date)
print(returnStories())
print(returnChapters(story_id))


print("-----------------Adding to story -------------------")
sentence2 = "I arrived here yesterday, and my first task is to assure my dear sister of my welfare and increasing confidence in the success of my undertaking. "
# use military time?
date2 = "11:09 October 31, 2024"
addChapter(story_id, sentence2, author, date2)
sentence3 = "I am already far north of London, and as I walk in the streets of Petersburgh, I feel a cold northern breeze play upon my cheeks, which braces my nerves and fills me with delight. "
# use military time?
date3 = "10:25 November 3, 2024"
addChapter(story_id, sentence3, author, date3)
sentence4 = "Do you understand this feeling? This breeze, which has travelled from the regions towards which I am advancing, gives me a foretaste of those icy climes. "
addChapter(story_id, sentence4, author, date3)
addChapter(story_id, sentence4, author, date3)
sentence5 = "Inspirited by this wind of promise, my daydreams become more fervent and vivid. I try in vain to be persuaded that the pole is the seat of frost and desolation; it ever presents itself to my imagination as the region of beauty and delight. There, Margaret, the sun is for ever visible, its broad disk just skirting the horizon and diffusing a perpetual splendour. "
addChapter(story_id, sentence5, author, date3)
print(returnStories())
print(returnChapters(story_id))

print("-----------------Deleting chapters and stories-------------------")
deleteChapter(story_id, 5)
print(returnStories())
print(returnChapters(story_id))
deleteStory(story_id)
print(returnStories())