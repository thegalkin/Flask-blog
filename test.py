import sys
import sqlite3
import random
import datetime
import time

"""conn = sqlite3.connect("texts.db")
c = conn.cursor()
c.execute("SELECT ID FROM `texts`")
g = c.fetchall()
print(g)
if 2 in g:
    print(True)"""
dateComputer = int(time.time())
date = datetime.datetime.fromtimestamp(dateComputer).strftime("%d %b %Y %H:%M")

print(date)