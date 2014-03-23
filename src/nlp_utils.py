from __future__ import print_function
from nltk.corpus import stopwords  #from nltk import tokenize
#from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.probability import FreqDist
import logging
#import os
#import sys
import string
#import re

itrchgbl = [['i','you','he','she','we'],['is','are','was'],['i\'ve','he\'s','you\'re','she\'s','we\'ve'],['am','is']]

stopList = stopwords.words( "english" ) + list(string.punctuation) + [e for ls in itrchgbl for e in ls]

clicheBlacklist = ['a','an','am','he','his','her','our','i','my','the','they','she','you','your']

def getNGrams(tokens, n):
    thengrams = []
    i = 0
    while i < len(tokens):
        if i+n < len(tokens):
            ngram = tokens[i:i+n]
            thengrams.append(ngram)
        i = i + 1
    return thengrams

def interchangable( word1, word2 ):
    for ls in itrchgbl:
        if word1 in ls and word2 in ls:
            return True
    return False

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
    intLen1 = len(wL1)
    intLen2 = len(wL2)
    if intLen1 < intLen2:
        return iDist( wL2, wL1 )
    if intLen2 == 0 or intLen1 == 0:
        print('error')
        return 0
    else:
        d = intLen1 / intLen2

    freqCount1 = {}
    freqCount2 = {}
    for w in wL1:
        try:
            freqCount1[w.lower()] += 1
        except:
            freqCount1[w.lower()] = 1

    for w in wL2:
        try:
            freqCount2[w.lower()] += 1
        except:
            freqCount2[w.lower()] = 1

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

