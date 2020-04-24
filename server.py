from flask import Flask, render_template, request, json, flash, redirect, url_for
import sqlite3
#from flask_admin import Admin
#from flask_basicauth import BasicAuth
import bcrypt
app = Flask(__name__)
app.secret_key = b"HJ22$@sa#9HdSEsdwddc-s-$"



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
        c.execute("SELECT password FROM `users` WHERE login=?;", (login,))
        #f.write("{}\n".format(c))
        hashedPassword = c.fetchall()
        if len(hashedPassword) != 0:
            #хеш проверка и итог
            
            f.write("{}\n".format(hashedPassword[0][0]))
            f.close()
            hashedPassword = hashedPassword[0][0]
            if bcrypt.checkpw(password.encode("utf-8"), hashedPassword):
                return render_template("editor.html", login=login)
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
    return render_template("index.html")

#404
@app.route('/texts/<textName>')
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

#Тексты
def texts():
    return render_template("texts.html")

#Текстовый редактор
def editor(login):
    return render_template("editor.html")   

#О создателях
@app.route('/about')
def about():
    return render_template("about.html")

def user():
    







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




























if __name__ == "__main__":
    app.run(debug=True)