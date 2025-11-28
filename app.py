from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

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
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    ownerid = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String(255), unique=True, nullable=False)
    address = db.Column(db.String(255), unique=False, nullable=True)
    capacity = db.Column(db.Integer, unique=False)
    description = db.Column(db.String(255), unique=False, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    houseid = db.Column(db.Integer, db.ForeignKey("house.id"))
    name = db.Column(db.String(255), unique=True, nullable=False)
    checked = db.Column(db.Integer, unique=False, nullable=True)

# Wrapper for login check
def login_required(f):
    @wraps(f)
    def decorated_functions(*args, **kwargs):
        if "user_id" not in session:
            flash("You need to log in first", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_functions


# HOME PAGE
@app.route("/")
@app.route("/home")
def home():
    if "username" in session:
        return redirect(url_for('welcome'))
    return render_template("index.html")


# SIGNUP PAGE
@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]


        if User.query.filter_by(username=username).first():
            flash("Username already exists", "error")
            return render_template("signup.html")
        
        if User.query.filter_by(email=email).first():
            flash("Email already registered", "error")
            return render_template("signup.html")
        
        # Create new user in database
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        session["username"] = new_user.username
        session["email"] = new_user.email
        flash("Your account has been successfully created!", "success")
        return redirect(url_for("welcome"))
    return render_template("signup.html")


# LOGIN PAGE
@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # Get form data
        # username = request.form["username"] # Changed to email for login
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        # Check if user exists and password is correct
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["email"] = user.email
            flash("Login successful!", "success")
            return redirect(url_for("welcome"))
        
        flash("Invalid username or password.", "error")
        return render_template("login.html")
    
    return render_template("login.html")
    
@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for("home"))


# WELCOME PAGE
@app.route("/welcome")
@login_required
def welcome():
    user=User.query.get(session["user_id"])
    return render_template("welcome.html", user=user)

# DASHBOARD PAGE
@app.route("/dashboard")
@login_required
def dashboard():
    user=User.query.get(session["user_id"])
    return render_template("dashboard.html", user=user)


# HOUSE LIST PAGE
@app.route("/houselist")
def houselist():    
    houses = House.query.all()
    return render_template("houselist.html", houses=houses)

# CREATE HOUSE PAGE
@app.route("/createhouse", methods=["GET","POST"])
@login_required
def createhouse():
    if request.method == "POST":
        name = request.form.get("name")
        address = request.form.get("address")
        capacity = request.form.get("capacity")
        description = request.form.get("description")
        password = request.form.get("password")

        user = User.query.get(session["user_id"])

        if not all([name, address, capacity, description, password]):
            flash("Fill all the information, please", "error")
            return redirect(url_for("createhouse"))
        
        new_house = House(
            name=name,
            address=address,
            capacity=int(capacity),
            description=description,
            password=password,
            ownerid=user.id
        )
        db.session.add(new_house)
        db.session.commit()
        flash("House created successfully!", "success")
        return redirect(url_for("houselist"))
    
    return render_template("createhouse.html")

# TASK PAGE
@app.route("/taskpage/<int:house_id>")
def taskpage(house_id):
    house = House.query.get_or_404(house_id)
    return render_template("taskpage.html", house=house)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)