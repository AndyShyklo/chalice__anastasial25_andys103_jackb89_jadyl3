from story_database import *

title1 = "Frankenstein"
sentence1 = "You will rejoice to hear that no disaster has accompanied the commencement of an enterprise which you have regarded with such evil forebodings."
author = "Admin"
# use military time?
date = "10:23 October 30, 2024"

print("-------------------Creating Story--------------------------")
deleteStories()
createStories()
story_id = addStory(title1, author, sentence1, date)
print(returnStories())
print(returnChapters(1))


print("-----------------Adding to story -------------------")
sentence2 = "I arrived here yesterday, and my first task is to assure my dear sister of my welfare and increasing confidence in the success of my undertaking. "
author = "Admin"
# use military time?
date2 = "11:09 October 31, 2024"
addChapter(story_id, sentence2, author, date2)
print(returnStories())
print(returnChapters(1))