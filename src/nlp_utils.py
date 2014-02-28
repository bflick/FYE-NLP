from __future__ import print_function
from nltk.corpus import stopwords  #from nltk import tokenize
#from nltk.corpus.reader.plaintext import PlaintextCorpusReader
import logging
#import os
#import sys
import string
#import re
from word import word

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
