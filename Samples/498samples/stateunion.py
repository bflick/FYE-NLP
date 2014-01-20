######################################################################
##
import sys
import nltk
import random
from os import listdir
from utilspackage import *

######################################################################
## start here for mimicking book

######################################################################
## function from book
def document_features(document):
    doc_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in doc_words)
    return features

######################################################################
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

######################################################################
## my function for trimming stop words, etc., from tokens
## we take in a general list and return a 'list' without stop words,
## without length 1 words, and of words that are entirely alpha
##
## the alpha constraint may be too limiting, but we will use it for now 
## 
## Parameters: 
##     words - a 'list' of word strings
## Returns: 
##     newWords - a 'list' of word strings
def trimTokens(words):
    newWords = []
    stopList = getStopList()

    for word in words:
        word = word.lower()

        if word in stopList: continue
        if 2 >= len(word): continue

        if word.isalpha():
            newWords.append(word)

    return newWords

######################################################################
## start here for mimicking book
categories = ('rep', 'dem')
documents = []
wordsInDocuments = []
for category in categories:
    ##################################################################
    ##
    folderName = 'state_union/' + category
    print "The input folder name is '%s'\n" % (folderName)
  
    ##################################################################
    ##
    filesInFolder = listdir(folderName)
    filesToUse = []
    for fileName in filesInFolder:
        filesToUse.append(fileName)
    print 'Files to be used are: ', filesToUse

    ######################################################################
    ## we read
    for fileName in filesToUse:
#        print "\nFOLDER, NAME ", folderName, fileName
#        thisFileText = open(folderName + '/' + fileName).read()
        thisFile = nltk.corpus.PlaintextCorpusReader(folderName, fileName)
#        print thisFile.words()
        trimmedTokens = trimTokens(thisFile.words())
#        print trimmedTokens
        wordsInDocuments = wordsInDocuments + trimmedTokens
        documents.append((trimmedTokens, category))

#sys.exit(1)

######################################################################
## NOW WE ACTUALLY DO THE WORK

random.shuffle(documents)

#for doc in documents:
#    print 'TEXT ', doc[0]
#    print 'CTGY ', doc[1]
#sys.exit(1)

freqs_all_words = nltk.FreqDist(w.lower() for w in wordsInDocuments)

print 'TOTAL NUMBER OF WORDS:  ', len(wordsInDocuments)
print 'NUMBER OF UNIQUE WORDS: ', len(freqs_all_words)

fraction = 0.20
wordCountToUse = int(fraction*len(freqs_all_words))
print 'USE ', 100*fraction, ' PCT, OR ', wordCountToUse
#sys.exit(1)

word_features = freqs_all_words.keys()[:wordCountToUse]

#for i in range(0,len(word_features)):
#  print '%5d %s' %(i, word_features[i])
#sys.exit(1)

#printDict('FEATURES', document_features(movie_reviews.words('pos/cv957_8737.txt')))

#featuresets = [(document_features(d), c) for (d, c) in documents]

featuresets = []
for doc, category in documents:
    featuresets.append((document_features(doc), category))

print 'NUMBER OF DOCUMENTS ', len(documents)
docCountBy2 = len(documents)/2

training_set = featuresets[docCountBy2:]
test_set = featuresets[:docCountBy2] 

classifier = nltk.NaiveBayesClassifier.train(training_set)

print nltk.classify.accuracy(classifier, test_set)
classifier.show_most_informative_features(20)

sys.exit(1)

######################################################################
## functions

######################################################################
## trim the stopwords from the sentences and return a trimmed list
def trimStopWords(sentences, stopwords):
    newSentences = []
    for sent in sentences:
        newSentence = []
        for word in sent:
            word = word.lower()
            if word not in stopwords:
                newSentence.append(word)
        newSentences.append(newSentence)
#        print 'OLD ', sent
#        print 'NEW ', newSentence
    return newSentences

######################################################################
## compute theoverlaps
def computeOverlaps(fileName, trimmedSentences):
    sims = []
    for sub1 in range(0, len(trimmedSentences)-1):
        for sub2 in range(sub1+1, len(trimmedSentences)):
            sent1 = trimmedSentences[sub1]
            sent2 = trimmedSentences[sub2]
    
            if len(sent1) < 3: continue
            if len(sent2) < 3: continue
    
            setSent1 = set(sent1)
            setSent2 = set(sent2)
            inter = setSent1.intersection(setSent2)
            overlap = len(inter)
            overlap1 = int(100*float(overlap)/float(len(sent1)))
            overlap2 = int(100*float(overlap)/float(len(sent2)))
            s = '%6d %6d %6d %6d %6d' % (sub1, sub2, overlap, overlap1, overlap2)
    #        print '%s' % (s)
            if (overlap1 >= 50) and (overlap2 >= 50):
                if overlap1 >= overlap2:
                    sims.append([overlap1, s])
                if overlap1 > overlap1:
                    sims.append([overlap2, s])
    
    #printList('SORTED LIST', sorted(sims))
    
    for item in sorted(sims):
        sSplit = item[1].split()
        sub1 = int(sSplit[0])
        sub2 = int(sSplit[1])
        sent1 = trimmedSentences[sub1]
        sent2 = trimmedSentences[sub2]
    
        setSent1 = set(sent1)
        setSent2 = set(sent2)
        inter = set(sent1).intersection(set(sent2))
        
#        print ''
#        print item
#        print '      %-s' % (str(inter))
#        print '     %4d %-s' % (sub1, str(sent1))
#        print '     %4d %-s' % (sub2, str(sent2))
#        print '     %4d %-s' % (sub1, str(thisFile.sents()[sub1]))
#        print '     %4d %-s' % (sub2, str(thisFile.sents()[sub2]))
    
    print fileName, ' SENTENCES ', len(trimmedSentences), ', PAIRS WITH OVERLAP ', len(sims)
    
######################################################################
## main code starts here

######################################################################
## open and read, then add to, a stop list
stopListFile = open('stoplistNLTK.txt')
stopList = stopListFile.read().split()
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

######################################################################
## hard code the full path name of the files to be read
folderName = '/Users/dabuell/csce500static/nltk/nltk_data/corpora/state_union'
#folderName = '/Users/buell/csce500static/nltk/nltk_data/corpora/state_union'
#folderName = '/Users/duncanbuell/csce500static/nltk/nltk_data/corpora/state_union'
#print "The input folder name is '%s'\n" % (folderName)

######################################################################
## here's the magic 'listdir' command that lists file names in folder
## we want the files for the Truman State of the Union addresses
filesInFolder = listdir(folderName)
filesToUse = []
for fileName in filesInFolder:
#    if ('Truman' in fileName) and ('1946' in fileName):
#    if 'Truman' in fileName:
#        filesToUse.append(fileName)
    filesToUse.append(fileName)

#print 'Files to be used are: ', filesToUse

######################################################################
## we are going to read the Truman State of the Union addresses
## the magic construction here is the PlainTextCorpusReader
## then we will trim the stop words
##
##
for fileName in filesToUse:
#    print "\nFOLDER, NAME ", folderName, fileName
    thisFile = nltk.corpus.PlaintextCorpusReader(folderName, fileName)
    trimmedSentences = trimStopWords(thisFile.sents(), stopList)
    computeOverlaps(fileName, trimmedSentences)

