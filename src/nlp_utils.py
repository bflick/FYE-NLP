from __future__ import print_function
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import logging
import string
import re
import word

clicheBlacklist = ['a','an','am','he','his','her','our','i','my','the','they','she','you','your']

stopList = stopwords.words( "english" ) + list(string.punctuation)

rePosList = [r'NN.*', r'VB.*', r'PR.*', r'JJ.*', r'RB.*', r'WP.*']

weights = {}
with open('../assets/weights.txt') as file:
    for line in file:
        (pos, w) = line.split(':')
        weights[pos.strip()] = float(w)*5.0

similarityTolerance = 0.7

def getNGrams(tokens, n):
    thengrams = []
    i = 0
    while i < len(tokens):
        if i+n < len(tokens):
            ngram = tokens[i:i+n]
            thengrams.append(ngram)
        i = i + 1
    return thengrams

def normPos(pos):
    for exp in rePosList:
        if re.match(exp, pos):
            return pos[:2]
    return pos

def openFileReturnString( fileName ):
    filePtr = open( fileName )
    text = filePtr.read()
    filePtr.close()
    return text

def openFileReturnTokens( fileName, delim=None ):
    filePtr = open( fileName )
    text = filePtr.read()
    filePtr.close()
    return text.split( delim )

def printDict( label, theDict ):
    print( str(label) )
    for first, second in theDict.items():
        print( '%s : %s' % ( str(first), str(second) ))
    return

def printList( theList ):
    for item in theList:
        print( str(item) )
    return

def removeList( text, blacklist ):
    textMinusBL = []
    for x in text:
        if isinstance(x, str):
            if not x in blacklist:
                textMinusBL += [x]
        elif isinstance(x, list):
            textMinusBL.append( removeList( x, blacklist ))
    return textMinusBL

def removeListPunct( text ):
    return removeList( text, string.punctuation )

def removeStopList( text ):
    return removeList( text, stopList )

def removeRawPunct( rawStr ):
    table = string.maketrans("","")
    rs = rawStr.translate(table, string.punctuation)
    return rs.strip()

def binarySearch(needle, haystack):
    end = len(haystack) - 1
    mid = end / 2
    begin = 0
    while begin <= end:
        mid = (end + begin) / 2
        if needle == haystack[mid]:
            return mid
        else:
            if needle < haystack[mid]:
                end = mid - 1
            else:
                begin = mid + 1
    return None

def clicheIntersection( ngram, cliche ):
    ret = []

    for e in ngram:
        if e in cliche and ret.count(e) < cliche.count(e):
            ret.append(e)

    return ret

def setIntersection( list1, list2 ):
    s1 = set(list1)
    s2 = set(list2)
    return [e for e in s1 if e in s2]


def iDist( wL1, wL2 ):
    intLen1 = float(len(wL1))
    intLen2 = float(len(wL2))
    d = 0.0
    if intLen1 < intLen2:
        return iDist( wL2, wL1 )
    if intLen2 == 0 or intLen1 == 0:
        print('nlp_utils.iDist: error')
        return 0
    else:
        d = float(intLen1 / intLen2)

    freqCount1 = {}
    freqCount2 = {}
    for w in wL1:
        try:
            freqCount1[w.lower()] += 1.0
        except:
            freqCount1[w.lower()] = 1.0

    for w in wL2:
        try:
            freqCount2[w.lower()] += 1.0
        except:
            freqCount2[w.lower()] = 1.0

    rDist = 0.0
    nSet = setIntersection( wL1, wL2 )
    for w in nSet:
        rDist += abs(freqCount1[w.lower()] - (freqCount2[w.lower()]*d))
    wL1 = set(wL1)
    wL2 = set(wL2)
    for w in wL1:
        if w not in nSet:
            rDist += freqCount1[w.lower()]
    for w in wL2:
        if w not in nSet:
            rDist += freqCount2[w.lower()] * d

    return rDist / (intLen1 + (intLen2 * d))

def isPunct( tkn ):
    punct = list(string.punctuation)
    punct.append('`')
    tkn = tkn.strip()
    if len(tkn) <= 2:
        if any((c in tkn) for c in punct):
            if not re.match(r'\w', tkn):
                return True
    return False

def wordDiff(wl1, wl2):
    wl1 = removeListPunct(wl1)
    wl2 = removeListPunct(wl2)
    cols = len(wl1) + 1
    rows = len(wl2) + 1
    matrix = [[0 for j in range(cols)] for i in range(rows)]
    for i in range(rows):
        matrix[i][0] = i
    for j in range(cols):
        matrix[0][j] = j
    for i in range(1, rows):
        for j in range(1, cols):
            if word.word.getStem(wl1[j - 1]) == word.word.getStem(wl2[i - 1]):
                matrix[i][j] = matrix[i-1][j-1]
            else:
                deletion = matrix[i-1][j] + 1
                insertion = matrix[i][j-1] + 1
                substitution = matrix[i-1][j-1] + 2
                matrix[i][j] = min(insertion, deletion, substitution)

    return matrix[-1][-1]

