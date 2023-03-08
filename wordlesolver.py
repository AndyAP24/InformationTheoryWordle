# Task 7: Implement a program worldesolver that takes two command line arguments (in the following order):

# file: a file with a list of five-letters words, one word per line;
# target*: a word that is present in the file, representing the target.
# Your program must then print on standard output, one per line, the sequence of guesses it makes to guess `target*, together with the value of H(T∣G,P)
#  (i.e., the value of the objective function for the guess) for each guess, and the obtained pattern, in the form

# guess1, H(T | G, P), YBGYB
# guess2,  H(T | G, P), YYGGB
# ...
# target,  0, GGGGG
# where, in the pattern, Y denotes a yellow square, B a black one, and G a green one. Extra credit: colored square emojis in place of the letters.

# An example file is attached below. Hint: While developing your program use a small subset of this file, or you will wait a long time for every run, unless you follow another hint below.

# You can use any programming language you want, as long as it is Python or Java =). If using Python, it must be possible to call your program with python wordlesolver.py file target. If using Java, your program must run with java Wordlesolver file target. If you really want to use a different programming language, please ask Matteo first, and add instructions on how to compile/run your program at the top of the README file included in your submission (see below).

# I expect your program to behave "well" (i.e., print an informative error message on standard error and exit) when the number of command line arguments is wrong, or file does not exist or is malformed (e.g., contains words of length different than five), or when target is not in file, or in any other case of error.

# Hint: given a target, the number of target words compatible with a pattern does not change from one round to another. Thus, assuming the dictionary of possible targets does not change, you can precompute it once for every possible combination of target and pattern, and have your program load these values from a file at the beginning of its execution. Doing this will greatly speed up the execution of your program.

# Hint: when filtering W
# , first eliminate the words non compatible with the black squares in the pattern, then those non compatible with the green squares in the pattern, and then those among the leftovers that are not compatible with the yellow squares. Doing this filtering correctly is trickier than it may look at first. =) Don't forget to filter out your guess.

import math
import sys
import random
import itertools as it
from collections import defaultdict


#Global variables:

#Possible words left
words = []

#Possible patterns left
global patterns;
patterns = []

#Filter words based on a guess made and resulting pattern.
#TODO: Optimize this piece of crap.
def filter_words(guess, pattern):
    global words
    new_words = []
    for word in words:
        flag = False
        for i in range(len(word)):
            if pattern[i] == "G" and word[i] != guess[i]:
                flag = True
            elif pattern[i] == "B" and guess[i] in word:
                #Current issue: If the guess is colog and the word is rossa, it will be filtered out. This is not correct.

                if word[i] == guess[i]:
                    flag = True
            elif pattern[i] == "Y" and word[i] == guess[i]:
                flag = True
            elif pattern[i] == "Y" and guess[i] not in word:
                flag = True
        
        if flag == False and word != guess:
            new_words.append(word)
    return new_words

 #Filter patterns based on a resulting pattern from a guess. Could do better by taking into account the number of yellows and greens.
def filter_patterns(pattern):
    global patterns
    new_patterns = []
    for p in patterns:
        #If the a square is green in the pattern, it must be green in the new pattern.
        #The number of greens + number of yellows must not decrease.
        if (p.count("G") + p.count("Y")) >= (pattern.count("G") + pattern.count("Y")):
            flag = False
            for i in range(len(p)):
                if pattern[i] == "G" and p[i] != "G":
                    flag = True
                    break
            if flag == False:
                new_patterns.append(p)
    patterns = new_patterns
#Calculate entropy of of the target at each step over the possible words left.
def calculate_entropy(some_words):
    if len(some_words) == 0:
        return 0
    entropy = math.log2(len(some_words))
    return entropy

#Generate all possible patterns (Combinations of 5 letters, each letter can be Y, B, or G)
def populate_pattern():
    pattern = []
    for i in it.product("YBG", repeat=5):
        pattern.append("".join(i))
    return pattern

#Pick a guess. This is the meat of the program. 
#For every possible guess resulting in every possible pattern, calculate the entropy of the target.
#Pick the guess that results in the lowest entropy average over all patterns.
def pick_guess():
    global words
    global patterns


    print ("words: ", len(words))

    min_alpha = float("inf")
    best_guess = "No guess found"

    for guess in words:
        # Create a dictionary to keep track of the number of compatible words for each pattern
        pattern_dict = {}
        for t in words:
            # Find the pattern
            pattern = generate_pattern(guess, t)
            
            if pattern not in patterns:
                continue
            # Add the pattern to the dictionary
            count = pattern_dict.get(pattern)
            if count is None:
                pattern_dict[pattern] = 1
            else:
                pattern_dict[pattern] = count + 1
        alpha = 0
        # Iterate through each pattern and add log of the size of the pruned alphabet
        for w in words:
            p = generate_pattern(guess, w)
            count = pattern_dict[p]
            alpha = alpha + math.log2(count)
        
        alpha = alpha / len(pattern_dict)
        # print(guess + " " + str(pattern_dict) + " " + str(alpha))
        if alpha < min_alpha:
            min_alpha = alpha
            best_guess = guess

        
    print(best_guess, min_alpha)
    return best_guess


#Generate pattern after a guess has been made.
def generate_pattern(guess, target):
    pattern = ["B", "B", "B", "B", "B"]
    #Make target a list so we can replace letters.
    target = list(target)
    guess = list(guess)

    #If the letter is in the same position, it's green.
    #If the letter is in the word, but not in the same position, it's yellow (But be careful not to count the same letter twice)
    #If the letter is not in the word, it's black.
    for i in range(len(target)):
        if target[i] == guess[i]:
            pattern[i] = "G"
            target[i] = " "
            guess[i] = " "
    
    for i in range(len(target)):
        if guess[i] in target and guess[i] != " ":
            pattern[i] = "Y"
            target[target.index(guess[i])] = " "
            guess[i] = " "
    


        

    
    return "".join(pattern)
        

#Load words from file
def load_words(file):
    words = []
    with open(file, "r") as f:
        for line in f:
            word = line.strip().lower()
            if len(word) == 5:
                words.append(word) 
            else:
                print("Invalid word of length different than 5: {}".format(word))
                sys.exit(1)
    return words



#This is supposed to do the whole thing.
def wordlesolver(words_file, target):
    global words; words = load_words(words_file)
    if target not in words:
        print("Target not in words file")
        sys.exit(1)
    global patterns
    patterns = populate_pattern()

    print ("Initial patterns: ", len(patterns))
    # guess = pick_guess()
    guess = "crane"

    #Do the above steps in a loop until you get the target.
    while guess != target:
        
        
        pattern = generate_pattern(guess, target)
        print (pattern)
        filter_patterns(pattern)
        words = filter_words(guess, pattern)
        
        if guess == target:
            print ("Target found")
            sys.exit(0)
        if len(words) == 0:
            print("No words left")
            sys.exit(1)
        
        guess = pick_guess()


def pattern_check(p, t):
    words_file = "wordlewords.txt"
    global words
    words = load_words(words_file)
    if t not in words:
        print(f"Target {t} not in words file")
        sys.exit(1)
    global patterns
    patterns = populate_pattern()
    return filter_words(p, t)



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python wordlesolver.py words_file target")
        sys.exit(1)
    
    words_file = sys.argv[1]
    target = sys.argv[2].lower()
    wordlesolver(words_file, target)