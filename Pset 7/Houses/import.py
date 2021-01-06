# import data from the characters.csv
import csv
import cs50
import sys

# create db class to treat it as SQL execute functions
open("students.db", "w").close()
db = cs50.SQL("sqlite:///students.db")

# create the table as in the check50 it didnt have students.db
db.execute("CREATE TABLE students (first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMERIC)")

def main():
    if (len(sys.argv) != 2):
        print("Usage: python import.py characters.csv")
        return

    with open(sys.argv[1], "r") as file:
        reader = csv.DictReader(file, delimiter=",")

        for row in reader:
            house = row["house"]
            birth = row["birth"]
            name = row["name"]
            nameList = list(name.split())
            if len(nameList) == 3:
                first = nameList[0]
                middle = nameList[1]
                last = nameList[2]
            else:
                first = nameList[0]
                middle = "NULL"
                last = nameList[1]

            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",first, middle, last, house, birth)


main()



