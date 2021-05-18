import csv
import sys
from cs50 import SQL

#In roster.py, write a program that prints a list of students for a given house in alphabetical order.
#Your program should query the students table in the students.db database for all of the students in the specified house.
#Your program should then print out each student’s full name and birth year (formatted as, e.g., Harry James Potter, born 1980 or Luna Lovegood, born 1981).
#Each student should be printed on their own line.
#Students should be ordered by last name. For students with the same last name, they should be ordered by first name.

if len(sys.argv) != 2: # If there are not 2 arguements
    print("Usage: python roster.py house_name") # Print proper usage
    exit(1)


db = SQL("sqlite:///students.db") # Database will have been imported from Import.py
roster = db.execute("SELECT * FROM students WHERE house = (?) ORDER BY last, first", sys.argv[1])

for row in roster:
        print(row["first"] + " " + (row["middle"] + " " if row["middle"] else "") + row["last"] + ", born " + str(row["birth"]))

    # Within internal brackets, if row["middle"] checks to see if it exisit with a value as opposed to seeing if it is equalt to None.
    # str used to allow birth year to print as a string rather than how is it stored as an int.
