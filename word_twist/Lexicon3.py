import itertools
from random import choice

from Board import Board


# So, here's what I've done. The letters in each word in a lexicon are
# alphabatized to create a key. All words with the same key are stored
# in a "node" (for example, "lion" and "loin" are stored together under
# the key "ilno"). Nodes are stored in levels based on word length (all
# 4-letter words are in the same level object, all 3-letter words are in
# the same level object). The Lexicon class keeps a dictionary of levels
# (key = word length, value = instance of level object). I thought about
# storing edges to make a directed graph, but that got to be pretty
# complicated when I considered that some level 5 keys would need edges
# directly to level 3 keys, etc. The way it's set up, it handles insertion
# of new words and even duplicates of words.
class Lexicon:
    # Class variables:
    # _levelDict
    maxLength = None
    minLength = None

    # This initializes the object with a _levelDict and adds each word in the
    # list to the data structure
    def __init__(self, lexiconList):
        self._levelDict = {}
        self.maxLength = 0
        self.minLength = 100
        for word in lexiconList:
            self.AddWord(word)

    # This adds a word to the appropriate level Object based on word length.
    # keeps track of max word length
    def AddWord(self, myString):
        key = len(myString)
        if key < self.minLength:
            self.minLength = key
        if key > self.maxLength:
            self.maxLength = key
        self._levelDict.setdefault(key, Level()).AddWord(myString)

    # This selects a random key based on the max word length and finds the
    # solution set based on that key.
    # It generates a board object and passes that back to the caller.
    def GetBoard(self, minNum, maxNum):
        # get a random key based on max word length (makes sure the max num
        # exist by comparing with max length)
        maxNum = min(maxNum, self.maxLength)
        randKey = self._levelDict[maxNum].GetRandomKey()
        solutionSet = set()
        # for every number in the min and max range inclusive, create a set of
        # possible keys based on the randomkey)
        testKey = None
        for level in range(minNum, maxNum + 1):
            keys = itertools.combinations(randKey, level)
            # for every key in a set of possible keys, check for words and add
            # them to the solution set
            for key in keys:
                if testKey != key:
                    testKey = key
                    print("else: {} {}".format(testKey, key))
                    levelObject = self._levelDict.get(level, None)
                    if levelObject is not None:
                        solutionSet = solutionSet.union(
                            levelObject.Contains("".join(key))
                        )
                else:
                    print("if: {} {}".format(testKey, key))
                    break
        # Create instance of Board and return it to the main
        return Board(randKey, list(solutionSet))

    # string for testing
    def __str__(self):
        output = ""
        for key in self._levelDict:
            output += str(self._levelDict[key]) + "\n"
        return output


# This is a level class that stores all words in a level (by alphabetized key)
class Level:
    def __init__(self):
        self._nodeDict = {}

    # adds a word to the correct node or makes a new node if it doesn't
    # already exist
    def AddWord(self, myString):
        key = "".join(sorted(myString))
        self._nodeDict.setdefault(key, set()).add(myString)

    # returns a random key
    def GetRandomKey(self):
        return choice(list(self._nodeDict.keys()))

    # if key not there, return empty set.
    # if key found, return set associated with key
    def Contains(self, keyString):
        return self._nodeDict.get(keyString, set())

    # string for testing
    def __str__(self):
        return str(self._nodeDict)
