import cs50 
import math 
import string

#index = 0.0588 * L - 0.296 * S - 15.8    Coleman Liau Index

providedText = cs50.get_string("Text: \n")
numLetters = 0
numSentences = 0 
numWords = 1

for char in providedText:
    if char.isalpha():
        numLetters += 1
    if char.isspace():
        numWords += 1
    if char in [".", "?", "!"]:
        numSentences += 1

print(f"Letters in text: {numLetters}")
print(f"Words in text: {numWords}")
print(f"Sentences in text: {numSentences}")

colemanLiauIndex = round(0.0588 * (numLetters / numWords * 100) - 0.296 * (numSentences / numWords * 100) - 15.8)
    
if colemanLiauIndex >= 16:
    print("Grade 16+")
elif colemanLiauIndex < 1:
    print("Before Grade 1")
else:
    print(f"Grade {colemanLiauIndex}")
    