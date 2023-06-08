import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from flask import redirect, render_template, request, session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
import random
import time

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL("sqlite:///quiz.db")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def retry(message, page):
        flash(message)
        return render_template(page)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    session["winning"] = 0
    if request.method == "POST":
        if request.form.get("button1") == "New Game":
            db.execute(f"UPDATE users SET count = count + 1 WHERE id = {session['user_id']}")
            return redirect("/game")
        elif request.form.get("button2") == "High Scores":
            return redirect("/scores")
        elif request.form.get("button3") == "Log Out":
            return redirect("/logout")
    else:
        return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    thispage = "login.html"
    if request.method == "POST":
        if not request.form.get("username"):
            return retry("Must provide username!", thispage)
        elif not request.form.get("password"):
            return retry("Must provide password!", thispage)
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return retry("Invalid username and/or password!", thispage)
        session["user_id"] = rows[0]["id"]
        session["winning"] = 0
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    session["winning"] = 0
    thispage = "register.html"
    chars = "1234567890"
    special = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

    usernames = db.execute("SELECT username FROM users")
    usernameslist = []
    for i in range(len(usernames)):
        usernameslist = usernames[i]["username"]
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return retry("Must provide username!", thispage)
        elif username in usernameslist:
            return retry("Username already exists!", thispage)
        elif not password:
            return retry("Must provide password!", thispage)
        elif not (password == request.form.get("confirmation")):
            return retry("Passwords do not match!", thispage)
        elif (len(password) < 7) or (len(password) > 20):
            return retry("Password of invalid length", thispage)
        elif not (any((c in chars) for c in password) and any((c in special) for c in password)):
            return retry("Password must contain one special symbol and one number!", thispage)
        else:
            hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, hash)
            return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/result", methods=["GET", "POST"])
@login_required
def result():
    if request.method == "POST":
        if request.form.get("button1") == "Play Again":
            db.execute(f"UPDATE users SET count = count + 1 WHERE id = {session['user_id']}")
            return redirect("/game")
        elif request.form.get("button2") == "Back to Menu":
            return redirect("/")
        elif request.form.get("button3") == "Log Out":
            return redirect("/logout")
    else:
        return render_template("result.html", prize=session["winning"])

@app.route("/scores", methods=["GET", "POST"])
@login_required
def scores():
    if request.method == "POST":
        if request.form.get("exitgame") == "exitgame":
            return redirect("/")
    else:
        users = db.execute("SELECT username, money, count FROM users ORDER BY money DESC LIMIT 10")
        return render_template("scores.html", users=users)


@app.route("/game", methods=["GET", "POST"])
@login_required
def game():
    money = [0, 500, 1000, 2000, 5000, 10000, 20000, 50000, 75000, 150000, 250000, 500000, 1000000]
    if request.method == "POST":
        stage = db.execute(f"SELECT stage FROM gamestate WHERE userid = {session['user_id']}")
        if request.form.get("answer") == '1':
            time.sleep(6)
            db.execute(f"UPDATE gamestate SET stage = stage + 1 WHERE userid = {session['user_id']}")
            stage = db.execute(f"SELECT stage FROM gamestate WHERE userid = {session['user_id']}")
            if stage[0]['stage'] == 12:
                session["winning"] = 1000000
                db.execute(f"UPDATE users SET money = money + {session['winning']} WHERE id = {session['user_id']}")
                return redirect("result")
            questions = db.execute(f"SELECT * FROM ingame WHERE userid = {session['user_id']} AND gamestage = {stage[0]['stage']}")
            answers = db.execute(f"SELECT * FROM answers WHERE questionid = {questions[0]['questionid']}")
            random.shuffle(answers)
            currentmoney = money[stage[0]['stage']+1]
            return render_template("game.html", questions=questions, answers=answers, currentmoney=currentmoney, stage=stage[0]["stage"]+1, money=money)
        elif request.form.get("exitgame") == "exitgame":
            return redirect("/")
        else:
            time.sleep(6)
            session["winning"] = money[stage[0]['stage']]
            db.execute(f"UPDATE users SET money = money + {session['winning']} WHERE id = {session['user_id']}")
            return redirect("/result")

    else:
        exists = db.execute(f"SELECT count(*) FROM gamestate WHERE userid = {session['user_id']}")
        if exists[0]["count(*)"] > 0:
            db.execute(f"DELETE FROM gamestate WHERE userid = {session['user_id']}")
            db.execute(f"DELETE FROM ingame WHERE userid = {session['user_id']}")

        db.execute(f"INSERT INTO gamestate (userid) VALUES ({session['user_id']})")
        questionset = (db.execute("SELECT * FROM (SELECT * FROM game WHERE difficulty = 0) ORDER BY RANDOM() LIMIT 5") +
        db.execute("SELECT * FROM (SELECT * FROM game WHERE difficulty = 1) ORDER BY RANDOM() LIMIT 4") +
        db.execute("SELECT * FROM (SELECT * FROM game WHERE difficulty = 2) ORDER BY RANDOM() LIMIT 3"))

        insertquery = "INSERT INTO ingame (userid, questionid, questiontext, difficulty, gamestage) VALUES(?, ?, ?, ?, ?)"
        for i in range(len(questionset)):
            db.execute(insertquery, session['user_id'], questionset[i]['id'], questionset[i]['question'], questionset[i]['difficulty'], i)

        questions = db.execute(f"SELECT * FROM ingame WHERE userid = {session['user_id']} AND gamestage = 0")
        answers = db.execute(f"SELECT * FROM answers WHERE questionid = {questions[0]['questionid']}")
        random.shuffle(answers)
        currentmoney = money[1]
        stage = 1
        session["winning"] = 0
        return render_template("game.html", questions=questions, answers=answers, currentmoney=currentmoney, stage=stage, money=money)

"""
    TODO
    abilities
        ability counter in gamestate
        50/50
        expert opinion
        ask the audience
    MEDIA queries
        make it mobile friendly!
    readme/publish
    """

