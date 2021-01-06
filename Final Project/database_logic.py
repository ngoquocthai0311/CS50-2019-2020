import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash


def connect():
    try:
        conn = sqlite3.connect("data.db")
        return conn
    except (Exception) as error:
        print(error.__traceback__)


def add_user(username, password):
    conn = connect()
    cursor = conn.cursor()
    hash = generate_password_hash(password)
    cursor.execute(
        "INSERT INTO users ('username', 'hash') VALUES (?, ?);", (username, hash))
    conn.commit()
    conn.close()


def add_password(user, accountname, password, appname, url):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords ('username', 'appname', 'accountname', 'password', 'url') VALUES (?, ?, ?, ?, ?);",
                   (user, appname, accountname, password, url))
    conn.commit()
    conn.close()

def get_password_info(username, accountname, appname):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM passwords WHERE username=? AND accountname=? AND appname=?",
                   (username, accountname, appname))
    row = cursor.fetchall()
    return row


def delete_password(user, accountname, appname):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passwords WHERE username=? AND accountname=? AND appname=?",
                   (user, accountname, appname))
    conn.commit()
    conn.close()


def exist_user(user_name, password):
    if (not user_name or not password):
        return False

    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM users WHERE username=?', (user_name,))
    row = cursor.fetchall()
    if (len(row) != 1 or not check_password_hash(row[0][1], password)):
        return False
    return True

def exit_password(username, accountname, appname):
    list = get_password_info(username, accountname, appname)
    if (not list):
        return False
    return True


def get_passwords(username):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM passwords WHERE username=?;", (username, ))
    row = cursor.fetchall()
    return row


def update_password(username, accountname, password, appname, url):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE passwords SET password=? WHERE username=? AND accountname=? AND appname=? AND url=?",
                   (password, username, accountname, appname, url))
    conn.commit()
    conn.close()
