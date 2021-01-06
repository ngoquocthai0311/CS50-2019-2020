# TODO
import cs50
import sys

def main():
    if (len(sys.argv) != 2):
        print("Usage: python roster.py house")
        return

    house = sys.argv[1]
    db = cs50.SQL("sqlite:///students.db")
    listName = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", house)

    for row in listName:
        if row["middle"] == "NULL":
            middle = ""
        else:
            middle = row["middle"] + " "
        print(row["first"] + " " + middle + row["last"] + ", born " + str(row["birth"]))



main()