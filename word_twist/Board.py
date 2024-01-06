from enum import Enum

# This class contains the solution set and methods to print a board and
# and guess a word in a board.


class Board:
    # Class Variables (based on python convention, the underscore indicates
    # that they should be respected as private (even if there isn't really
    # a way to make them private):
    # solved (boolean that denotes if the board is solved)
    # __seed (the random seed used to generate the solution set)
    # __solutionSet (list of word Objects)

    # This initializes the Board object. It requires a list of words and
    # creates a list of word objects from them.
    def __init__(self, seed, solutionSet):
        self.solved = False
        self.__seed = seed
        # sorts be length and alphabetically
        solutionSet.sort(key=lambda s: (len(s), s))
        self.__solutionSet = []
        for word in solutionSet:
            self.__solutionSet.append(WordObject(word))

    # This essential creates a string representation of the current board.
    def PrintBoard(self):
        # A string to build onto
        boardString = "\n"
        # A count of how many words still need to be solved
        leftToSolve = 0
        # An initial word length to determine when we need to print a new line
        length = len(str(self.__solutionSet[0]))
        for wordObject in self.__solutionSet:
            # Check if the wordObject string is the same length as the current
            # length. Appends current wordObject string
            if len(str(wordObject)) == length:
                boardString += "[{}]".format(str(wordObject))
                if wordObject.wordState == WordState.Unsolved:
                    leftToSolve += 1
            # If word length increases, print appropriate message, increase
            # length, reset left to solve, and append current wordObject string
            else:
                boardString += "\n{} {}-letter words left to solve\n\n".format(
                    leftToSolve, length
                )
                length = len(str(wordObject))
                leftToSolve = 0
                boardString += "[{}]".format(str(wordObject))
                if wordObject.wordState == WordState.Unsolved:
                    leftToSolve += 1
        boardString += "\n{} {}-letter words left to solve\n".format(
            leftToSolve, length
        )
        boardString += "\nUse these letters: {}\n".format(self.__seed.upper())
        return boardString

    # This takes a guess string and compares it too the string objects. If
    # it's an empty string (indicating the user has given up) all unsolved
    # word objectws are updated to GaveUp). If it matches an unsolved word,
    # it updates that word Object state, checks to see if the puzzle is
    # solved, and stops the loop.
    def Guess(self, myString):
        # Check if board is already solved
        if self.solved is False:
            # Compare guess string with wordObjects
            for wordObject in self.__solutionSet:
                # If the guess string changes a wordObject state to True,
                # check if the puzzle is solved and break out of the loop
                if wordObject.Guess(myString):
                    self.solved = self.Solve()
                    break
        # Returns current value of solves
        # (True if puzzle all solved, False if puzzle not yet solved)
        return self.solved

    # This method checks is the puzzle is solved and returns a bool value
    # (true if solved, false if not solved)
    def Solve(self):
        # If any wordObject is in an unsolved state, return False
        for wordObject in self.__solutionSet:
            if wordObject.wordState == WordState.Unsolved:
                return False
        # If you exit the for loop with all words in a solved state,
        # return True.
        return True


# This is a Word State enumeration used by the WordObject class.
class WordState(Enum):
    Unsolved = 1
    Solved = 2
    GaveUp = 3


# The WordObject class contains the data and methods associated with a word in
# the game: the word string value, it's mask, and it's state
# (solved, unsolved, gave up).
# Other classes can call this object's Guess to compare a string with the word
# string value (Guess also handles a Give Up state change). I overrode the
# __str__ to return the appropriate string based on the word Object state.
class WordObject:
    # Class Variables (based on python convention, the underscore indicates
    # that they should be respected as private (even if there isn't really
    # a way to make them private):
    # __word
    # __wordMask
    # wordState

    # Initializes the values of the word object.
    def __init__(self, myString):
        self.__word = myString
        self.__wordMask = "-" * len(self.__word)
        self.wordState = WordState.Unsolved

    # Returns the appropriate string based on the state of the word Object.
    def __str__(self):
        if self.wordState == WordState.Unsolved:
            return self.__wordMask
        elif self.wordState == WordState.Solved:
            return self.__word
        elif self.wordState == WordState.GaveUp:
            return "{}".format(self.__word.upper())

    # This updates the state of the __word from unsolved to solved
    # (if passed in string matches the word) or gave up (if passed
    # in string is empty). It does not allow a wordObject to be change
    # states unless it is unsolved. It returns a bool (True if wordState
    # changes to Solved, False if wordstate remains unsolved)
    def Guess(self, myString):
        if self.wordState == WordState.Unsolved:
            if myString == self.__word:
                self.wordState = WordState.Solved
                return True
            elif myString == "":
                self.wordState = WordState.GaveUp
                return False
        else:
            return False
