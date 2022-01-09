"""
    accurate in terms of handling all occurences, casing and special characters
"""

from re import split
from time import perf_counter
import os
import psutil


def get_columns(filename):
    """
        read a csv file and yield column contents
        returns a generator
    """

    with open(filename, encoding="utf-8") as csv_file:
        for line in csv_file.readlines():
            
            if line == "\n":
                continue
            
            line = line.strip("\n")
            
            yield line.split(",")


def handle_case(word: str, rep_str: str):
    """
        test case and format rep_str to match word's case and return it
        returns a str
    """

    if word.istitle():
        
        return rep_str.title()
    elif word.isupper():
        return rep_str.upper()
    else:
        return rep_str


start = perf_counter()
input_file = open("t8.shakespeare.txt", encoding="utf-8")
output_file = open("t8.shakespeare.translated.txt", "a", encoding="utf-8")
results_file = open("frequency.csv", "a", encoding="utf-8")
find_words_file = open("find_words.txt", encoding="utf-8")


english_french_words = {columns[0]: columns[1]
                        for columns in get_columns("french_dictionary.csv")}

word_frequency = {line.strip("\n"): 0 for line in find_words_file.readlines()}

for line in input_file.readlines():
    
    words = line.split()
    for word in words:
        
        word = split("[.,:;!'/\")]", word)[0]
        if word.lower() in word_frequency:
            
            r = handle_case(word, english_french_words[word.lower()])
            line = line.replace(word, r)
            
            word_frequency[word.lower()] += 1
    output_file.write(line)


results_file.write(f"English,French,Frequency\n")
for row in english_french_words.items():
    results_file.write(f"{row[0]},{row[1]},{word_frequency[row[0]]}\n")


input_file.close()
output_file.close()
results_file.close()
find_words_file.close()


time_taken = perf_counter() - start
memory_usage = psutil.Process(os.getpid()).memory_info().rss / 1048576
print(f"[TIME TO PROCESS] : {time_taken} seconds")
print(f"[MEMORY USED] : {memory_usage} MB")
with open("Performance.txt", "w") as f:
    f.writelines(["TIME TO PROCESS: " + str(time_taken) + "sec" ,  "\n MEMORY USED: " + str(memory_usage) + "MB"])