#! /usr/bin/python
from matplotlib.lines import Line2D
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
PARSED_FP = '..'+ os.sep + 'parsedInfo.txt'
COMPLEX_FP = '..'+ os.sep + 'complexityInfo.txt'
CLICHE_FP = '..'+ os.sep + 'clicheInfo.txt'


def main():

    if len(sys.argv) == 2:
        filePath = sys.argv[1]
    else:
        filePath = '..'+os.sep+ 'FYE-TEXT' +os.sep+ '102'

    assignments = {} # to contain 101 and 102 files
    assignments = parseFolder( filePath )

    writeComplexity(assignments, COMPLEX_FP)
    writeFile(assignments, PARSED_FP)

    # The runtime for this part is pretty rediculous,
    # I think finding new sentences is less important
    # especially when the word diff is already used
#    for pid in assignments.iterkeys():
#        print pid
#        newSents = assignments[pid].getNewSents()
#        for para, sent in newSents:
#            print assignments[pid].final.paras[para].sentences[sent].rawText, '\n'

#        print '\n\n'


def plotPairs(): #(x, y):
    keys = ['interDistance',
            'draft|complexityPairs',
            'final|complexityPairs',
            'draft|avgComplexity',
            'final|avgComplexity',
            'wordDifference']

    f = open(COMPLEX_FP, 'r')
    complexity = pickle.load(f)
    f.close()
    print type(complexity) is dict
    for p_key in complexity.iterkeys():
        paper = complexity[p_key]
        print paper[keys[1]]
        xs = []
        ys = []
        for x, y in paper[keys[1]]:
            xs.append(x)
            ys.append(y)
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.set_title(keys[1])
        ax1.set_xlabel('sentence position')
        ax1.set_ylabel('sentence complexity')
        ax1.plot(xs, ys, c='r', label='sentence complexity')
        leg = ax1.legend()
        fig.savefig('..' + os.sep + p_key + '_' + keys[1] + '.png')

        final_pairs = paper[keys[2]]
        xs = []
        ys = []
        for x, y in final_pairs:
            xs.append(x)
            ys.append(y)
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.set_title(keys[1])
        ax1.set_xlabel('sentence position')
        ax1.set_ylabel('sentence complexity')
        ax1.plot(xs, ys, c='r', label='sentence complexity')
        leg = ax1.legend()
        fig.savefig('..' + os.sep + p_key + '_' + keys[2] + '.png')


def stringifyCliches(assignmentDict, ClicheDict, draftOrFinal):
    ret = ''
    maxlen = 80
    lines = []
    b = list(string.punctuation) + ['t','s','ll']
    for pid, a in assignmentDict.items():
        Cliches = ClicheDict[pid]
        lines += [('>>>>>' + pid.replace('final', draftOrFinal), '')]
        for loc in Cliches:
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
x                                evenline += '\n' + tkn + ' '
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
            ret += t + '\n'
            if i < len(cliche):
                ret +=  cliche[i] + '\n'
    return ret


def writeCliches(assignmentDict, fClicheDict, dClicheDict, filePath):
    draftClicheString = stringifyCliches(assignmentDict, dClicheDict, 'draft')
    finalClicheString = stringifyCliches(assignmentDict, fClicheDict, 'final')
    ffile =  open(CLICHE_FP, 'w')
    ffile.write(draftClicheString + '\n\n')
    ffile.write(finalClicheString)
    ffile.close()


def getHighlightPairs(paper, pid, locationDict):
    specialPunct = ['``','(']
    highlightPairs = []
    testStr = ''
    for para, sent, word,  feature in locationDict[pid]:
        featureList = feature.split()
        words = paper.paras[para].sentences[sent].words
        taggedWords = paper.paras[para].sentences[sent].taggedWords

        highlightStart = 0
        highlightEnd = 0
        if para > 0:
            highlightStart = sum([len(paper.paras[i].rawText) for i in xrange(0, para)])
        if sent > 0:
            highlightStart += sum([len(paper.paras[para].sentences[i].rawText) for i in xrange(0, sent)])

        if word > 0:
            #The sentence.rawText function isn't perfect, but this
            #algorithm parallels it
            lastTkn = ' '
            for i in xrange(0, word):
                if taggedWords[i][1] in specialPunct:
                    highlightStart += 1 + len(words[i])
                else:
                    if lastTkn[-1] in ["'", '-'] and len(words[i]) <= 2:
                        highlightStart -= 1
                    highlightStart += len(words[i])
                    if i + 1 < len(words) and not nlp_utils.isPunct(words[i + 1]):
                        if taggedWords[i] not in specialPunct:
                            highlightStart += 1

                lastTkn = words[i].strip()
        if word > 0:
            highlightEnd = highlightStart
            lastTkn = ' '
            for i in xrange(word, word + len(featureList)):
                if taggedWords[i][1] in specialPunct:
                    highlightEnd += 1 + len(words[i])
                else:
                    if lastTkn[-1] in ["'", '-'] and len(words[i]) <= 2:
                        highlightEnd -= 1
                    highlightEnd += len(words[i])
                    if i + 1 < len(words) and not nlp_utils.isPunct(words[i + 1]):
                        if taggedWords[i] not in specialPunct:
                            highlightEnd += 1

                lastTkn = words[i].strip()
        else:
            highlightEnd = highlightStart + len(feature)
        highlightPairs.append((highlightStart, highlightEnd))

    return highlightPairs
    

