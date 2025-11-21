from flask import Flask, render_template, request, redirect
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/dashboard")
def login():
    return render_template("dashboard.html")




if __name__ in "__main__":
    app.run(debug=True)