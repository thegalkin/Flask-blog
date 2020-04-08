import sqlite3
conn = sqlite3.connect("texts.db")
c = conn.cursor()
c.execute('''CREATE TABLE texts (textName, textContent, author, date)''')
conn.commit()
conn.close()