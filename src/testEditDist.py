from nltk.corpus.reader.plaintext import PlaintextCorpusReader
#from nltk import tokenize
from assignment import assignment
import os
import sys
from sentence import sentence
import utilspackage as util

"""
    First Year English - Natural Language Processing
"""

def main() :

    assignmentList = [] # to contain 101 and 102 files

    filePath = '../FYE-TEXT/Test/'

    assignmentList += parseFolder( filePath )

    for i, a in enumerate( assignmentList ):
        print '\n assignment ' + str(i) + ' contains ' + str(a.customEditDist()) + ' edits.'
        print '\n'

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
