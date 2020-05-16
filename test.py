import sqlite3
nick = "io"
conn = sqlite3.connect("userData.db")
c = conn.cursor()
isReal = c.execute("SELECT nick FROM `userData` WHERE nick=?;", (nick,)).fetchone()
print(isReal)
conn.close()