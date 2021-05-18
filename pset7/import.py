import csv
import sys
from cs50 import SQL


# If there are not two provided arguements, exit and print proper usage statement.
if len(sys.argv) != 2:
    print("Usage: python import.py characters.csv")
    exit(1) #exit with error 1
    
db = SQL("sqlite:///students.db")

filename = sys.argv[1] # filename is 2nd argv
# Check that filename ends with .csv extension, otherwise exit and print request for csv.
if (filename.endswith(".csv")) != True:
    print("Data provided must be in csv format")
    exit(2)
print("Valid Usage")
# open the csv file and read with DictReader
with open(filename, "r") as characters:
    dictReader = csv.DictReader(characters, delimiter = ",")
# Split the names up using .split()
    for row in dictReader:
        name = row["name"]
        nameList = name.split()
# If character only has 2 names (No middle name) attribute None to middle name in table
        if len(nameList) == 2:
            firstName = nameList[0]
            lastName = nameList[1]
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)", firstName, None, lastName, row["house"], row["birth"])
# Character has middle name so all points in row filled with data from csv.
        elif len(nameList) == 3:
            firstName = nameList[0]
            middleName = nameList[1]
            lastName = nameList[2]
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)", firstName, middleName, lastName, row["house"], row["birth"])




