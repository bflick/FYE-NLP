#! /usr/bin/python2

from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk import tokenize
from assignment import assignment
import os
import sys
import timeit
import nlp_utils

"""
    First Year English - Natural Language Processing
"""

def main():
    assignments = [] # to contain 101 and 102 files

    filePath = '../FYE-TEXT/102'
    assignments += parseFolder( filePath )

    dPassives, fPassives = getPassives( assignments )

    for key, entry in fPassives.items():
        print "final", key
        print key, entry
        print "draft", key
        print key, dPassives[key]


#    dCliches, fCliches = getCliches( assignments )
#
#    for key, entry in fCliches:
#        print key, entry
#        print key, dCliches[key]

    #nlp_utils.printDict( 'draft cliches\n', dCliches )
    #nlp_utils.printDict( 'final cliches\n', fCliches )

    #rawTx = assignments[0].final.rawText
    #paraL = [t.words for gg in assignments[0].final.paras for t in gg.sentences ]
    #print paraL, '\n'

    #bm = nlp_utils.removeStopList(rawTx)
    #ftw = nlp_utils.removeStopList(paraL)
    #print bm, '\n'
    #print ftw, '\n'

    #print assignments[0].draft.rawText
    #print '\n'
    #print assignments[0].final.rawText

    #print assignments[0].numEdits
    #print assignments[0].final.findNewSents(assignmentList[0].draft)

def getCliches( assignmentList ):
    draftCliches = {}
    finalCliches = {}
    for i, a in enumerate( assignmentList ):
        pid = 'Paper ' + str(i)
        draftCliches[pid] = []
        finalCliches[pid] = []
        for loc in a.draft.findCliches():
            draftCliches[pid] += [loc[0],loc[1], a.draft.paras[loc[0]].sentences[loc[1]].rawText]
        for loc in a.final.findCliches():
            finalCliches[pid] += [loc[0],loc[1], a.final.paras[loc[0]].sentences[loc[1]].rawText]
    return draftCliches, finalCliches

def getPassives( assignmentList ):
    draftPassives = {}
    finalPassives = {}
    for i, a in enumerate( assignmentList ):
        pid = 'Paper ' + str(i)
        draftPassives[pid] = []
        finalPassives[pid] = []
        for loc in a.draft.findPassives():
            draftPassives[pid].append(( loc[0], loc[1], a.draft.paras[loc[0]].sentences[loc[1]].rawText ))
        for loc in a.final.findPassives():
            finalPassives[pid].append(( loc[0], loc[1], a.final.paras[loc[0]].sentences[loc[1]].rawText ))

    return draftPassives, finalPassives

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
