#! /usr/bin/python

from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk import tokenize
from assignment import assignment
import os
import sys
import timeit
import nlp_utils
import string

"""
    First Year English - Natural Language Processing
"""

def main():
    assignments = {} # to contain 101 and 102 files

    filePath = '../FYE-TEXT/Test'
    assignments = parseFolder( filePath )

    for pid in assignments.iterkeys():
        size = 0
        para1 = ''
        para1tags = ''
        lasttkn = ''
        lastpos = ''
        for sent in assignments[pid].final.paras[0].sentences:
            print sent.rawText
            tags = ''
            for tkn, pos in sent.taggedWords:
                tags += pos + '  '
            print tags
            print sent.complexity, '\n'

        print pid
        print assignments[pid].final.getAvgComplexity()
        print assignments[pid].draft.getAvgComplexity()
        print '\n'

    #dCliches, fCliches = getCliches( assignments )
    #printCliches( assignments, dCliches, fCliches )

    #draftNominals, finalNominals = getNominals( assignments )
    #for pid in assignments.keys():
    #    print draftNominals[pid]
    #    print finalNominals[pid]

def printCliches( assignmentDict, dClicheDict, fClicheDict ):
    maxlen = 80
    lines = []
    b = list(string.punctuation) + ['t','s','ll']
    for pid, a in assignmentDict.items():
        fCliches = fClicheDict[pid]
        lines += [('Final ' + pid, '')]
        for loc in fCliches:
            sent = a.final.paras[loc[0]].sentences[loc[1]].words
            foundAt = loc[2]
            width = 0
            oddline = ''
            evenline = ''
            for i, word in enumerate(sent):

                if width > maxlen:
                    oddline += '\n'
                    evenline += '\n'
                    width = 0

                oddline += word
                width += len(word)
                if i < len(sent) - 1 and not sent[i+1] in b:
                    width += 1
                    evenline += ' '
                    oddline += ' '

                if word in b:
                    foundAt += 1

                evenline += ' '*len(word)

                if i == foundAt:
                    if len(loc[3]) + width > maxlen:
                        cwid = width
                        cList = loc[3]
                        cList = cList.split()
                        for tkn in cList:
                            if len(tkn) + cwid > maxlen:
                                evenline += '\n' + tkn + ' '
                                cwid = 0
                            else:
                                evenline += tkn + ' '
                    else:
                        evenline += loc[3]

            lines.append(( oddline, evenline ))

    for l in lines:
        stutext = l[0].split('\n')
        cliche = l[1].split('\n')
        for i, t in enumerate(stutext):
            print t
            if i < len(cliche):
                print cliche[i]


def getNominals( assignmentDict ):
    draftNoms = {}
    finalNoms = {}
    nominal = nlp_utils.openFileReturnTokens( '../assets/nominalizations.txt' )
    nomBlacklist = nlp_utils.openFileReturnTokens( '../assets/nominalBlacklist.txt' )
    for pid, a in assignmentDict.items():
        draftNoms[pid] = []
        finalNoms[pid] = []
        for loc in a.draft.findNominalizations( nominal, nomBlacklist ):
            draftNoms[pid].append(( loc[0], loc[1], loc[2], loc[3] ))

        for loc in a.final.findNominalizations( nominal, nomBlacklist ):
            finalNoms[pid].append(( loc[0], loc[1], loc[2], loc[3] ))

    nlp_utils.printDict('label', draftNoms)
    return draftNoms, finalNoms

"""
    getCliches - finds the locations in each paper for passive voiced sentences
    @param assignment list
    @return a tuple of dictionaries containing lists of sentences locations containg a cliche
"""
def getCliches( assignmentDict ):
    draftCliches = {}
    finalCliches = {}
    for pid, a in assignmentDict.items():
        draftCliches[pid] = []
        finalCliches[pid] = []
        # loc[0]=paragraph, loc[1]=sentence, loc[2]=ngram, loc[3]=cliche
        for loc in a.draft.findCliches():
            draftCliches[pid].append(( loc[0], loc[1], loc[2], loc[3] ))

        for loc in a.final.findCliches():
            finalCliches[pid].append(( loc[0], loc[1], loc[2], loc[3] ))

    return draftCliches, finalCliches

"""
    getPassives - finds the locations in each paper for passive voiced sentences
    @param assignment list
    @return a tuple of dictionaries containing lists of passive sentences
"""
def getPassives( assignmentDict ):
    draftPassives = {}
    finalPassives = {}
    for pid, a in assignmentDict.items():
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
    assignments = {}
    draftReader = PlaintextCorpusReader(dirPath, '\d+draft\d*.*')
    finalReader = PlaintextCorpusReader(dirPath, '\d+final\d*.*')

    numFiles = len( os.listdir( dirPath ))
    assert numFiles % 2 == 0

    finalIdsSortedList = finalReader.fileids()
    draftIdsSortedList = draftReader.fileids()

    for pid in finalReader.fileids():
#        pid = 'Paper ' + str(i)
        final = finalReader.paras( pid ) #finalIdsSortedList[i] )
        draft = draftReader.paras( pid ) #draftIdsSortedList[i] )
        assn = assignment( draft, final )
        assignments[pid] = assn

    return assignments


if __name__ == '__main__' :
    main()