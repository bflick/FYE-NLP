#! /usr/bin/python

from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk import tokenize
import os
import sys
import utilspackage as util

"""
    First Year English - Natural Language Processing
"""

def main() :
    assignmentList = [] # to contain 101 and 102 files

    filePath = '../FYE-TEXT/101/'
    draftReader, finalReader = parse_folder( filePath )
    numFiles = len( os.listdir( filePath ))

    assert numFiles % 2 == 0

    finalIdsSortedList = finalReader.fileids().sort()
    draftIdsSortedList = draftReader.fileids().sort()
    for i in range( numFiles / 2 ):
        final = finalReader.paras( finalIdsSortedList[i] )
        draft = draftReader.paras( draftIdsSortedList[i] )
        assn = assignment( draft, final )
        assignmentList.append( assn )

    filePath = '../FYE-TEXT/102/'
    draftReader, finalReader = parse_folder( filePath )
    numFiles = len( os.listdir( filePath ))

    assert numFiles % 2 == 0

    finalIdsSortedList = finalReader.fileids().sort()
    draftIdsSortedList = draftReader.fileids().sort()
    for i in range( numFiles / 2 ):
        final = finalReader.paras( finalIdsSortedList[i] )
        draft = draftReader.paras( draftIdsSortedList[i] )
        assn = assignment( draft, final )
        assignmentList.append( assn )

def parseFolder( dirPath ):
    draftReader = PlaintextCorpusReader(dirPath, '[0-9]draft[0-9].txt')
    finalReader = PlaintextCorpusReader(dirPath, '[0-9]final[0-9].txt')
    return draftReader, finalReader

if __name__ == '__main__' :
    main()
