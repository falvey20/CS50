import csv
from sys import argv

def longest_match(dna_sequence, str_sequence): # define function for use in main to establish longest chain of str_sequence
    longest_str_chain = 0 # initialise longes chain to 0
    search_window_size = len(str_sequence) # length of dna sequence that will be searched is the length of each str
    for i in range(len(dna_sequence)): # until entire dna sequence is searched
        count = 0 # count keeps tally of number of repetitions in current loop
        while True:
            first_index = i + search_window_size * count # first search index position is i plus the window size(multiplied for each increased count)
            end_index = first_index + search_window_size # end position of index search is the first in addition to the length of current str_sequence
            if dna_sequence[first_index:end_index] == str_sequence: # if the current window selected is equal to the str_sequence increase count by 1
                count += 1
                if count > longest_str_chain: # if the count is now longer than the longest_chain update the value of the lognest chain
                    longest_str_chain = count
            else:
                break
    return longest_str_chain # longest chain to be used in main

def main():
    if len(argv) != 3: # if there are not 3 arguements (dna.py file.csv file.txt) return proper usage format
        print("Usage: python dna.py data.csv sequence.txt")
        exit(1) # return error 1

    database = open(argv[1]) # the csv database is provided in the positon after program name
    data = csv.DictReader(database) # DictReader creates readable dictionariy to 'data'

    with open(argv[2]) as dnafile: # with open closes by default
        dna_sequence = dnafile.read() # dna_sequence stores read dna file

    counts = {} # curly braces for dictionary, store the longest match from dna and strsequences

    for str_sequence in data.fieldnames[1:]: # isolate each str_sequence from fieldname 1 (ignoring 'names')
        counts[str_sequence] = longest_match(dna_sequence, str_sequence)

    for row in data: # for each row in data if the counts for the str_sequence are the same as the integer euqivalent of the rows str_sequences
        if all(counts[str_sequence] == int(row[str_sequence]) for str_sequence in counts):
            print(row["name"])
            database.close()
            return
    print("No Match")
    database.close()
main()











































