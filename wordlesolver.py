# Task 7: Implement a program worldesolver that takes two command line arguments (in the following order):
# Hint: given a target, the number of target words compatible with a pattern does not change from one round to another. Thus, assuming the dictionary of possible targets does not change, you can precompute it once for every possible combination of target and pattern, and have your program load these values from a file at the beginning of its execution. Doing this will greatly speed up the execution of your program.

import math
import sys
import emoji

# Dictionary, pruned as we go
words = []


# Filter words based on a guess made and resulting pattern
def filter_words(guess, pattern):
    global words
    new_words = []
    for word in words:
        if generate_pattern(guess, word) == pattern:
            new_words.append(word)
    return new_words


# Calculate entropy of the target at each step over the possible words left
def calculate_entropy(some_words):
    if len(some_words) == 0:
        return 0
    entropy = math.log2(len(some_words))
    return entropy


# For every combination of guess and target, calculate alpha and pick the target with the lowest alpha
def pick_guess(target):
    global words

    min_alpha = float("inf")
    best_guess = "No guess found"

    for guess in words:
        # Create a dictionary to keep track of the number of compatible words for each pattern
        pattern_dict = {}
        for t in words:
            # Find the pattern
            pattern = generate_pattern(guess, t)

            # Add the pattern to the dictionary
            count = pattern_dict.get(pattern)
            if count is None:
                pattern_dict[pattern] = 1
            else:
                pattern_dict[pattern] = count + 1

        # Calculate alpha
        alpha = 0
        for w in words:
            p = generate_pattern(guess, w)
            count = pattern_dict[p]
            alpha = alpha + math.log2(count)

        if alpha < min_alpha:
            min_alpha = alpha
            best_guess = guess

    pattern = generate_pattern(best_guess, target)
    print(f"{best_guess}, {round(min_alpha, 2)}, {emoji_pattern(pattern)}")
    return best_guess


# Generate pattern after a guess has been made
def generate_pattern(guess, t):
    pattern = ["B", "B", "B", "B", "B"]
    # Make target a list so we can replace letters
    t = list(t)
    guess = list(guess)

    # Follow rules to generate pattern
    for i in range(len(t)):
        if t[i] == guess[i]:
            pattern[i] = "G"
            t[i] = None
            guess[i] = ""

    for i in range(len(t)):
        if guess[i] in t:
            pattern[i] = "Y"
            t[t.index(guess[i])] = None
            guess[i] = ""

    return "".join(pattern)


# Load words from file
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


# Translate a pattern of "Y", "G", "B" into emojis
def emoji_pattern(pattern):
    pattern_emoji = ""
    for color in pattern:
        if color == "G":
            pattern_emoji += emoji.emojize(":green_square:")
        elif color == "Y":
            pattern_emoji += emoji.emojize(":yellow_square:")
        else:
            pattern_emoji += emoji.emojize(":black_large_square:")
    return pattern_emoji


# Run the solver
def wordlesolver(words_file, target):
    global words
    words = load_words(words_file)
    if target not in words:
        print("Target not in words file")
        sys.exit(1)

    # This guess is hardcoded from a full run we did (which took ~35 min)
    guess = "tares"
    alpha = 114372.87
    pattern = generate_pattern(guess, target)
    print(f"{guess}, {alpha}, {emoji_pattern(pattern)}")

    # Do the above steps in a loop until you get the target
    while guess != target:

        pattern = generate_pattern(guess, target)
        words = filter_words(guess, pattern)
        
        if len(words) == 0:
            print("No words left")
            sys.exit(1)

        guess = pick_guess(target)

    print("Target found!")

# Helper method for test_pattern_check() tester method
def pattern_check(p, t):
    words_file = "wordlewords.txt"
    global words
    words = load_words(words_file)
    if t not in words:
        print(f"Target {t} not in words file")
        sys.exit(1)
    return filter_words(t, p)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python wordlesolver.py words_file target")
        sys.exit(1)

    words_file = sys.argv[1]
    target = sys.argv[2].lower()
    wordlesolver(words_file, target)