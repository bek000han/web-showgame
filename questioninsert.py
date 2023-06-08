import csv, sqlite3

con = sqlite3.connect("quiz.db")
cur = con.cursor()

with open('questions.csv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['difficulty'], i['question']) for i in dr]

cur.executemany("INSERT INTO game (difficulty, question) VALUES (?, ?);", to_db)
con.commit()
con.close()