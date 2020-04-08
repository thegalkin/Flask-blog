from flask import Flask, render_template
import sqlite3











app = Flask(__name__)
@app.route('/')
@app.route('/index')
def main():
    return render_template("index.html")

@app.route('/texts/<textName>')
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
def texts():
    return render_template("texts.html")   
if __name__ == "__main__":
    app.run(debug=True)