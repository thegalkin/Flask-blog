from flask import Flask, render_template
import sqlite3
#from flask_admin import Admin
from flask_basicauth import BasicAuth












app = Flask(__name__)

#app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

#admin = Admin(app, name='microblog', template_mode='bootstrap3')

app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = '1234'
app.config['BASIC_AUTH_USERNAME'] = 'user'
app.config['BASIC_AUTH_PASSWORD'] = '1234'
basic_auth = BasicAuth(app)
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
"""@app.route('/admin')
@basic_auth.required
def admin():
    return render_template("admin/index.html")"""








if __name__ == "__main__":
    app.run(debug=True)