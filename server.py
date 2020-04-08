from flask import Flask, render_template,

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def main():
    return render_template("index.html")

@app.route('/texts/<textName>')
def texts():
    return render_template("texts.html")   
if __name__ == "__main__":
    app.run(debug=True)