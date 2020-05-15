from flask import Flask, render_template, request, json, flash, redirect, url_for, session, abort
import sqlite3
#from flask_admin import Admin
#from flask_basicauth import BasicAuth
import bcrypt
import time
import random
import datetime
import smtplib
import jwt
from email.message import EmailMessage
app = Flask(__name__)
app.secret_key = b"HJ22$@sa#9HdSEsdwddc-s-$"
bootstrapTheme = """<link href="https://stackpath.bootstrapcdn.com/bootswatch/4.4.1/cyborg/bootstrap.min.css" rel="stylesheet" integrity="sha384-l7xaoY0cJM4h9xh1RfazbgJVUZvdtyLWPueWNtLAphf/UbBgOVzqbOTogxPwYLHM" crossorigin="anonymous">"""
domain = "domasdadsasdasdain.ru"
domain = "localhost"
#Логин
@app.route("/login", methods=('POST', 'GET'))
def login():
    f = open("dev_output.txt", "a+")
    if request.method == 'POST':
        #подключение форм
        login = request.form['inputLogin']
        password = request.form['inputPassword']
        #подключение бд
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        """connUserData = sqlite3.connect("userData.db")
        g = connUserData.cursor()"""
        c.execute("SELECT password FROM `users` WHERE login=?;", (login,))
        #f.write("{}\n".format(c))
        hashedPassword = c.fetchall()
        """g.execute("SELECT image FROM `userData` WHERE nick=?", (login,))
        userIcon = g.fetchone()"""
        if len(hashedPassword) != 0:
            #хеш проверка и итог
            
            f.write("{}\n".format(hashedPassword[0][0]))
            f.close()
            hashedPassword = hashedPassword[0][0]
            if bcrypt.checkpw(password.encode("utf-8"), hashedPassword):
                session["user"] = login
                session["icon"] = url_for('static', filename="images/users/{}.jpg".format(login))
                
                
                return redirect("/id/{}".format(login))
            else:
                return render_template("loginError.html")
        else:
            return render_template("loginError.html")

    return render_template("login.html")

#Регистрация
@app.route('/register', methods=('POST', 'GET'))
def regForm():
    
    if request.method == 'POST':
        login = request.form['inputLogin']
        #f.write("email is:{}".format(email))
        password = request.form['inputPassword'].encode('UTF-8')
        #f.write("password is:{}".format(password))
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM `users` WHERE login=?;", (login,))
        x = c.fetchall()
        if len(x) > 0:
            registerStatus = False
            
            return redirect(url_for("AuthError"))
        else:
            reger = [login, bcrypt.hashpw(password, bcrypt.gensalt())]
            #f.write("reger is:{}".format(reger))
            #f.close()
            c.execute("INSERT INTO users VALUES (?,?);", reger)
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
    return render_template("register.html")

    
#Ошибка аутентификации    
@app.route("/AuthError")
def AuthError():
    return render_template("AuthError.html")

#Главная
@app.route('/')
@app.route('/index')
def main():
    connTexts = sqlite3.connect("texts.db")
    g = connTexts.cursor()
    latestPosts = g.execute("SELECT * FROM `texts` ORDER BY dateComputer ASC LIMIT 5;")
    latestPosts = latestPosts.fetchall()
    connTexts.commit()
    connTexts.close()
    return render_template("index.html", fullPostData=latestPosts)

#404

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

#Тексты
@app.route("/texts/<textIDinput>")
def texts(textIDinput):
    try:
        connTexts = sqlite3.connect("texts.db")
        g = connTexts.cursor()
        fullPostData = g.execute("SELECT * FROM `texts` WHERE ID=?;", (textIDinput,))
        fullPostData = fullPostData.fetchall()
        fullPostData = fullPostData[0]
        textName = fullPostData[1]
        textContents = fullPostData[2]
        author = fullPostData[3]
        date = fullPostData[4]
        return render_template("texts.html", textIDinput=textIDinput, textName=textName, textContents=textContents, author=author, date=date)
    except IndexError:
        abort(404)
