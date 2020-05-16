from flask import (Flask, render_template, request, json, flash, redirect, url_for, session, abort)
from email.message import EmailMessage
import bcrypt, time, random, datetime, smtplib, jwt, os, sqlite3, shutil



app = Flask(__name__)
app.secret_key = b"HJ22$@sa#9HdSEsdwddc-s-$"
bootstrapTheme = """<link href="https://stackpath.bootstrapcdn.com/bootswatch/4.4.1/cyborg/bootstrap.min.css" rel="stylesheet" integrity="sha384-l7xaoY0cJM4h9xh1RfazbgJVUZvdtyLWPueWNtLAphf/UbBgOVzqbOTogxPwYLHM" crossorigin="anonymous">"""
domain = "domasdadsasdasdain.ru"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Вычищаем текст от "вирусов"
def cleaner(text):
    for i in r"^%&<>\[\]{}]/": 
                text = text.replace(i, "", -1)
    return text

#Логин
@app.route("/login", methods=('POST', 'GET'))
def login():
    f = open("dev_output.txt", "a+")
    if request.method == 'POST':
        #подключение форм
        login = request.form['inputLogin']
        login = cleaner(login)
        password = request.form['inputPassword']
        password = cleaner(password)
        #подключение бд
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT password FROM `users` WHERE login=?;", (login,))
        hashedPassword = c.fetchall()
        if len(hashedPassword) != 0:
            #хеш проверка и итог
            
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
        login = cleaner(login)
        password = request.form['inputPassword']
        password = cleaner(password)
        password = password.encode('UTF-8')
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM `users` WHERE login=?;", (login,))
        x = c.fetchall()
        if len(x) > 0:
            registerStatus = False
            
            return redirect(url_for("AuthError"))
        else:
            reger = [login, bcrypt.hashpw(password, bcrypt.gensalt())]
            c.execute("INSERT INTO users VALUES (?,?);", reger)
            conn.commit()
            conn.close()
            connData = sqlite3.connect("userData.db")
            g = connData.cursor()
            reger2 = [login, "Hi everyone, this is me"]
            g.execute("INSERT INTO `userData` VALUES(?,NULL,?,NULL,NULL);", reger2)
            connData.commit()
            connData.close()
            if os.path.exists("static/images/users/placeholder.jpg"):
                shututil.copy("static/images/users/{}.jpg".format(userID))
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
            textContent = cleaner(textContent)
            textName = request.form['textName']
            textName = cleaner(textName)
            fullPostData = [(randID, textName, textContent, author, date, rating, dateComputer)]

            c.executemany("INSERT INTO `texts` VALUES(?,?,?,?,?,?,?)", fullPostData)

            conn.commit()
            conn.close()
            
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

#Выход из аккаунта
@app.route("/logout")
def logOut():
    session.pop('user', None)
    session.pop('icon', None)
    time.sleep(0.5)
    return redirect(url_for("login"))

#Забыл пароль  
@app.route("/forgot", methods=('POST', 'GET'))
def forgot():
    if not session.get("user"):
        if request.method == "POST":
            login = request.form["inputLogin"]
            login = cleaner(login)
            conn = sqlite3.connect("userData.db")
            c = conn.cursor()
            c.execute("SELECT email FROM `userData` WHERE nick=?", (login,))
            email = c.fetchone()
            email = email[0]
            f = open("dev_output.txt", "a")
            if email != None:
                localHash = jwt.encode(
                                {'reset_password': login, 'exp': time() + 600},
                                app.config['SECRET_KEY'], algorithm='HS512').decode('utf-8')

                link = url_for("/forget/{}".format(localHash))
                msg = EmailMessage()
                msg.set_content(link)
                msg['Subject'] = "Password reset"
                msg['From'] = "password@{}".format(domain)
                msg['To'] = email              
                s = smtplib.SMTP('localhost')
                s.send_message(msg)
                s.quit()

        return render_template("forgot.html")
    else: 
        abort(404)

#Непосредственно забывание пароля
@app.route("/forget/<localHash>", methods=('POST', 'GET'))
def forget(localHash):
    data = jwt.decode(localHash, app.config['SECRET_KEY'],
                      algorithms=['HS512'])['reset_password']
    if request.method == "POST":
        password = request.form["inputPassword"]
        password = cleaner(password)
        password = password.encode('UTF-8')
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        newPass = bcrypt.hashpw(password, bcrypt.gensalt())
        temp = [newPass, login]
        c.execute("UPDATE `users` SET password=? WHERE login=?", temp)
        redirect(url_for("login"))

    return render_template("forget.html")

#Редактирование профиля
@app.route("/usercorrect", methods=("POST", "GET"))
def usercorrect():
    if session.get("user"):
        userID = session.get("user")
        conn = sqlite3.connect("userData.db")
        c = conn.cursor()
        f = open("dev_output.txt", "a")
        temp = "images/users/{}.jpg".format(userID)
        imageLink = url_for('static', filename=temp)
        about = c.execute("SELECT about FROM `userData` WHERE nick=?;", (userID,))
        
        about = about.fetchall()
        
        about = str(about)
        about = about[about.find("'")+1:about.rfind("'")]
        
        if request.method == "POST":
            if request.form["newAbout"]:
                newAbout = request.form["newAbout"]
                if newAbout != about:
                    c.execute("UPDATE `userData` SET about=? WHERE nick=?", [newAbout, userID])
                    conn.commit()   
                    conn.close()
            if request.files.get("newImage"):
                if 'newImage' not in request.files:
                    flash('No file part, try again')
                    
                file = request.files['newImage']
                if file and file.filename.endswith(".jpg"):
                    filename = userID + ".jpg"
                    f.write(str(type(file)))
                    if os.path.exists("static/images/users/{}.jpg".format(userID)):
                        os.remove("static/images/users/{}.jpg".format(userID))
                    file.save("static/images/users/{}.jpg".format(userID))
                    f.write("image seems to be edited")
                    #return redirect("/id/{}".format(userID))
            return redirect(url_for("usercorrect"))
        return render_template("usercorrect.html", bootstrapTheme=bootstrapTheme, nick=userID, imageLink=imageLink, about=about)

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


if __name__ == "__main__":
    app.run(debug=True)
