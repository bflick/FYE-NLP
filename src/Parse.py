#! /usr/bin/python

from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk import tokenize
from assignment import assignment
import os
import sys
import nlp_utils

"""
    First Year English - Natural Language Processing
"""

def main() :
    assignmentList = [] # to contain 101 and 102 files

    filePath = '../FYE-TEXT/Test/'
    assignmentList += parseFolder( filePath )

    loc = assignmentList[0].draft.findCliches()
    print loc

    #rawTx = assignmentList[0].final.rawText
    #paraL = [t.words for gg in assignmentList[0].final.paras for t in gg.sentences ]
    #print paraL, '\n'

    #bm = nlp_utils.removeStopList(rawTx)
    #ftw = nlp_utils.removeStopList(paraL)
    #print bm, '\n'
    #print ftw, '\n'

    #print assignmentList[0].draft.rawText
    #print '\n'
    #print assignmentList[0].final.rawText

    #print assignmentList[0].numEdits
    #print assignmentList[0].final.findNewSents(assignmentList[0].draft)

"""
    parseFolder
    @param dirPath - a string value of the folder in which corpus source files
                     are contained
    @return a list of assignment objects containing rough and final drafts
    @error if the number of final and rough drafts in the folder do not match
"""
def parseFolder( dirPath ):
    assignments = []
    draftReader = PlaintextCorpusReader(dirPath, '\d+draft\d*.*')
    finalReader = PlaintextCorpusReader(dirPath, '\d+final\d*.*')

    numFiles = len( os.listdir( dirPath ))
    assert numFiles % 2 == 0

    finalIdsSortedList = finalReader.fileids()
    draftIdsSortedList = draftReader.fileids()

    for i in range(len(finalReader.fileids())):
        final = finalReader.paras( finalIdsSortedList[i] )
        draft = draftReader.paras( draftIdsSortedList[i] )
        assn = assignment( draft, final )
        assignments.append( assn )

    return assignments

if __name__ == '__main__' :
    main()
