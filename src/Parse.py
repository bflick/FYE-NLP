#! /usr/bin/python

from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk import tokenize
from assignment import assignment
import os
import sys
import utilspackage as util

"""
    First Year English - Natural Language Processing
"""

def main() :
    assignmentList = [] # to contain 101 and 102 files

    filePath = '../FYE-TEXT/101/'
    draftReader, finalReader = parseFolder( filePath )
    numFiles = len( os.listdir( filePath ))

    assert numFiles % 2 == 0

    finalIdsSortedList = finalReader.fileids()
    draftIdsSortedList = draftReader.fileids()

    for i in range(len(finalReader.fileids())):
        final = finalReader.paras( finalIdsSortedList[i] )
        draft = draftReader.paras( draftIdsSortedList[i] )
        assn = assignment( draft, final )
        assignmentList.append( assn )

    print assignmentList[0].draft.rawText
    print '\n'
    print assignmentList[0].final.rawText

    #print assignmentList[0].numEdits
    print assignmentList[0].final.findNewSents(assignmentList[0].draft)
"""
    filePath = '../FYE-TEXT/102/'
    draftReader, finalReader = parseFolder( filePath )
    numFiles = len( os.listdir( filePath ))

    assert numFiles % 2 == 0

    finalIdsSortedList = finalReader.fileids()
    draftIdsSortedList = draftReader.fileids()

    for i in range(len(finalReader.fileids())):

        final = finalReader.paras( finalIdsSortedList[i] )
        draft = draftReader.paras( draftIdsSortedList[i] )
        assn = assignment( draft, final )
        assignmentList.append( assn )
"""

def parseFolder( dirPath ):
#    draftReader = PlaintextCorpusReader(dirPath, '[0-9][0-9][0-9]draft[0-9].txt')
#   finalReader = PlaintextCorpusReader(dirPath, '[0-9][0-9][0-9]final[0-9].txt')

    draftReader = PlaintextCorpusReader(dirPath, '001draft[0-9].txt')
    finalReader = PlaintextCorpusReader(dirPath, '001final[0-9].txt')
    return draftReader, finalReader

if __name__ == '__main__' :
    main()
