"""
Description: This little program reads in a file containing a lexicon,
builds a lexicon data structure, allows the user to pick an min and max
word length, select a random word of the max word length, and gets all
the words that are permutations of the letters in that word between the
min and max word length.
Problems: I really wanted to make a directed graph to solve the problem,
but then decided it was more complicated to do that then the problem
deserved. PS, this starts to have some noticable performance issues when
generating the board when you set min and max word length ranges to 2-12,
and lags A LOT (like a minute-ish) when you set min and max word word
length to 2-18. Although the game play is still fine.
"""


from Lexicon import Lexicon


# generator used to efficiently read file
def readBigFile(fileObject):
    # A big fat loop
    while True:
        data = fileObject.readline().strip()
        # breaks when data is some 0 or empty container
        if not data:
            break
        yield data


userInput = "a"
# default lexicon used for testing
lexicon = {
    "loving",
    "voling",
    "lingo",
    "login",
    "ling",
    "lion",
    "loin",
    "long",
    "gin",
    "ion",
    "log",
    "nil",
    "nog",
    "oil",
}
boardObject = None

# Read File Loop
while userInput != "q":
    userInput = input(
        "Enter a file name, enter to use a default lexicon, or q to quit: "
    )
    # check if using default lexicon
    if userInput == "":
        print("The game will use the tiny, tiny default lexicon.")
        break
    # Open file, empty lexicon, build new lexicon, break out of loop
    try:
        with open(userInput, "r") as lexiconFile:
            lexicon = set()
            for word in readBigFile(lexiconFile):
                lexicon.add(word)
        break
    # Catch File not found errors, print message, reloop
    except FileNotFoundError:
        if userInput != "q":
            print("I can't find that file. Try again.")
        continue

# Build Database (it the user isn't quitting)
if userInput != "q":
    print("loading...")
    lexicon = Lexicon(lexicon)

# Game Loop
while userInput != "q":
    # Game Prep Loop
    while userInput != "q":
        try:
            # Get board parameters
            userInput = input("Enter a minimum word size or q to quit: ")
            minSize = int(userInput)
            userInput = input("Enter a maximum word size or q to quit: ")
            maxSize = int(userInput)
            # Check that min and max numbers makes sence
            if (
                (minSize < lexicon.minLength)
                or (minSize > maxSize)
                or (maxSize > lexicon.maxLength)
            ):
                print("Woh there. Your numbers are fishy!")
                print(
                    "I know I didn't tell you this before, but your word "
                    "size must be between {} and {} inclusive.".format(
                        lexicon.minLength, lexicon.maxLength
                    )
                )
                continue
            # Create board object
            boardObject = lexicon.GetBoard(minSize, maxSize)
            print("Let's Play!!! You can press enter to give up or q to quit.")
            break
        except ValueError:
            if userInput != "q":
                print("You entered something that is not a number. Try again.")
            continue

    # Game Play Loop
    while userInput != "q":
        # Print Board
        print(boardObject.PrintBoard())
        # Accept input
        userInput = input("Guess a word: ")
        # check for quit
        if userInput == "q":
            boardObject.Guess("")
            print(boardObject.PrintBoard())
            print("YOU ARE A QUITTER! SHAME...")
            break
        # check for give up
        elif userInput == "":
            boardObject.Guess(userInput)
            print(boardObject.PrintBoard())
            print("Good Try!\nLet's Play Again!\n")
            break
        # check for solve
        elif boardObject.Guess(userInput.strip().lower()):
            print(boardObject.PrintBoard())
            print("YOU WON!!\nLet's Play Again!\n")
            break

print("Goodbye!!!!")