#Текстовый редактор
@app.route("/editor", methods=('POST', 'GET'))
def editor():
    if session.get("user"):
        if request.method == 'POST':
            conn = sqlite3.connect("texts.db")
            c = conn.cursor()
            temp = 1
            #make an ID
            while temp != 0:
                randID = random.randint(999999,999999999999)
                c.execute("SELECT * FROM `texts` WHERE ID=?", (randID,))
                temp = len(c.fetchall())
            
            dateComputer = int(time.time())
            date = datetime.datetime.fromtimestamp(dateComputer).strftime("%d %b %Y %H:%M")
            rating = 0
            author = session["user"]
            textContent = request.form['text']
            for i in r"^%&<>\[\]{}]/": # Вычищаем текст от "вирусов"
                textContent = textContent.replace(i, "", -1)
            textName = request.form['textName']
            fullPostData = [(randID, textName, textContent, author, date, rating, dateComputer)]

            c.executemany("INSERT INTO `texts` VALUES(?,?,?,?,?,?,?)", fullPostData)

            conn.commit()
            conn.close()
            """with open("dev_output.txt", "a") as f:
                f.write(postText + "\n")"""
            return redirect("/texts/{}".format(randID))



        return render_template("editor.html")   
    else:
        return redirect(url_for("login"))
#О создателях
@app.route('/about')
def about():
    return render_template("about.html")

 #User Page
@app.route('/id/<userID>')
def user(userID):
    try:
        yourPage = False
        f = open("dev_output.txt", "a")
        connTexts = sqlite3.connect("texts.db")
        g = connTexts.cursor()
        conn = sqlite3.connect("userData.db")
        c = conn.cursor()
        temp = "images/users/{}.jpg".format(userID)
        imageLink = url_for('static', filename=temp)
        about = c.execute("SELECT about FROM `userData` WHERE nick=?;", (userID,))
        
        about = about.fetchall()
        
        about = str(about)
        about = about[about.find("'")+1:about.rfind("'")]
        
        
        fullPostData = g.execute("SELECT * FROM `texts` WHERE author=?;", (userID,))
        fullPostData = fullPostData.fetchall()
        f.write(str(fullPostData[0]))

        #if this if your page
        if "user" in session:
            if session["user"] == userID:
                yourPage = True
            
                

        conn.commit()   
        conn.close()
        connTexts.commit()
        connTexts.close()
        f.close()
        return render_template("userPage.html", bootstrapTheme=bootstrapTheme, nick=userID, imageLink=imageLink, about=about, fullPostData=fullPostData, yourPage=yourPage)
    except IndexError:
        abort(404)
@app.route("/logout")
def logOut():
    session.pop('user', None)
    session.pop('icon', None)
    time.sleep(0.5)
    return redirect(url_for("login"))
@app.route("/forgot", methods=('POST', 'GET'))
def forgot():
    if not session.get("user"):
        if request.method == "POST":
            login = request.form["inputLogin"]
            conn = sqlite3.connect("userData.db")
            c = conn.cursor()
            c.execute("SELECT email FROM `userData` WHERE nick=?", (login,))
            email = c.fetchone()
            email = email[0]
            f = open("dev_output.txt", "a")
            f.write(str(email))
            if email != None:
                localHash = jwt.encode(
                                {'reset_password': login, 'exp': time() + 600},
                                app.config['SECRET_KEY'], algorithm='HS512').decode('utf-8')

                f.write(str(localHash))
                link = url_for("/forget/{}".format(localHash))
                msg = EmailMessage()
                msg.set_content(link)
                msg['Subject'] = "Password reset"
                msg['From'] = "gozammer@gmail.com" #"password@{}".format(domain)
                msg['To'] = email              
                s = smtplib.SMTP('localhost')
                s.send_message(msg)
                s.quit()

        return render_template("forgot.html")
    else: 
        abort(404)

@app.route("/forget/<localHash>", methods=('POST', 'GET'))
def forget(localHash):
    data = jwt.decode(localHash, app.config['SECRET_KEY'],
                      algorithms=['HS512'])['reset_password']
    if request.method == "POST":
        login = request.form["inputPassword"]
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT password FROM `users` WHERE login=?", (login,))
        email = c.fetchone()
        email = email[0]

    return render_template("forget.html")
#code trash
"""app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='microblog', template_mode='bootstrap3')"""
"""@app.route('/register')
def register():
    return render_template("register.html")"""
"""@app.route('/admin')
@basic_auth.required
def admin():
    return render_template("admin/index.html")"""
"""while about.find(",") != -1:
            about = about.replace(",", " OR ")"""
        
"""posts = posts.split(",")
posts = [int(posts[i]) for i in range(len(posts))]
f.write(str(posts) + " - posts" + "\n")"""
        
        #fullPostData = texts.query.filter_by(userID=author).first_or_404()

"""{% lilPost = 83 %}
{% lilPost = post/100 * 10 %}"""

#posts = c.execute("SELECT posts FROM `userData` WHERE nick=?;", (userID,))
        #temp = ""
# Страшный костыль, который избавляет от еще большего ужаса из базы данных вида: [('[1,2]',)]
#dfffff
#dfdfd
#gfgfgfg
























if __name__ == "__main__":
    app.run(debug=True)