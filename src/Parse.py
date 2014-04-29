#! /usr/bin/python

from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk import tokenize
from assignment import assignment
import itertools
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
        
    writeComplexity(assignments, '../complexityInfo.txt')
    writeFile(assignments, '../parsedInfo.txt')

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

def needSpace(tkn):
    if any((c in tkn) for c in string.punctuation):
        return False
    return True

def getHighlightPairs(paper, pid, locationDict):
    highlightPairs = []
    testStr = ''
    for para, sent, word,  feature in locationDict[pid]:
        featureList = feature.split()
        words = paper.paras[para].sentences[sent].words
        highlightStart = 0
        highlightEnd = 0
        if para > 0:
            highlightStart = sum([len(paper.paras[i].rawText) for i in xrange(0, para)])
        if sent > 0:
            highlightStart += sum([len(paper.paras[para].sentences[i].rawText) for i in xrange(0, sent)])

        if word > 0:
            for i in xrange(word):
                highlightStart += len(words[i])
                if needSpace(words[i]):
                    highlightStart += 1

        highlightEnd = highlightStart
        for i in xrange(word, word + len(featureList)):
            highlightEnd += len(words[i])
            if needSpace(words[i]):
                highlightEnd += 1

        print pid, feature, para, sent, word
        print paper.rawText[highlightStart:highlightEnd+1], '\n'

        highlightPairs.append((highlightStart, highlightEnd))

    return highlightPairs

def writeComplexity(assignmentDict, pathName):
    keys = ['interDistance',
            'draft|complexityPairs',
            'final|complexityPairs',
            'draft|avgComplexity',
            'final|avgComplexity']

    paperComplexity = dict()
    for pid, a in assignmentDict.items():
        paperComplexity[pid] = { keys[0] : a.draftFinalDist(),
                                 keys[1] : list(),
                                 keys[2] : list(),
                                 keys[3] : a.draft.getAvgComplexity(),
                                 keys[4] : a.final.getAvgComplexity() }
        for p in a.draft.paras:
            for i, s in enumerate(p.sentences):
                paperComplexity[pid][keys[1]].append((i, s.complexity))
        for p in a.final.paras:
            for i, s in enumerate(p.sentences):
                paperComplexity[pid][keys[2]].append((i, s.complexity))

    ffile = open(pathName, 'w')
    for pid in paperComplexity.iterkeys():
        ffile.write(pid + '\n')
        ffile.write(keys[0] + ': ' + str(paperComplexity[pid][keys[0]]) + '\n')
        ffile.write(keys[1] + ': ' )
        for pair in paperComplexity[pid][keys[1]]:
            ffile.write(str(pair) + ' ')
        ffile.write('\n' + keys[2] + ' ')
        for pair in paperComplexity[pid][keys[2]]:
            ffile.write(str(pair) + ' ')
        ffile.write('\n')
        ffile.write(keys[3] + ': ' + str(paperComplexity[pid][keys[3]]) + '\n')
        ffile.write(keys[4] + ': ' + str(paperComplexity[pid][keys[4]]) + '\n')

    ffile.close()

def writeFile(assignmentDict, pathName):
    (draftNominals, finalNominals) = getNominals(assignmentDict)
    (draftCliches, finalCliches) = getCliches(assignmentDict)
    (draftPassives, finalPassives) = getPassives(assignmentDict)
#    nlp_utils.printDict('draftNominals', draftNominals)
#    nlp_utils.printDict('draftCliches', draftCliches)
#    nlp_utils.printDict('draftPassives', draftPassives)
    highlightPairs = dict()
    for pid in assignmentDict.iterkeys():
        highlightPairs[pid + '(draft nominals)'] = getHighlightPairs(assignmentDict[pid].draft, pid, draftNominals)
        highlightPairs[pid + '(draft cliches)'] = getHighlightPairs(assignmentDict[pid].draft, pid, draftCliches)
        highlightPairs[pid + '(draft passives)'] = getHighlightPairs(assignmentDict[pid].draft, pid, draftPassives)
        highlightPairs[pid + '(final nominals)'] =  getHighlightPairs(assignmentDict[pid].final, pid, finalNominals)
        highlightPairs[pid + '(final cliches)'] =  getHighlightPairs(assignmentDict[pid].final, pid, finalCliches)
        highlightPairs[pid + '(final passives)'] = getHighlightPairs(assignmentDict[pid].final, pid, finalPassives)

#    nlp_utils.printDict('highlights', highlightPairs) #<<<<<<<<<<<

    ffile = open(pathName, 'w')
    for pid in assignmentDict.iterkeys():
        ffile.write(pid + 'draft\n')
        ffile.write('\ncliches ')
        for i, pair in enumerate(highlightPairs[pid + '(draft cliches)']):
#            print pid, draftCliches[pid][i][3]
#            print assignmentDict[pid].draft.rawText[pair[0]:pair[1]]
            ffile.write(str(pair) + ' ')
        ffile.write('\nnominals ')
        for pair in highlightPairs[pid + '(draft nominals)']:
            ffile.write(str(pair) + ' ')
        ffile.write('\npassives ')
        for i, pair in enumerate(highlightPairs[pid + '(draft passives)']):
#            print pid, draftPassives[pid][i][3]
#            print assignmentDict[pid].draft.rawText[pair[0]:pair[1]], '\n'
            ffile.write(str(pair) + ' ')
        ffile.write('\n' + assignmentDict[pid].draft.rawText + '\n\n')
        
        ffile.write(pid + 'final\n')
        ffile.write('\ncliches ')
        for pair in highlightPairs[pid + '(final cliches)']:
            ffile.write(str(pair) + ' ')
        ffile.write('\nnominals ')
        for pair in highlightPairs[pid + '(final nominals)']:
            ffile.write(str(pair) + ' ')
        ffile.write('\npassives ')
        for pair in highlightPairs[pid + '(final passives)']:
            ffile.write(str(pair) + ' ')
        ffile.write('\n' + assignmentDict[pid].final.rawText + '\n\n')
    ffile.close()

def getNominals( assignmentDict ):
    draftNoms = {}
    finalNoms = {}
    nominal = nlp_utils.openFileReturnTokens( '../assets/nominalizations.txt' )
    nomBlacklist = nlp_utils.openFileReturnTokens( '../assets/nominalBlacklist.txt' )
    for pid, a in assignmentDict.items():
        draftNoms[pid] = []
        finalNoms[pid] = []
        for para, sent, word, nominal in a.draft.findNominalizations( nominal, nomBlacklist ):
            draftNoms[pid].append(( para, sent, word, nominal ))

        for para, sent, word, nominal in a.final.findNominalizations( nominal, nomBlacklist ):
            finalNoms[pid].append(( para, sent, word, nominal ))

#    nlp_utils.printDict('label', draftNoms)
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
            draftPassives[pid].append(( loc[0], loc[1], 0, a.draft.paras[loc[0]].sentences[loc[1]].rawText ))

        for loc in a.final.findPassives():
            finalPassives[pid].append(( loc[0], loc[1], 0, a.final.paras[loc[0]].sentences[loc[1]].rawText ))

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
        final = finalReader.paras( pid ) #finalIdsSortedList[i] )
        draft = draftReader.paras( pid ) #draftIdsSortedList[i] )
        assn = assignment( draft, final )
        assignments[pid] = assn

    return assignments


if __name__ == '__main__' :
    main()
