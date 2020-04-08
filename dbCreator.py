import sqlite3
conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute('''CREATE TABLE users (login, password)''')
conn.commit()
conn.close()