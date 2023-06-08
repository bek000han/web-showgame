import csv, sqlite3

con = sqlite3.connect("quiz.db")
cur = con.cursor()

with open('answers.csv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['questionid'], i['answer'], i['correct']) for i in dr]

cur.executemany("INSERT INTO answers (questionid, answer, correct) VALUES (?, ?, ?);", to_db)
con.commit()
con.close()