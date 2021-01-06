from flask import Flask, render_template, session, request, redirect
from flask_session import Session
from tempfile import mkdtemp
from helpers import login_required, apology
from checkers import checkValid, isEmpty
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from database_logic import add_user, exist_user, add_password, get_passwords, delete_password, get_password_info, update_password, exit_password

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


# create session
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
@login_required
def index():
    return render_template("index.html",  user_name=session["user_name"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        if (not exist_user(username, password)):
            return apology("Invalid username or password", 404)

        session["user_name"] = username
        return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if (request.method == "GET"):
        return render_template("register.html")
    else:
        password = request.form.get(
            "password")
        username = request.form.get("username")
        # check if valid
        if (not checkValid(username, password, request.form.get("passwordCheck"))):
            return apology("Invalid username or password", 403)
        # if user and password are valid
        add_user(username, password)
        # save the user in the session
        session["user_name"] = username
        return redirect("/")


@app.route("/broad", methods=["GET", "POST"])
@login_required
def broad():
    if (request.method == "GET"):
        list = get_passwords(session["user_name"])
        return render_template("broad.html", list=list)
    else:
        string = request.form.get("password_info")
        list = string.split()
        delete_password(session["user_name"], list[0], list[1])
        return redirect("/broad")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if (request.method == "GET"):
        return render_template("add.html")
    else:
        accountname = request.form.get("accountname")
        password = request.form.get("password")
        appname = request.form.get("appname")
        url = request.form.get("url")

        if (isEmpty(accountname, password, appname, url)):
            return apology("Please fill all the empty places", 404)
        if (exit_password(session["user_name"], accountname, appname)):
            return apology("This password has already existed", 404)

        add_password(session["user_name"], accountname, password, appname, url)
        return render_template("add.html", message="successfully added!")


@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    if (request.method == "POST"):
        if (request.form.get("update_needed")):
            accountname = request.form.get("accountname")
            password = request.form.get("password")
            appname = request.form.get("appname")
            url = request.form.get("url")
            update_password(session["user_name"],
                            accountname, password, appname, url)
            return render_template("update.html", message="Successfully updated", list=get_password_info(session["user_name"], accountname, appname))
        string = request.form.get("password_info")
        list = string.split()
        password_data = get_password_info(
            session["user_name"], list[0], list[1])
        return render_template("update.html", list=password_data)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run(debug=True)
