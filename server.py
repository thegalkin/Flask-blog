from flask import Flask, render_template
import sqlite3
#from flask_admin import Admin
from flask_basicauth import BasicAuth
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired







app = Flask(__name__)

#app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

#admin = Admin(app, name='microblog', template_mode='bootstrap3')

app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = '123456789'
app.config['BASIC_AUTH_USERNAME'] = 'user'
app.config['BASIC_AUTH_PASSWORD'] = '123456789'
basic_auth = BasicAuth(app)

class registrationForm(FlaskForm):
    email = TextField('email', [validators.Length(min=4, max=50)])
    password = PasswordField('password', [
        validators.Length(min = 9, max=30)
        
    ])
@app.route('/submit', methods = ('GET', 'POST'))
def submit():
    form = registrationForm()
    if form.validate_on_submit():
        return redirect('success')
    return render_template('register.html', form=form)


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