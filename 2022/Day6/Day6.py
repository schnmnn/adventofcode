import pandas as pd

def find_duplicates(string):
    # Create an empty dictionary to store the frequency of each character
    frequency = {}

    # Iterate over each character in the string
    for char in string:
        # If the character is not in the dictionary, add it with a frequency of 1
        if char not in frequency:
            frequency[char] = 1
        # If the character is already in the dictionary, increment its frequency by 1
        else:
            frequency[char] += 1

    # Create an empty list to store the duplicates
    duplicates = []

    # Iterate over the dictionary and append any characters with a frequency greater than 1 to the list of duplicates
    for char, count in frequency.items():
        if count > 1:
            duplicates.append(char)

    return duplicates


def create_substring(length):
    length_input = length
    string = input
    substrings_all = []
    for i in range(len(string)):
        substring = string[i:i+length_input]
        substrings_all.append(substring)
    return substrings_all


with open('Day6_input.txt') as f:
    input = f.read()
    

    
substrings_1 = create_substring(4)[:-3]

counter = 0
for i in substrings_1:
    duplicates = find_duplicates(i)
    if duplicates == []:
        break
    counter += 1
    
answer_1 = counter + 4
print('The answer to part one is ' + str(answer_1))

substrings_2 = create_substring(14)[:-13]

counter = 0
for i in substrings_2:
    duplicates = find_duplicates(i)
    if duplicates == []:
        break
    counter += 1
    
answer_2 = counter + 14

print('The answer to part two is ' + str(answer_2))
