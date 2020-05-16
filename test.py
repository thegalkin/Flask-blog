import sqlite3
newPostId = 10
connData = sqlite3.connect("userData.db")
connData.row_factory = lambda cursor, row: row[0]
g = connData.cursor()
login = "io"

temp = g.execute("SELECT posts FROM `userData` WHERE nick=?;", (login,)).fetchall()
print(temp)
temp.append(newPostId)

g.execute("UPDATE `userData` SET posts=? WHERE nick=?;", [newPostId, login])
print(temp)
temp = g.execute("SELECT posts FROM `userData` WHERE nick=?;", (login,)).fetchone()[0]
print(temp)
connData.close()