def writeComplexity(assignmentDict, pathName):
    keys = ['interDistance',
            'draft|complexityPairs',
            'final|complexityPairs',
            'draft|avgComplexity',
            'final|avgComplexity',
             'wordDifference']

    paperComplexity = dict()
    for pid, a in assignmentDict.items():
        paperComplexity[pid] = { keys[0] : a.draftFinalDist(),
                                 keys[1] : list(),
                                 keys[2] : list(),
                                 keys[3] : a.draft.getAvgComplexity(),
                                 keys[4] : a.final.getAvgComplexity(),
                                 keys[5] : a.numEdits }
        sentNum = 0
        for p in a.draft.paras:
            for s in p.sentences:
                paperComplexity[pid][keys[1]].append((sentNum, s.complexity))
                sentNum += 1
        sentNum = 0
        for p in a.final.paras:
            for s in p.sentences:
                paperComplexity[pid][keys[2]].append((sentNum, s.complexity))
                sentNum += 1

    ffile = open(pathName, 'wb')
    pickle.dump(complexity, pathName)
    ffile.close()


def writeFile(assignmentDict, pathName):
    (draftNominals, finalNominals) = getNominals(assignmentDict)
    (draftCliches, finalCliches) = getCliches(assignmentDict)
    (draftPassives, finalPassives) = getPassives(assignmentDict)

    writeCliches(assignmentDict, draftCliches, finalCliches, CLICHE_FP)

    highlightPairs = dict()
    for pid in assignmentDict.iterkeys():
        highlightPairs[pid + '(draft nominals)'] = getHighlightPairs(assignmentDict[pid].draft, pid, draftNominals)
        highlightPairs[pid + '(draft cliches)'] = getHighlightPairs(assignmentDict[pid].draft, pid, draftCliches)
        highlightPairs[pid + '(draft passives)'] = getHighlightPairs(assignmentDict[pid].draft, pid, draftPassives)
        highlightPairs[pid + '(final nominals)'] =  getHighlightPairs(assignmentDict[pid].final, pid, finalNominals)
        highlightPairs[pid + '(final cliches)'] =  getHighlightPairs(assignmentDict[pid].final, pid, finalCliches)
        highlightPairs[pid + '(final passives)'] = getHighlightPairs(assignmentDict[pid].final, pid, finalPassives)

    ffile = open(pathName, 'w')
    for pid in assignmentDict.iterkeys():
        draftId = pid.replace('final', 'draft')
        ffile.write('>>>>>' + draftId + '\n')
        ffile.write('\ncliches ')
        for i, pair in enumerate(highlightPairs[pid + '(draft cliches)']):
            ffile.write(str(pair) + ' ')
        ffile.write('\nnominals ')
        for pair in highlightPairs[pid + '(draft nominals)']:
            ffile.write(str(pair) + ' ')
        ffile.write('\npassives ')
        for i, pair in enumerate(highlightPairs[pid + '(draft passives)']):
            ffile.write(str(pair) + ' ')
        ffile.write('\n' + assignmentDict[pid].draft.rawText + '\n\n')

        ffile.write('>>>>>' + pid + '\n')
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
    nominal = nlp_utils.openFileReturnTokens('..'+os.sep+'assets'+os.sep+'nominalizations.txt')
    nomBlacklist = nlp_utils.openFileReturnTokens('..'+os.sep+'assets'+os.sep+'nominalBlacklist.txt')
    for pid, a in assignmentDict.items():
        draftNoms[pid] = []
        finalNoms[pid] = []
        for para, sent, word, nominal in a.draft.findNominalizations( nominal, nomBlacklist ):
            draftNoms[pid].append(( para, sent, word, nominal ))

        for para, sent, word, nominal in a.final.findNominalizations( nominal, nomBlacklist ):
            finalNoms[pid].append(( para, sent, word, nominal ))

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
