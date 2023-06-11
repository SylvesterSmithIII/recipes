from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask import jsonify

from helpers import login_required, random_recipe
# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///recipes.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/register", methods=["GET", "POST"])
def register():
    # if form submitted
    if request.method == "POST":
        # get value of form submittion
        username = request.form.get("username")
        password = request.form.get("password")
        password_2 = request.form.get("confirmation")
        # check for blank fields or unavailable usernames
        if username == "" or len(db.execute("SELECT username FROM users WHERE username = ?", username)) > 0:
            invalid = "Username already taken :/"
            return render_template("register.html", invalid=invalid)
        if password == "" or password != password_2:
            invalid = "Passowrds do not match"
            return render_template("register.html", invalid=invalid)
        # hash password for security
        password = generate_password_hash(password)
        # insert username and hashed password into database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password)
        # query database for username
        rows = db.execute("SELECT id FROM users WHERE username = ?", username)
        # remember which user is logged in
        session["user_id"] = rows[0]["id"]
        # render home page
        return redirect("/")

    return render_template("register.html")

@app.route("/login",  methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            invalid = "Invalid Username or Password :/"
            return render_template("login.html", invalid=invalid)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/")
@login_required
def index():
    recipe = random_recipe()
    session["recipe"] = recipe
    return render_template("index.html", recipe=recipe)

@app.route("/add-meal", methods=["POST"])
def add_meal():
    current_user = session["user_id"]
    recipe = session["recipe"]

    db.execute("INSERT INTO meals (user_id, name) VALUES (?, ?)", current_user, recipe['name'])

    if (len(db.execute("SELECT * FROM saved_recipes WHERE name = ?", recipe["name"])) == 0):
        db.execute("INSERT INTO saved_recipes (name, instructions, image_link, youtube_link) VALUES (?, ?, ?, ?)", recipe['name'], recipe['instructions'], recipe['image'], recipe['youtube_link'])
        recipe_id = db.execute("SELECT id FROM saved_recipes WHERE name = ?", recipe['name'])
        for i in range(len(recipe["ingredients"])):
            ingredient = recipe["ingredients"][i]
            measurement = recipe["measurments"][i]
            db.execute("INSERT INTO ingredients (recipe_id, ingredients, measurements) VALUES (?, ?, ?)", recipe_id[0]['id'], ingredient, measurement)

    added = "Adding recipe successful"
    return redirect("/")

@app.route("/history")
@login_required
def history():
    try:
        saved_recipes = db.execute("SELECT saved_recipes.name, saved_recipes.image_link FROM saved_recipes JOIN meals ON saved_recipes.name = meals.name WHERE meals.user_id = ?", session["user_id"])
    except Exception:
        print("No history Exception")

    return render_template("history.html", saved_recipes=saved_recipes)

""" test """