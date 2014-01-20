## DEFINED FUNCTIONS
##def checkArgs(number, message):
##def cleanUpCharacters(text):
##def computeFreqs(tokens):
##def getFromRawInput(message):
##def getNGrams(tokens, n):
##def globForFileNames(pathName, fileNameToMatch):
##def lowerCaseTokenList(tokens):
##def openFileReturnString(fileName):
##def openFileReturnTokens(fileName):
##def printDict(label, theDict):
##def printDictFlipped(label, theDict):
##def printDictSorted(label, theDict):
##def printDictSortedFlipped(label, theDict):
##def printList(label, theList):
##def splitStringIntoSentences(text):
##def splitTokenListIntoSentences(tokenList):

######################################################################
##
import sys
from collections import defaultdict
from math import log

######################################################################
## Check Arguments. This checks that the number of command line
## arguments is correct. If not, it prints the 'message' as
## instruction to the user as to how many arguments and what kind of
## arguments there should be. 
##
## Parameters:
##     number : the number of args to expect
##     message : the message to print if the arg count is incorrect
##
def checkArgs(number, message):
    if len(sys.argv) != number:
        print message
        sys.exit(1)

######################################################################
## Clean up the characters, remove punctuation, fix diacriticals, etc.
## This sets up lists of characters.
## The first set is standard punctuation.
## The second set is smart quotes from Microsoft Word.
## The third set is foreign diacriticals.
##
## The first and second kinds of chars are replaced with blanks.
## The third kind are Anglicized.
##
## Parameters:
##     text : the input text to clean, as a single string
##     message : the message to print if the arg count is incorrect
##
## Returns:
##     the cleaned text as a single string
##
def cleanUpCharacters(text):
    charstoclean = list("_-,.;:()[]{}`'?!") + ['"']
    charstoclean2 = list('\xd0\xd1\xd2\xd3\xd4\xd5') # smart quotes, etc.
    newtext = ''
    textsplit = text.split()
    for word in textsplit:
        newword = ''
        for i in range(0, len(word)):
            char = word[i]
            char = char.lower()
            if char in charstoclean:
                char = ' '
            if char in charstoclean2:
                char = ' '
            if char == '\x88': ## foreign diacriticals
                char = 'a'
            if char == '\x8e':
                char = 'e'
            if char == '\x8f':
                char = 'e'
            if char == '\x92':
                char = 'i'
            newword = newword + char
        newtext = newtext + ' ' + newword
    return newtext

######################################################################
## Compute the freqs of tokens in a list of tokens.
## We assume that the tokens can be used as keys in a dict.
## 
## Parameters:
##     tokens : the list of tokens to compute freqs of
##
## Returns:
##     the dict of freqs
##
def computeFreqs(tokens):
    freqs = defaultdict(int)
    for token in tokens:
        freqs[token] = freqs[token] + 1
    return freqs

######################################################################
## Get a string input from raw input.
## 
## Parameters:
##     message : the prompt to print
##
## Returns:
##     the string input from the console
##
def getFromRawInput(message):
    s = raw_input(message + ": ")
    return s

######################################################################
## GET NGRAMS
def getNGrams(tokens, n):
    thengrams = []
    i = 0
    while i < len(tokens):
        if i+n < len(tokens):
            ngram = tokens[i:i+n]
            thengrams.append(ngram)
        i = i + 1
    return thengrams

######################################################################
## Glob a directory for filenames.
## 
## Parameters:
##     directory : the directory to search
##     fileName : the file names to match
##
## Returns:
##     the list of file names
##
def globForFileNames(directory, fileNameToMatch):
    fileNames = glob(directory + '/' + fileNameToMatch)
    return fileNames

######################################################################
## Lowercase all the words in a list of 'string' tokens.
##
## Parameters:
##     tokens : the list of tokens to lowercase
##
## Returns:
##     the dict of freqs
##
def lowerCaseTokenList(tokens):
    ttt = []
    for word in tokens:
        word = word.lower()
        ttt.append(word)
    return ttt

