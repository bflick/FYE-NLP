# -*- coding: utf-8 -*-
"""
Created on Thu Nov 07 19:46:45 2013

@author: Chris Holcomb
"""
################################################################

import sys
import nltk
from glob import glob
from collections import defaultdict
from nltk.text import Text
################################################################
##
## Functions
##
################################################################
##
## get the stop list and augment it with punctuation
def getStopList():
    stopList = open('stoplistNLTK.txt').read().split()
    stopList.append('"')
    stopList.append("'")
    stopList.append('.')
    stopList.append(',')
    stopList.append('!')
    stopList.append('?')
    stopList.append('-')
    stopList.append('--')
    stopList.append('(')
    stopList.append(')')

    return stopList
    
#################################################################
##
def cleanSmartQuotes(text):
    text = text.lower()
    text = text.replace("\x91", ' ')
    text = text.replace("\x92", "'")
    text = text.replace('\x94', '"')
    text = text.replace('\x93', '"')
    text = text.replace('\x85', ' ')
    
    return text
    
##################################################################
##
## Function: splits a text into its constituent sentences
## Input: a text as a single string
## Returns: a nested list with each sublist a tokenized sentence
##
def createSentences(text):
    currentSent = []
    sentenceList = []
    punctuation = ".", "?", "!" #endswith() will accept a tuple as argument
    
    wordList = text.split()

    for word in wordList:
        currentSent.append(word)
        if word.endswith(punctuation):
            sentenceList.append(currentSent)
            currentSent = []
    
    return sentenceList
    
#####################################################################
##
def cleanPunct(text):
    text = text.lower()
    text = text.replace('.', ' ')
    text = text.replace(',', ' ')
    text = text.replace('!', ' ')
    text = text.replace(';', ' ')
    text = text.replace(':', ' ')
    text = text.replace('-', ' ')
    text = text.replace('?', ' ')
    text = text.replace("'", ' ')
    text = text.replace('"', ' ')
    
    return text

######################################################################
## Function: removes citation fragments from tokenized list
## Input: tokenized list
## Return: tokenized list
def removeCitations(tokens):
    newList = []
    end = ')', '),', ').', ')"'
    i = 0
    while i < len(tokens):
        if tokens[i].startswith('(') and tokens[i+1].endswith(end):
            i = i + 2
        elif tokens[i].startswith('(') and tokens[i].endswith(end):
            i += 1
        else:
            newList.append(tokens[i])
            i += 1
        
    return newList

######################################################################
## Function: reads in all the files and turns them into a tokenized list
## Input: file names
## Return: all files combined into a single list of tokens
def megaTokens(dataFiles):
    megaTokens = []
    for file in dataFiles:
        text1 = open(file).read()
        text1 = cleanSmartQuotes(text1)
        text1 = cleanPunct(text1)
        text1 = text1.lower()
        tokens1 = text1.split()
        for word in tokens1:
            megaTokens.append(word)
            
    return megaTokens

###################################################################
##
def tokenize(text):
    text = cleanSmartQuotes(text)
    text = cleanPunct(text)
    tokens = text.split()
    tokens = removeCitations(tokens)
    
    return tokens
                
##################################################################
##
## Function: counts the number of times a word appears in a document
## Input: list of tokens
## Returns: a sorted list of tuples (words, count)
def wordFrequency(tokens):
    #freq = defaultdict(int)
    stopList = getStopList()
    newWords = []
    
    for word in tokens:
        if word in stopList: continue
        #freq[word] = freq[word] + 1
        newWords.append(word)
    
    #freq = sorted(freq.items())
    freq = nltk.FreqDist(w.lower() for w in newWords)

    return freq

##################################################################
##
## Function: apply part of spech tags to tokenized list
## Input: list of words
## Return: list of tuples (word, tag)
def tagTokens(tokens):
    taggedTokens = nltk.pos_tag(tokens)
    
    return taggedTokens

##################################################################
def lexicalDiversity(tokens):
    stopList = getStopList()
    newWords = []
    
    for word in tokens:
        if word in stopList: continue
        #freq[word] = freq[word] + 1
        newWords.append(word)
    
    lexdiv = float(len(newWords))/float(len(set(newWords)))
    
    return lexdiv
    
###################################################################
##
## Function: profiles each document in dataFiles
## Input: list of files
## Returns: a profile of each file
def documentProfile(dataFiles):
    for file in dataFiles:
        currentFile = open(file)
        text = currentFile.read()
        sentences = createSentences(text)
        tokens = tokenize(text)
        wordFreq = wordFrequency(tokens)
        ari = computeARI(sentences)
        #taggedTokens = tagTokens(tokens)
        print 'File name: ', file[16:]
        print 'Word count: ', len(tokens)
        print 'Sentence count: ', len(sentences)
        print 'Avg. words/sent: ', len(tokens)/len(sentences)
        print 'Lexical diversity: ', lexicalDiversity(tokens)
        print 'Readability Index: ', ari
        print 'Ten most frequent words: ', wordFreq.items()[:9]
        print
        #print 'Tags: ', taggedTokens[:9]
        
    
###################################################################
##
def findCliches(text):
    cliches = open('cliches.txt').read()
    cliches = cliches.replace('\n', ' ')
    cliches = cliches.split('/')
    
    for cliche in cliches:
        if cliche in text:
            print cliche
            

######################################################################
## COMPUTE AUTOMATIC READABILITY INDEX
def computeARI(sentences):
    info = extractcounts(sentences)
    ari = 4.71 * info[0] / info[1] + 0.5 * info[1] / info[2] - 21.43
    return ari

######################################################################                 
######################################################################
## EXTRACT CHARACTER, WORD, AND SENTENCE COUNTS
def extractcounts(sentences):
    charcount = 0
    wordcount = 0
    for sent in sentences:
        for word in sent:
            charcount = charcount + len(word)
            wordcount = wordcount + 1
    return ( charcount, wordcount, len(sentences) )


#################################################################
##
## Main Program Stasts Here
##
#################################################################


dataFiles = glob('justTextENGL101/*.txt')

#megaTokens = megaTokens(dataFiles)
#megaText = Text(megaTokens)

#dataFiles

documentProf = documentProfile(dataFiles)
print documentProf



