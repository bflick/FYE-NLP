from __future__ import print_function
from nltk.corpus import stopwords  #from nltk import tokenize
#from nltk.corpus.reader.plaintext import PlaintextCorpusReader
import logging
#import os
#import sys
import string
#import re

def getNGrams(tokens, n):
    thengrams = []
    i = 0
    while i < len(tokens):
        if i+n < len(tokens):
            ngram = tokens[i:i+n]
            thengrams.append(ngram)
        i = i + 1
    return thengrams

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

def removeList( text, blacklist ):
    textMinusStopWords = []
    if isinstance(text, str):
        text = removeRawPunct( text )
        text = text.split()

    for x in text:
        if isinstance(x, list):
            textMinusStopWords.append( removeList( x, blacklist ))
        else:
            textMinusStopWords += [x for x in text if x not in blacklist]

    return textMinusStopWords

def removeListPunct( text ):
    return removeList( text, string.punctuation )

def removeStopList( text ):
    blacklist = stopwords.words( "english" )
    blacklist += string.punctuation
    return removeList( text, blacklist )

def removeRawPunct( rawStr ):
    table = string.maketrans("","")
    rs = rawStr.translate(table, string.punctuation)
    if rs[-1] == ' ':
        del rs[-1]
    return rs

def setIntersection( list1, list2 ):
    s1 = set(list1)
    s2 = set(list2)
    return [e for e in s1 if e in s2]