######################################################################
## Open and read a file, returning a 'string' of the file.
##
## Parameters:
##     fileName : the name of the file to open and read
##
## Returns:
##     the file as a 'string'
##
def openFileReturnString(fileName):
    filePtr = open(fileName)
    text = filePtr.read()
    return text

######################################################################
## Open and read a file, returning a 'list' of tokens of the file.
##
## Parameters:
##     fileName : the name of the file to open and read
##
## Returns:
##     the file as a 'list' of tokens
##
def openFileReturnTokens(fileName):
    filePtr = open(fileName)
    text = filePtr.read()
    return text.split()

######################################################################
## Print a dict as key and value.
##
## We print essentially unformatted, but we allow for formatting.
##
## Parameters:
##     label : the label to print at the head of the output
##     theDict : the dictionary to print
##
def printDict(label, theDict):
    print '%s' % (str(label))
    for first, second in theDict.items():
        print '%s : %s' % (str(first), str(second))
    return

######################################################################
## Print a dict, flipped, as value and key.
##
## We print essentially unformatted, but we allow for formatting.
##
## Parameters:
##     label : the label to print at the head of the output
##     theDict : the dictionary to print
##
def printDictFlipped(label, theDict):
    print '%s' % (str(label))
    for first, second in theDict.items():
        print '%s : %s' % (str(second), str(first))
    return

######################################################################
## Print a dict as key and value, sorted by keys.
##
## We print essentially unformatted, but we allow for formatting.
##
## Parameters:
##     label : the label to print at the head of the output
##     theDict : the dictionary to print
##
def printDictSorted(label, theDict):
    print '%s' % (str(label))
    for first, second in sorted(theDict.items()):
        print '%s : %s' % (str(first), str(second))
    return

######################################################################
## Print a dict, flipped as value and key, sorted by value.
##
## We print essentially unformatted, but we allow for formatting.
##
## Parameters:
##     label : the label to print at the head of the output
##     theDict : the dictionary to print
##
def printDictSortedFlipped(label, theDict):
    flippedList = []
    for first, second in theDict.items():
        flippedList.append([second, first])

    flippedList = sorted(flippedList)
    print '%s' % (str(label))
    for item in flippedList:
        print '%s : %s' % (str(item[0]), str(item[1]))

    return

######################################################################
## Print a list.
##
## We print essentially unformatted, but we allow for formatting.
##
## Parameters:
##     label : the label to print at the head of the output
##     theList : the list to print
##
def printList(label, theList):
    print '%s' % (str(label))
    for item in theList:
        print '%s' % (str(item))
    return

######################################################################
## Split a string into sentences.
##
## We split naively based on period, question mark, excl mark.
##
## Parameters:
##     text : the text string
##
## Returns:
##     theList : the list of sentences returned, each sentence
##               a list of tokens
##
def splitStringIntoSentences(text):
    SENTENCEENDINGS = ( '.', '!', '?' )
    tokens = text.split()
    sentenceslist = []
    sent = [] 
    for token in tokens:
        sent = sent + [ token ]
        if token in SENTENCEENDINGS:
            sentenceslist = sentenceslist + [ sent ]
            sent = [] 
    if len(sent) > 0: 
        sentenceslist = sentenceslist + [ sent ]
    return sentenceslist

######################################################################
## Split a token list into sentences.
##
## We split naively based on period, question mark, excl mark.
##
## Parameters:
##     tokenList : the list of tokens
##
## Returns:
##     theList : the list of sentences returned, each sentence
##               a list of tokens
##
def splitTokenListIntoSentences(tokenList):
    SENTENCEENDINGS = ( '.', '!', '?' )
    sentenceslist = []
    sent = [] 
    for token in tokenList:
        if token[-1] in SENTENCEENDINGS:
            sent = sent + [ token[0:-1] ]
            sentenceslist = sentenceslist + [ sent ]
            sent = [] 
        else:
            sent = sent + [ token ]
    if len(sent) > 0: 
        sentenceslist = sentenceslist + [ sent ]
    return sentenceslist

