import sqlite3
conn = sqlite3.connect("posts.db")
c = conn.cursor()
c.execute('''CREATE TABLE post (id, title, rating, text, author)''')
conn.commit()
conn.close()