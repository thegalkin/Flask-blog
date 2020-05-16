import sqlite3
newPostId = 10
connData = sqlite3.connect("userData.db")

g = connData.cursor()
login = "io"

temp = g.execute("SELECT posts FROM `userData` WHERE nick=?;", (login,)).fetchone()[0]
print(temp)
temp = temp.replace("[", "")
temp = temp.replace("]", "")
temp = temp.split(",")
for i in range(len(temp)):
    temp[i] = int(temp)
#temp.append(newPostId)

g.execute("UPDATE `userData` SET posts=? WHERE nick=?;", [newPostId, login])
print(temp)
temp = g.execute("SELECT posts FROM `userData` WHERE nick=?;", (login,)).fetchone()[0]
print(temp)
connData.close()