from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "SomeSecretKey"  # Replace with a secure key in production

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Database Model (Model for each User ~ Single Row in Database)
class User(db.Model):
    # Class variables for the User model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# HOME PAGE
@app.route("/")
@app.route("/home")
def home():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template("index.html")

# SIGNUP PAGE
@app.route("/signup", methods=['GET','POST'])
def signup():
    # Get form data
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    # Check if user already exists
    if user:
        return render_template("index.html", error="Username already exists")
    else:
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for("dashboard"))

# LOGIN PAGE
@app.route("/login", methods=['GET','POST'])
def login():
    # Get form data
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    # Check if user exists and password is correct
    if user and user.check_password(password):
        session["username"] = user.username
        return redirect(url_for("dashboard"))
    else:
        return render_template("index.html", error="Invalid username or password")
    


# DASHBOARD PAGE
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")






if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)