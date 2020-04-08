from flask import Flask
app = Flask(__name__)
@app.route("/user/<id>/")
def user_profile(id):
    return "this page belongs to user #{}".format(id)
    
if __name__ == "__main__":
    app.run(debug=True)