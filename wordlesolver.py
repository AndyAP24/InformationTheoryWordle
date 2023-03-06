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
from collections import defaultdict


import sys
import random
from collections import defaultdict
import itertools

def filter_words(words, pattern, guess):
    filtered_words = []
    return filtered_words

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

def wordlesolver(words_file, target):
    words = load_words(words_file)
    if target not in words:
        print("Target not in words file")
        sys.exit(1)

def pattern_gen():
    """
    Returns a list of all possible 'BGY' patterns of size 5
    """
    return [numToPattern(n) for n in range(3**5)]

def numToPattern(n):
    """
    Converts number to a ternary digit using "B", "Y", and "G"
    """
    if n == 0:
        return "BBBBB"
    ps = []
    while n:
        n, r = divmod(n, 3)
        ps.append(numToLetter(r))
    
    while len(ps) < 5: # pad out "B"s (aka 0s)
        ps.append("B")

    return ''.join(reversed(ps))

def numToLetter(k):
    assert k >= 0, "invalid value for num"
    assert k < 3, "invalid value for num"
    if k == 0:
        return "B"
    if k == 1:
        return "Y"
    if k == 2:
        return "G"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python wordlesolver.py words_file target")
        sys.exit(1)
    
    words_file = sys.argv[1]
    target = sys.argv[2].lower()
    wordlesolver(words_file, target)