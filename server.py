from flask import Flask, render_template, request, json, flash, redirect, url_for
import sqlite3
#from flask_admin import Admin
from flask_basicauth import BasicAuth
"""from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired"""








app = Flask(__name__)
app.secret_key = b"HJ22$@sa#9HdSEsdwddc-s-$"
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = '123456789'
#app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
#admin = Admin(app, name='microblog', template_mode='bootstrap3')
def basAuth():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM `users`")
    x = c.fetchall()
    for line in x:
        app.config['BASIC_AUTH_USERNAME'] = line[0]
        app.config['BASIC_AUTH_PASSWORD'] = line[1]
    basic_auth = BasicAuth(app)
    c.close()
basAuth()

basic_auth = BasicAuth(app)

@app.route('/register', methods=('POST', 'GET'))
def regForm():
    
    if request.method == 'POST':
        #f = open("dev_output.txt", "a+")
        email = request.form['inputEmail']
        #f.write("email is:{}".format(email))
        password = request.form['inputPassword']
        #f.write("password is:{}".format(password))
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM `users` WHERE login=?;", (email,))
        x = c.fetchall()
        if len(x) > 0:
            registerStatus = False
            
            return redirect(url_for("AuthError"))
        else:
            reger = [email, password]
            #f.write("reger is:{}".format(reger))
            #f.close()
            c.execute("INSERT INTO users VALUES (?,?);", reger)
            conn.commit()
            conn.close()
            return redirect(url_for("editor"))
    return render_template("register.html")
"""@app.route('/register')
def reg():"""
    
    
@app.route("/AuthError")
def AuthError():
    return render_template("AuthError.html")

@app.route('/')
@app.route('/index')
def main():
    return render_template("index.html")
@app.route('/register')
def register():
    return render_template("register.html")
@app.route('/texts/<textName>')
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
def texts():
    return render_template("texts.html")
@app.route('/editor')
@basic_auth.required
def editor():
    return render_template("editor.html")   
@app.route('/about')
def about():
    return render_template("about.html")
"""@app.route('/admin')
@basic_auth.required
def admin():
    return render_template("admin/index.html")"""








if __name__ == "__main__":
    app.run(debug=True)