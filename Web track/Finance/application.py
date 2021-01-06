import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # return a list of dict objs
    userInfo= db.execute("SELECT * FROM bought where user_id = :user_id", user_id = session["user_id"])
    currentTotal = 0
    for each in userInfo:
        currentTotal += each["total"]
    return render_template("index.html", defaultCash=10000, userInfo = userInfo, currentTotal = currentTotal)
    # return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if (request.method == "POST"):
        if not request.form.get("symbol") or not request.form.get("shares"):
            return apology("Invalid symbol or shares", 403)
        # check if symbol is valid or not
        stockInfoList = lookup(request.form.get("symbol"))
        if (not stockInfoList):
            return apology("Invalid symbol", 403)

        # insert the data into database and redirect to index page
        db.execute("INSERT INTO history ('user_id', 'symbol', 'shares', 'price', 'datetime') VALUES (:user_id, :symbol, :shares, :price, :datetime)",
            user_id=session["user_id"], symbol=stockInfoList["symbol"],
            shares=request.form.get("shares"), price=(stockInfoList["price"] * float(request.form.get("shares"))),
            datetime=datetime.now())
        # insert the data to "bought" table in database
        boughtList = db.execute("SELECT * FROM bought WHERE user_id = :user_id", user_id = session["user_id"])
        if (not boughtList):
            db.execute("INSERT INTO bought ('user_id', 'symbol', 'shares', 'price', 'total', 'name') VALUES (:user_id, :symbol, :shares, :price, :total, :name)",
            user_id = session["user_id"], symbol=stockInfoList["symbol"],
            shares=request.form.get("shares"), price=float(stockInfoList["price"]),
            total = (stockInfoList["price"] * float(request.form.get("shares"))),
            name = stockInfoList["name"])
        else:
            for each in boughtList:
                if (each["symbol"] == request.form.get("symbol")):
                    currentPrice = each["price"];
                    currentShares = each["shares"]
                    db.execute("UPDATE bought SET shares = :shares, price = :price, total = :total WHERE user_id = :user_id AND symbol = :symbol",
                    shares = int(currentShares) + int(request.form.get("shares")),
                    price = float(currentPrice),
                    total = stockInfoList["price"] * float(request.form.get("shares")),
                    user_id = session["user_id"], symbol = stockInfoList["symbol"])
        # calculate the price after the purchase
        currentCash = db.execute("SELECT cash FROM users WHERE id = :user_id;", user_id = session["user_id"])
        db.execute("UPDATE users SET cash=:price WHERE id= :user_id", price=(currentCash[0]["cash"] - stockInfoList["price"]* float(request.form.get("shares"))), user_id = session["user_id"])
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    historyList = db.execute("SELECT * FROM history WHERE user_id=:user_id", user_id = session["user_id"])
    return render_template("history.html", history = historyList)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if (request.method == "GET"):
        return render_template("quote.html")
    else:
        if not request.form.get("symbol"):
            return apology("Symbol is required", 403)
        stockInfoList = lookup(request.form.get("symbol"))
        if (stockInfoList):
            return render_template("/quoted.html", list = stockInfoList)
        else:
            return apology("Symbol is invalid", 403)


@app.route("/register", methods=["GET", "POST"])
def register():
    if (request.method == "GET"):
        return render_template("register.html")
    else:
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif (request.form.get("password") != request.form.get("passwordCheck")):
            return apology("Passwords do not match", 403)

        password = generate_password_hash(request.form.get("password"))
        username = request.form.get("username")
        db.execute("INSERT INTO users ('username', 'hash') VALUES (:username, :password)",
        username=username, password=password)
        return redirect("/login")
    # return apology("TODO")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if (request.method == "POST"):
        if not request.form.get("symbol") or not request.form.get("shares"):
            return apology("Invalid symbol or shares", 403)

        # take the stockInfoList info from look up function
        stockInfoList = lookup(request.form.get("symbol"))
        # check if shares are still equal
        availableShares = db.execute("SELECT * FROM bought WHERE :user_id = :user_id AND symbol = :symbol",
            user_id = session["user_id"],
            symbol = request.form.get("symbol"))
        availableShares[0]["shares"] -= int(request.form.get("shares"))
        if (availableShares[0]["shares"] < 0):
            return apology("Invalid shares, you may run out of shares", 403)
        elif (availableShares[0]["shares"] == 0):
            # delete the row in "bought" table
            db.execute("DELETE FROM bought WHERE user_id = :user_id AND symbol = :symbol",user_id = session["user_id"],symbol = stockInfoList["symbol"])
            # insert to "history" table
            db.execute("INSERT INTO history ('user_id', 'symbol', 'shares', 'price', 'datetime') VALUES (:user_id, :symbol, :shares, :price, :datetime)",
                user_id=session["user_id"], symbol=stockInfoList["symbol"],
                shares= -1 * int(request.form.get("shares"), price=(stockInfoList["price"] * int(request.form.get("shares"))),
                datetime=datetime.now()))
            # redirect the page
            return redirect("/")
        # if availableShares are still > 0 after selling shares
        # insert the data into "history" table
        db.execute("INSERT INTO history ('user_id', 'symbol', 'shares', 'price', 'datetime') VALUES (:user_id, :symbol, :shares, :price, :datetime)",
            user_id=session["user_id"], symbol=stockInfoList["symbol"],
            shares=-1 * int(request.form.get("shares")), price=(stockInfoList["price"] * float(request.form.get("shares"))),
            datetime=datetime.now())
        # insert the data to "bought" table in database
        boughtList = db.execute("SELECT * FROM bought WHERE user_id = :user_id AND symbol = :symbol", user_id = session["user_id"], symbol = stockInfoList["symbol"])
        db.execute("UPDATE bought SET shares = :shares, price = :price, total = :total WHERE user_id = :user_id AND symbol = :symbol",
                    shares = availableShares[0]["shares"],
                    price = stockInfoList["price"],
                    total = stockInfoList["price"] * float(request.form.get("shares")),
                    user_id = session["user_id"], symbol = stockInfoList["symbol"])
        # calculate the price after the selling
        currentCash = db.execute("SELECT cash FROM users WHERE id = :user_id;", user_id = session["user_id"])
        db.execute("UPDATE users SET cash=:price WHERE id= :user_id", price=(currentCash[0]["cash"] + stockInfoList["price"]* int(request.form.get("shares"))), user_id = session["user_id"])
        return redirect("/")
    else:
        options = db.execute("SELECT symbol FROM bought WHERE user_id = :user_id", user_id = session["user_id"])
        return render_template("sell.html", options = options)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
