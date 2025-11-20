from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def index():
    return "testing 123"

@app.route("/login")
def login():
    return "login"



if __name__ in "__main__":
    app.run(debug=True)